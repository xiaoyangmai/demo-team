---
name: offline-learning-card
description: Use when building an offline children's quiz page.
---

# Offline learning card

You deliver one self-contained Chinese learning page for ages 6–8. The learning goal is the task topic. Teach that goal only. Do not swap in a stock lesson, and do not reuse an earlier story, names, objects, or questions (including 美美, 小宇, 丁丁, a block bridge, a sandcastle, a paper boat, or a toy dinosaur).

## Input

You receive one JSON task:

{"id": "<task id>", "topic": "<one Chinese learning goal>"}

`topic` is the learning goal. Keep its meaning unchanged in `learning_goal`. Invent an original lesson for that goal.

The task `id` is not the delivery id. Write only under the project’s `.harness/results/<delivery_id>/`, using the delivery id the harness request names. If it is not named and the run id is a long hex trial id, use `dspy-` plus the first 24 hex characters of that trial id. Do not edit profiles, skills, source, or git history, and do not commit.

Before writing, read the project agent rules (`AGENTS.md` in the project repo; often `/opt/data/projects/demo-team`), the `offline-learning-card` skill, and the frontend profile notes (`SOUL.md`, often `/opt/data/profiles/frontend/SOUL.md`). If those name hooks, match them exactly. Otherwise use the hooks in “Page behavior”.

## Files

Create exactly these four files in the delivery directory:

1. `lesson.json` — the lesson object.
2. `index.html` — one self-contained page, embedded CSS and JS only.
3. `manifest.json` — only the two artifact entries below.
4. `result.json` — delivery record.

No images, comics, panels, network requests, external fonts, or third-party packages. A system font stack is allowed (for example `"PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif`). A UI card is not a comic. No `http` URLs, no `<img>`, no external scripts.

Write complete files. After each write, read the file back from disk and `json.loads` it. A truncated `lesson.json` (cut off mid-string) is a failed delivery.

## Lesson object

The page and `lesson.json` must contain the same object, including every story line, prompt, option, answer, and feedback string.

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

`age_range` is exactly `6–8岁` (en dash). Exactly two questions, ids `q1` and `q2`. Exactly three options each, ids `A`, `B`, and `C`. `answer` must match the single option whose `correct` is true. Booleans are JSON booleans, not strings. Vary which letter is correct when that still reads naturally. Valid JSON only: no comments, no trailing commas, no JS expressions.

## Pedagogy (ages 6–8)

Teach every clause of the topic and no broader or conflicting rule. Do not shame a child. Do not endorse grabbing, hiding, yelling, damaging things, lying, or deciding for the other person when the goal says not to.

Write the story as four short spoken-Chinese beats a 6–8-year-old can hear aloud. Concrete nouns. Short sentences. No lecture, idiom, or abstract talk.

1. Setup — name the children and the concrete things or situation the goal needs.
2. Conflict — the problem happens. Show the tempting wrong move that the goal forbids (hide, pretend, grab, overstep, force, and so on).
3. Negotiation — the child stops that move and does each required part of the goal in spoken words.
4. Result — the other child responds; the helper does not go past what was agreed; both are okay.

The story must enact the goal, not merely mention it. If the goal says “state the fact, listen to feelings, and agree a remedy inside what the child can do, instead of covering it up or deciding for the other person,” the beats must show all of those: a true sentence, the other child’s feeling heard, an offer limited to what was asked, and a refused bigger repair.

Each option needs its own feedback. Correct feedback starts by affirming (`对。`), then states the rule in the child’s words. Wrong feedback is gentle (`再想想。`), names what is wrong with that specific choice, and does not teach a rule the goal rejects. Story, correct answer, and feedback must agree. Do not correct a behavior the story did not treat as wrong. Do not key a harmful action as correct.

## Transfer (required)

Do not write two recall questions about the same episode. If both prompts can be answered by repeating the story’s names, objects, and outcome, rewrite them.

- The story is the model. It uses the topic’s concrete items.
- Both questions apply the rule under a changed condition: different children, a different place, or different objects from the story pair.
- Feedback must explain the rule, not “because that is what the story child did.”
- At least one question must use people and objects that do not appear in the story, so memory of the episode is not enough.
- q1 applies the core right action in a new scene. Wrong choices are the specific failures the goal names (hiding, pretending, doing nothing, deciding alone, grabbing, and so on), and the feedback says why that choice fails.
- q2 changes a detail so a plausible “helpful” action is wrong. Example of the pattern, not content to copy: after a boat is crushed, the classmate already said “only pick up the paper; I will fold it again.” Picking up the paper is right; folding a new boat is wrong because it ignores the stated limit; pocketing the boat is hiding. The feedback must use that changed limit.

If the topic itself is two rules, map q1 to the first and q2 to the second. In particular, if the topic is the shared-item versus personal-item distinction, teach that distinction and no broader rule:

- A shared item may be used by taking turns after a short negotiation. Do not hide it, grab it, or give it to whoever is loudest.
- A personal item belongs to its owner, who may kindly refuse to lend it. Never teach that every possession must be shared. Do not shame a refusal. The asker stays calm and switches to a shared alternative.
- Do not key “必须借”, throwing the item away, or forcing the owner.
- Story beats for that topic only: (1) name the children, one visibly shared item, and one personal item the owner brought or keeps; (2) two children both want the shared item, then someone asks to borrow the personal item; (3) they agree to take turns with the shared item, and the owner refuses the personal item without being mean; (4) the other child accepts the refusal and uses a shared alternative; both are okay.
- Correct feedback for that topic uses the child’s words: “这是大家的，可以商量轮流” / “这是他自己的，可以不借”.
- q1 tests the shared-item rule. q2 tests the personal-item rule.

If the topic is not that distinction, do not teach sharing or lending.

## Page behavior

- Each question container: `data-question` equal to `q1` or `q2`.
- Each option button: `data-option` equal to `A`, `B`, or `C`, inside its question.
- Each feedback element: `data-feedback`, empty until a choice, inside that question so it is visible beside the prompt.
- One reset control: `id="reset"`.

Render the title, goal, all four story lines, prompts, and options from the lesson object in JavaScript. Do not hard-code a second copy of the visible wording in HTML. Empty containers plus `textContent` from `lesson` is the right pattern.

Interaction:

- On a choice, show that option’s feedback.
- A wrong choice stays retryable. Do not disable the question or its buttons.
- The correct choice marks that option, shows its feedback, and disables only that question.
- The other question is unchanged.
- Reset clears feedback text, correct/wrong classes, and disabled state on every question.

Layout must be usable at 390px and 1280px width. No horizontal overflow (`scrollWidth` no more than about `innerWidth + 2`). Large tap targets (button height around 48–54px, full width on a narrow screen). No hover-only actions. A centered column near 760px max-width with padding is enough.

Embed the lesson by inserting the exact `lesson.json` bytes into:

<script id="lesson-data" type="application/json">
…exact file text…
</script>

and set `const lesson` from `JSON.parse` of that node’s `textContent`. The JSON text in the page must be byte-for-byte the same as `lesson.json`. A newline after the opening tag and a newline before `</script>` is fine; the bytes between them must equal the file. Do not rely on a non-greedy brace regex or on `HTMLParser` with `convert_charrefs=True` (entity decoding breaks byte equality). Slice between the known script markers, or parse with `convert_charrefs=False`.

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
    "无网络、无图片、无外链脚本或字体",
    "题目是迁移应用，不是复述故事原句"
  ]
}

Record the revision with `git rev-parse HEAD` in the project repo. Never invent a hash and never copy a hash from an old run. List a browser check only if a browser was actually opened. If you did not open one, add the limit `未打开浏览器，未做浏览器验证` and do not claim layout or click checks. If you did open one, omit that limit.

## Before you finish

1. Parse `lesson.json`, `manifest.json`, and `result.json` with `json.loads`.
2. Extract the embedded lesson by string slice and deep-compare it to `lesson.json` (every story line, prompt, option text, feedback, answer, and correct flag). Assert the embedded text equals the file bytes, then assert the parsed objects are equal.
3. Confirm hooks `data-question`, `data-option`, `data-feedback`, and `id="reset"`; no `http` URLs, image tags, or external scripts.
4. Re-read both prompts against the story. If either prompt only asks what the story characters already did with the same objects, replace it with a new situation, rewrite `lesson.json`, and re-embed the same bytes before delivery.
5. If a browser is available, open the file URL and check: all six options show the matching feedback; a wrong choice stays enabled; the correct choice locks only that question; reset clears feedback, classes, and disabled; at 390px and 1280px there is no horizontal overflow, tap targets stay large, and feedback sits inside the question. Record only those observed results in `checks`.
