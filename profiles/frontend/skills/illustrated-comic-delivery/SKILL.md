---
name: illustrated-comic-delivery
description: Use when making multi-page illustrated comics with HTML.
---

# Illustrated comic delivery

## Always-on rules

- Lock a character sheet before the first image: name, age range, hair, clothing colors, and one prop. Repeat that sheet in every prompt. Do not restyle mid-story.
- Each page is a real generated illustration with 2–3 bordered panels. Do not substitute text, SVG, or placeholder art.
- Keep on-image text to one short line. If a page’s lettering is garbled, regenerate that page with fewer or no words and put the sentence in the HTML caption instead.
- Name files `page-01`, `page-02`, and so on, using the extension of the bytes actually returned. A `.png` path can still be JPEG.
- Deliver only files that were generated and opened. Discard failed regenerations.
- HTML reads in page order, one figure per page, relative image paths, and alt text that states that page’s story beat.

## Procedure

1. Write the character sheet and one task-appropriate story beat per page. For a learning goal, plan an age-appropriate situation, a relevant choice or action by the characters, and its consequence. Show the key choice through the image and, when needed, short legible dialogue or a reader-visible HTML caption. Do not encourage children to try dangerous tasks alone before asking for help, and do not rely on a closing moral to convey the lesson.
2. Generate page 1. Inspect it. If hair, clothing, or panel count is wrong, regenerate before continuing.
3. Generate later pages with the previous good page as the style reference, and state that the new page is a new scene, not a copy.
4. After each page, check continuity: same people, the event follows the previous page, and this page does its beat. For a learning goal, check that the relevant action and consequence are understandable from the image together with any reader-visible captions; verify the captions agree with the image once written, and revise the page or caption if either check fails.
5. Copy each kept image into the requested directory. Read the file header and rename to the real format (`FF D8 FF` is `.jpg`; the PNG signature is `.png`).
6. Decode every kept file (SOF size for JPEG, or chunk walk plus inflate for PNG). Then write `index.html`.
7. Open the HTML and confirm each image is complete with a non-zero natural size.
8. Report page count, panel count, absolute paths, and the open check. Mention unused regenerations only as a count, not as delivered files.
