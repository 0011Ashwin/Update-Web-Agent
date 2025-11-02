# 📍 Task ID Location - Visual Guide

## 🎯 Where is My Task ID? (Visual Walkthrough)

### Location 1: File Explorer 📁

```
Your Project Folder
    │
    ├── 📁 src
    ├── 📁 assets
    ├── 📁 tmp  ◄── Open this folder
    │   │
    │   ├── 📁 agent_history  ◄── Open this folder
    │   │   │
    │   │   ├── 📁 20251028_143022_123456  ◄── This IS your Task ID!
    │   │   │   ├── 📄 20251028_143022_123456.json
    │   │   │   └── 🖼️ 20251028_143022_123456.gif
    │   │   │
    │   │   ├── 📁 20251028_142510_789012  ◄── Another Task ID
    │   │   │   ├── 📄 20251028_142510_789012.json
    │   │   │   └── 🖼️ 20251028_142510_789012.gif
    │   │   │
    │   │   └── 📁 20251028_142005_456789  ◄── Another Task ID
    │   │       ├── 📄 20251028_142005_456789.json
    │   │       └── 🖼️ 20251028_142005_456789.gif
    │   │
    │   ├── 📁 ghost_data
    │   └── 📁 task_notes
    │
    ├── 📄 webui.py
    └── 📄 README.md
```

**Step-by-Step:**
1. Open File Explorer (Windows Key + E)
2. Navigate to: `E:\Project-AGENT-Web\Web-Agent-main\`
3. Open folder: `tmp\`
4. Open folder: `agent_history\`
5. **SEE THE FOLDERS? Each folder name = Task ID!**
6. Right-click folder name → Copy
7. You now have the Task ID!

---

### Location 2: PowerShell 💻

**Open PowerShell in your project folder:**

```powershell
PS E:\Project-AGENT-Web\Web-Agent-main> cd tmp\agent_history
PS E:\Project-AGENT-Web\Web-Agent-main\tmp\agent_history> dir

    Directory: E:\Project-AGENT-Web\Web-Agent-main\tmp\agent_history

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        10/28/2025   2:30 PM                20251028_143022_123456  ◄── Task ID
d-----        10/28/2025   2:25 PM                20251028_142510_789012  ◄── Task ID
d-----        10/28/2025   2:20 PM                20251028_142005_456789  ◄── Task ID
```

**Quick Command:**
```powershell
# List all Task IDs
Get-ChildItem -Path ".\tmp\agent_history" -Directory | Select-Object Name
```

**Output:**
```
Name
----
20251028_143022_123456  ◄── Copy this!
20251028_142510_789012  ◄── Or this!
20251028_142005_456789  ◄── Or this!
```

---

### Location 3: Dashboard 📊

**In Ghost WebUI:**

```
┌──────────────────────────────────────────────────────┐
│                   📊 Dashboard                        │
├──────────────────────────────────────────────────────┤
│                                                       │
│  [🔄 Refresh Dashboard]  ◄── Click this first        │
│                                                       │
│  ┌────────────────────────────────────────────────┐ │
│  │              Recent Tasks                      │ │
│  ├────────────────────┬──────┬──────┬────────────┤ │
│  │ Task               │Status│Steps │ Timestamp  │ │
│  ├────────────────────┼──────┼──────┼────────────┤ │
│  │ Search Python...   │ ✅   │  5   │ 14:30:22  │ │  ◄── This task
│  │ Open Google        │ ✅   │  3   │ 14:25:10  │ │
│  │ Find docs          │ ❌   │  7   │ 14:20:05  │ │
│  └────────────────────┴──────┴──────┴────────────┘ │
│                                                       │
└──────────────────────────────────────────────────────┘
```

**To get Task ID:**
1. Note the timestamp: `14:30:22`
2. Note the date: Today's date
3. Task ID format: `20251028_143022_xxxxxx`
4. Go to File Explorer and find folder with that date/time
5. Or use PowerShell to list and match

---

### Location 4: In Ghost After Running Task 🤖

**When task completes, you'll see:**

```
┌──────────────────────────────────────────────────────┐
│              🤖 Run Agent                             │
├──────────────────────────────────────────────────────┤
│                                                       │
│  Task: Search for Python tutorials                   │
│                                                       │
│  Status: ✅ Task Completed                           │
│                                                       │
│  Task Outputs:                                       │
│  ┌────────────────────────────────────────────────┐ │
│  │ 📄 Agent History JSON                          │ │
│  │    20251028_143022_123456.json  ◄── Task ID!  │ │
│  │    [Download]                                  │ │
│  │                                                │ │
│  │ 🖼️ Task Recording GIF                          │ │
│  │    20251028_143022_123456.gif   ◄── Task ID!  │ │
│  │    [View]                                      │ │
│  └────────────────────────────────────────────────┘ │
│                                                       │
└──────────────────────────────────────────────────────┘
```

**Just copy the number from the filename!**

---

## 🎨 Task ID Breakdown

### Understanding the Format

```
20251028_143022_123456
│      │ │    │ │    │
│      │ │    │ └────┴─► Microseconds (unique identifier)
│      │ │    └────────► Seconds (22)
│      │ └─────────────► Minutes & Hours (14:30 = 2:30 PM)
│      └───────────────► Day (28)
└──────────────────────► Year & Month (2025-10)

Full meaning: October 28, 2025 at 2:30:22.123456 PM
```

### Real Example

```
Task ID: 20251028_143022_123456

Breaking it down:
- Date: October 28, 2025
- Time: 14:30:22 (2:30:22 PM)
- Unique: 123456 microseconds

This tells you WHEN the task was created!
```

---

## ✅ How to Verify You Have the Right Task ID

### Test 1: Check if folder exists
```powershell
# Replace with your Task ID
Test-Path ".\tmp\agent_history\20251028_143022_123456"
```
**Should return:** `True`

### Test 2: Check if JSON file exists
```powershell
# Replace with your Task ID
Test-Path ".\tmp\agent_history\20251028_143022_123456\20251028_143022_123456.json"
```
**Should return:** `True`

### Test 3: View task details
```powershell
# Replace with your Task ID
$json = Get-Content ".\tmp\agent_history\20251028_143022_123456\20251028_143022_123456.json" | ConvertFrom-Json
$json.task
```
**Should show:** Your task description

---

## 🎯 Common Mistakes

### ❌ Wrong: Using the filename
```
20251028_143022_123456.json  ◄── NO! This is a file, not the Task ID
```

### ✅ Correct: Using the folder name
```
20251028_143022_123456  ◄── YES! This is the Task ID
```

### ❌ Wrong: Adding file extension
```
Task ID: 20251028_143022_123456.json  ◄── NO!
```

### ✅ Correct: Just the folder name
```
Task ID: 20251028_143022_123456  ◄── YES!
```

### ❌ Wrong: Including path
```
Task ID: tmp/agent_history/20251028_143022_123456  ◄── NO!
```

### ✅ Correct: Just the ID
```
Task ID: 20251028_143022_123456  ◄── YES!
```

---

## 🚀 Pro Tips

### 1. Always Use the Latest Task
The most recent task has the highest timestamp:
```
20251028_143022_123456  ◄── Latest (14:30:22)
20251028_142510_789012  ◄── Older  (14:25:10)
20251028_142005_456789  ◄── Oldest (14:20:05)
```

### 2. Match by Time
If you ran a task at 2:30 PM, look for `14302` in the Task ID

### 3. Quick Copy Shortcut
```powershell
# Copy latest Task ID to clipboard in one command
(gci ".\tmp\agent_history" -Directory | sort CreationTime -Desc | select -First 1).Name | scb
```

### 4. Create a Function
Add to your PowerShell profile:
```powershell
function gtid {
    # Get Task ID
    (Get-ChildItem ".\tmp\agent_history" -Directory | 
     Sort-Object CreationTime -Descending | 
     Select-Object -First 1).Name | Set-Clipboard
    $id = Get-Clipboard
    Write-Host "✅ Copied to clipboard: $id" -ForegroundColor Green
}

# Usage: Just type 'gtid' in PowerShell
```

---

## 📝 Usage Example

Once you have the Task ID:

```
1. Copy Task ID: 20251028_143022_123456

2. Go to Ghost WebUI → 📝 Notes & Visualization

3. Click on "🔄 Step Flowchart" tab

4. Paste Task ID: [20251028_143022_123456]

5. Click [📊 Load Flowchart]

6. See your beautiful visualization! ✨
```

---

## 🆘 Still Can't Find It?

### Quick Diagnostic:

```powershell
# Run this diagnostic script
Write-Host "=== Ghost Task ID Diagnostic ===" -ForegroundColor Cyan

# Check if folder exists
if (Test-Path ".\tmp\agent_history") {
    Write-Host "✅ agent_history folder exists" -ForegroundColor Green
    
    # Count tasks
    $count = (Get-ChildItem ".\tmp\agent_history" -Directory).Count
    Write-Host "📊 Found $count task(s)" -ForegroundColor Yellow
    
    if ($count -gt 0) {
        Write-Host "`nYour Task IDs:" -ForegroundColor Cyan
        Get-ChildItem ".\tmp\agent_history" -Directory | 
            Sort-Object CreationTime -Descending |
            ForEach-Object {
                Write-Host "  📁 $($_.Name)" -ForegroundColor White
                Write-Host "     Created: $($_.CreationTime)" -ForegroundColor Gray
            }
    } else {
        Write-Host "❌ No tasks found. Run a task first!" -ForegroundColor Red
    }
} else {
    Write-Host "❌ agent_history folder not found!" -ForegroundColor Red
    Write-Host "📍 Expected at: .\tmp\agent_history" -ForegroundColor Yellow
}
```

---

## 📚 Related Documentation

- **GHOST_FEATURES.md** - How to use Task IDs in visualizations
- **QUICK_REFERENCE.md** - Quick commands for Task IDs
- **INSTALLATION_GUIDE.md** - Setup instructions

---

**You're now a Task ID expert! 🎓👻**

Remember: **Folder name in `tmp/agent_history/` = Task ID**

It's that simple! 🎉
