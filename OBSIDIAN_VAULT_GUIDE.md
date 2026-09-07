# Update-Web-Agent + Obsidian Vault Integration

## Overview

The Update-Web-Agent now integrates with Obsidian Desktop to create a **real-time agent brain and knowledge base**. As your agent searches, researches, and discovers information, all findings are automatically written to an Obsidian vault that you can open in the Obsidian Desktop app.

This creates a persistent, searchable, and linkable knowledge management system for your projects.

## Features

✅ **Real-time sync**: Agent findings appear in Obsidian instantly  
✅ **Structured storage**: Research, Findings, Task Logs, Concepts organized by type  
✅ **Auto-metadata**: Timestamps, confidence levels, sources tracked automatically  
✅ **Markdown format**: Full Obsidian features (tags, links, embeds, queries)  
✅ **OmniRoute integration**: Works seamlessly with local OmniRoute proxy  
✅ **Async writing**: Non-blocking, fast agent execution  

## Setup

### 1. Fix .env Configuration

The `.env` file has been updated with proper dotenv syntax (not Windows batch `set` commands):

```env
ANTHROPIC_ENDPOINT=http://localhost:20128
ANTHROPIC_API_KEY=sk-994bd13c21f1dd82-749150-df4bdba7
ANTHROPIC_MODEL=auto/best-free

DEFAULT_LLM=anthropic

OBSIDIAN_VAULT_PATH=d:\Obsidian\Update-Web-Agent-Vault
OBSIDIAN_ENABLE_AUTO_SAVE=true
```

### 2. Verify OmniRoute Connection

Run the connectivity test:

```bash
python check_omniroute.py
```

Expected output:
```
✅ OmniRoute: Ready
✅ Obsidian Vault: Ready
✅ Vault Manager: Ready
✅ All systems ready! You can now start the agent.
```

### 3. Open Vault in Obsidian

1. **Launch Obsidian Desktop**
2. **Click "Open vault as folder"**
3. **Select:** `d:\Obsidian\Update-Web-Agent-Vault`
4. **Done!** The vault is now open and monitoring

## Vault Structure

```
Update-Web-Agent-Vault/
├── Research/              # Web research findings
├── Findings/              # Key discoveries & analysis
├── Task Logs/             # Chronological task execution
├── Concepts/              # Technical explanations
├── Tools & Integrations/  # External tool docs
├── Errors & Debugging/    # Issues & solutions
├── _metadata/             # Internal metadata
└── INDEX.md               # Vault entry point
```

## How Agent Writes to Vault

### 1. Research Notes
When the agent performs web research:

```python
await write_research_to_vault(
    topic="Machine Learning Best Practices",
    content="Found 5 papers on model optimization...",
    tags=["ai", "ml", "research"],
    metadata={"source": "arxiv"}
)
```

Creates: `Research/Machine Learning Best Practices - 20260905-113357.md`

### 2. Findings
When the agent discovers something important:

```python
await write_finding_to_vault(
    title="Critical Performance Improvement",
    finding="Batch size of 64 increases throughput by 40%",
    source="https://example.com/optimization",
    confidence="high"
)
```

Creates: `Findings/Critical Performance Improvement - 20260905-113357.md`

### 3. Task Logs
Automatic logging of all task execution:

```python
await write_task_log_to_vault(
    task_id="task-20260905-113357",
    task_name="Web Research Task",
    status="completed",
    details="Found 12 relevant sources",
    result="Documented in Research folder"
)
```

Creates: `Task Logs/task-20260905-113357 - Web Research Task.md`

## Configuration Options

In `.env`:

| Variable | Purpose | Example |
|----------|---------|---------|
| `OBSIDIAN_VAULT_PATH` | Full path to vault directory | `d:\Obsidian\Update-Web-Agent-Vault` |
| `OBSIDIAN_ENABLE_AUTO_SAVE` | Auto-write to vault on discoveries | `true` |
| `ANTHROPIC_ENDPOINT` | OmniRoute proxy endpoint | `http://localhost:20128` |
| `ANTHROPIC_API_KEY` | API key for OmniRoute | `sk-...` |
| `ANTHROPIC_MODEL` | Model selection | `auto/best-free` |

## Python API

Import and use vault functions in your agent code:

```python
from src.utils.obsidian_vault import (
    get_vault_manager,
    write_research_to_vault,
    write_finding_to_vault,
    write_task_log_to_vault
)

# Write research
await write_research_to_vault(
    topic="My Research",
    content="Markdown content here",
    tags=["tag1", "tag2"]
)

# Write finding
await write_finding_to_vault(
    title="Finding Title",
    finding="Description",
    source="https://url",
    confidence="high"  # high, medium, low
)

# Log task
await write_task_log_to_vault(
    task_id="unique-id",
    task_name="Task Name",
    status="running",  # started, running, completed, failed
    details="Current status",
    result="Final result (optional)"
)

# Get vault path
vault = get_vault_manager()
if vault.is_enabled():
    path = vault.get_vault_path()
    print(f"Vault at: {path}")
```

## Agent Integration

The agent now automatically logs:

- **Task start** when `browser_use_agent.run()` begins
- **Step execution** within the run loop
- **Task completion** with execution summary
- **Failures** with error details
- **Interruptions** (Ctrl+C) with state

No manual vault writing needed—it's automatic!

## Obsidian Best Practices

### Recommended Plugins

Install these plugins in Obsidian for better integration:

1. **Dataview** - Query and visualize markdown metadata
   ```dataview
   LIST FROM "Research" WHERE tags CONTAINS "ml"
   ```

2. **Backlinks** - See connections between notes automatically

3. **Calendar** - Browse vault by date

4. **Tag Wrangler** - Organize and manage tags

### Querying the Vault

In any Obsidian note, use DataView queries:

```
# Recent Research
```dataview
LIST file.ctime AS "Created" FROM "Research" SORT file.ctime DESC LIMIT 10
```

# High Confidence Findings
```dataview
TABLE confidence, source FROM "Findings" WHERE confidence = "high"
```

# Tasks by Status
```dataview
GROUP BY status FROM "Task Logs"
```
```

### Linking Between Notes

Obsidian automatically creates backlinks. Reference other notes:

```markdown
See also: [[Machine Learning Best Practices]]
Based on: [[Critical Performance Improvement]]
Task: [[task-20260905-113357 - Web Research Task]]
```

## Troubleshooting

### Vault not showing up in Obsidian

1. Check `OBSIDIAN_VAULT_PATH` in `.env` points to correct location
2. Run `python check_omniroute.py` to initialize vault
3. Restart Obsidian
4. Use "Open vault as folder" and select the directory

### Files not syncing in real-time

1. Obsidian file auto-refresh delay is 1-2 seconds by default
2. Refresh manually: `Ctrl+R` in Obsidian
3. Ensure `OBSIDIAN_ENABLE_AUTO_SAVE=true` in `.env`

### Unicode/Encoding errors

- Vault now writes with UTF-8 encoding
- All emoji and special characters should work
- Report any encoding issues

### Agent not writing to vault

1. Check logs for vault manager initialization errors
2. Run `check_omniroute.py` to test vault writing
3. Verify disk space and folder permissions
4. Check that vault path exists and is writable

## Performance Notes

- Vault writing is **async** and non-blocking
- Agent execution continues while files are written
- Multiple simultaneous writes are queued
- No impact on agent speed or LLM latency

## Examples

### Research Task with Auto-Logging

```python
# Agent automatically logs this task
await browser_agent.run(
    task="Research best practices for ML model deployment",
    max_steps=50
)

# Results appear in vault automatically:
# - Research/Best practices for ML model deployment - {timestamp}.md
# - Task Logs/{task_id} - Research best practices....md
```

### Manual Research Logging

```python
# In your agent code
research_content = """
## Key Findings
- Point 1
- Point 2

## Sources
- [Paper 1](https://...)
- [Paper 2](https://...)
"""

await write_research_to_vault(
    topic="ML Deployment Best Practices",
    content=research_content,
    tags=["ml", "deployment", "research"],
    metadata={"priority": "high", "review_status": "pending"}
)
```

## Next Steps

1. ✅ Fix `.env` file (DONE)
2. ✅ Initialize Obsidian vault (DONE)
3. ✅ Test OmniRoute connection (DONE)
4. 🚀 Run your agent—findings go to Obsidian automatically!
5. 📖 Use Obsidian as your project knowledge base

---

**Questions?** Check the agent logs for vault writing details or run `check_omniroute.py` to diagnose issues.

**This vault is now your agent's second brain. Every discovery, research finding, and task log becomes searchable knowledge.**
