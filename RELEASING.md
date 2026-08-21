# Releasing

CampusWeave currently has no publishable release. Repository history and an
`origin` remote exist, but the source candidate has no public license, tag,
published distribution, or verified remote CI result.

## Candidate preparation

Before publication:

1. Add an approved public license and any required third-party attribution.
2. Verify the established repository history and intended GitHub remote.
3. Confirm the version in `RELEASE_STATUS.md` and
   `docs/releases/0.1.0-alpha.1.md`.
4. Run the complete local gate in `CONTRIBUTING.md`.
5. Inspect all three checked-in screenshots for private or target-specific data.
6. Run `python3 scripts/validate_machine_docs.py` and confirm that the checked-in
   catalog remains `not_generated`.
7. Review the complete candidate for credentials, customer data, target
   evidence, private plans, and local tool state.
8. Verify the GitHub Actions result on the exact candidate commit.

Do not infer a repository URL, release URL, or publication identity from the
local directory name.

## Publication

Publication requires explicit repository-owner approval for the exact commit,
tag, and release contents. The intended first tag is `v0.1.0-alpha.1`, with the
matching notes under `docs/releases/`.

Local tests do not prove that a remote workflow, tag, or release completed.
Verify the rendered repository, workflow result, tag, and release after
publication.
