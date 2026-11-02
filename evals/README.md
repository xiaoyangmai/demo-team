# Evaluation materials

The executable current learning-card protocol is `harness/dspy_project.py`.
Private train/validation/test inputs live outside this repository and are hashed
in each Self-Evolution experiment receipt. Frozen held-out cases are not published
to the producer's workspace.

Grader calibration controls are defined in `harness/dspy_project.py`; their
expected boundaries are development material, never held-out evidence. `children-comic.json`
describes a separate illustrated-comic target and does not govern this learning
card experiment. Adopting a new production target requires its own dataset,
artifact checker and baseline; a high card score does not establish comic quality.
