---
name: offline-learning-card
description: Use when building an offline children's quiz page.
---

# Offline learning card

## Always-on rules

- Deliver one self-contained `index.html` with embedded CSS and JS. No network, images, fonts, or third-party packages.
- Keep story, prompts, options, answers, and feedback identical in the page and `lesson.json`. Author the content; do not import a stock lesson.
- For ages 6–8, use short spoken Chinese. Give each option specific, kind feedback. A wrong answer stays retryable until it is correct.
- Distinguish shared items that can be taken in turns from personal items the owner may refuse to lend. Do not teach that every possession must be shared.
- Honor requested hooks exactly: question containers, option buttons, feedback elements, and the reset control use the ids and data attributes named in the task.
- A UI card is not a comic. Do not generate panels or images unless the task asks for an illustrated comic.

## Procedure

1. Read the project agent rules and record the real git revision. Write only inside the requested result directory. Do not edit profiles, skills, source, or commit.
2. Draft the story as setup, conflict, negotiation, and result. Then write two three-choice questions whose correct choices follow that story.
3. Put the same lesson object in `lesson.json` and inside the page script. Render story and questions from that object so the visible text cannot drift.
4. Mark the correct choice, show that option's feedback, and disable the question only after a correct answer. Reset clears feedback, classes, and disabled state on every question.
5. Write `manifest.json` with only the requested artifact entries. Write `result.json` with the profile, delivery id, actual revision, summary, checks that ran, and limits.
6. Parse every JSON file and compare the embedded lesson to `lesson.json`, including every story line, prompt, option, and feedback. Do not claim a browser check unless a browser was actually opened.
