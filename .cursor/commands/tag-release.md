---
description: Tag source with release version from change-log
---

# Tag source with release version

## Task
Read the latest release version from `change-log.md` (not the Unreleased section), create a git tag with that version, and push the tag to GitHub (origin).

## Requirements
1. Find the most recent version number in `change-log.md` (format: M.m.b)
2. Create a git tag in the format `vVERSION` (e.g., for version 0.5.1, create tag `v0.5.1`)
3. Push the tag to origin (GitHub)

## Example
If the latest release in `change-log.md` is `## [0.5.1]`, then:
- Create tag: `v0.5.1`
- Push tag: `git push origin v0.5.1`
