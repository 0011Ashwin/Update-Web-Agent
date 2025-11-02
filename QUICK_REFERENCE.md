# 👻 Ghost Upgrade - Quick Reference Card

## 🚀 Quick Start (5 Minutes)

### 1. Add New Files (Copy from provided code)
```
src/webui/components/dashboard_tab.py
src/webui/components/notes_visualization_tab.py
src/utils/ghost_data_capture.py
```

### 2. Update interface.py
Add these imports:
```python
from src.webui.components.dashboard_tab import create_dashboard_tab
from src.webui.components.notes_visualization_tab import create_notes_tab
```

Add these tabs in the `gr.Tabs()` section:
```python
with gr.TabItem("📊 Dashboard"):
    create_dashboard_tab(ui_manager)

with gr.TabItem("📝 Notes & Visualization"):
    create_notes_tab(ui_manager)
```

### 3. Create Directories
```powershell
New-Item -ItemType Directory -Force -Path ".\tmp\ghost_data\sessions"
New-Item -ItemType Directory -Force -Path ".\tmp\ghost_data\graphs"
New-Item -ItemType Directory -Force -Path ".\tmp\ghost_data\notes"
New-Item -ItemType Directory -Force -Path ".\tmp\task_notes"
```

### 4. Run & Test
```powershell
python webui.py
```

---

## 📊 Feature Access

| Feature | Location | Action |
|---------|----------|--------|
| **Dashboard** | 📊 Dashboard tab | Click "🔄 Refresh Dashboard" |
| **Step Flowchart** | 📝 Notes → Step Flowchart | Enter Task ID → Click "📊 Load" |
| **Mind Map** | 📝 Notes → Mind Map | Enter Task ID → Click "🗺️ Generate" |
| **Task Notes** | 📝 Notes → Task Notes | Enter ID & Text → Click "💾 Save" |

---

## 🔍 Finding Task IDs

### Method 1: File System
```powershell
Get-ChildItem -Path ".\tmp\agent_history" -Directory | Select-Object Name
```

**Explanation:**
- Task IDs are folder names in `.\tmp\agent_history\`
- Format: `YYYYMMDD_HHMMSS_microseconds`
- Example: `20251028_143022_123456`

### Method 2: Dashboard
Look at the Recent Tasks table in the Dashboard tab

**Detailed Guide:** See `HOW_TO_FIND_TASK_ID.md` for complete instructions

### Method 3: Agent Output
Task ID is displayed when agent completes in the "Task Outputs" section

### Quick Copy to Clipboard
```powershell
# Copy most recent Task ID
(Get-ChildItem ".\tmp\agent_history" -Directory | Sort-Object CreationTime -Descending | Select-Object -First 1).Name | Set-Clipboard
Write-Host "Task ID copied!"
```

---

## 📁 File Locations

```
tmp/
├── agent_history/          # Original task data
│   └── {task_id}/
│       ├── {task_id}.json
│       └── {task_id}.gif
├── ghost_data/            # Enhanced capture
│   ├── sessions/          # Session data + reports
│   ├── graphs/            # Graph data
│   └── notes/             # Session notes
└── task_notes/            # UI notes
```

---

## 🎨 Dashboard Metrics

| Metric | Color | Meaning |
|--------|-------|---------|
| **Total Tasks** | Purple | All tasks executed |
| **Successful** | Green | Completed without errors |
| **Failed** | Red | Tasks with errors |
| **Total Steps** | Orange | Combined steps across all tasks |
| **Success Rate** | Gradient | Percentage bar (Green/Purple) |

---

## 💡 Common Tasks

### View Analytics
1. Go to Dashboard tab
2. Click refresh button
3. View metrics and recent tasks

### Visualize Task
1. Run a task in "Run Agent" tab
2. Note the Task ID (shown in output)
3. Go to "Notes & Visualization"
4. Enter Task ID
5. Choose Flowchart or Mind Map

### Document Task
1. Complete a task
2. Go to "Task Notes" sub-tab
3. Enter Task ID and notes
4. Click "Save Note"
5. Click "Refresh Notes" to view all

### Export Data
```powershell
# Copy session data
Copy-Item ".\tmp\ghost_data\sessions\*.json" -Destination ".\exports\"

# View markdown report
notepad ".\tmp\ghost_data\sessions\{session_id}_summary.md"
```

---

## 🔧 Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Tabs don't show | Check imports in interface.py |
| Dashboard empty | Run tasks first, then refresh |
| Flowchart error | Verify Task ID is correct |
| Notes won't save | Check folder permissions |
| Import errors | `pip install --upgrade gradio` |

---

## 🎯 Keyboard Shortcuts

When using the UI:
- **Tab** - Navigate between fields
- **Enter** - Submit in text boxes
- **Ctrl+C** - Copy data from displays
- **Ctrl+R** - Refresh browser (if UI stuck)

---

## 📊 Data Format Quick Reference

### Session File Structure
```json
{
  "session_id": "...",
  "task": "...",
  "steps": [...],
  "stats": {
    "total_steps": 0,
    "successful_actions": 0,
    "total_tokens": 0
  }
}
```

### Note File Structure
```json
[
  {
    "task_id": "...",
    "content": "...",
    "timestamp": "..."
  }
]
```

---

## 🎨 Customization Quick Tips

### Change Colors
Edit in component files:
```python
# Purple theme
--ghost-primary: #7546f2
--ghost-secondary: #9046f2

# Success color
#28c878

# Error color
#f24646
```

### Adjust Animation Speed
```css
animation: fadeIn 0.6s;  /* Make slower: 1.2s */
transition: all 0.3s;    /* Make slower: 0.6s */
```

---

## 📞 Quick Commands

```powershell
# Start Ghost
python webui.py

# Check for errors
python -m py_compile src/webui/components/dashboard_tab.py

# List all task IDs
Get-ChildItem ".\tmp\agent_history" -Directory

# View latest session
Get-ChildItem ".\tmp\ghost_data\sessions" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# Clean old data (keep last 10)
Get-ChildItem ".\tmp\agent_history" | Sort-Object CreationTime | Select-Object -SkipLast 10 | Remove-Item -Recurse
```

---

## 🎯 Best Practices

✅ **DO:**
- Refresh dashboard after running tasks
- Document complex tasks with notes
- Review flowcharts for debugging
- Export important session data regularly

❌ **DON'T:**
- Delete agent_history folder (needed for visualization)
- Edit JSON files manually (may corrupt data)
- Run too many tasks without checking disk space
- Forget to refresh dashboard

---

## 🔮 Coming Soon

- Real-time dashboard updates
- Export to PDF
- Task comparison tools
- AI-powered insights
- Chart.js graphs
- Collaborative features

---

## 📖 Full Documentation

- **INSTALLATION_GUIDE.md** - Detailed setup guide
- **GHOST_FEATURES.md** - Complete feature documentation
- **UPGRADE_NOTES.md** - What's new overview

---

## ✨ Pro Tips

💡 Use Task Notes to document:
- Why a task was run
- Expected vs actual results
- Issues encountered
- Solutions applied

💡 Review Step Flowcharts to:
- Understand agent reasoning
- Identify bottlenecks
- Debug failed tasks
- Optimize task descriptions

💡 Check Dashboard regularly to:
- Monitor success rates
- Track token usage
- Identify patterns
- Celebrate wins! 🎉

---

**Keep this reference handy for quick access to Ghost's powerful features!** 👻

Print or save this as a PDF for easy reference while using Ghost.
