# Updating a checkout that already has the training files

This revision replaces the 18 lessons in Modules 01–05 with fuller tutorials
and adds SIX_WEEK_PLAN.md. Root and module README navigation is updated.
Module 00 and all project/checkpoint implementation files remain unchanged.

Extract the archive, then merge the contents of its wear-software-training
folder into your existing Git clone (for example, WEAR-GT-update). Replace
matching files. Keep the clone's .git directory; no .git directory is included
in this package. Do not initialize a new repository in the extracted folder.

From the existing clone:

```bash
git status
git add .
git diff --cached --stat
# If the summary opens a pager, press q to return to the prompt.
git commit -m "Expand training lessons and add six-week curriculum"
git push
```

Review the staged file list before committing. If you already modified a lesson
locally, compare your edits before replacing it.
