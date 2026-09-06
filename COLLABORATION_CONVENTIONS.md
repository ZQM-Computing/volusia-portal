# COLLABORATION CONVENTIONS — PROJECT VOLUSIA
# Multi-Writer Protocol for a Shared Network Drive + Coexisting Git
# Version: 1.0 | Date: 2026-09-03 | Owner: ZQM Labs / Project Volusia Ops

---

## 0. WHY THIS EXISTS

This repository is edited by MULTIPLE humans and AI agents at the same time
on a shared network drive (`\\ZQM-GARDEN-03\web\14_Projects\Active\Project-Volusia`).
On 2026-09-03 a second writer git-initialized and re-structured the repo
mid-session, replaced files being edited, and an edit tool briefly reported
files as missing while other tools still saw them (see §9). These conventions
are the contract for every writer — human or agent.

Default assumption: **any file you have not JUST read has changed.**

---

## 1. CURRENT REALITY (2026-09-03)

- Shared drive working copy: repo root on `\\ZQM-GARDEN-03\web\...`.
- Git: `main` branch, 102 tracked files, full history present (Phase 1
  Foundation commit). Git was initialized by a CONCURRENT writer mid-session.
- Two machine identities: the repo was committed from `ZQM-NODE-4`; other
  machines (e.g. this one, `zqmco`) hit `dubious ownership` and must use the
  `safe.directory` workaround in §4.
- Generated artifacts (`volusia.db`, `fetch_log.jsonl`) were committed; they
  change on every pipeline run and should be untracked (§4, §8).
- Read tools on this share can briefly return ENOENT for files that exist.

---

## 2. GOLDEN RULES

1. **One writer per file at a time** — claim before you edit (§3).
2. **Re-read immediately before every write.** Never edit from memory or from
   a read older than a few seconds.
3. **Write atomically** — temp file in the same folder, then `os.replace()`
   via `Tools/collab/atomic_write.py`. Readers never see a half-written file.
4. **Verify after every write** — re-read touched lines; `py_compile` Python.
5. **Append when you can, splice only when you must.** End-of-file appends
   collide far less than mid-file surgery.
6. **Divide work by WHOLE FILES** (§7 ownership map). Two writers in one file
   is a coordination failure, not a technical problem.

---

## 3. CLAIM PROTOCOL — FOR UNCOMMITTED, ACTIVE EDITS

Claims are TTL'd JSON locks in `claims/` (git-ignored). Helper:
`Tools/collab/claim.py`.

    python Tools/collab/claim.py claim   <path> --owner "alex" --minutes 60
    python Tools/collab/claim.py status  <path>
    python Tools/collab/claim.py scan
    python Tools/collab/claim.py release <path> --owner "alex"

Rules:
- Claimed by someone else? **Pick different work.** `--force` only with the
  owner's explicit agreement.
- `--owner` = stable name (human, or agent + session id).
- Renew before the 60-min TTL expires (re-`claim`, same owner).
- Release when the write + verification is done.
- A claim is a courtesy signal, not a hard lock. Final protection is still
  Golden Rule 2 + 3.

---

## 4. GIT PROTOCOL — THE PRIMARY COLLISION KILLER

Git exists now; use it aggressively. On this share, enable it for your
machine first (one-time):

    git config --global --add safe.directory "//ZQM-GARDEN-03/web/14_Projects/Active/Project-Volusia"

(Or per-invocation, without touching global config:

    git -c safe.directory="//ZQM-GARDEN-03/web/14_Projects/Active/Project-Volusia" -C <repo> status

)

Every session:
1. `git status` BEFORE starting — know the dirty state.
2. Stay on `main` unless a branch is intentional.
3. Commit SMALL, logical changes with messages citing the contribution id
   (e.g. `P1-014`). One change = one commit makes diff review easy for every
   other writer.
4. NEVER commit generated artifacts: `volusia.db`, `fetch_log.jsonl`,
   `__pycache__/`, `.env`. If `git status` shows them, untrack them (§8).
5. After edits: `git status` again, `git diff --stat` to confirm scope, then
   commit. Announce in `CONTRIBUTION_LOG.md`.
6. Do not commit while another writer's claim is active on the same files
   (§3). A clean commit is the safe handoff point.
7. Line endings: normalize once via `.gitattributes` (`* text=auto`); never
   reformat in the same commit as content changes.

---

## 5. EDITING — BY FILE TYPE

### Markdown / plain text
- Append at the END or at a marked `<!-- APPEND HERE -->` anchor.
- Per-area detail in DEDICATED files; central status docs hold ONLY pointers.
- Do not reformat a document in the same change as content.

### Python
- `python -m py_compile <file>` after every write.
- Small hunks, exact anchors, fresh read of the region first.
- Never run a formatter in the same change as logic.
- Prefer ADDITIVE functions/classes over rewriting existing ones.

### JSON / JSONL
- `open(path, "a")` is only safe when writers serialize. Prefer:
  1. SQLite table (single writer, short transactions)
  2. One file per writer (`fetch_log_<writer>.jsonl`) + merge
  3. Locked append or full-file atomic rewrite
- Never let two processes append to one JSONL indefinitely.

### SQLite (volusia.db)
- Only ONE process runs `refresh_v2.py` at a time (single Task Scheduler job).
- RECOMMENDED (pipeline owner): `sqlite3.connect(DB_PATH, timeout=30)` +
  `PRAGMA busy_timeout=30000`. Keep the default journal mode on the network
  share (WAL shared memory is flaky over SMB); move to WAL/Postgres when local.

### Config / secrets
- `.env` is the single source of truth; never hardcode secrets again.
- Rotating a key = claim both `.env` and `config.py`, update, announce.

---

## 6. TOOL USAGE FOR AI AGENTS (Cline & similar)

1. **`read_files` IMMEDIATELY before every edit.** Cached reads lie — on
   2026-09-03 the share even returned ENOENT for files that existed while
   another writer was restructuring.
2. **Prefer `insert_line`** for appends/additive changes — it does not depend
   on matching stale text.
3. **Tiny, exact `old_text` anchors.** A one-character whitespace mismatch =
   STOP; re-read; do not guess.
4. **On "No replacement performed": re-read and retry from fresh state.**
   NEVER recreate the file from memory to "fix" a mismatch.
5. **"File created successfully" on an existing file = RED FLAG.** Verify
   immediately that nothing was clobbered.
6. **Never batch multiple edits to the SAME file in one parallel block.**
   Same-file edits are sequential (call → inspect → next). Different-file
   edits may be parallel.
7. **End every change with a read-back** of the touched lines.
8. For small files you fully hold: whole-file atomic rewrite via
   `Tools/collab/atomic_write.py`.

---

## 7. FILE OWNERSHIP MAP (2026-09-03)

One designated owner per area so two writers never need the same file.

| Area                  | Files (examples)                                  | Owner           |
|-----------------------|---------------------------------------------------|-----------------|
| Data pipeline         | refresh_v2.py, run_full_refresh.py, fetchers/, Data/ | Data Lead    |
| Portal                | portal_app.py, openapi.yaml (Data part)           | Technical Lead  |
| Contribution system   | contribution-api/, contribution_api.py, CONTRIBUTION/ | Community Liaison |
| Governance / charters | MISSION_STATEMENT.md, *GOV*.md, *CHARTER*.md      | Exec Sponsor    |
| Status / sync         | Q4_2026_DELIVERY_STATUS.md, Sync_Notes.md         | Ops / Comms Lead |
| Tools / methods       | TOOLS_CATALOG.md, Methodology/, reliability docs  | Tool Owner / Methodologist |
| Repo meta / CI        | README.md, CONTRIBUTING.md, .github/              | Ops (git owner) |

---

## 8. WORKSPACE HYGIENE

- `claims/` (TTL locks) and `Tools/_scratch/` (drafts) are git-ignored.
- Draft in `Tools/_scratch/`, promote with ONE atomic rename.
- Root `.gitignore` covers `.env`, `*.db`, `*.jsonl`, `claims/`, `*.lock`,
  `Tools/_scratch/`. If you find generated files tracked, untrack:
      git rm --cached <generated-file>
- Announce every completed change in `CONTRIBUTION_LOG.md` with the exact
  files touched so others re-read only what moved.

---

## 9. INCIDENT LOG — 2026-09-03

- **Repo re-structured mid-session.** A concurrent writer ran `git init`,
  added `README.md`, `CONTRIBUTING.md`, `.github/`, `docs/`, a static site and
  committed — while I was editing. `read_files` briefly returned ENOENT for
  files that existed. Lesson: treat the share as volatile; `Test-Path` /
  `Get-Content` are the fallback verification.
- **`run_full_refresh.py`** was rewritten by the concurrent writer before my
  edit → "No replacement performed". Lesson: claim + re-read before edits.
- **`portal_app.py`** got a 4-edit parallel batch to the SAME file → 2 landed,
  2 failed on stale anchors; fixed sequentially with `py_compile` after each.
  Lesson: same-file edits sequential; verify after every step.
- **`volusia.db` / `fetch_log.jsonl` committed** → every pipeline run dirties
  `git status`. Lesson: gitignore + untrack generated artifacts (§8).

---

## 10. COMMAND CHEAT-SHEET

    # claim → edit → verify → release
    python Tools/collab/claim.py claim   CONTRIBUTING.md --owner alex --minutes 60
    python Tools/collab/claim.py status  CONTRIBUTING.md
    python -m py_compile some_file.py
    python Tools/collab/claim.py release CONTRIBUTING.md --owner alex

    # atomic write (script or stdin)
    python Tools/collab/atomic_write.py path/to/file --content "text"
    echo "text" | python Tools/collab/atomic_write.py path/to/file

    # git hygiene (run the safe.directory line once per machine first, §4)
    git status
    git diff --stat
    git add -p
    git commit -m "P1-014: ..."

---

Document owner: Project Volusia Ops / Communications Lead
Related: CONTRIBUTING.md, PROJECT_VOLUSIA_GOV.md
Next review: 2026-12-02
