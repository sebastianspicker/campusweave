# Release cleanup

CampusWeave `0.1.0-alpha.1` is an unpublished local source candidate. The
current release blockers are maintained in [RELEASE_STATUS.md](../RELEASE_STATUS.md);
the candidate procedure is in [RELEASING.md](../RELEASING.md).

## Candidate review

Before requesting publication approval, run the complete local gate in
[CONTRIBUTING.md](../CONTRIBUTING.md), inspect the final diff, and confirm the
repository contains no credentials, tenant identifiers, target-derived
contracts, inventories, request or response captures, audit exports, private
plans, or local tool state.

The three synthetic screenshots are static documentation assets. Review the
relevant local routes manually in a current browser before replacing them;
there is no automated screenshot-regeneration workflow.

Inspect the browser views and images for private data before review. The images
are documentation evidence, not browser accessibility, tenant, device, or
deployment proof.

## Do not infer publication

Local tests and a configured Git remote do not prove a tag, release,
distribution, remote CI result, Pages deployment, license, or compatibility
with a live Relution tenant. Those items require separate verification after
explicit authorization.
