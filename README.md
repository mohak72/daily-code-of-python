Daily Python snippets

This repository holds short daily Python snippets.

How it works

- Run `python generate_daily.py` to create a new date-stamped snippet in `daily/`.
- Use `python generate_daily.py --commit` to create a local git commit for the generated file.
- Pushing to GitHub must be done locally by you (e.g. `git push`) after configuring auth.

Automating commits

A GitHub Actions workflow is included to run on a schedule. It cannot push without
credentials configured as repository secrets (see the workflow file for details).
