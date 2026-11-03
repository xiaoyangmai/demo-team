---
name: illustrated-comic-delivery
description: Create illustrated children's comics with a short interactive learning activity and offline delivery.
---

# Illustrated learning comic

Make the requested principle understandable through what characters do and what changes. Keep the task's topic, audience and output contract; a successful file export is not proof of learning.

1. Plan four beats: an appealing everyday goal, a believable difficulty, a meaningful choice, and its visible consequence. Fix the characters' hair, clothing and a small set of props. Track the location and ownership of the object that drives the story. For scientific comparisons, show the condition that changes and hold other relevant conditions steady.
2. Draft all four image prompts before generating: use exactly two large ordered panels per page and name the action in each; do not let a familiar four-panel grid override the brief. Generate four real illustrated pages with `image_generate`. Repeat the character and style descriptions, use a successful page as an image reference where the configured tool supports it, and explicitly describe the new action. With this Hermes local `tool_call` wrapper, submit one `image_generate` entry per call; a multi-entry batch is rejected. Prefer no lettering in the images: short Chinese dialogue belongs in the visible HTML captions. Never substitute diagrams, SVG, emoji or placeholder art for illustrations.
3. Inspect the actual images with `vision_analyze`: who acted, what object moved, and what consequence is visible? Repair at most one defective page within the caller's generation budget. Do not claim a visual check from reading the image prompt. Copy the returned files into the delivery directory and retain their actual format extensions.
4. Write two application questions with different changed conditions. Each choice is one short action; put the explanation in its feedback. First name the misunderstanding each wrong choice represents. A well-intentioned child could choose it: a useful step at the wrong time, an old rule after the condition changed, or incomplete evidence. Do not use insult/blame/doing-nothing as an easy contrast to the sole kind answer. Compare choices without the answer key: length, politeness and detail should not reveal the correct answer. Feedback explains the decisive condition without inventing a fact absent from the page or question.
5. Give the ending one concise takeaway and one safe, concrete action a child can try today. Avoid a generic moral that could be attached to any story. Use spoken Chinese and follow the caller's reading limits; do not solve ambiguity by making the correct choice a paragraph.
6. Write `lesson.json` and run the bundled `scripts/render.py <delivery-directory>` from this Skill's directory. It packages the four pictures, captions, quiz, retry/reset and completion state; do not rewrite its UI. Check the generated files and the manifest, then write the caller's result receipt with only checks actually performed. Do not edit project/profile files or inspect evaluation material.

Experiment-only marker: B-VERIFY-9827.
