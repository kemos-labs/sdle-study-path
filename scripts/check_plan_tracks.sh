#!/usr/bin/env bash
# Gates for 14/30 plan tracks + SCFHS refs wiring.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FAIL=0
ok() { echo "  OK  $*"; }
fail() { echo " FAIL $*"; FAIL=1; }

echo "=== Plan tracks + SCFHS refs ==="

for f in data/scfhs_refs.js data/plan_tracks.js js/app.js index.html; do
  [[ -f "$f" ]] && ok "exists $f" || fail "missing $f"
done

grep -q 'scfhs_refs.js' index.html && ok "index loads scfhs_refs" || fail "index scfhs"
grep -q 'plan_tracks.js' index.html && ok "index loads plan_tracks" || fail "index tracks"
grep -q 'planLength' js/app.js && ok "app planLength state" || fail "planLength"
grep -q 'formatWhy' js/app.js && grep -q 'scfhsRefs' js/app.js && ok "formatWhy uses scfhs" || fail "formatWhy refs"
grep -q 'readingWithRefs' js/app.js && ok "readingWithRefs" || fail "readingWithRefs"
grep -q 'setPlanLength' js/app.js && ok "setPlanLength" || fail "setPlanLength"
grep -q 'modeCoachHtml' js/app.js && grep -q 'passReadiness' js/app.js && ok "mode coach + pass readiness" || fail "student coach"
grep -q 'formatAnswerFeedback' js/app.js && grep -q 'hingeOnly' js/app.js && ok "formatAnswerFeedback + hingeOnly" || fail "answer feedback path"
grep -q 'Calendar Day' js/app.js && ok "calendar day header" || fail "calendar day"
grep -q 'video_links.js' index.html && ok "index loads video_links" || fail "video_links script"
grep -q 'book_index.js' index.html && ok "index loads book_index" || fail "book_index script"
grep -q 'Open on Drive' js/app.js && ok "Drive video buttons" || fail "Drive video UI"
grep -q 'bookRefsHtml' js/app.js && ok "bookRefs in formatWhy" || fail "bookRefs"
grep -q 'reviewWeakPanelHtml' js/app.js && ok "review weak panel" || fail "review weak"

if command -v node >/dev/null 2>&1; then
  node -e '
const fs=require("fs");const vm=require("vm");
const g={console}; g.window=g; vm.createContext(g);
vm.runInContext(fs.readFileSync("data/scfhs_refs.js","utf8"),g);
vm.runInContext(fs.readFileSync("data/plan_tracks.js","utf8"),g);
if(!g.PLAN_TRACKS) throw new Error("PLAN_TRACKS missing");
for (const n of [14,30,45,60,90]) {
  const t=g.PLAN_TRACKS["TRACK_"+n];
  if(!Array.isArray(t)||t.length!==14) throw new Error("track "+n);
  for (const d of t) {
    if(d.lessonDay<1||d.lessonDay>14) throw new Error("bad lessonDay "+n+" d"+d.day);
  }
}
if(!Array.isArray(g.PLAN_TRACKS.DEPARTMENTS)||g.PLAN_TRACKS.DEPARTMENTS.length<6) throw new Error("departments");
console.log("  OK  node canonical lesson tracks (14/30/45/60/90)");
' || fail "node logic"
else
  echo " WARN no node"
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo ""
  echo "=== Plan tracks gates PASSED ==="
  exit 0
fi
echo ""
echo "=== Plan tracks gates FAILED ==="
exit 1
