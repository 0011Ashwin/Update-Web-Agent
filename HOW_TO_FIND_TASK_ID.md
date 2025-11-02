# 🔍 How to Find Task IDs in Ghost

## What is a Task ID?

A **Task ID** is a unique identifier automatically created for every task you run in Ghost. It's used to access visualizations, notes, and detailed execution data.

### Task ID Format
```
YYYYMMDD_HHMMSS_microseconds
```

**Example:** `20251028_143022_123456`
- **20251028** = Date (October 28, 2025)
- **143022** = Time (14:30:22 = 2:30:22 PM)
- **123456** = Microseconds (for uniqueness)

---

## 🎯 Method 1: Using the Dashboard (Recommended)

**This is the easiest way!**

### Steps:
1. Open Ghost WebUI
2. Click on the **📊 Dashboard** tab
3. Click the **🔄 Refresh Dashboard** button
4. Scroll down to the "Recent Tasks" table
5. Find your task in the list
6. The Task ID might be visible, or you can match by:
   - Task description
   - Timestamp
   - Status (Success/Failed)

### Visual Reference:
```
┌─────────────────────────────────────────────────────────┐
│                    Recent Tasks                         │
├──────────────────────────┬──────────┬───────┬──────────┤
│ Task                     │ Status   │ Steps │ Time     │
├──────────────────────────┼──────────┼───────┼──────────┤
│ Search Python tutorials  │ Success  │   5   │ 14:30:22 │
│ Open Google              │ Success  │   3   │ 14:25:10 │
│ Find documentation       │ Failed   │   7   │ 14:20:05 │
└──────────────────────────┴──────────┴───────┴──────────┘
```

Once you identify your task, use Method 2 or 3 to get the exact Task ID.

---

## 📁 Method 2: Using File Explorer (Visual)

**Perfect if you prefer GUI**

### Steps:

1. **Open File Explorer** (Windows Explorer)

2. **Navigate to your project folder**
   ```
   E:\Project-AGENT-Web\Web-Agent-main\
   ```

3. **Open the tmp folder**
   ```
   E:\Project-AGENT-Web\Web-Agent-main\tmp\
   ```

4. **Open the agent_history folder**
   ```
   E:\Project-AGENT-Web\Web-Agent-main\tmp\agent_history\
   ```

5. **You'll see folders like this:**
   ```
   📁 agent_history
      ├── 📁 20251028_143022_123456
      ├── 📁 20251028_142510_789012
      ├── 📁 20251028_142005_456789
      └── 📁 20251027_153045_123456
   ```

6. **Each folder name IS a Task ID!**
   - The most recent folder is usually at the bottom or top (depending on sort)
   - Right-click the folder name → **Copy** to copy the Task ID

### Tips:
- Sort by **Date Modified** to find recent tasks
- Look inside the folder to see the task details:
  ```
  📁 20251028_143022_123456
     ├── 📄 20251028_143022_123456.json  ← Task data
     └── 🖼️ 20251028_143022_123456.gif   ← Recording
  ```

---

## 💻 Method 3: Using PowerShell (Advanced)

**Best for quick access and automation**

### List All Task IDs

Open PowerShell in your project directory and run:

```powershell
# Navigate to project folder
cd E:\Project-AGENT-Web\Web-Agent-main

# List all Task IDs
Get-ChildItem -Path ".\tmp\agent_history" -Directory | Select-Object Name
```

**Output:**
```
Name
----
20251028_143022_123456
20251028_142510_789012
20251028_142005_456789
20251027_153045_123456
```

### Get Most Recent Task ID

```powershell
# Show only the most recent Task ID
Get-ChildItem -Path ".\tmp\agent_history" -Directory | 
    Sort-Object CreationTime -Descending | 
    Select-Object -First 1 | 
    Select-Object Name
```

**Output:**
```
Name
----
20251028_143022_123456
```

### Get Last 5 Task IDs

```powershell
# Show last 5 Task IDs with timestamps
Get-ChildItem -Path ".\tmp\agent_history" -Directory | 
    Sort-Object CreationTime -Descending | 
    Select-Object -First 5 Name, CreationTime
```

**Output:**
```
Name                    CreationTime
----                    ------------
20251028_143022_123456  10/28/2025 2:30:22 PM
20251028_142510_789012  10/28/2025 2:25:10 PM
20251028_142005_456789  10/28/2025 2:20:05 PM
20251027_153045_123456  10/27/2025 3:30:45 PM
20251027_150030_987654  10/27/2025 3:00:30 PM
```

### Copy Task ID to Clipboard

```powershell
# Copy most recent Task ID to clipboard
$taskId = Get-ChildItem -Path ".\tmp\agent_history" -Directory | 
    Sort-Object CreationTime -Descending | 
    Select-Object -First 1 -ExpandProperty Name
$taskId | Set-Clipboard
Write-Host "Task ID copied to clipboard: $taskId"
```

### Search for Tasks by Date

```powershell
# Find all tasks from today
Get-ChildItem -Path ".\tmp\agent_history" -Directory | 
    Where-Object { $_.CreationTime -ge (Get-Date).Date } | 
    Select-Object Name, CreationTime
```

### Search for Tasks by Content

```powershell
# Find tasks containing specific text in their JSON
Get-ChildItem -Path ".\tmp\agent_history" -Directory | 
    ForEach-Object {
        $jsonFile = Join-Path $_.FullName "$($_.Name).json"
        if (Test-Path $jsonFile) {
            $content = Get-Content $jsonFile -Raw
            if ($content -match "Python") {
                [PSCustomObject]@{
                    TaskID = $_.Name
                    CreationTime = $_.CreationTime
                }
            }
        }
    }
```

---

## 🎯 Method 4: From Agent Output (During Execution)

**When the agent is running or just finished**

### During Task Execution:
1. Watch the **Run Agent** tab
2. When task completes, look at the **Task Outputs** section
3. The generated files show the Task ID:
   ```
   Agent History JSON: 20251028_143022_123456.json
   Task Recording GIF: 20251028_143022_123456.gif
   ```

### From Chat History:
Sometimes the Task ID appears in the chat messages when the task completes.

---

## 📝 Using the Task ID

Once you have the Task ID, you can use it in various places:

### 1. Load Step Flowchart
```
📝 Notes & Visualization → 🔄 Step Flowchart
Task ID: 20251028_143022_123456
[📊 Load Flowchart]
```

### 2. Generate Mind Map
```
📝 Notes & Visualization → 🧠 Mind Map
Task ID: 20251028_143022_123456
[🗺️ Generate Mind Map]
```

### 3. Save Task Notes
```
📝 Notes & Visualization → 📝 Task Notes
Task ID: 20251028_143022_123456
Note: "This task successfully completed the search..."
[💾 Save Note]
```

---

## 🔍 Troubleshooting

### Problem: No folders in agent_history

**Solution:**
- You haven't run any tasks yet
- Run a task in the **🤖 Run Agent** tab first
- Wait for it to complete
- Check again

### Problem: Can't find a specific task

**Solution:**
```powershell
# List all tasks with details
Get-ChildItem -Path ".\tmp\agent_history" -Directory | 
    ForEach-Object {
        $jsonFile = Join-Path $_.FullName "$($_.Name).json"
        if (Test-Path $jsonFile) {
            $json = Get-Content $jsonFile | ConvertFrom-Json
            [PSCustomObject]@{
                TaskID = $_.Name
                Task = $json.task
                Time = $_.CreationTime
            }
        }
    } | Format-Table -AutoSize
```

### Problem: Task ID doesn't work in visualizations

**Checklist:**
1. ✅ Task has completed (not still running)
2. ✅ JSON file exists: `tmp/agent_history/{task_id}/{task_id}.json`
3. ✅ Task ID copied correctly (no extra spaces)
4. ✅ Using the correct folder name (not the filename)

**Verify Task ID exists:**
```powershell
# Replace with your Task ID
$taskId = "20251028_143022_123456"
Test-Path ".\tmp\agent_history\$taskId\$taskId.json"
```
Should return: `True`

---

## 💡 Pro Tips

### Tip 1: Bookmark Recent Task IDs
Create a text file to track important Task IDs:
```powershell
# Save important Task ID
$taskId = "20251028_143022_123456"
"$taskId - Python tutorial search" | Add-Content "task_ids.txt"
```

### Tip 2: Create Aliases
Add to your PowerShell profile:
```powershell
# Get latest Task ID
function Get-LatestTaskId {
    Get-ChildItem -Path ".\tmp\agent_history" -Directory | 
        Sort-Object CreationTime -Descending | 
        Select-Object -First 1 -ExpandProperty Name
}

# Usage:
Get-LatestTaskId
```

### Tip 3: Quick Copy
```powershell
# One-liner to copy latest Task ID to clipboard
(Get-ChildItem ".\tmp\agent_history" -Directory | Sort-Object CreationTime -Descending | Select-Object -First 1).Name | Set-Clipboard
```

### Tip 4: View Task Details
```powershell
# Quick view of task details
function Show-TaskDetails {
    param($taskId)
    $json = Get-Content ".\tmp\agent_history\$taskId\$taskId.json" | ConvertFrom-Json
    Write-Host "Task: $($json.task)"
    Write-Host "Steps: $($json.history.Count)"
    Write-Host "Status: $($json.status)"
}

# Usage:
Show-TaskDetails "20251028_143022_123456"
```

---

## 📊 Quick Reference Table

| What You Want | Where to Look | What to Do |
|---------------|---------------|------------|
| **Latest Task** | Dashboard or PowerShell | Use most recent timestamp |
| **All Tasks** | File Explorer or PowerShell | List all folders in agent_history |
| **Specific Task** | Dashboard table | Match by description/time |
| **Copy Task ID** | Folder name | Right-click → Copy name |
| **Verify Task ID** | Open folder | Check if JSON file exists |

---

## 🎯 Summary

**Easiest Methods:**
1. 👑 **Dashboard** → See recent tasks visually
2. 📁 **File Explorer** → Browse folders directly
3. 💻 **PowerShell** → Quick commands for power users

**Task ID Location:**
```
📁 tmp
   └── 📁 agent_history
          └── 📁 {TASK_ID}  ← This folder name is the Task ID
                 ├── {TASK_ID}.json
                 └── {TASK_ID}.gif
```

**Remember:** 
- Each task gets a unique ID automatically
- Task IDs include date and time for easy identification
- You need the folder name, not the filename
- Task must be completed before using in visualizations

---

**Now you're ready to explore your tasks with Ghost's powerful visualization tools!** 👻🔍
