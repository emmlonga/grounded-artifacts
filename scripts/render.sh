#!/bin/zsh
# Deterministic render: content_final.md -> pandoc + profile reference.docx -> DOCX -> PDF -> page PNGs
# -> extracted text -> compare.py and check_names.py. No agent decides anything here.
#
# Usage: scripts/render.sh <content_final.md> <profile> <out.docx> [max_pages]
#   profile     plain (a folder under profiles/ with reference.docx)
#   out.docx    e.g. final/product-story.docx; PDF, text and pages/ are written next to it
#   max_pages   optional page budget; more pages is a FAIL
# Env: GROUNDING=path (default: ../grounding.md from content_final.md)
#      PDF_ENGINE=word|libreoffice|none (default: word if installed, else libreoffice if found)
#      WORD_TIMEOUT=seconds (default 300): shell watchdog on the Word step; on expiry the step is killed,
#      "word: timed out" is printed and LibreOffice is used if found, else pdf: FAIL. Never a hang.
# Render isolation (after a shared render-folder incident in which concurrent renders contaminated each other's PDFs):
#   every Word render works in its own folder under a unique file name, addresses its document in Word by that
#   name (never "active document"), and holds a lock so Word renders run one at a time; afterwards
#   scripts/pdfcheck.py reads the PDF itself and fails the render if it does not carry this Markdown's
#   title, headings and sentences. A foreign or stale PDF is therefore a FAIL, not a silent pass.
set -u
setopt null_glob

KIT="$(cd "$(dirname "$0")/.." && pwd)"
MD="${1:?usage: render.sh <content_final.md> <profile> <out.docx> [max_pages]}"
PROFILE="${2:?profile missing}"
OUT="${3:?out.docx missing}"
MAX_PAGES="${4:-}"
REF="$KIT/profiles/$PROFILE/reference.docx"
[[ -f "$REF" ]] || { echo "no reference.docx for profile '$PROFILE': run python3 profiles/build_reference_docx.py $PROFILE"; exit 2; }
OUTDIR="$(cd "$(dirname "$OUT")" && pwd)"
NAME="$(basename "$OUT" .docx)"
DOCX="$OUTDIR/$NAME.docx"; PDF="$OUTDIR/$NAME.pdf"; TXT="$OUTDIR/$NAME.txt"; PAGES="$OUTDIR/pages"
GROUNDING="${GROUNDING:-$(cd "$(dirname "$MD")" && pwd)/../grounding.md}"
typeset -A RESULT

# 1. Markdown -> DOCX. `# Title` becomes the document Title; `##` -> Heading 1; `###` -> Heading 2.
# HTML comments (freeze header) are removed first: they never render, and a leading comment would
# stop pandoc from promoting `# Title` to the Title style.
python3 -c 'import re,sys; sys.stdout.write(re.sub(r"<!--.*?-->\n?", "", open(sys.argv[1], encoding="utf-8").read(), flags=re.S))' "$MD" \
  | pandoc --from markdown --to docx --reference-doc "$REF" --shift-heading-level-by=-1 \
      --resource-path "$(dirname "$MD")" -o "$DOCX" \
  || { echo "pandoc failed"; exit 2; }
echo "docx: $DOCX"

# 2. DOCX -> PDF.
ENGINE="${PDF_ENGINE:-}"
if [[ -z "$ENGINE" ]]; then
  if [[ -d "/Applications/Microsoft Word.app" ]]; then ENGINE=word
  elif command -v soffice >/dev/null; then ENGINE=libreoffice
  else ENGINE=none; fi
fi
rm -f "$PDF"
if [[ "$ENGINE" == word ]]; then
  # Word is sandboxed: work inside its container to avoid file-access prompts. One unique folder and file
  # name per render, so two renders never share a path and the document name is unique inside Word.
  RUNID="$(date +%s)-$$-$RANDOM"
  WORKROOT="$HOME/Library/Containers/com.microsoft.Word/Data/gdaw_render"
  WORK="$WORKROOT/$RUNID"; WDOC="$NAME-$RUNID.docx"; WPDF="$NAME-$RUNID.pdf"
  mkdir -p "$WORK"; cp "$DOCX" "$WORK/$WDOC"
  # Serialize Word renders: an atomic mkdir lock, taken over from a dead holder, waited for up to WORD_TIMEOUT.
  LOCK="$WORKROOT/.lock"; LWAIT=0; GOT_LOCK=0
  while (( LWAIT < ${WORD_TIMEOUT:-300} )); do
    if mkdir "$LOCK" 2>/dev/null; then echo $$ > "$LOCK/pid"; GOT_LOCK=1; break; fi
    HOLDER="$(cat "$LOCK/pid" 2>/dev/null)"
    if [[ -n "$HOLDER" ]] && ! kill -0 "$HOLDER" 2>/dev/null; then rm -rf "$LOCK"; continue; fi
    sleep 1; (( LWAIT++ ))
  done
  if (( ! GOT_LOCK )); then echo "word: another render held the lock for ${WORD_TIMEOUT:-300} s"; fi
  # The AppleScript timeout does not cover a modal or file-access prompt before the body runs; a shell
  # watchdog does. The document is addressed by its unique name, polled until Word has it open.
  osascript <<EOF >/dev/null 2>&1 &
with timeout of 180 seconds
  tell application "Microsoft Word"
    open POSIX file "$WORK/$WDOC"
    repeat 120 times
      if exists document "$WDOC" then exit repeat
      delay 0.25
    end repeat
    set theDoc to document "$WDOC"
    save as theDoc file name POSIX file "$WORK/$WPDF" file format format PDF
    close theDoc saving no
  end tell
end timeout
EOF
  OSA=$!; WAITED=0; TIMED_OUT=0
  while kill -0 $OSA 2>/dev/null; do
    if (( WAITED >= ${WORD_TIMEOUT:-300} )); then kill $OSA 2>/dev/null; TIMED_OUT=1; break; fi
    sleep 1; (( WAITED++ ))
  done
  wait $OSA 2>/dev/null
  (( GOT_LOCK )) && rm -rf "$LOCK"
  if (( TIMED_OUT )); then
    echo "word: timed out after ${WORD_TIMEOUT:-300} s"
    if command -v soffice >/dev/null; then ENGINE=libreoffice; else ENGINE="word (timed out)"; fi
  else
    [[ -f "$WORK/$WPDF" ]] && cp "$WORK/$WPDF" "$PDF"
  fi
  rm -rf "$WORK"
fi
if [[ "$ENGINE" == libreoffice ]]; then
  soffice --headless --convert-to pdf --outdir "$OUTDIR" "$DOCX" >/dev/null 2>&1
fi
if [[ -f "$PDF" ]]; then
  echo "pdf ($ENGINE): $PDF"
  # Identity: the PDF must carry this Markdown's title, headings and sentences (scripts/pdfcheck.py).
  if python3 "$KIT/scripts/pdfcheck.py" --md "$MD" --pdf "$PDF"; then RESULT[pdf]=PASS
  else echo "pdf: FAIL - the PDF does not carry this document (foreign or stale render); pages not trusted"; RESULT[pdf]=FAIL; fi
else echo "pdf: not produced (engine: $ENGINE) - page QA impossible"; RESULT[pdf]=FAIL; fi

# 3. PDF -> page images, page count.
if [[ -f "$PDF" ]]; then
  mkdir -p "$PAGES"; rm -f "$PAGES"/page-*.png(N)
  N=$(python3 - "$PDF" "$PAGES" <<'PY'
import sys, pymupdf
doc = pymupdf.open(sys.argv[1])
for i, page in enumerate(doc, 1):
    page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save(f"{sys.argv[2]}/page-{i:02d}.png")
print(doc.page_count)
PY
)
  echo "pages: $N -> $PAGES"
  if [[ -n "$MAX_PAGES" ]]; then
    if (( N <= MAX_PAGES )); then RESULT[pages]=PASS; else RESULT[pages]=FAIL; fi
    echo "page budget: $N / $MAX_PAGES ${RESULT[pages]}"
  fi
fi

# 4. Text extraction from the DOCX.
if command -v textutil >/dev/null; then textutil -convert txt -stdout "$DOCX" > "$TXT"
else pandoc -t plain --wrap=none "$DOCX" -o "$TXT"; fi
echo "text: $TXT"

# 5. Checks.
echo "--- compare.py"
if [[ -f "$GROUNDING" ]]; then python3 "$KIT/scripts/compare.py" --md "$MD" --text "$TXT" --grounding "$GROUNDING"
else echo "(no grounding at $GROUNDING: constants not checked)"; python3 "$KIT/scripts/compare.py" --md "$MD" --text "$TXT"; fi
if (( $? == 0 )); then RESULT[compare]=PASS; else RESULT[compare]=FAIL; fi

echo "--- check_names.py"
if [[ -f "$GROUNDING" ]]; then
  python3 "$KIT/scripts/check_names.py" --grounding "$GROUNDING" "$MD" "$TXT"
  case $? in 0) RESULT[names]=PASS;; 3) RESULT[names]=SKIPPED;; *) RESULT[names]=FAIL;; esac
else RESULT[names]=SKIPPED; echo "(no grounding: names not checked)"; fi

echo "--- summary"
FAILED=0
for k in pdf pages compare names; do
  [[ -n "${RESULT[$k]:-}" ]] || continue
  echo "$k: ${RESULT[$k]}"
  [[ "${RESULT[$k]}" == FAIL ]] && FAILED=1
done
echo "next: Render QA on every image in $PAGES with templates/render-qa-checklist.md"
exit $FAILED
