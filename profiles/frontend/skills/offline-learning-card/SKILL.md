---
name: offline-learning-card
description: Use when building an offline children's quiz page.
---

# Offline learning card

## Input

You receive one JSON task:

{"id": "<task id>", "topic": "<one Chinese learning goal>"}

The topic is the learning goal. Invent an original lesson for that goal. Do not copy a stock lesson, and do not reuse a previous story, names, or questions.

## What to deliver

Write only inside the requested result directory (project `.harness/results/<delivery_id>/`). Do not edit profiles, skills, source, or git history, and do not commit.

Create exactly these files:

1. `lesson.json` — the lesson object below.
2. `index.html` — one self-contained page, embedded CSS and JS only.
3. `manifest.json` — only the two artifact entries below.
4. `result.json` — delivery record.

No images, comics, panels, network requests, external fonts, or third-party packages. A system font stack in CSS is allowed. A UI card is not a comic.

## Lesson object

Use this shape. The page and `lesson.json` must contain the same object, including every story line, prompt, option, answer, and feedback string.

{
  "title": "<short Chinese title>",
  "age_range": "6–8岁",
  "learning_goal": "<the task topic, unchanged in meaning>",
  "story": ["<setup>", "<conflict>", "<negotiation>", "<result>"],
  "questions": [
    {
      "id": "q1",
      "prompt": "<spoken Chinese>",
      "answer": "A" | "B" | "C",
      "options": [
        {"id": "A", "text": "<choice>", "feedback": "<specific kind feedback>", "correct": false},
        {"id": "B", "text": "<choice>", "feedback": "<specific kind feedback>", "correct": true},
        {"id": "C", "text": "<choice>", "feedback": "<specific kind feedback>", "correct": false}
      ]
    },
    {"id": "q2", "prompt": "...", "answer": "...", "options": ["...three options A B C..."]}
  ]
}

`answer` must match the single option whose `correct` is true. Exactly two questions, ids `q1` and `q2`. Exactly three options each, ids `A`, `B`, and `C`. Vary which letter is correct when that still reads naturally.

## Pedagogy (ages 6–8)

Teach this distinction and no broader rule: a shared item may be used by taking turns after a short negotiation; a personal item belongs to its owner, who may kindly refuse to lend it. Never teach that every possession must be shared. Do not shame a refusal, and do not endorse grabbing, hiding, yelling, or damaging things.

Write the story as four short spoken-Chinese beats:

1. Setup — name the children, one shared item that is visibly shared, and one personal item the owner brought or keeps.
2. Conflict — two children both want the shared item; then someone asks to borrow the personal item.
3. Negotiation — they agree to take turns with the shared item; the owner refuses the personal item without being mean.
4. Result — the other child accepts the refusal and uses a shared alternative; both are okay.

Language: short sentences a 6–8-year-old can hear aloud. Concrete nouns. No lecture, idiom, or abstract “ownership” talk.

Each option needs its own feedback. Correct feedback starts by affirming, then states the rule in the child’s words (“这是大家的，可以商量轮流” / “这是他自己的，可以不借”). Wrong feedback is gentle (“再想想”), names what is wrong with that specific choice, and does not say personal things must be lent. Story, correct answer, and feedback must agree. Do not correct a behavior the story did not treat as wrong.

## Transfer (required)

Do not write two recall questions about the same episode. If both prompts can be answered by repeating the story’s names, objects, and outcome, rewrite them.

- The story is the model. It uses the topic’s concrete items.
- Both questions apply the rule under a changed condition: different children, a different place, or different objects from the story pair.
- q1 tests the shared-item rule (negotiate turns; do not hide, grab, or give it to whoever is loudest).
- q2 tests the personal-item rule (the owner may say no; the asker stays calm and switches to a shared alternative). Do not key “必须借”, throwing the item away, or forcing the owner.
- Feedback must explain the rule, not “because that is what the story child did.”
- At least one question must use people and objects that do not appear in the story, so memory of the episode is not enough.

## Page behavior

Read the project agent rules, the `offline-learning-card` skill, and the frontend profile notes first. If they name hooks, match them exactly. Otherwise use:

- Each question container: `data-question` equal to `q1` or `q2`.
- Each option button: `data-option` equal to `A`, `B`, or `C`, inside its question.
- Each feedback element: `data-feedback`, empty until a choice.
- One reset control: `id="reset"`.

Render the title, goal, all four story lines, prompts, and options from the lesson object. Do not hard-code a second copy of the visible wording.

Interaction:

- On a choice, show that option’s feedback.
- A wrong choice stays retryable. Do not disable the question.
- The correct choice marks that option, shows its feedback, and disables only that question.
- Reset clears feedback text, correct/wrong classes, and disabled state on every question.

Layout must be usable at 390px and 1280px width. Large tap targets. Feedback visible next to the question. No hover-only actions.

Embed the lesson by inserting the exact `lesson.json` text into:

<script id="lesson-data" type="application/json">…exact JSON…</script>

and set `const lesson` from `JSON.parse` of that node. The JSON text in the page must be byte-for-byte the same as `lesson.json` (same strings; no comments, trailing commas, or JS expressions).

## manifest.json

{"artifacts":[
  {"path":"index.html","name":"index.html","kind":"document","content_type":"text/html"},
  {"path":"lesson.json","name":"lesson.json","kind":"data","content_type":"application/json"}
]}

Do not list `manifest.json` or `result.json`.

## result.json

{
  "profile": "frontend",
  "delivery_id": "<the requested delivery id>",
  "source_revision": "<real git rev-parse HEAD of the project>",
  "summary": "<one Chinese sentence: age, goal, four-beat story, two retryable transfer questions, page matches lesson.json>",
  "checks": ["<only checks that actually ran>"],
  "limits": [
    "未打开浏览器则写明未做浏览器验证",
    "无网络、无图片、无外链脚本或字体",
    "题目是迁移应用，不是复述故事原句"
  ]
}

Record the revision with `git rev-parse HEAD` in the project repo. Never invent a hash. List a browser check only if a browser was actually opened.

## Before you finish

1. Parse `lesson.json`, `manifest.json`, and `result.json`.
2. Extract the embedded lesson and deep-compare it to `lesson.json` (every story line, prompt, option text, feedback, answer, and correct flag). Use a real JSON parse, not a non-greedy brace regex.
3. Confirm hooks `data-question`, `data-option`, `data-feedback`, and `id="reset"`; no `http` URLs, image tags, or external scripts.
4. Re-read both prompts against the story. If either prompt only asks what the story characters already did with the same objects, replace it with a new situation before writing the files.
