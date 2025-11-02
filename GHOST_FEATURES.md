# 👻 Ghost - Advanced Features Guide

## Overview

Ghost now includes powerful visualization, analytics, and note-taking features that provide comprehensive insights into your AI agent's activities.

## 🆕 New Features

### 1. 📊 Dashboard Tab

The Dashboard provides real-time analytics and insights into your agent's performance:

#### Features:
- **Task Statistics**: View total tasks, successful tasks, failed tasks, and total steps
- **Success Rate**: Visual progress bar showing overall success rate
- **Recent Tasks**: Table displaying the 10 most recent tasks with:
  - Task description
  - Status (Success/Failed)
  - Number of steps
  - Timestamp

#### How to Use:
1. Navigate to the **📊 Dashboard** tab
2. Click **🔄 Refresh Dashboard** to update the statistics
3. View your agent's performance metrics at a glance

---

### 2. 📝 Notes & Visualization Tab

This comprehensive tab includes three powerful sub-features:

#### A. 🔄 Step Flowchart

Visualize your agent's execution as a beautiful, animated flowchart:

**Features:**
- Animated step-by-step visualization
- Each step shows:
  - Action type
  - Reasoning
  - Duration
  - Token usage
- Hover effects for better interaction
- Color-coded status indicators

**How to Use:**
1. Go to **📝 Notes & Visualization** → **🔄 Step Flowchart**
2. Enter the Task ID (see "How to Find Task ID" section below)
3. Click **📊 Load Flowchart**
4. View the animated flowchart of your agent's steps

**How to Find Task ID:**
There are three easy ways to find your Task ID:

**Method 1: From Dashboard (Easiest)**
1. Go to **📊 Dashboard** tab
2. Click **🔄 Refresh Dashboard**
3. Look at the "Recent Tasks" table
4. The Task ID is shown in the table or you can find it in the file system

**Method 2: From File Explorer**
1. Navigate to: `./tmp/agent_history/` folder
2. Each folder name IS the Task ID
3. Example: `20251028_143022_123456` is a Task ID
4. Copy the folder name to use in visualizations

**Method 3: From PowerShell**
```powershell
# List all available Task IDs
Get-ChildItem -Path ".\tmp\agent_history" -Directory | Select-Object Name

# Show most recent Task ID
Get-ChildItem -Path ".\tmp\agent_history" -Directory | Sort-Object CreationTime -Descending | Select-Object -First 1 | Select-Object Name
```

**Task ID Format:**
- Task IDs follow this format: `YYYYMMDD_HHMMSS_microseconds`
- Example: `20251028_143022_123456`
  - `20251028` = October 28, 2025
  - `143022` = 2:30:22 PM
  - `123456` = Microseconds for uniqueness

#### B. 🧠 Mind Map

View your task execution as an interactive mind map:

**Features:**
- Central node displaying the main task
- Branch nodes for each step
- Animated scaling and hover effects
- Grid layout for optimal space usage
- Shows up to 8 key steps

**How to Use:**
1. Go to **📝 Notes & Visualization** → **🧠 Mind Map**
2. Enter the Task ID
3. Click **🗺️ Generate Mind Map**
4. Explore the visual representation of your task

#### C. 📝 Task Notes

Create and manage detailed notes for your tasks:

**Features:**
- Save notes for specific tasks
- View all notes with timestamps
- JSON export of notes
- Persistent storage

**How to Use:**
1. Go to **📝 Notes & Visualization** → **📝 Task Notes**
2. Enter Task ID
3. Write your notes in the text area
4. Click **💾 Save Note**
5. Click **🔄 Refresh Notes** to view all notes

---

### 3. 🎯 Enhanced Data Capture System

Ghost automatically captures comprehensive data for every task execution:

#### Automatically Captured Data:
- **Step-by-Step Information**:
  - Action taken
  - Reasoning
  - State information
  - Screenshots
  - Success/failure status
  - Duration and token usage
  
- **Session Statistics**:
  - Total steps
  - Successful actions
  - Failed actions
  - Total tokens used
  - Total duration
  - Success rate

- **Generated Reports**:
  - JSON session data
  - Markdown summary report
  - Graph data for visualization

#### Storage Locations:
```
./tmp/ghost_data/
├── sessions/          # JSON session files
│   ├── {session_id}.json
│   └── {session_id}_summary.md
├── graphs/           # Graph data files
│   └── {session_id}_graph.json
└── notes/           # Task notes
    └── {task_id}_note.json
```

---

## 📈 Visualization Features

### Color Coding
- **Purple/Indigo** (#7546f2): Primary actions and successful operations
- **Green** (#28c878): Successful tasks and positive metrics
- **Red** (#f24646): Failed tasks and errors
- **Orange** (#f2ba46): Warnings and important information

### Animations
- **Fade-in animations**: Smooth entrance of elements
- **Hover effects**: Interactive feedback on cards and buttons
- **Pulse animations**: Highlight important metrics
- **Flow animations**: Visual connections between steps

---

## 🚀 Best Practices

### 1. Regular Dashboard Monitoring
- Check the dashboard after completing multiple tasks
- Monitor success rates to identify patterns
- Review recent tasks for quick insights

### 2. Detailed Step Analysis
- Use the Step Flowchart for debugging failed tasks
- Analyze reasoning at each step
- Check duration and token usage for optimization

### 3. Mind Map for Planning
- Generate mind maps to understand task structure
- Share mind maps with team members
- Use for documentation and presentations

### 4. Comprehensive Note-Taking
- Document important findings during task execution
- Add context about specific task requirements
- Record issues and solutions for future reference

---

## 📊 Data Export

All data is stored in standard JSON format for easy export and integration:

### Session Data Format:
```json
{
  "session_id": "20251028_143022_123456",
  "task": "Search for Python tutorials",
  "start_time": "2025-10-28T14:30:22.123456",
  "end_time": "2025-10-28T14:32:45.789012",
  "status": "completed",
  "steps": [
    {
      "step_number": 1,
      "action": "navigate",
      "reasoning": "Opening Google to search",
      "success": true,
      "duration": 2.5,
      "tokens": 150
    }
  ],
  "stats": {
    "total_steps": 5,
    "successful_actions": 5,
    "failed_actions": 0,
    "total_tokens": 750,
    "total_duration": 143.23
  }
}
```

---

## 🔧 Technical Details

### Dependencies
All visualization features use:
- **Gradio**: For UI components
- **Python standard library**: json, os, datetime
- **No external visualization libraries required**

### Performance
- Lightweight HTML/CSS rendering
- Minimal memory footprint
- Fast data loading from JSON files
- Responsive design for all screen sizes

---

## 🎨 Customization

### CSS Variables
You can customize the Ghost theme by modifying these CSS variables in `interface.py`:

```css
--ghost-primary: #7546f2;
--ghost-secondary: #9046f2;
--ghost-background: #13131f;
--ghost-card: #22222f;
--ghost-text: #e0e0ff;
--ghost-border: #4c3ba1;
--ghost-shadow: rgba(117, 70, 242, 0.2);
```

---

## 🆘 Troubleshooting

### Dashboard Not Loading
- Ensure `./tmp/agent_history` directory exists
- Check file permissions
- Click refresh button multiple times

### Flowchart Not Displaying
- Verify the Task ID is correct
- Check that the task has completed
- Ensure JSON file exists in agent_history folder

### Notes Not Saving
- Check write permissions for `./tmp/task_notes`
- Ensure Task ID is provided
- Verify content is not empty

---

## 🔮 Future Enhancements

Coming soon:
- Real-time graphs with Chart.js integration
- Export to PDF/HTML
- Advanced filtering and search
- Comparison between multiple tasks
- AI-powered insights and recommendations
- Collaborative note-sharing
- Custom dashboard widgets

---

## 📞 Support

For issues or feature requests, please check the main README.md or create an issue in the repository.

---

**Ghost - Your Intelligent Browser Companion** 👻
