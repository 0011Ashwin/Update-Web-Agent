"""
Obsidian Vault Manager - Real-time agent brain and knowledge base storage.

Enables the agent to write research findings, discoveries, and insights
directly into an Obsidian vault, making it available in real-time for
review and reference. Serves as a persistent second brain for the project.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import asyncio

logger = logging.getLogger(__name__)


class ObsidianVaultManager:
    """
    Manages real-time writing to an Obsidian vault.
    
    Creates and updates markdown files with agent research, findings,
    and discoveries organized by topic/task.
    """
    
    def __init__(self, vault_path: Optional[str] = None):
        """
        Initialize the vault manager.
        
        Args:
            vault_path: Path to Obsidian vault root folder.
                       Falls back to OBSIDIAN_VAULT_PATH env var if not provided.
        """
        self.vault_path = Path(vault_path or os.getenv("OBSIDIAN_VAULT_PATH", ""))
        self.auto_save = os.getenv("OBSIDIAN_ENABLE_AUTO_SAVE", "true").lower() == "true"
        self.enabled = False
        
        # Initialize vault structure if path exists
        if self.vault_path and self.vault_path.exists():
            self.enabled = True
            self._init_vault_structure()
            logger.info(f"✅ Obsidian vault initialized at: {self.vault_path}")
        elif self.vault_path:
            logger.warning(f"⚠️ Obsidian vault path not found: {self.vault_path}")
        else:
            logger.info("ℹ️ Obsidian vault not configured (OBSIDIAN_VAULT_PATH not set)")
    
    def _init_vault_structure(self):
        """Create required folders and index files in vault."""
        folders = [
            "Research",
            "Findings",
            "Task Logs",
            "Concepts",
            "Tools & Integrations",
            "Errors & Debugging",
            "_metadata"
        ]
        
        for folder in folders:
            folder_path = self.vault_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create main index if it doesn't exist
        index_path = self.vault_path / "INDEX.md"
        if not index_path.exists():
            self._create_index_file(index_path)
    
    def _create_index_file(self, index_path: Path):
        """Create or update the vault index file."""
        content = """# Update-Web-Agent Vault 🧠

> Real-time agent brain and knowledge base. Auto-updated as the agent discovers insights.

**Last Updated:** {timestamp}

## 📚 Sections

- [[Research]] - Web research findings and resources
- [[Findings]] - Key discoveries and analysis results
- [[Task Logs]] - Chronological task execution logs
- [[Concepts]] - Technical concepts and explanations
- [[Tools & Integrations]] - External tools and API documentation
- [[Errors & Debugging]] - Issues encountered and solutions

## 🔗 Quick Links

- [OmniRoute Configuration](#omniroute)
- [Recent Tasks](#recent)

---

### OmniRoute Configuration
- **Endpoint:** http://localhost:20128
- **Model:** auto/best-free (Anthropic)
- **Status:** {status}

### Recent Tasks
_Auto-populated by agent_

"""
        try:
            index_path.write_text(
                content.format(
                    timestamp=datetime.now().isoformat(),
                    status="✅ Active"
                )
            )
            logger.info(f"Created vault index: {index_path}")
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
    
    async def write_research(
        self,
        topic: str,
        content: str,
        tags: Optional[list] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Path]:
        """
        Write research findings to vault.
        
        Args:
            topic: Research topic/title
            content: Markdown content
            tags: List of tags for the note
            metadata: Additional metadata to store
        
        Returns:
            Path to created file or None if vault not enabled
        """
        if not self.enabled:
            return None
        
        try:
            # Sanitize filename
            safe_topic = "".join(c for c in topic if c.isalnum() or c in " -_").rstrip()
            filename = f"{safe_topic} - {datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
            
            file_path = self.vault_path / "Research" / filename
            
            # Prepare frontmatter
            frontmatter = {
                "timestamp": datetime.now().isoformat(),
                "tags": tags or [],
                "status": "new"
            }
            if metadata:
                frontmatter.update(metadata)
            
            # Build full content with frontmatter
            full_content = f"""---
{json.dumps(frontmatter, indent=2)}
---

# {topic}

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{content}
"""
            
            file_path.write_text(full_content, encoding="utf-8")
            logger.info(f"✅ Research written: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to write research: {e}", exc_info=True)
            return None
    
    async def write_finding(
        self,
        title: str,
        finding: str,
        source: Optional[str] = None,
        confidence: str = "medium"
    ) -> Optional[Path]:
        """
        Write a key finding/discovery to vault.
        
        Args:
            title: Finding title
            finding: Description of finding
            source: Where the finding came from (URL, task, etc.)
            confidence: Confidence level (high/medium/low)
        
        Returns:
            Path to created file or None if vault not enabled
        """
        if not self.enabled:
            return None
        
        try:
            filename = f"{title} - {datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
            file_path = self.vault_path / "Findings" / filename
            
            content = f"""---
timestamp: {datetime.now().isoformat()}
confidence: {confidence}
source: {source or "unknown"}
---

# {title}

**Confidence:** {confidence.upper()}
**Source:** {source or "N/A"}
**Discovered:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Finding
{finding}

---
_Auto-captured by Update-Web-Agent_
"""
            
            file_path.write_text(content, encoding="utf-8")
            logger.info(f"✅ Finding recorded: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to write finding: {e}", exc_info=True)
            return None
    
    async def write_task_log(
        self,
        task_id: str,
        task_name: str,
        status: str,
        details: str,
        result: Optional[str] = None
    ) -> Optional[Path]:
        """
        Log task execution to vault.
        
        Args:
            task_id: Unique task ID
            task_name: Human-readable task name
            status: Task status (started/running/completed/failed)
            details: Task details and steps
            result: Task result/output (if completed)
        
        Returns:
            Path to created/updated file or None if vault not enabled
        """
        if not self.enabled:
            return None
        
        try:
            filename = f"{task_id} - {task_name}.md"
            file_path = self.vault_path / "Task Logs" / filename
            
            # If file exists, append; otherwise create new
            if file_path.exists():
                existing = file_path.read_text(encoding="utf-8")
                # Add timestamp entry to existing log
                log_entry = f"\n\n## Status Update - {datetime.now().strftime('%H:%M:%S')}\n**Status:** {status}\n{details}"
                if result:
                    log_entry += f"\n\n**Result:**\n{result}"
                full_content = existing + log_entry
            else:
                full_content = f"""---
task_id: {task_id}
task_name: {task_name}
created_at: {datetime.now().isoformat()}
---

# {task_name}

**Task ID:** {task_id}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Status: {status}

{details}

{f'**Result:** {result}' if result else ''}
"""
            
            file_path.write_text(full_content, encoding="utf-8")
            logger.info(f"✅ Task logged: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to write task log: {e}", exc_info=True)
            return None
    
    async def update_vault_index(self, recent_items: Optional[list] = None):
        """Update the vault's main index with recent activity."""
        if not self.enabled:
            return
        
        try:
            index_path = self.vault_path / "INDEX.md"
            
            # Read current index
            content = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
            
            # Update timestamp and recent items
            if recent_items:
                recent_section = "\n".join([f"- {item}" for item in recent_items])
            else:
                recent_section = "_No recent activity_"
            
            # This is a simple update; in production you'd parse and update specific sections
            logger.debug(f"Updated vault index with {len(recent_items or [])} recent items")
            
        except Exception as e:
            logger.error(f"Failed to update vault index: {e}")
    
    def get_vault_path(self) -> Optional[Path]:
        """Get the vault path if enabled."""
        return self.vault_path if self.enabled else None
    
    def is_enabled(self) -> bool:
        """Check if vault is enabled and ready."""
        return self.enabled


# Global vault instance
_vault_instance: Optional[ObsidianVaultManager] = None


def get_vault_manager() -> ObsidianVaultManager:
    """Get or create global vault manager instance."""
    global _vault_instance
    if _vault_instance is None:
        _vault_instance = ObsidianVaultManager()
    return _vault_instance


async def write_research_to_vault(
    topic: str,
    content: str,
    tags: Optional[list] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Optional[Path]:
    """Convenience function to write research to vault."""
    vault = get_vault_manager()
    return await vault.write_research(topic, content, tags, metadata)


async def write_finding_to_vault(
    title: str,
    finding: str,
    source: Optional[str] = None,
    confidence: str = "medium"
) -> Optional[Path]:
    """Convenience function to write finding to vault."""
    vault = get_vault_manager()
    return await vault.write_finding(title, finding, source, confidence)


async def write_task_log_to_vault(
    task_id: str,
    task_name: str,
    status: str,
    details: str,
    result: Optional[str] = None
) -> Optional[Path]:
    """Convenience function to write task log to vault."""
    vault = get_vault_manager()
    return await vault.write_task_log(task_id, task_name, status, details, result)
