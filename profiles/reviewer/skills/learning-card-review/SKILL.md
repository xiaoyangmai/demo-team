---
name: learning-card-review
description: Review a supplied children's learning-card lesson JSON for meaningful application, concise choices, and grounded feedback; return evidence for one targeted repair.
---

# Learning-card content review

Read only the delivery's specified lesson.json. Do not edit artifacts, inspect other deliveries, load producer plans, or start agents/CLI processes. The caller owns the next frontend turn and final acceptance.

For each question, quote the story action corresponding to the correct option. Compare the decision and its relevant conditions, not names or objects. A renamed repetition is recall. At least one question must require an unshown application of the learning principle and offer a credible, well-intentioned partial solution that misses a decisive condition; the other question may be recall. A new noun alone proves nothing.

Check that a child aged 6–8 can compare concise choices at one decision point. Flag multi-actor action chains and unsupported or contradictory feedback. Do not reward length or require both questions to be applications. Kind feedback must not call a false claim honest or invent facts.

Return only JSON: `{"questions":[{"id":"q1","story_action_quote":"...","decision_already_enacted":true,"new_decision":"...","plausible_partial_option":"..."}],"has_valid_application":false,"readability_issues":[],"consistency_issues":[],"required_repairs":[]}`.

Each required repair names the item, quotes the defect, and explains which decision or factual relationship must change. Leave it empty if no repair is needed. This review supplies actionable feedback, not an acceptance score. Do not call a runtime or start a second review.
