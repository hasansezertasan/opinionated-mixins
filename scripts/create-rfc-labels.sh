#!/usr/bin/env bash
# Create (or update) the GitHub labels the RFC process relies on.
#
# Requires the GitHub CLI (`gh`) authenticated against this repo.
# Idempotent: `--force` updates a label if it already exists.
#
# Usage:
#   scripts/create-rfc-labels.sh            # target the current repo
#   GH_REPO=owner/name scripts/create-rfc-labels.sh
set -euo pipefail

# label name | color (hex, no #) | description
labels=(
  "rfc|5319e7|Request for Comments — proposal PR (see docs/rfcs/README.md)"
  "status:accepted|0e8a16|RFC accepted — implementation may proceed"
  "status:rejected|d73a4a|RFC rejected — will not proceed"
  "status:deferred|fbca04|RFC deferred — revisit later"
  "status:withdrawn|6a737d|RFC withdrawn by the author"
)

for entry in "${labels[@]}"; do
  IFS='|' read -r name color description <<<"$entry"
  echo "Creating/updating label: $name"
  gh label create "$name" --color "$color" --description "$description" --force
done

echo "Done. RFC labels are in place."
