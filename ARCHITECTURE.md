# 👻 Ghost Architecture & Data Flow

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Ghost WebUI                              │
│                      (Gradio Interface)                          │
└─────────────────────────────────────────────────────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
    ┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
    │  Agent Settings  │ │   Browser    │ │   Run Agent      │
    │      Tab         │ │  Settings    │ │      Tab         │
    └──────────────────┘ └──────────────┘ └──────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
    ┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
    │   📊 Dashboard   │ │  📝 Notes &  │ │  🎁 Marketplace  │
    │       Tab        │ │ Visualization│ │      Tab         │
    │    (NEW!)        │ │    (NEW!)    │ │                  │
    └──────────────────┘ └──────────────┘ └──────────────────┘
                │                │
                ▼                ▼
    ┌────────────────────────────────────┐
    │    WebuiManager                    │
    │  (Component Management)            │
    └────────────────────────────────────┘
                │
                ▼
    ┌────────────────────────────────────┐
    │   Browser Use Agent                │
    │  (Task Execution Engine)           │
    └────────────────────────────────────┘
                │
                ▼
    ┌────────────────────────────────────┐
    │   GhostDataCapture                 │
    │  (Enhanced Data Collection) (NEW!) │
    └────────────────────────────────────┘
                │
                ▼
    ┌────────────────────────────────────┐
    │   Data Storage Layer               │
    │   - Agent History                  │
    │   - Ghost Data                     │
    │   - Task Notes                     │
    └────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

### Task Execution Flow

```
User Input (Task)
       │
       ▼
┌──────────────────┐
│   Run Agent      │ ◄── Agent Settings
│      Tab         │ ◄── Browser Settings
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Start Session    │ ──► GhostDataCapture.start_session()
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Execute Step 1  │
└──────────────────┘
       │
       ├──► Capture Step Data
       │    └──► GhostDataCapture.capture_step()
       │         └──► Save to sessions/{id}.json
       │
       ▼
┌──────────────────┐
│  Execute Step 2  │
└──────────────────┘
       │
       ├──► Capture Step Data
       │
       ▼
      ...
       │
       ▼
┌──────────────────┐
│  Execute Step N  │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Task Complete   │
└──────────────────┘
       │
       ├──► End Session
       │    └──► GhostDataCapture.end_session()
       │         ├──► Generate summary.md
       │         ├──► Generate graph.json
       │         └──► Save final statistics
       │
       ▼
┌──────────────────┐
│  Show Results    │
│  - History JSON  │
│  - Recording GIF │
│  - Final Output  │
└──────────────────┘
```

### Visualization Flow

```
User Action
       │
       ├─────────────┬──────────────┬─────────────┐
       │             │              │             │
       ▼             ▼              ▼             ▼
┌────────────┐ ┌───────────┐ ┌──────────┐ ┌───────────┐
│ Dashboard  │ │ Flowchart │ │ Mind Map │ │   Notes   │
│  Refresh   │ │   Load    │ │   Load   │ │   Save    │
└────────────┘ └───────────┘ └──────────┘ └───────────┘
       │             │              │             │
       ▼             ▼              ▼             ▼
┌────────────────────────────────────────────────────┐
│              Load Task Data                         │
│  - Read from agent_history/                        │
│  - Read from ghost_data/sessions/                  │
│  - Read from task_notes/                           │
└────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────┐
│              Process Data                           │
│  - Calculate statistics                            │
│  - Generate HTML visualizations                    │
│  - Format step information                         │
└────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────┐
│              Render to UI                          │
│  - Animated cards                                  │
│  - Interactive tables                              │
│  - Step flowcharts                                 │
│  - Mind maps                                       │
└────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
Web-Agent-main/
│
├── src/
│   ├── webui/
│   │   ├── components/
│   │   │   ├── agent_settings_tab.py
│   │   │   ├── browser_settings_tab.py
│   │   │   ├── browser_use_agent_tab.py
│   │   │   ├── deep_research_agent_tab.py
│   │   │   ├── load_save_config_tab.py
│   │   │   ├── dashboard_tab.py           ◄── NEW
│   │   │   └── notes_visualization_tab.py ◄── NEW
│   │   │
│   │   ├── interface.py                   ◄── UPDATED
│   │   └── webui_manager.py
│   │
│   ├── utils/
│   │   ├── ghost_data_capture.py          ◄── NEW
│   │   └── (other utilities)
│   │
│   ├── agent/
│   ├── browser/
│   └── controller/
│
├── tmp/
│   ├── agent_history/           # Original agent data
│   │   └── {task_id}/
│   │       ├── {task_id}.json
│   │       └── {task_id}.gif
│   │
│   ├── ghost_data/              # Enhanced capture (NEW)
│   │   ├── sessions/
│   │   │   ├── {session_id}.json
│   │   │   └── {session_id}_summary.md
│   │   ├── graphs/
│   │   │   └── {session_id}_graph.json
│   │   └── notes/
│   │       └── {session_id}_notes.json
│   │
│   └── task_notes/              # UI notes (NEW)
│       └── {task_id}_note.json
│
├── webui.py
├── requirements.txt
│
├── INSTALLATION_GUIDE.md        ◄── NEW
├── GHOST_FEATURES.md            ◄── NEW
├── UPGRADE_NOTES.md             ◄── NEW
├── QUICK_REFERENCE.md           ◄── NEW
└── README.md                    ◄── UPDATED
```

---

## 🔄 Component Interactions

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                  │
│  (Gradio Components - Buttons, Text, Charts)            │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Component Layer                         │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐ │
│  │Dashboard │  │  Notes   │  │  Agent Tabs          │ │
│  │   Tab    │  │   Tab    │  │  (Existing)          │ │
│  └──────────┘  └──────────┘  └──────────────────────┘ │
│       │             │                    │              │
│       └─────────────┴────────────────────┘              │
│                     │                                   │
└─────────────────────┼───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Management Layer                            │
│                                                          │
│  ┌──────────────────┐      ┌────────────────────────┐ │
│  │  WebuiManager    │◄────►│  GhostDataCapture     │ │
│  │  (Component Mgmt)│      │  (Data Collection)    │ │
│  └──────────────────┘      └────────────────────────┘ │
│           │                          │                  │
└───────────┼──────────────────────────┼──────────────────┘
            │                          │
            ▼                          ▼
┌─────────────────────────────────────────────────────────┐
│                 Execution Layer                          │
│                                                          │
│  ┌──────────────────┐      ┌────────────────────────┐ │
│  │  Browser Agent   │      │  Controller            │ │
│  │  (Task Executor) │◄────►│  (Browser Control)     │ │
│  └──────────────────┘      └────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│                  Storage Layer                           │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │Agent History │  │ Ghost Data   │  │  Task Notes  │ │
│  │   (JSON)     │  │ (JSON + MD)  │  │   (JSON)     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Data Schema

### Session Data Schema

```javascript
{
  // Session Identification
  "session_id": "YYYYMMDD_HHMMSS_microseconds",
  "task": "String - User's task description",
  
  // Timing
  "start_time": "ISO 8601 timestamp",
  "end_time": "ISO 8601 timestamp",
  
  // Status
  "status": "completed | failed | cancelled",
  "final_result": "String - Final output",
  
  // Metadata
  "metadata": {
    "llm_provider": "openai | anthropic | etc",
    "llm_model": "gpt-4 | claude-3 | etc",
    "use_vision": true | false
  },
  
  // Steps Array
  "steps": [
    {
      "step_number": 1,
      "timestamp": "ISO 8601 timestamp",
      "action": "navigate | click | type | etc",
      "reasoning": "Why this action was taken",
      "state": { /* Browser state object */ },
      "screenshot": "base64 encoded image",
      "success": true | false,
      "duration": 2.5,  // seconds
      "tokens": 150,
      "errors": []
    }
  ],
  
  // Notes
  "notes": [
    {
      "timestamp": "ISO 8601 timestamp",
      "type": "user | system | agent",
      "content": "Note text",
      "metadata": {}
    }
  ],
  
  // Statistics
  "stats": {
    "total_steps": 5,
    "successful_actions": 5,
    "failed_actions": 0,
    "total_tokens": 750,
    "total_duration": 143.23
  }
}
```

### Dashboard Analytics Schema

```javascript
{
  "total_tasks": 10,
  "successful_tasks": 8,
  "failed_tasks": 2,
  "total_steps": 50,
  "total_duration": 1200.5,
  "total_tokens": 15000,
  
  "tasks_by_date": {
    "2025-10-28": 5,
    "2025-10-27": 3,
    "2025-10-26": 2
  },
  
  "recent_tasks": [
    {
      "id": "20251028_143022_123456",
      "task": "Search for Python tutorials",
      "status": "Success",
      "steps": 5,
      "timestamp": 1730123456.789
    }
  ]
}
```

---

## 🎨 UI Component Hierarchy

```
GhostWebUI (Gradio Blocks)
│
├── Header (Markdown)
│   └── Ghost Logo + Title
│
└── Tabs (Gradio Tabs)
    │
    ├── Agent Settings Tab
    │   └── LLM Configuration Forms
    │
    ├── Browser Settings Tab
    │   └── Browser Configuration Forms
    │
    ├── Run Agent Tab
    │   ├── User Input (Textbox)
    │   ├── Chatbot (Agent Interaction)
    │   ├── Control Buttons (Run/Stop/Pause/Clear)
    │   ├── Browser View (HTML)
    │   └── Outputs (File/Image)
    │
    ├── 📊 Dashboard Tab (NEW)
    │   ├── Refresh Button
    │   ├── Metrics Cards (HTML)
    │   │   ├── Total Tasks Card
    │   │   ├── Successful Tasks Card
    │   │   ├── Failed Tasks Card
    │   │   └── Total Steps Card
    │   ├── Success Rate Bar (HTML)
    │   └── Recent Tasks Table (HTML)
    │
    ├── 📝 Notes & Visualization Tab (NEW)
    │   ├── Sub-Tab: Step Flowchart
    │   │   ├── Task ID Input
    │   │   ├── Load Button
    │   │   └── Flowchart Display (HTML)
    │   │
    │   ├── Sub-Tab: Mind Map
    │   │   ├── Task ID Input
    │   │   ├── Generate Button
    │   │   └── Mind Map Display (HTML)
    │   │
    │   └── Sub-Tab: Task Notes
    │       ├── Task ID Input
    │       ├── Note Content (Textbox)
    │       ├── Save Button
    │       ├── Refresh Button
    │       └── Notes Display (JSON)
    │
    ├── Agent Marketplace Tab
    │   └── Deep Research Sub-Tab
    │
    └── Load & Save Config Tab
        └── Configuration Management
```

---

## 🔌 Integration Points

### For Custom Extensions

```python
# Add custom metric to dashboard
def load_task_analytics():
    analytics = {
        # ... existing metrics ...
        "custom_metric": calculate_custom_metric()
    }
    return analytics

# Add custom visualization
def create_custom_visualization_tab(ui_manager):
    with gr.Column():
        # Your custom UI components
        pass
    
    # Register with manager
    ui_manager.add_components("custom_viz", components)

# Hook into data capture
from src.utils.ghost_data_capture import ghost_capture

# Before task
session_id = ghost_capture.start_session(task)

# During execution
ghost_capture.capture_step(step_num, step_data)

# After task
ghost_capture.end_session(result, status)
```

---

## 🎯 Event Flow

```
User Action
    │
    ▼
Gradio Event Trigger
    │
    ▼
Event Handler Function
    │
    ├──► Read UI Components
    │
    ├──► Process Data
    │    ├──► Load from Storage
    │    ├──► Transform Data
    │    └──► Generate Visuals
    │
    ├──► Update UI Components
    │
    └──► Yield Results
         │
         ▼
    Gradio Updates UI
         │
         ▼
    User Sees Results
```

---

This architecture supports:
- ✅ Modular component design
- ✅ Separation of concerns
- ✅ Easy extensibility
- ✅ Data persistence
- ✅ Real-time updates
- ✅ Rich visualizations

**The Ghost architecture is designed for scalability and maintainability!** 👻
