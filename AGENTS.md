# Agent instructions — speechify-api (Python SDK)

This is a **Fern-generated** SDK. It is published to **PyPI** as `speechify-api`.
The source of truth for the API surface lives in the `SpeechifyInc/speechify-api`
repo (`fern/`); this repo receives generated code on the `sdk-release` branch.

**Read this before doing anything that touches a release.** A botched release here
publishes to an immutable public registry and breaks the contract with every
customer who installs the package. This file exists because we already did that
once — see "Postmortem" below.

## The golden rule

**Publishing to PyPI is IRREVERSIBLE.** A version, once uploaded, can never be
overwritten or reused — only *yanked* (hidden from resolution), and yanking
requires a human web session (there is no token/API/CI path for it).

Never trigger a publish until you have, in order:

1. **Audited the release plumbing** (this file, the workflow, the config).
2. **Confirmed the version is correct in EVERY version-bearing file** (see checklist).
3. **Dry-run built and asserted the artifact version** matches the intended tag.
4. **Got explicit human sign-off** for the publish itself.

Do NOT admin-merge release PRs to force a publish. Do NOT bypass required reviews.

## Version-surface checklist — the mistake we keep making

The #1 failure mode is **a generated version string not getting bumped**, so the
package publishes under the wrong number (or reports a false version to the API).
A single stale string is a published contract break, not a typo.

There are exactly **four** version literals in the tree, plus the tag. All five
must agree **in the published artifact** — check every one, never check one and
assume the rest. Two are committed by the release PR, two are stamped in CI:

| Literal | Who sets it | Correct on `main`? |
|---|---|---|
| `pyproject.toml` → `[tool.poetry].version` | release-please `extra-files` (toml) | yes — committed |
| `.fern/metadata.json` → `sdkVersion` | release-please `extra-files` (json) | yes — committed |
| `client_wrapper.py` → `User-Agent` | **stamped in CI from the tag** | no — stale between releases, by design |
| `client_wrapper.py` → `X-Fern-SDK-Version` | **stamped in CI from the tag** | no — stale between releases, by design |

- `pyproject.toml` → `[tool.poetry].version` — the artifact version. `[project]`
  declares `dynamic = ["version"]` and has **no** `version` key; poetry-core reads
  `[tool.poetry]`. Do not add `[project].version`. **Load-bearing**: `poetry build`
  reads it, so it must be committed by the release PR.
- `src/speechify/core/client_wrapper.py` → `User-Agent` **and** `X-Fern-SDK-Version`
- `.fern/metadata.json` → `sdkVersion`
- the git tag created for the release (bare semver — `include-v-in-tag: false`)

**The tag is the source of truth.** Everything else is either bumped to match it
by release-please or rewritten to match it at publish time.

Not version literals, so leave them alone:

- `.release-please-manifest.json` — release-please's own state, it owns this.
- `src/speechify/version.py` — resolves `__version__` from installed package
  metadata at import time. Nothing to bump.

Fast audit:

```bash
grep -rnE '[0-9]+\.[0-9]+\.[0-9]+' \
  pyproject.toml src/speechify/core/client_wrapper.py .fern/metadata.json
```

On a checked-out `main` this grep will show `client_wrapper.py` behind the last
release. **That is expected** — see the stamping section below. What must never
disagree is the *published* artifact, which the publish job builds from a stamped
and asserted tree.

`X-Fern-SDK-Version` / `User-Agent` are sent on every request. If they lie, your
telemetry, version-gating, and support debugging are all wrong for that release.

## Known plumbing traps

- **The default `python` release-type does NOT bump this `pyproject.toml`.** Its
  updater resolves `parsed.project || parsed.tool.poetry` — our `[project]` table
  exists, so it wins the `||`, has no `version`, declares `dynamic = ["version"]`,
  and the updater logs `dynamic version found ... Skipping update` and returns the
  file unchanged. It never falls through to `[tool.poetry]`. The `extra-files`
  entry `$.tool.poetry.version` is therefore **load-bearing, not redundant** —
  delete it and the published artifact silently keeps the old version.
- **Do not add a `$.project.version` jsonpath.** There is no such key. The
  `GenericToml` updater logs `No entries modified` and no-ops, so it buys nothing
  while implying coverage that does not exist. Adding a static `[project].version`
  to "fix" it would contradict `dynamic = ["version"]` and break the PEP 621 build.
- **Never point a `type: "generic"` extra-file at a Fern-generated file.** The
  `generic` updater only rewrites a line carrying an `x-release-please-version`
  marker, and it no-ops **silently** when the marker is absent. `client_wrapper.py`
  is generated and **cannot** be `.fernignore`d, so every regeneration strips the
  marker and re-arms that trap. This is the exact failure that shipped `2.0.1`
  under the `3.0.0` tag. There is deliberately no `generic` entry in
  `release-please-config.json` — do not add one back.
- **`.fern/metadata.json` was uncovered until now.** It drifted to `2.0.1` while
  the package was on `3.0.1`. It is covered by a `json` updater on `$.sdkVersion`.
  It is *not* a marker file — the `json` updater is jsonpath-based and survives
  regeneration, which is why it is safe to rely on.

## Version stamping — how `client_wrapper.py` gets the right version

**A fix that lives inside a generated file is not a fix.** Markers are gone.
Instead, the `publish` job rewrites the two Fern-owned literals from
`needs.release-please.outputs.tag_name` immediately before building.

The `publish` job runs three steps in this order, and the order is the design:

1. **Stamp** — rewrite `User-Agent` and `X-Fern-SDK-Version` in
   `client_wrapper.py` from the tag.
2. **Assert** — independently re-read all four literals and compare each to the
   tag. Fails on a mismatch *or* on a literal that has gone missing.
3. **Publish** — `poetry publish --build`.

Never reorder these, and never let the publish step run without both in front of
it. The assertion is a check on the stamp's result, not a substitute for it.

The stamp step **fails the build if a target literal is not found**. A Fern
regeneration that renames or restructures those lines must break the release
loudly — a stamp that quietly matches nothing is the same silent-no-op class that
caused the 3.0.0 incident. If it fails, fix the pattern in the stamp step *and*
the matching pattern in the assertion; do not delete the check.

`include-v-in-tag` is false so the tag is bare semver. The stamp tolerates a
leading `v`, rejects anything that is not semver, and preserves a prerelease or
build suffix verbatim (`4.0.0-rc.1` stamps as `4.0.0-rc.1`, never `4.0.0`).

### Stale strings on `main` are expected — do not "fix" them

The stamp edits the **CI checkout only**. Nothing is committed back. So between
releases, `main`'s `client_wrapper.py` carries whatever version Fern last
generated, and it will usually look out of date.

**This is correct behaviour, not a bug.** The published artifact is always right
because it is built from the stamped tree. If you "helpfully" hand-edit those
strings on `main`, you gain nothing — the next regeneration overwrites you and
the next release stamps over you anyway. Leave them alone.

## After every Fern regeneration

`.fernignore` protects these from being overwritten — they are safe:

`.github/workflows/ci.yml`, `.github/workflows/release-please.yml`,
`.github/workflows/manual-publish.yml`, `release-please-config.json`,
`.release-please-manifest.json`, `CHANGELOG.md`, `AGENTS.md`.

These are **regenerated** and must be re-checked by hand every single time:

- [ ] `src/speechify/core/client_wrapper.py` — the two header lines still have
      the shape the stamp step matches. Do **not** check the version values
      themselves; they are stamped at publish time and are expected to be stale:

      ```python
      "User-Agent": "speechify-api/<semver>",
      "X-Fern-SDK-Version": "<semver>",
      ```

      Same key names, same quoting, same `speechify-api/` prefix. If a regen
      changed any of that, update the patterns in **both** the stamp step and the
      publish assertion in `release-please.yml`.
- [ ] `pyproject.toml` — `[tool.poetry].version` still present; `[project]` still
      `dynamic` and still has no `version` key.
- [ ] `.fern/metadata.json` — `sdkVersion` key still named that.
- [ ] `release-please-config.json` — still has **no** `type: "generic"` entry.

Verify the shapes without caring about the values:

```bash
grep -nE '"(User-Agent|X-Fern-SDK-Version)":' src/speechify/core/client_wrapper.py
```

If any of the above moved or was renamed, fix it *before* merging — the stamp
step and the publish assertion will both fail the release otherwise (by design).

## Publish assertion

`release-please.yml`'s `publish` job runs a version/tag assertion **after the
stamp step and before** `poetry publish --build`. It fails the job if any of the
four literals disagrees with the tag, **or if a literal has gone missing
entirely** — a missing literal is the silent-no-op class and is treated as a hard
failure, not a skip. Every value and the tag are printed on failure. Keep the
order **stamp → assert → publish**.

`manual-publish.yml` is the recovery path for a one-off republish; it asserts the
built artifact filename against an explicit `expected_version` input.

## Merging a release PR

- The repo allows **squash merge only** (merge commits and rebase are disabled).
  Squash uses `PR_TITLE` + `PR_BODY`, so the **PR body becomes the commit message
  on `main`** — that is the only thing release-please parses.
- A `Release-As: X.Y.Z` footer must therefore live in the **PR body**, as the
  final line, standalone, unindented and without backticks. In a commit message
  trailer position it is ignored if indented or fenced.
- `BREAKING CHANGE:` footers belong in the PR body too, for the same reason.

## If a release has already gone wrong

- **Wrong version on PyPI:** it is permanent. Fix the version wiring, cut a NEW
  correct version, and **yank** the bad one (human, via
  `https://pypi.org/manage/project/speechify-api/release/<version>/`).
- **Tag points at a bad commit:** the tag/GitHub release can be recreated on the
  corrected commit (public history mutation — back up the old SHA + notes first).
- Never delete a PyPI release to "reuse" the number. You can't.

## Postmortem — the 3.0.0 release (why this file exists)

A routine regeneration was pushed straight to publish. Failures, in order:

1. Breaking-change PRs were admin-merged past the review gate.
2. Nothing bumped the version. `git show 2f19983 --stat` is the evidence: the
   release commit touched **only** `.release-please-manifest.json` and
   `CHANGELOG.md`. Both updaters had failed silently, for two different reasons:
   - `pyproject.toml` was already `dynamic = ["version"]`, so the default `python`
     updater logged `Skipping update` and left `[tool.poetry].version` at `2.0.1`.
     The config had no `extra-files` TOML entry to catch it.
   - the `generic` entry for `client_wrapper.py` was configured but the file had
     no `x-release-please-version` marker, so it no-opped without erroring.
3. release-please tagged `3.0.0`; `poetry build` read `[tool.poetry].version` and
   produced `2.0.1` → **`speechify-api 2.0.1` was published to PyPI** (immutable),
   carrying the 3.0.0 breaking code under a patch number.
4. Each stale version string was found reactively, one at a time, instead of via
   one exhaustive version-surface audit.

The follow-up fix at the time was to make `[project].version` static. **That fix
does not survive a Fern regeneration** — the next regen restored
`dynamic = ["version"]` and re-armed the trap. Adding an `x-release-please-version`
marker to `client_wrapper.py` was the same mistake wearing a different hat: also
inside a generated file, also stripped by the next regen, also silent. Both are
gone now.

Durable fixes live in exactly three places: `.fernignore`-protected files
(`release-please-config.json`), values derived from the tag at publish time (the
stamp step), or an assertion that fails the build (the publish assertion). If a
proposed fix is a literal written into a generated file, it is not durable —
it is a countdown to the next regeneration.

Lesson: **audit the whole release surface first, dry-run, get sign-off, then
publish.** Treat one stale version string as a signal to check every other one,
and never rely on a fix that lives in a generated file.
