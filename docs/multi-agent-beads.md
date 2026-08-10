# Sequential agent workflow with Beads

This project uses the shared Beads database routed by
`metadata.project=esphome-technibel-scdf32`. Beads is the durable coordination plane;
chat messages are not authoritative task state.

## Operating model

Execute implementation work sequentially and keep at most one project issue `in_progress`.
Each session or agent receives one bounded Beads issue with explicit inputs, owned files,
acceptance criteria, verification, and rollback when state changes are involved.

Dependencies define execution:

- no dependency between two issues means either may be selected next;
- `blocks` means the dependent issue must wait;
- `parent-child` groups work but does not by itself impose an execution order;
- `discovered-from` records follow-up work found during implementation or review.

Before editing, an agent must atomically claim its issue:

```sh
bd update <issue-id> --claim
bd show <issue-id>
```

If the claim fails because another actor owns the issue, the agent must stop and choose
different ready work. Agents must not share ownership of an implementation issue. Finish
or pause the claimed issue durably before another implementation agent starts.

## Sequential implementation

The coordinator prepares the graph before delegation:

1. Split work into roughly one-hour, independently verifiable issues.
2. Define file or subsystem ownership clearly enough for a later session to resume.
3. Add dependencies for real ordering constraints.
4. Confirm ready work with the project metadata filter.
5. Give each agent the issue ID; the issue contains the durable scope.

Useful queries:

```sh
bd ready --metadata-field project=esphome-technibel-scdf32 --json
bd list --status blocked --metadata-field project=esphome-technibel-scdf32 --json
bd show <issue-id>
```

Each implementer records exact verification evidence in the issue before closure. Any
new defect or additional scope becomes a separate issue linked with `discovered-from`;
it must not silently expand the claimed task.

## Cross-review by handoff

When Florent requests a review or the change risk justifies independent verification,
the coordinator creates one self-contained project handoff for a fresh agent/session.
The review issue:

- depends on the implementation issue;
- names the commit or exact diff to review;
- has a different assignee;
- includes correctness, safety, regression, test-evidence, documentation, and rollback checks;
- produces either recorded approval or actionable findings.

Actionable findings become child or `discovered-from` issues. A later implementation
session addresses them, followed by review verification when needed. Implementation and
review do not run concurrently. For high-risk hardware or live changes, the review gate
remains blocking until both implementation and review acceptance criteria pass.

## Git and handoff

An agent must not leave intended work only in a working tree. Before handoff it reviews
`git diff --numstat` and the semantic diff, runs the required validation, and commits the
complete intended change atomically. The coordinator confirms that the commit contains
only the claimed scope before handing work to the next session.

Repository state, pushed remote state, Beads state, and the dedicated live VM are four
distinct states and must be reported separately.

## Concurrency policy

Do not enable simultaneous Beads writers or migrate to Dolt server mode for this workflow.
Serialize Beads mutations, implementation, review, and Git commits. If Florent later
chooses concurrent execution, treat the storage-mode and worktree design as a separate
infrastructure decision with backup, rollback, and a concurrency smoke test.
