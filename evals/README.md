# Evaluation materials

The executable current illustrated-comic protocol is `harness/dspy_project.py`.
Private train/validation/test inputs live outside this repository and are hashed
in each Self-Evolution experiment receipt. Frozen held-out cases are not published
to the producer's workspace.

Grader calibration controls are defined in `harness/dspy_project.py`; their
expected boundaries are development material, never held-out evidence. `children-comic.json`
describes an earlier illustrated-comic contract; it is historical material, not a
second active grader. The current contract adds an interactive quiz and ending,
so its experiments use fresh baselines. Earlier learning-card scores do not
establish comic quality and are not compared numerically with current scores.
