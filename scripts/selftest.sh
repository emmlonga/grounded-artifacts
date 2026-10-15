#!/bin/zsh
# Self-test of the V0 render path and checks, with a negative proof for every check.
# Run after changing a script or a profile:  scripts/selftest.sh [plain]
set -u
KIT="$(cd "$(dirname "$0")/.." && pwd)"
T="$KIT/scripts/selftest"
PROFILE="${1:-plain}"
TMP="$(mktemp -d)"
FAILS=0
ok()  { echo "PASS  $1"; }
bad() { echo "FAIL  $1"; FAILS=$((FAILS + 1)); }
expect() {  # expect <exit code wanted> <label> <command...>
  local want=$1 label=$2; shift 2
  "$@" > "$TMP/out.txt" 2>&1; local got=$?
  if [[ $got == $want ]]; then ok "$label (exit $got)"; else bad "$label (exit $got, wanted $want)"; cat "$TMP/out.txt"; fi
}

echo "== positive: render the fixture ($PROFILE)"
expect 0 "render.sh produces DOCX, PDF, pages; compare and names pass" \
  "$KIT/scripts/render.sh" "$T/final/content_final.md" "$PROFILE" "$T/final/selftest.docx" 1
[[ -s "$T/final/selftest.docx" && -s "$T/final/selftest.pdf" && -s "$T/final/pages/page-01.png" ]] \
  && ok "output files exist" || bad "output files missing"
expect 0 "wordcount within outline caps" python3 "$KIT/scripts/wordcount.py" "$T/final/content_final.md" --outline "$T/outline.md"

expect 0 "check_names accepts the story frame" \
  python3 "$KIT/scripts/check_names.py" --grounding "$T/grounding.md" "$T/story-frame.md"
{ sed 's/^Governed by:.*/Governed by: artifact_brief.md (approved 2026-09-30) · grounding.md v0 · outline.md v0/' \
    "$KIT/templates/draft_header.md"; } > "$TMP/draft.md"
printf '**Version:** v3\n' > "$TMP/grounding.md"; printf '**Version:** v2\n' > "$TMP/story-frame.md"
printf '**Version:** v1\n' > "$TMP/outline.md"
expect 0 "stamp_header writes the governing versions" python3 "$KIT/scripts/stamp_header.py" "$TMP/draft.md"
grep -q '^Governed by: artifact_brief.md (approved 2026-09-30) · grounding.md v3 · story-frame.md v2 · outline.md v1$' "$TMP/draft.md" \
  && ok "draft header carries grounding v3, story-frame v2, outline v1" || bad "draft header not stamped"

echo "== render isolation (Word engine): the shared-folder contamination class"
if [[ -d "/Applications/Microsoft Word.app" && "${PDF_ENGINE:-word}" == word ]]; then
  # Fixture B: a different document (title, headings and opening sentence changed).
  sed -e 's/^# Project Harbor: faster delivery-time estimates/# Project Beacon: a different document entirely/' \
      -e 's/^## The opportunity/## The opportunity, seen from Beacon/' \
      -e 's/^## What we built/## What Beacon built/' \
      -e 's/^## The outcome/## The Beacon outcome/' \
      -e 's/dispatchers re-quoted delivery times by hand for every delayed order/planners re-planned every route on paper each morning/' \
      "$T/final/content_final.md" > "$TMP/b.md"
  mkdir -p "$TMP/ra" "$TMP/rb" "$TMP/rc"
  # (1) Two renders at once: each PDF must carry its own document.
  "$KIT/scripts/render.sh" "$T/final/content_final.md" "$PROFILE" "$TMP/ra/a.docx" 1 > "$TMP/ra.txt" 2>&1 & PA=$!
  "$KIT/scripts/render.sh" "$TMP/b.md" "$PROFILE" "$TMP/rb/b.docx" 1 > "$TMP/rb.txt" 2>&1 & PB=$!
  wait $PA; RA=$?; wait $PB; RB=$?
  if [[ $RA == 0 && $RB == 0 ]] && grep -q 'pdf identity: PASS' "$TMP/ra.txt" && grep -q 'pdf identity: PASS' "$TMP/rb.txt"; then
    ok "two concurrent Word renders each produced their own PDF (identity PASS on both)"
  else bad "concurrent renders contaminated or failed"; cat "$TMP/ra.txt" "$TMP/rb.txt"; fi
  # (2) A foreign PDF is detected: fixture A's Markdown against fixture B's PDF.
  expect 1 "pdfcheck fails a PDF that carries another document" \
    python3 "$KIT/scripts/pdfcheck.py" --md "$T/final/content_final.md" --pdf "$TMP/rb/b.pdf"
  expect 0 "pdfcheck passes a PDF that carries its own document" \
    python3 "$KIT/scripts/pdfcheck.py" --md "$TMP/b.md" --pdf "$TMP/rb/b.pdf"
  # (3) A document already open in Word (the second failure path): render A while a foreign document is open.
  FWORK="$HOME/Library/Containers/com.microsoft.Word/Data/gdaw_render/selftest-foreign-$$"; FDOC="foreign-open-$$.docx"
  mkdir -p "$FWORK"; cp "$TMP/rb/b.docx" "$FWORK/$FDOC"
  osascript -e "tell application \"Microsoft Word\" to open POSIX file \"$FWORK/$FDOC\"" >/dev/null 2>&1
  "$KIT/scripts/render.sh" "$T/final/content_final.md" "$PROFILE" "$TMP/rc/a.docx" 1 > "$TMP/rc.txt" 2>&1; RC=$?
  osascript -e "tell application \"Microsoft Word\" to close document \"$FDOC\" saving no" >/dev/null 2>&1
  rm -rf "$FWORK"
  if [[ $RC == 0 ]] && grep -q 'pdf identity: PASS' "$TMP/rc.txt"; then
    ok "a render with a foreign document open in Word still produced its own PDF"
  else bad "render with a foreign document open in Word contaminated or failed"; cat "$TMP/rc.txt"; fi
else
  echo "SKIP  render isolation cases (Word engine not available or PDF_ENGINE overridden)"
fi

echo "== post-freeze departure report (scripts/departures.py)"
D="$KIT/scripts/departures.py"; F="$T/final/content_final.md"; G="$T/grounding.md"
sed 's/Activation rose by 20%/Activation rose by 25%/' "$F" > "$TMP/d-num.md"
python3 "$D" --frozen "$F" --edited "$TMP/d-num.md" --grounding "$G" > "$TMP/out.txt"
grep -q '\[number added\]' "$TMP/out.txt" && grep -q 'K1' "$TMP/out.txt" && ok "departures surfaces a changed number and maps it to its constant" || { bad "changed number not surfaced"; cat "$TMP/out.txt"; }
sed 's/fell by about half/fell by half/' "$F" > "$TMP/d-qual.md"
python3 "$D" --frozen "$F" --edited "$TMP/d-qual.md" --grounding "$G" > "$TMP/out.txt"
grep -q "qualifier dropped: 'about'" "$TMP/out.txt" && ok "departures surfaces a dropped qualifier" || { bad "dropped qualifier not surfaced"; cat "$TMP/out.txt"; }
sed 's/I saw that the delay was not in the data/We saw that the delay was not in the data/' "$F" > "$TMP/d-attr.md"
python3 "$D" --frozen "$F" --edited "$TMP/d-attr.md" --grounding "$G" > "$TMP/out.txt"
grep -q 'attribution switched' "$TMP/out.txt" && ok "departures surfaces an I/we switch" || { bad "I/we switch not surfaced"; cat "$TMP/out.txt"; }
sed 's/six weeks/eight weeks/' "$F" > "$TMP/d-stale.md"
python3 "$D" --frozen "$F" --edited "$TMP/d-stale.md" --grounding "$G" > "$TMP/out.txt"
grep -q '\[stale rendering\] (K2)' "$TMP/out.txt" && ok "departures surfaces a stale constant rendering" || { bad "stale rendering not surfaced"; cat "$TMP/out.txt"; }
sed -e 's/dispatchers re-quoted delivery times by hand for every delayed order/every delayed order had its delivery time re-quoted by hand/' \
    -e 's/We shipped a delivery-time estimate that dispatchers could trust without re-checking it/We shipped a delivery-time estimate dispatchers could trust and did not need to re-check/' "$F" > "$TMP/d-prose.md"
python3 "$D" --frozen "$F" --edited "$TMP/d-prose.md" --grounding "$G" > "$TMP/out.txt"
grep -q '^none detected' "$TMP/out.txt" && ok "departures stays silent on prose-only rewording" || { bad "prose-only rewording produced findings"; cat "$TMP/out.txt"; }
python3 "$D" --frozen "$F" --edited "$T/final/selftest.docx" --grounding "$G" > "$TMP/out.txt"
grep -q '^none detected' "$TMP/out.txt" && ok "departures reads a DOCX and ignores its headings" || { bad "unchanged DOCX produced findings"; cat "$TMP/out.txt"; }

echo "== determinism: two renders, same content parts"
PDF_ENGINE=none "$KIT/scripts/render.sh" "$T/final/content_final.md" "$PROFILE" "$TMP/again.docx" >/dev/null 2>&1
python3 - "$T/final/selftest.docx" "$TMP/again.docx" <<'PY' && ok "only docProps/core.xml (timestamp) differs" || bad "render not deterministic"
import sys, zipfile
a, b = (zipfile.ZipFile(p) for p in sys.argv[1:])
diff = [n for n in a.namelist() if n != "docProps/core.xml" and a.read(n) != b.read(n)]
print(diff) if diff else None
sys.exit(1 if diff else 0)
PY

echo "== negative proofs: each check must fail on a planted defect"
sed 's/At a mid-size logistics company/At Acme Freight/' "$T/final/content_final.md" > "$TMP/leak.md"
expect 1 "check_names catches a planted real name" \
  python3 "$KIT/scripts/check_names.py" --grounding "$T/grounding.md" "$TMP/leak.md"
printf 'Volume grew past 1,240,000\nshipments that year.\n' > "$TMP/leak2.txt"
expect 1 "check_names catches a confidential metric split across a line break" \
  python3 "$KIT/scripts/check_names.py" --grounding "$T/grounding.md" "$TMP/leak2.txt"
sed 's/At a mid-size logistics company/At ACMÉ FREIGHT/' "$T/final/content_final.md" > "$TMP/leak3.md"
expect 1 "check_names ignores case and accents" \
  python3 "$KIT/scripts/check_names.py" --grounding "$T/grounding.md" "$TMP/leak3.md"
expect 3 "check_names reports a grounding with no map as SKIPPED" \
  python3 "$KIT/scripts/check_names.py" --grounding "$T/outline.md" "$T/final/content_final.md"
sed 's/six weeks/eight weeks/' "$T/final/content_final.md" > "$TMP/stale.md"
expect 1 "compare catches a stale constant rendering" \
  python3 "$KIT/scripts/compare.py" --md "$TMP/stale.md" --grounding "$T/grounding.md"
sed 's/a delivery-time estimate/a best-in-class delivery-time estimate/' "$T/final/content_final.md" > "$TMP/forbid.md"
expect 1 "compare catches forbidden phrasing" \
  python3 "$KIT/scripts/compare.py" --md "$TMP/forbid.md" --grounding "$T/grounding.md"
grep -v 'The main learning' "$T/final/selftest.txt" > "$TMP/lost.txt"
expect 1 "compare catches a sentence lost in rendering" \
  python3 "$KIT/scripts/compare.py" --md "$T/final/content_final.md" --text "$TMP/lost.txt"
{ cat "$T/final/content_final.md"; for i in {1..30}; do echo "Padding words to exceed the cap."; done; } > "$TMP/long.md"
expect 0 "wordcount reports a section over its cap without failing" \
  python3 "$KIT/scripts/wordcount.py" "$TMP/long.md" --outline "$T/outline.md"
grep -q 'ADVISORY (over planning cap)' "$TMP/out.txt" && ok "over-cap reading printed as ADVISORY (over planning cap)" || bad "over-cap reading missing"

sed 's/Project Harbor/Project Nimbus/' "$T/story-frame.md" > "$TMP/frame-leak.md"
expect 1 "check_names catches a planted code name in the story frame" \
  python3 "$KIT/scripts/check_names.py" --grounding "$T/grounding.md" "$TMP/frame-leak.md"
rm "$TMP/story-frame.md"
expect 2 "stamp_header fails when a governing file is missing" python3 "$KIT/scripts/stamp_header.py" "$TMP/draft.md"
printf '**Word cap:** 20\n**Total cap:** 20\n**Fit guardrail:** 40\n' > "$TMP/guard.md"
{ echo "## One"; for i in {1..6}; do echo "Five words in this line."; done; } > "$TMP/advisory.md"
expect 0 "wordcount reads over a cap within the guardrail as advisory" \
  python3 "$KIT/scripts/wordcount.py" "$TMP/advisory.md" --outline "$TMP/guard.md"
grep -q 'wordcount: ADVISORY (over planning cap)$' "$TMP/out.txt" && ok "ADVISORY (over planning cap) printed" || bad "over-cap reading missing"
{ echo "## One"; for i in {1..8}; do echo "Five words in this line."; done; } > "$TMP/overguard.md"
expect 0 "wordcount reads over the fit guardrail as advisory, never a failure" \
  python3 "$KIT/scripts/wordcount.py" "$TMP/overguard.md" --outline "$TMP/guard.md"
grep -q 'wordcount: ADVISORY (over fit guardrail: preview likely to fail)$' "$TMP/out.txt" \
  && ok "ADVISORY (over fit guardrail) printed" || bad "over-guardrail reading missing"
{ cat "$T/final/content_final.md"; for i in {1..120}; do echo; echo "Padding paragraph $i to push the render past its page budget."; done; } > "$TMP/pages.md"
GROUNDING="$T/grounding.md" "$KIT/scripts/render.sh" "$TMP/pages.md" "$PROFILE" "$TMP/pages.docx" 1 > "$TMP/out.txt" 2>&1
if [[ $? != 0 ]] && grep -q 'page budget: .* / 1 FAIL' "$TMP/out.txt"; then ok "render.sh fails a render over its page maximum"
else bad "render.sh did not fail a render over its page maximum"; cat "$TMP/out.txt"; fi

rm -rf "$TMP"
echo "== $FAILS failure(s)"
exit $(( FAILS > 0 ))
