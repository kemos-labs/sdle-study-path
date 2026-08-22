SDLE Study Path — deploy package
Built: 2026-08-22T01:31Z

This folder is the same app as local:
  cd sdle-prep && python3 -m http.server 8765

Includes:
  - All 8 tabs (Today, Days, Pass, Always, Extra, MCQs, Progress, Feedback)
  - Full in-app readings (lessons.js)
  - Full MCQ bank + quizzes/mocks (questions.js)
  - Google Drive video links (no video files)

Does NOT include:
  - data/raw PDFs (~470MB) — archive only; content already in lessons/questions
  - Local video files — use Open on Drive
  - node_modules, scripts, print tooling

Serve:
  cd dist && python3 -m http.server 8766
  Open http://localhost:8766

Host (examples):
  - Cloudflare Pages / Netlify: upload this dist/ folder
  - Prefer private / password / Access if bank materials are restricted

Progress is stored in the browser (localStorage), same as localhost.
