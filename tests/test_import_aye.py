import pytest

from importers.import_aye import corrected_judge_score, strict_yes_no


@pytest.mark.parametrize("answer, expected", [
    ("Yes, the Democrats will likely win.", 1.0),
    ("No. Historical trends suggest otherwise.", 0.0),
    ("**No** — unlikely given current polling.", 0.0),
    ("Based on the data... Answer: Yes", 1.0),
    ("My prediction - no", 0.0),
])
def test_explicit_answers_are_graded(answer, expected):
    assert strict_yes_no(answer) == expected


@pytest.mark.parametrize("answer", [
    "I cannot provide predictions about sports outcomes.",        # contains "no" inside "cannot"
    "There is no official confirmation from Rockstar Games.",    # "no" mid-sentence is not an answer
    "Nobody knows yet.",                                           # "No" only as part of a word
    "It's not possible to know the outcome.",
    "",
])
def test_everything_else_abstains(answer):
    assert strict_yes_no(answer) is None


def test_failed_judge_read_is_not_scored_as_1():
    assert corrected_judge_score({"score": "1", "reason": "failed to parse judge output"}) is None
    assert corrected_judge_score({"score": "1", "reason": "ERROR: timeout"}) is None
    assert corrected_judge_score({"score": "1", "reason": "Answer is factually wrong."}) == 1
    assert corrected_judge_score({"score": "4", "reason": "Good."}) == 4
