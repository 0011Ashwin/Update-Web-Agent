# 🚀 Ghost Upgrade Implementation Guide

## Overview

This guide will walk you through integrating the new Dashboard, Notes & Visualization, and Enhanced Data Capture features into your Ghost project.

## 📋 Prerequisites

- Python 3.11+
- Gradio installed
- Existing Ghost/Browser-Use WebUI installation
- Basic familiarity with Python and file structure

## 🔧 Step-by-Step Installation

### Step 1: Verify Your Current Installation

First, make sure your project structure looks like this:

```
Web-Agent-main/
├── src/
│   ├── webui/
│   │   ├── components/
│   │   │   ├── agent_settings_tab.py
│   │   │   ├── browser_settings_tab.py
│   │   │   ├── browser_use_agent_tab.py
│   │   │   ├── deep_research_agent_tab.py
│   │   │   └── load_save_config_tab.py
│   │   ├── interface.py
│   │   └── webui_manager.py
│   └── utils/
├── tmp/
│   └── agent_history/
├── webui.py
└── requirements.txt
```

### Step 2: Create New Component Files

#### 2.1 Create Dashboard Component

Create file: `src/webui/components/dashboard_tab.py`

You can copy the entire content from the dashboard_tab.py file that was created.

**Key Functions:**
- `load_task_analytics()` - Loads task data from agent history
- `generate_dashboard_html()` - Creates dashboard visualization
- `generate_recent_tasks_table()` - Creates recent tasks table
- `refresh_dashboard()` - Updates dashboard data
- `create_dashboard_tab()` - Main tab creation function

#### 2.2 Create Notes & Visualization Component

Create file: `src/webui/components/notes_visualization_tab.py`

This file contains:
- `TaskNotesManager` class for managing notes
- `generate_step_flowchart()` - Creates step-by-step flowchart
- `generate_mind_map()` - Creates mind map visualization
- `create_notes_tab()` - Main tab creation function

#### 2.3 Create Enhanced Data Capture Utility

Create file: `src/utils/ghost_data_capture.py`

This file contains the `GhostDataCapture` class with methods:
- `start_session()` - Begin tracking a new task
- `capture_step()` - Record each step
- `add_note()` - Add notes to session
- `end_session()` - Finalize and save all data
- `_generate_summary_report()` - Create markdown reports
- `_generate_graph_data()` - Generate visualization data

### Step 3: Update Interface File

Edit: `src/webui/interface.py`

**3.1 Add Import Statements**

At the top of the file, add:

```python
from src.webui.components.dashboard_tab import create_dashboard_tab
from src.webui.components.notes_visualization_tab import create_notes_tab
```

**3.2 Add New Tabs to UI**

Find the `gr.Tabs()` section and add the new tabs:

```python
with gr.Tabs() as tabs:
    with gr.TabItem("⚙️ Agent Settings"):
        create_agent_settings_tab(ui_manager)

    with gr.TabItem("🌐 Browser Settings"):
        create_browser_settings_tab(ui_manager)

    with gr.TabItem("🤖 Run Agent"):
        create_browser_use_agent_tab(ui_manager)

    # NEW: Add Dashboard Tab
    with gr.TabItem("📊 Dashboard"):
        create_dashboard_tab(ui_manager)
    
    # NEW: Add Notes & Visualization Tab
    with gr.TabItem("📝 Notes & Visualization"):
        create_notes_tab(ui_manager)

    with gr.TabItem("🎁 Agent Marketplace"):
        gr.Markdown(
            """
            ### Agents built on Browser-Use
            """,
            elem_classes=["tab-header-text"],
        )
        with gr.Tabs():
            with gr.TabItem("Deep Research"):
                create_deep_research_agent_tab(ui_manager)

    with gr.TabItem("📁 Load & Save Config"):
        create_load_save_config_tab(ui_manager)
```

### Step 4: Create Required Directories

Run these commands in PowerShell:

```powershell
# Create data directories
New-Item -ItemType Directory -Force -Path ".\tmp\ghost_data\sessions"
New-Item -ItemType Directory -Force -Path ".\tmp\ghost_data\graphs"
New-Item -ItemType Directory -Force -Path ".\tmp\ghost_data\notes"
New-Item -ItemType Directory -Force -Path ".\tmp\task_notes"

# Verify directories were created
Get-ChildItem -Path ".\tmp" -Directory
```

### Step 5: (Optional) Integrate Data Capture into Agent

To automatically capture data during agent execution, edit: `src/webui/components/browser_use_agent_tab.py`

**5.1 Add Import at Top**

```python
from src.utils.ghost_data_capture import ghost_capture
```

**5.2 Start Session When Task Begins**

Find the `run_agent_task` function and add after task initialization:

```python
async def run_agent_task(
        webui_manager: WebuiManager, components: Dict[gr.components.Component, Any]
) -> AsyncGenerator[Dict[gr.components.Component, Any], None]:
    
    # ... existing code ...
    
    task = components.get(user_input_comp, "").strip()
    if not task:
        gr.Warning("Please enter a task.")
        yield {run_button_comp: gr.update(interactive=True)}
        return
    
    # NEW: Start data capture session
    session_id = ghost_capture.start_session(task, metadata={
        "llm_provider": llm_provider_name,
        "llm_model": llm_model_name,
        "use_vision": use_vision
    })
    
    # ... rest of existing code ...
```

**5.3 Capture Steps**

Find the `_handle_new_step` callback and add:

```python
async def _handle_new_step(
        webui_manager: WebuiManager, state: BrowserState, output: AgentOutput, step_num: int
):
    # ... existing code ...
    
    # NEW: Capture step data
    step_data = {
        "action": output.action[0].action_name if output.action else "Unknown",
        "reasoning": output.current_state.important_contents[0] if output.current_state.important_contents else "",
        "state": output.current_state.model_dump() if hasattr(output.current_state, 'model_dump') else {},
        "screenshot": state.screenshot if hasattr(state, 'screenshot') else None,
        "success": True,  # Determine based on your logic
        "duration": 0,  # Calculate from timing data
        "tokens": 0  # Get from output if available
    }
    
    ghost_capture.capture_step(step_num, step_data)
    
    # ... rest of existing code ...
```

**5.4 End Session When Task Completes**

Find where the task completes and add:

```python
def _handle_done(webui_manager: WebuiManager, history: AgentHistoryList):
    # ... existing code ...
    
    # NEW: End data capture session
    final_result = history.final_result() if hasattr(history, 'final_result') else None
    status = "completed" if not history.errors() else "failed"
    
    ghost_capture.end_session(final_result=final_result, status=status)
    
    # ... rest of existing code ...
```

### Step 6: Test the Installation

**6.1 Start the Application**

```powershell
python webui.py
```

**6.2 Verify New Tabs Appear**

Check that you see:
- 📊 Dashboard tab
- 📝 Notes & Visualization tab

**6.3 Test Dashboard**

1. Navigate to Dashboard tab
2. Click "🔄 Refresh Dashboard"
3. Should see metric cards (may show 0 if no tasks run yet)

**6.4 Run a Test Task**

1. Go to "🤖 Run Agent" tab
2. Configure LLM settings
3. Run a simple task (e.g., "Search for Python on Google")
4. Let it complete

**6.5 Test Visualizations**

1. Go to Dashboard → Click refresh → Should see 1 task
2. Go to Notes & Visualization → Step Flowchart
3. Find your task ID in `./tmp/agent_history/` folder
4. Enter the task ID and click "📊 Load Flowchart"
5. Should see animated flowchart

### Step 7: Verify Data Capture

Check that files were created:

```powershell
# Check for session data
Get-ChildItem -Path ".\tmp\ghost_data\sessions" -Recurse

# Check for agent history
Get-ChildItem -Path ".\tmp\agent_history" -Recurse
```

You should see:
- JSON files in `ghost_data/sessions/`
- Markdown summary files
- Graph data files

## 🔍 Troubleshooting

### Issue: Tabs Don't Appear

**Solution:**
1. Check import statements in `interface.py`
2. Verify file paths are correct
3. Check for syntax errors in new component files
4. Restart the application

```powershell
# Check for Python errors
python -m py_compile src/webui/components/dashboard_tab.py
python -m py_compile src/webui/components/notes_visualization_tab.py
```

### Issue: Dashboard Shows No Data

**Solution:**
1. Ensure tasks have been run and completed
2. Check that `./tmp/agent_history/` contains task data
3. Verify directory permissions
4. Click refresh button multiple times

```powershell
# Check if history files exist
Get-ChildItem -Path ".\tmp\agent_history" -Recurse -Filter "*.json"
```

### Issue: Flowchart Won't Load

**Solution:**
1. Verify the Task ID is correct (check folder names in agent_history)
2. Ensure JSON file exists: `./tmp/agent_history/{task_id}/{task_id}.json`
3. Check file is valid JSON
4. Check console for error messages

```powershell
# List all task IDs
Get-ChildItem -Path ".\tmp\agent_history" -Directory | Select-Object Name
```

### Issue: Notes Not Saving

**Solution:**
1. Check folder permissions for `./tmp/task_notes/`
2. Ensure Task ID is provided
3. Verify note content is not empty
4. Check console for error messages

```powershell
# Check permissions
Get-Acl ".\tmp\task_notes"

# Create if missing
New-Item -ItemType Directory -Force -Path ".\tmp\task_notes"
```

### Issue: Import Errors

**Solution:**
```powershell
# Verify Gradio is installed
pip show gradio

# Reinstall if needed
pip install --upgrade gradio

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

## 🎨 Customization

### Change Colors

Edit the CSS in `dashboard_tab.py` or `notes_visualization_tab.py`:

```python
# Dashboard colors
"background: linear-gradient(135deg, rgba(117, 70, 242, 0.2), ...)"  # Purple gradient
"color: #7546f2"  # Purple text
"border: 1px solid #4c3ba1"  # Purple border

# Success color
"color: #28c878"  # Green

# Error color
"color: #f24646"  # Red
```

### Adjust Animation Speed

In the CSS sections, modify animation durations:

```css
animation: fadeIn 0.6s ease-out;  /* Change 0.6s to slower/faster */
transition: all 0.3s ease;  /* Change 0.3s for hover effects */
```

### Add Custom Metrics

Edit `load_task_analytics()` in `dashboard_tab.py`:

```python
def load_task_analytics(history_path: str = "./tmp/agent_history") -> Dict:
    analytics = {
        # Add your custom metrics here
        "custom_metric": 0,
        # ... existing metrics
    }
    # ... calculate your metrics
    return analytics
```

## 📊 Data Format Reference

### Session Data Structure

```json
{
  "session_id": "20251028_143022_123456",
  "task": "Task description",
  "start_time": "2025-10-28T14:30:22.123456",
  "end_time": "2025-10-28T14:32:45.789012",
  "status": "completed",
  "metadata": {},
  "steps": [
    {
      "step_number": 1,
      "timestamp": "2025-10-28T14:30:25.123456",
      "action": "navigate",
      "reasoning": "Opening website",
      "state": {},
      "screenshot": "base64_data",
      "success": true,
      "duration": 2.5,
      "tokens": 150,
      "errors": []
    }
  ],
  "notes": [],
  "stats": {
    "total_steps": 5,
    "successful_actions": 5,
    "failed_actions": 0,
    "total_tokens": 750,
    "total_duration": 143.23
  }
}
```

## 🚀 Advanced Integration

### Export Dashboard Data

Add this function to `dashboard_tab.py`:

```python
def export_dashboard_data(analytics: Dict) -> str:
    """Export dashboard data as CSV"""
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Metric', 'Value'])
    
    for key, value in analytics['stats'].items():
        writer.writerow([key, value])
    
    return output.getvalue()
```

### Add Real-time Updates

Modify `create_dashboard_tab()` to include auto-refresh:

```python
# Add this after creating the dashboard display
with gr.Row():
    auto_refresh = gr.Checkbox(label="Auto-refresh (every 10s)", value=False)

# Add refresh loop
def auto_refresh_loop(enabled):
    import time
    while enabled:
        time.sleep(10)
        analytics = load_task_analytics()
        yield generate_dashboard_html(analytics)
```

## 📖 Additional Resources

- **GHOST_FEATURES.md** - Detailed feature documentation
- **UPGRADE_NOTES.md** - Quick reference guide
- Original README.md - Installation and setup

## ✅ Post-Installation Checklist

- [ ] All three new files created in correct locations
- [ ] `interface.py` updated with new imports and tabs
- [ ] Required directories created in `tmp/`
- [ ] Application starts without errors
- [ ] Dashboard tab visible and functional
- [ ] Notes & Visualization tab visible
- [ ] Can run a test task successfully
- [ ] Task appears in dashboard after refresh
- [ ] Can load flowchart with task ID
- [ ] Can save and view notes
- [ ] Data files created in `ghost_data/` folder

## 🎯 Next Steps

1. **Run several tasks** to populate the dashboard
2. **Explore visualizations** with different task IDs
3. **Create notes** to document important findings
4. **Customize colors** to match your preferences
5. **Integrate data capture** for automatic tracking
6. **Share feedback** on what features you'd like next

## 💡 Tips

- Task IDs are the folder names in `./tmp/agent_history/`
- Dashboard updates only when you click refresh (not real-time)
- Flowcharts work best with completed tasks
- Mind maps show up to 8 steps for optimal visualization
- All data is stored locally in JSON format for easy export
- Screenshots are stored as base64 in session data

## 🆘 Getting Help

If you encounter issues:

1. **Check console output** for error messages
2. **Verify file permissions** on tmp/ directories
3. **Ensure all imports** are correct
4. **Test with simple tasks** first
5. **Check Python version** (3.11+ required)
6. **Verify Gradio version** is compatible

Common commands:
```powershell
# Check Python version
python --version

# Verify Gradio installation
pip show gradio

# Test import
python -c "from src.webui.components.dashboard_tab import create_dashboard_tab; print('Success')"

# Check file syntax
python -m py_compile src/webui/components/dashboard_tab.py
```

---

## 🎉 Congratulations!

You've successfully upgraded your Ghost project with enterprise-level analytics and visualization capabilities!

Your agent now automatically captures and visualizes every action, providing unprecedented insight into its behavior.

**Enjoy your enhanced Ghost experience!** 👻✨
