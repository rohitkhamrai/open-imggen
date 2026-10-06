---
description: Always check logs of background tasks proactively
trigger: always_on
---

# Always Check Logs

When running background tasks or remote scripts (like bash scripts on Ubuntu), NEVER just wait indefinitely assuming they will succeed. 
Always proactively check the task output logs shortly after launching them to ensure they didn't fail early (e.g., due to 404 errors, missing dependencies, or syntax errors). If you don't check the logs, you might wait forever for a task that crashed on line 1.
