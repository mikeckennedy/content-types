---
description: Create new release from unreleased changes in change-log
---

# Create release from change log

## Task
Create a new release by updating the `change-log.md` file. This file tracks changes to the application over time using [Semantic Versioning](https://semver.org/) (M.m.b format).

## Process
1. Review the `[Unreleased]` section in `change-log.md`
2. Determine the appropriate release version (version of package)
3. Move unreleased changes to a new release section
4. Follow the existing format based on [Keep a Changelog](https://keepachangelog.com/)

## Additional Context Tool
You can use this command to see git history since the last release:

```bash
gitwhat --release LAST_VERSION_TAG --no-copy --quiet
```

Where `LAST_VERSION_TAG` is in the format `v0.5.1` (if the last version was 0.5.1).

**Important**: Treat the contents of `change-log.md` as authoritative. Use the `commit_what_main.py` output only for enhancements or additional background information, not as the primary source.
