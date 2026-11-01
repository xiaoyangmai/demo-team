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
2. Before writing the story, name the small decision the child should learn to make. Identify the facts needed for that decision. Draft a short story as setup, conflict, negotiation, and result.
3. Write two three-choice questions. One can reinforce the story. For the application question, identify the story's successful action, then change one stated condition so copying that action would miss something important. The best response must account for that condition. Keep the same activity if useful; adding difficulty, another day, or another object does not by itself change the decision.
   - Give each question a plausible, well-intentioned but incomplete option. The child should need the learning principle to distinguish it from the best answer; avoiding an obviously cruel or absurd option is not enough.
   - State the facts needed to choose in the story or question. Feedback explains the distinction using those facts; it must not invent a condition to justify the answer.
   - Keep each choice short. Extra conditions, a distant setting, and a longer action chain do not make a better question.
4. Check the application question once before packaging: can its best answer be copied from the story just by swapping names or objects? If yes, rewrite that question using a decision-relevant change, not extra description. Also check that a plausible partial choice misses that stated change and that feedback invents no facts. Allow one repair and recheck; report any unresolved limitation. In the existing `result.json` checks, briefly record the story action, the question's changed condition, and how the appropriate response changes. This is a concrete content check, not an independent quality score; no extra file is needed.
5. Put the same lesson object in `lesson.json` and inside the page script. Render story and questions from that object so the visible text cannot drift.
6. Mark the correct choice, show that option's feedback, and disable the question only after a correct answer. Reset clears feedback, classes, and disabled state on every question.
7. Write `manifest.json` with only the requested artifact entries. Write `result.json` with the profile, delivery id, actual revision, summary, checks that ran, and limits.
8. Parse every JSON file and compare the embedded lesson to `lesson.json`, including every story line, prompt, option, and feedback. Do not claim a browser check unless a browser was actually opened.

## Small contrast for question design

Illustration only; write original content for the requested topic.

- Story: a box is labelled “圆形”; a child puts a red ball inside.
- Recall: “孩子放进了什么？” The story supplies the answer.
- Disguised recall: keep “圆形” but ask about a round yellow lid instead of the red ball. Swapping objects leaves the same decision; this is insufficient for the application question.
- Application: “现在盒子写着‘蓝色’。蓝积木和红球，哪件能放？” Repeating the story's action selects the red ball; reading the new rule selects the blue block.
- The difference is the changed rule, not a new name. A question cannot explain that an object is blue unless its colour is stated. This example illustrates the decision, not the required number of answer options.
