# ESPHome Technibel SCDF32

IR control for the Technibel SCDF32C5I air conditioner through ESPHome and Home Assistant.

## Architecture

- This repository is the development, documentation, and version-control copy.
- The live ESPHome and Home Assistant environments run on a dedicated VM, separately from this repository.
- The repository and live VM are not assumed to synchronize automatically. Never assume a repository edit is live.
- Discover and verify the live paths and deployment mechanism on the VM before any deployment; do not reuse historical NAS paths.

## Current direction

- Treat `docs/plan-v2-validation.md` as the active validation plan and `docs/status.md` as historical session state.
- Validate Piste A (external IR) before attempting Piste B1 (direct receiver-line injection).
- The reverse-engineered frame encoding and checksum are frozen. Change physical timing only after instrumented comparison with the original remote.
- Every phase gate in the V2 plan must pass before advancing.
- Before connecting USB-grounded equipment to the AC electronics, confirm mains-to-logic isolation as required by phases 11–14. If isolation is ambiguous, B1 remains blocked.

## Key files

- `docs/plan-v2-validation.md`: authoritative staged plan and safety gates.
- `docs/protocol.md`: proprietary 48-bit IR protocol.
- `docs/control-strategies.md`: Piste A, B1, and B2 tradeoffs.
- `docs/wiring.md`: transmitter and sniffer wiring.
- `docs/troubleshooting.md`: known hardware diagnostic procedure.
- `esphome/ir-technibel-clim.yaml`: main ESPHome device configuration.
- `esphome/libraries/technibel_ir.h`: IR frame implementation.
- `homeassistant/climate-technibel-ha.yaml`: Home Assistant MQTT climate package.

## Validation and deployment

1. Validate ESPHome configuration before claiming a firmware change is ready.
2. Never perform a standalone local ESPHome compilation. Use the live ESPHome instance, which delegates builds to its remote compiler.
3. Identify the dedicated VM, live paths, access method, and rollback path before deployment.
4. Transfer approved repository files to the VM explicitly through the verified deployment mechanism; report repository state and live state separately.
5. Compile and flash through the live ESPHome environment only after validation succeeds.
6. Keep hardware changes atomic, reversible, and tied to the gatekeeper tests in the V2 plan.

## Git completion rule

- Do not leave project changes only in the working tree at handoff or session end.
- Finish an authorized change by validating it, reviewing the semantic diff and `git diff --numstat`, then committing every intended project file atomically.
- Preserve unrelated user changes and include them only when Florent explicitly asks to commit everything.
- Report any remaining untracked, modified, staged, or unpushed state explicitly. A commit is local history until it is pushed; do not claim remote publication without verifying it.

## Beads routing

- Use the shared Beads database from `BEADS_DIR`.
- Filter work with `--metadata-field project=esphome-technibel-scdf32`.
- Every created issue must include `--metadata '{"project":"esphome-technibel-scdf32"}'`; use `--set-metadata project=esphome-technibel-scdf32` only when updating an existing issue.
- Use Beads for durable task tracking; `docs/BACKLOG-legacy.md` is not the live tracker.
- Execute implementation issues sequentially, keep at most one project issue `in_progress`, and claim it atomically with `bd update <id> --claim` before editing.
- When Florent requests a review or the risk justifies independent verification, create a self-contained handoff to a fresh agent/session. The reviewer uses a separate issue and records findings as notes or `discovered-from` follow-up issues.
- See `docs/multi-agent-beads.md` for the project workflow.
