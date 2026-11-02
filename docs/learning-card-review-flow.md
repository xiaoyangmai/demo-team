# Learning-card review handoff

The caller uses existing Hermes profile APIs; no service or autonomous scheduler is added. A single Gateway run does not automatically chain profiles.

1. Invoke `frontend` with the task and one delivery directory. Wait for its terminal state and preserve its run id, trace and source revision. Files are a draft until reviewed; do not finalize yet.
2. Invoke `reviewer` with the task and that delivery's `lesson.json` path. It loads `learning-card-review`, reads only this lesson, and returns evidence-linked JSON without editing it.
3. If concrete repairs are requested, invoke `frontend` once with the same delivery id/path and `review_feedback`. It preserves the original lesson and repairs the cited issues. No repeated review-until-pass loop. A failed stage ends this delivery with its actual failure.
4. The caller finalizes the delivery using the last frontend run id, records all stage ids, downloads artifacts, and performs independent deterministic/model evaluation. Reviewer approval alone is insufficient.

Use one shared deadline/budget for the case, including production, review and optional repair. Keep source/runtime fixed across its stages. Do not spawn Hermes CLI inside a production run: CLI startup can sync bundled Skills and change profile context. Ordinary API delegation may require a later client turn; this explicit handoff uses the existing profile endpoints instead.
