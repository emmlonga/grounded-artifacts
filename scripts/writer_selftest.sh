#!/bin/zsh
# Self-test of writer resolution, provenance and the frozen-writer guard, with a negative proof for each.
# Run after changing writers/README.md, resolve_writer.py, stamp_header.py or the writer lines of SKILL.md:
#   scripts/writer_selftest.sh
set -u
KIT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
FAILS=0
V2=writers/decision-artifact-writing-v2.md
V2SHA=be61b6165fd04593d73d74f43901bf15d81e1c8abae904582824e7098757e66d
ok()  { echo "PASS  $1"; }
bad() { echo "FAIL  $1"; FAILS=$((FAILS + 1)); }
expect() {  # expect <exit code wanted> <label> <command...>
  local want=$1 label=$2; shift 2
  "$@" > "$TMP/out.txt" 2>&1; local got=$?
  if [[ $got == $want ]]; then ok "$label (exit $got)"; else bad "$label (exit $got, wanted $want)"; cat "$TMP/out.txt"; fi
}
has() { grep -qF -- "$2" "$TMP/out.txt" && ok "$1" || { bad "$1"; cat "$TMP/out.txt"; }; }
brief() {  # brief <dir> <mode> [writer row value]
  mkdir -p "$1"
  { echo "| Field | Value |"; echo "|---|---|"; echo "| Mode | $2 |"; [[ -n "${3:-}" ]] && echo "| Writer | $3 |"; } > "$1/artifact_brief.md"
}
R="$KIT/scripts/resolve_writer.py"

echo "== frozen bytes"
[[ "$(shasum -a 256 "$KIT/$V2" | cut -d' ' -f1)" == "$V2SHA" ]] && ok "$V2 matches $V2SHA" || bad "$V2 hash changed"
# Provenance only: the validation record's path is a symlink to the canonical writer. The test must not need the
# validation tree, so it is checked when present and skipped (not failed) when that evidence is not shipped.
VP="$KIT/docs/validation/writing-v2/experimental-decision-artifact-writing-v2.md"
if [[ -e "$VP" || -L "$VP" ]]; then
  [[ "$(shasum -a 256 "$VP" | cut -d' ' -f1)" == "$V2SHA" ]] \
    && ok "validation path resolves to the same bytes" || bad "validation path does not resolve to V2"
else
  echo "SKIP  validation path not present (validation evidence not shipped); the canonical $V2 is checked above"
fi

echo "== default resolution"
brief "$TMP/ps" product-story
expect 0 "product-story with no Writer row resolves" python3 "$R" "$TMP/ps/artifact_brief.md"
has "resolves to frozen writing-v2 as the mode default" "Writer: writing-v2 (default for product-story) · Writing V2 0.2.0, frozen · $V2 sha256 $V2SHA"
has "names the V2 file as the writing skill" "Writing skill: $KIT/$V2"
brief "$TMP/ps2" product-story default
expect 0 "product-story with Writer = default resolves" python3 "$R" "$TMP/ps2/artifact_brief.md"
has "Writer = default is the mode default" "Writer: writing-v2 (default for product-story)"
brief "$TMP/cp" commercial-proposal
expect 0 "commercial-proposal resolves" python3 "$R" "$TMP/cp/artifact_brief.md"
has "commercial-proposal keeps no writing skill" "Writer: none (default for commercial-proposal)"

echo "== per-run override"
brief "$TMP/ov" product-story none
expect 0 "Writer = none overrides the product-story default" python3 "$R" "$TMP/ov/artifact_brief.md"
has "override recorded as such" "Writer: none (override in brief)"
brief "$TMP/cpv2" commercial-proposal writing-v2
expect 0 "Writer = writing-v2 overrides the commercial-proposal default" python3 "$R" "$TMP/cpv2/artifact_brief.md"
has "override to a registered writer recorded as such" "Writer: writing-v2 (override in brief)"
# A challenger registered beside V2 (two pinned files, like an adapter plus an upstream skill) is selectable by name.
mkdir -p "$TMP/kit/writers" "$TMP/kit/upstream"
cp "$KIT/$V2" "$TMP/kit/$V2"; echo "adapter" > "$TMP/kit/writers/adapter.md"; echo "upstream" > "$TMP/kit/upstream/SKILL.md"
A=$(shasum -a 256 "$TMP/kit/writers/adapter.md" | cut -d' ' -f1); U=$(shasum -a 256 "$TMP/kit/upstream/SKILL.md" | cut -d' ' -f1)
{ sed '/^## Registry/,$d' "$KIT/writers/README.md"
  echo "## Registry"; echo; echo "| Writer | Status | File | SHA-256 |"; echo "|---|---|---|---|"
  echo "| writing-v2 | Writing V2 0.2.0, frozen | $V2 | $V2SHA |"
  echo "| challenger | adapter@test + upstream@test | writers/adapter.md | $A |"
  echo "| challenger | adapter@test + upstream@test | upstream/SKILL.md | $U |"; } > "$TMP/kit/writers/README.md"
brief "$TMP/ch" product-story challenger
expect 0 "a second registered writer is selectable per run" env WRITER_REGISTRY="$TMP/kit/writers/README.md" python3 "$R" "$TMP/ch/artifact_brief.md"
has "its every pinned file is in the provenance" "Writer: challenger (override in brief) · adapter@test + upstream@test · writers/adapter.md sha256 $A · upstream/SKILL.md sha256 $U"
has "its first file is the writing skill" "Writing skill: $TMP/kit/writers/adapter.md"
brief "$TMP/bad" product-story better-writing
expect 2 "an unregistered writer name fails" python3 "$R" "$TMP/bad/artifact_brief.md"
brief "$TMP/badmode" slides
expect 2 "a mode with no default writer fails" python3 "$R" "$TMP/badmode/artifact_brief.md"

echo "== frozen means frozen"
echo " " >> "$TMP/kit/$V2"
expect 1 "a modified V2 fails resolution" env WRITER_REGISTRY="$TMP/kit/writers/README.md" python3 "$R" "$TMP/ps/artifact_brief.md"
has "the failure names the file and both hashes" "does not match the pinned $V2SHA"
echo "upstream changed" > "$TMP/kit/upstream/SKILL.md"
expect 1 "a modified second file of a composite writer fails" env WRITER_REGISTRY="$TMP/kit/writers/README.md" python3 "$R" "$TMP/ch/artifact_brief.md"

echo "== provenance in the draft header"
printf '**Version:** v3\n' > "$TMP/ps/grounding.md"; printf '**Version:** v2\n' > "$TMP/ps/story-frame.md"
printf '**Version:** v1\n' > "$TMP/ps/outline.md"
sed 's/^Governed by:.*/Governed by: artifact_brief.md (approved 2026-10-01) · grounding.md v0/' "$KIT/templates/draft_header.md" > "$TMP/ps/draft.md"
expect 0 "stamp_header stamps a template header" python3 "$KIT/scripts/stamp_header.py" "$TMP/ps/draft.md"
grep -qxF "Writer: writing-v2 (default for product-story) · Writing V2 0.2.0, frozen · $V2 sha256 $V2SHA" "$TMP/ps/draft.md" \
  && ok "draft header records writer, version/status and sha256" || { bad "draft header Writer line"; head -12 "$TMP/ps/draft.md"; }
grep -v '^Writer:' "$TMP/ps/draft.md" > "$TMP/ps/d2.md"; mv "$TMP/ps/d2.md" "$TMP/ps/draft.md"
expect 0 "stamp_header adds the line to an older header without one" python3 "$KIT/scripts/stamp_header.py" "$TMP/ps/draft.md"
[[ $(grep -c '^Writer: writing-v2' "$TMP/ps/draft.md") == 1 ]] && sed -n '/^Governed by/{n;p;}' "$TMP/ps/draft.md" | grep -q '^Writer:' \
  && ok "Writer line inserted once, after Governed by" || bad "Writer line not inserted"
mkdir -p "$TMP/mod"; cp "$TMP/ps/"{artifact_brief,grounding,story-frame,outline,draft}.md "$TMP/mod/"; cp "$TMP/mod/draft.md" "$TMP/mod/before.md"
expect 3 "stamp_header fails on a modified writer" env WRITER_REGISTRY="$TMP/kit/writers/README.md" python3 "$KIT/scripts/stamp_header.py" "$TMP/mod/draft.md"
cmp -s "$TMP/mod/draft.md" "$TMP/mod/before.md" && ok "nothing written on failure" || bad "draft changed on failure"
grep -q '^Writer:' "$KIT/templates/freeze_header.md" && ok "freeze header carries the Writer line" || bad "freeze header has no Writer line"

echo "== delegations: the writing skill reaches only draft and draft-revise runs"
line=$(grep -n '^Writing skill (mode draft, and revise of the draft, only)' "$KIT/SKILL.md" | cut -d: -f1)
[[ -n "$line" ]] && ok "SKILL.md delegation line restricts the writing skill to draft and draft revise" || bad "delegation line"
grep -q 'No other delegation (readiness, grounding, frame, pass B, outline, any auditor) carries the writing skill' "$KIT/SKILL.md" \
  && ok "SKILL.md excludes upstream and auditor delegations" || bad "exclusion sentence missing"
for f in grounding-integrity-auditor audience-auditor; do
  grep -qiE 'writing skill|writers/|writing-v2' "$KIT/agents/$f.md" && bad "$f.md references a writer" || ok "$f.md reads no writer"
done
grep -E '^\| (grounding|frame|outline) \|' "$KIT/agents/content-developer.md" | grep -qi 'writing skill' \
  && bad "an upstream developer mode reads the writing skill" || ok "grounding, frame and outline read orders carry no writing skill"
grep -E '^\| draft \|' "$KIT/agents/content-developer.md" | grep -q 'the writing skill the coordinator names' \
  && ok "draft read order (and revise of the draft, by the stage's read order) carries the named writing skill" || bad "draft read order"
# The delegation the coordinator fills for draft and for revise of the draft, from the resolver's output.
python3 "$R" "$TMP/ps/artifact_brief.md" > "$TMP/res.txt"
for stage in "draft" "revise / draft audit, round 1"; do
  { echo "Read $KIT/agents/content-developer.md and follow it exactly."; echo "Mode or stage: $stage"
    echo "Writing skill (mode draft, and revise of the draft, only): $(sed -n 's/^Writing skill: //p' "$TMP/res.txt") ($(head -1 "$TMP/res.txt"))."; } > "$TMP/out.txt"
  has "$stage delegation names frozen V2 by path and hash" "$KIT/$V2 (Writer: writing-v2 (default for product-story) · Writing V2 0.2.0, frozen · $V2 sha256 $V2SHA)"
done

rm -rf "$TMP"
echo "== $FAILS failure(s)"
exit $(( FAILS > 0 ))
