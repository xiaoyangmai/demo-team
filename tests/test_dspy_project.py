from harness.dspy_project import decide, environment_report, DIMENSIONS


def grade(scores, passed=True):
    return {"score": 0.6 * min(scores) / 4 + 0.4 * sum(scores) / (4 * len(scores)), "passed": passed,
            "dimensions": dict(zip(DIMENSIONS, scores))}


def test_average_gain_cannot_hide_regression():
    result = decide({"baseline": [grade([3, 3, 3, 4, 3, 3])], "candidate": [grade([4, 4, 4, 3, 4, 4])]})
    assert result["mean_gain"] > 0
    assert not result["adopt"] and result["regressed_cases"] == [0]


def test_real_gain_without_regression_can_be_adopted():
    assert decide({"baseline": [grade([3]*6)], "candidate": [grade([4, 4, 3, 3, 3, 3])]})["adopt"]


def test_failed_candidate_and_equal_score_are_not_promoted():
    assert not decide({"baseline": [grade([3]*6)], "candidate": [grade([4]*6, False)]})["adopt"]
    assert not decide({"baseline": [grade([3]*6)], "candidate": [grade([3]*6)]})["adopt"]


def test_environment_contract_matches_control_plane():
    details = {"ready": True, "revision": "sha", "files": {"SOUL.md": "hash"}}
    assert environment_report({"ready": True, "check": {"ready": True, "details": details}}) == details
