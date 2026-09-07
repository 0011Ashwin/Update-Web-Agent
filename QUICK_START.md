# Quick Start: OmniRoute + Obsidian Vault

## ⚡ TL;DR - 3 Steps to Go

### Step 1: Verify Setup
```bash
cd d:\Web-testing-OG\Update-Web-Agent
python check_omniroute.py
```
✅ Should show: "All systems ready!"

### Step 2: Open Obsidian Vault
1. Launch Obsidian Desktop
2. Click "Open vault as folder"
3. Select: `d:\Obsidian\Update-Web-Agent-Vault`

### Step 3: Run Agent
```bash
python webui.py
# or run any agent task
```

**🎉 That's it! Agent research automatically appears in Obsidian.**

---

## 📁 Vault Locations

| Item | Path |
|------|------|
| **Vault Root** | `d:\Obsidian\Update-Web-Agent-Vault` |
| **Research** | `.../Research/` |
| **Findings** | `.../Findings/` |
| **Task Logs** | `.../Task Logs/` |
| **OmniRoute** | `http://localhost:20128` |

---

## 🔑 Key Configuration

**.env settings:**
```
ANTHROPIC_ENDPOINT=http://localhost:20128
ANTHROPIC_API_KEY=sk-994bd13c21f1dd82-749150-df4bdba7
OBSIDIAN_VAULT_PATH=d:\Obsidian\Update-Web-Agent-Vault
```

---

## 💻 Using the Vault in Code

```python
# Import vault functions
from src.utils.obsidian_vault import (
    write_research_to_vault,
    write_finding_to_vault,
    write_task_log_to_vault
)

# Write research
await write_research_to_vault(
    topic="My Topic",
    content="# My Research\n\nFindings here...",
    tags=["research"]
)

# Write finding
await write_finding_to_vault(
    title="Important Discovery",
    finding="What I found",
    source="https://url",
    confidence="high"
)

# Log task
await write_task_log_to_vault(
    task_id="task-001",
    task_name="Research Task",
    status="completed",
    details="Task details",
    result="Result summary"
)
```

---

## 🎯 What Happens Automatically

✅ Task starts → Logged to vault  
✅ Agent runs → Can write research & findings  
✅ Task completes → Summary logged to vault  
✅ Open Obsidian → All data synced and searchable  

---

## 🔍 Useful Obsidian Queries

In Obsidian, create notes with these DataView queries:

### Recent Research
```dataview
LIST FROM "Research" SORT file.ctime DESC LIMIT 10
```

### High-Confidence Findings
```dataview
TABLE confidence, source FROM "Findings" WHERE confidence = "high"
```

### Today's Tasks
```dataview
LIST FROM "Task Logs" WHERE file.ctime.year = date(today).year AND file.ctime.month = date(today).month AND file.ctime.day = date(today).day
```

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| Files not appearing | Restart Obsidian or press `Ctrl+R` |
| OmniRoute not found | Run `check_omniroute.py` to diagnose |
| Can't write to vault | Check folder permissions at `d:\Obsidian\Update-Web-Agent-Vault` |
| Encoding errors | Ensure .env is UTF-8 and uses forward slashes |

---

## 📚 Full Guide

See `OBSIDIAN_VAULT_GUIDE.md` for complete documentation.

---

**Your agent's second brain is now ready. Every discovery becomes searchable knowledge! 🧠**
