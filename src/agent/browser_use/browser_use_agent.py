from __future__ import annotations

import asyncio
import logging
import os
import json
from datetime import datetime

# from lmnr.sdk.decorators import observe
from browser_use.agent.gif import create_history_gif
from browser_use.agent.service import Agent, AgentHookFunc
from browser_use.agent.views import (
    ActionResult,
    AgentHistory,
    AgentHistoryList,
    AgentStepInfo,
)
from browser_use.browser.views import BrowserStateHistory
from browser_use.utils import time_execution_async
from dotenv import load_dotenv
try:
    from browser_use.agent.message_manager.utils import is_model_without_tool_support
except ImportError:
    def is_model_without_tool_support(model_name: str) -> bool:
        return False

# Import Obsidian vault manager
from src.utils.obsidian_vault import (
    get_vault_manager,
    write_research_to_vault,
    write_finding_to_vault,
    write_task_log_to_vault
)

load_dotenv()
logger = logging.getLogger(__name__)

SKIP_LLM_API_KEY_VERIFICATION = (
        os.environ.get("SKIP_LLM_API_KEY_VERIFICATION", "false").lower()[0] in "ty1"
)


class BrowserUseAgent(Agent):
    def _set_tool_calling_method(self) -> str | None:
        tool_calling_method = self.settings.tool_calling_method
        if tool_calling_method == 'auto':
            if is_model_without_tool_support(self.model_name):
                return 'raw'
            elif self.chat_model_library == 'ChatGoogleGenerativeAI':
                return None
            elif self.chat_model_library == 'ChatOpenAI':
                return 'function_calling'
            elif self.chat_model_library == 'AzureChatOpenAI':
                return 'function_calling'
            else:
                return None
        else:
            return tool_calling_method

    @time_execution_async("--run (agent)")
    async def run(
            self, max_steps: int = 100, on_step_start: AgentHookFunc | None = None,
            on_step_end: AgentHookFunc | None = None
    ) -> AgentHistoryList:
        """Execute the task with maximum number of steps"""

        loop = asyncio.get_event_loop()

        # Set up the Ctrl+C signal handler with callbacks specific to this agent
        from browser_use.utils import SignalHandler

        signal_handler = SignalHandler(
            loop=loop,
            pause_callback=self.pause,
            resume_callback=self.resume,
            custom_exit_callback=None,  # No special cleanup needed on forced exit
            exit_on_second_int=True,
        )
        signal_handler.register()
        
        # Log task start to vault
        task_id = f"task-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        task_name = getattr(self, 'task', 'Unnamed Task')
        
        try:
            await write_task_log_to_vault(
                task_id=task_id,
                task_name=str(task_name)[:100],
                status="started",
                details=f"Agent task initiated.\n**Max Steps:** {max_steps}"
            )
        except Exception as e:
            logger.debug(f"Could not log task start to vault: {e}")

        try:
            self._log_agent_run()

            # Execute initial actions if provided
            if self.initial_actions:
                result = await self.multi_act(self.initial_actions, check_for_new_elements=False)
                self.state.last_result = result

            for step in range(max_steps):
                # Check if waiting for user input after Ctrl+C
                if self.state.paused:
                    signal_handler.wait_for_resume()
                    signal_handler.reset()

                # Check if we should stop due to too many failures
                if self.state.consecutive_failures >= self.settings.max_failures:
                    logger.error(f'❌ Stopping due to {self.settings.max_failures} consecutive failures')
                    break

                # Check control flags before each step
                if self.state.stopped:
                    logger.info('Agent stopped')
                    break

                while self.state.paused:
                    await asyncio.sleep(0.2)  # Small delay to prevent CPU spinning
                    if self.state.stopped:  # Allow stopping while paused
                        break

                if on_step_start is not None:
                    await on_step_start(self)

                step_info = AgentStepInfo(step_number=step, max_steps=max_steps)
                await self.step(step_info)

                if on_step_end is not None:
                    await on_step_end(self)

                if self.history.is_done():
                    if self.settings.validate_output and step < max_steps - 1:
                        if not await self._validate_output():
                            continue

                    await self.log_completion()
                    
                    # Log successful completion to vault
                    try:
                        history_summary = self._summarize_history()
                        await write_task_log_to_vault(
                            task_id=task_id,
                            task_name=str(task_name)[:100],
                            status="completed",
                            details=f"Task completed successfully in {step + 1} steps.",
                            result=history_summary
                        )
                    except Exception as e:
                        logger.debug(f"Could not log task completion to vault: {e}")
                    
                    break
            else:
                error_message = 'Failed to complete task in maximum steps'

                self.history.history.append(
                    AgentHistory(
                        model_output=None,
                        result=[ActionResult(error=error_message, include_in_memory=True)],
                        state=BrowserStateHistory(
                            url='',
                            title='',
                            tabs=[],
                            interacted_element=[],
                            screenshot=None,
                        ),
                        metadata=None,
                    )
                )

                logger.info(f'❌ {error_message}')
                
                # Log failure to vault
                try:
                    await write_task_log_to_vault(
                        task_id=task_id,
                        task_name=str(task_name)[:100],
                        status="failed",
                        details=f"Task failed: {error_message}",
                        result=f"Stopped after {max_steps} steps without completion."
                    )
                except Exception as e:
                    logger.debug(f"Could not log task failure to vault: {e}")

            return self.history

        except KeyboardInterrupt:
            # Already handled by our signal handler, but catch any direct KeyboardInterrupt as well
            logger.info('Got KeyboardInterrupt during execution, returning current history')
            
            # Log interrupt to vault
            try:
                await write_task_log_to_vault(
                    task_id=task_id,
                    task_name=str(task_name)[:100],
                    status="interrupted",
                    details="Task was interrupted by user (Ctrl+C)"
                )
            except Exception as e:
                logger.debug(f"Could not log task interruption to vault: {e}")
            
            return self.history

        finally:
            # Unregister signal handlers before cleanup
            signal_handler.unregister()

            save_playwright_script_path = getattr(self.settings, 'save_playwright_script_path', None)
            if save_playwright_script_path:
                logger.info(
                    f'Agent run finished. Attempting to save Playwright script to: {save_playwright_script_path}'
                )
                try:
                    # Extract sensitive data keys if sensitive_data is provided
                    keys = list(self.sensitive_data.keys()) if self.sensitive_data else None
                    # Pass browser and context config to the saving method
                    self.history.save_as_playwright_script(
                        save_playwright_script_path,
                        sensitive_data_keys=keys,
                        browser_config=self.browser.config,
                        context_config=self.browser_context.config,
                    )
                except Exception as script_gen_err:
                    # Log any error during script generation/saving
                    logger.error(f'Failed to save Playwright script: {script_gen_err}', exc_info=True)

            await self.close()

            if self.settings.generate_gif:
                output_path: str = 'agent_history.gif'
                if isinstance(self.settings.generate_gif, str):
                    output_path = self.settings.generate_gif

                create_history_gif(task=self.task, history=self.history, output_path=output_path)

    def _summarize_history(self) -> str:
        """
        Create a summary of the agent execution history for vault logging.
        
        Returns:
            Markdown-formatted summary of task execution
        """
        try:
            summary_parts = []
            
            # Basic info
            history_len = len(self.history.history) if self.history and hasattr(self.history, 'history') else 0
            summary_parts.append(f"**Steps Executed:** {history_len}")
            
            # Try to get final URL if available
            if self.history and hasattr(self.history, 'history') and self.history.history:
                last_entry = self.history.history[-1]
                if hasattr(last_entry, 'state') and hasattr(last_entry.state, 'url'):
                    summary_parts.append(f"**Final URL:** {last_entry.state.url}")
            
            # Get result summary
            if self.history and hasattr(self.history, 'history') and self.history.history:
                for entry in self.history.history[-3:]:  # Last 3 entries
                    if hasattr(entry, 'result') and entry.result:
                        for result in entry.result:
                            if hasattr(result, 'extracted_content') and result.extracted_content:
                                summary_parts.append(f"\n**Found Content:**\n{result.extracted_content[:500]}")
                                break
            
            return "\n".join(summary_parts) if summary_parts else "Task execution completed"
        except Exception as e:
            logger.debug(f"Error summarizing history: {e}")
            return "Task execution completed (summary unavailable)"
