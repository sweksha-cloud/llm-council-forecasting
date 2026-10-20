"""
Prompts used for every forecast. Single models and council members get the
SAME forecast prompt, so deliberation is the only difference between a
single model's answer and the council's.

Bump PROMPT_ID whenever a prompt changes; it's saved with every forecast.
"""

import re

PROMPT_ID = "v2"  # v2: reasoning before probability (v1 put the number first; Llama answered 0.55 on almost everything)

FORECAST_SYSTEM = (
    "You are a careful forecaster. You estimate the probability of future events "
    "using what you know, base rates, and reasoning. You cannot look anything up. "
    "Always give a probability, even when uncertain; never refuse."
)

QUESTION_BLOCK = """Today's date: {today}
Question: {question}
Closes: {close_date}
How it resolves: {criteria}"""

FORECAST_USER = """{question_block}

Estimate the probability that this question resolves YES.
Respond with JSON only, in exactly this format:
{{"reasoning": "<2-4 sentences>", "probability": <number between 0 and 1>}}"""

CHAIRMAN_SYSTEM = (
    "You are the chair of a panel of forecasters. You read each panelist's "
    "independent forecast and reasoning, weigh their arguments, and give the "
    "panel's final probability. You cannot look anything up. Always give a "
    "probability; never refuse."
)

CHAIRMAN_USER = """{question_block}

The panelists answered independently:
{member_answers}

Weigh their arguments and give the panel's final probability that this question resolves YES.
Respond with JSON only, in exactly this format:
{{"reasoning": "<2-4 sentences>", "probability": <number between 0 and 1>}}"""

# Chair ablations (forecast/rechair.py, docs/decisions.md 2026-10-20). Same members' answers, same
# question block; only what the chair is shown changes. The setup name records the variant, and
# the rows keep the members' PROMPT_ID.
CHAIRMAN_NUMBERS_SYSTEM = (
    "You are the chair of a panel of forecasters. You read each panelist's "
    "independent probability and give the panel's final probability. You cannot "
    "look anything up. Always give a probability; never refuse."
)

CHAIRMAN_NUMBERS_USER = """{question_block}

The panelists answered independently (probabilities only):
{member_answers}

Give the panel's final probability that this question resolves YES.
Respond with JSON only, in exactly this format:
{{"reasoning": "<2-4 sentences>", "probability": <number between 0 and 1>}}"""

CHAIRMAN_REASONING_SYSTEM = (
    "You are the chair of a panel of forecasters. You read each panelist's "
    "independent reasoning (their probabilities are withheld), weigh their "
    "arguments, and give the panel's final probability. You cannot look anything "
    "up. Always give a probability; never refuse."
)

CHAIRMAN_REASONING_USER = """{question_block}

The panelists reasoned independently (their probabilities are withheld):
{member_answers}

Weigh their arguments and give the panel's final probability that this question resolves YES.
Respond with JSON only, in exactly this format:
{{"reasoning": "<2-4 sentences>", "probability": <number between 0 and 1>}}"""

# Debate, round 2 (forecast/debate.py, docs/decisions.md 2026-10-20): each member sees its own
# first answer and the other members' answers (anonymised), and may revise.
REVISE_USER = """{question_block}

Your earlier forecast: probability {own_p:.2f}. {own_reasoning}

The other panelists answered independently:
{member_answers}

Reconsider your forecast in light of their arguments. Keep it if you still think it is right.
Respond with JSON only, in exactly this format:
{{"reasoning": "<2-4 sentences>", "probability": <number between 0 and 1>}}"""

# Structured-output schema passed to Ollama so replies come back as JSON.
# Reasoning comes first so the model thinks before it commits to a number.
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "reasoning": {"type": "string"},
        "probability": {"type": "number"},
    },
    "required": ["reasoning", "probability"],
}

MAX_CRITERIA_CHARS = 1500


def question_block(question: str, close_date: str, criteria: str, today: str) -> str:
    criteria = " ".join((criteria or "Not specified.").split())
    if len(criteria) > MAX_CRITERIA_CHARS:
        criteria = criteria[:MAX_CRITERIA_CHARS] + "…"
    return QUESTION_BLOCK.format(today=today, question=question, close_date=close_date, criteria=criteria)


def member_answers_text(answers: list) -> str:
    """answers: list of (probability, reasoning). Panelists are anonymous (A, B, C…)."""
    lines = []
    for i, (p, reasoning) in enumerate(answers):
        lines.append(f"Panelist {chr(65 + i)}: probability {p:.2f}. {reasoning.strip()}")
    return "\n".join(lines)


# Probability-like numbers in a panelist's reasoning: "70%", "70 percent", "0.7", ".35", "1.0".
# Counts and dates ("3 debates", "2026") are left alone.
NUMBER_RE = re.compile(r"(?<![\w.])(?:\d+(?:\.\d+)?\s*(?:%|percent\b)|0?\.\d+|1\.0+)(?!\w|\.\d)", re.IGNORECASE)
REDACTED = "[number withheld]"


def redact_numbers(text: str) -> str:
    return NUMBER_RE.sub(REDACTED, text)


def member_numbers_text(answers: list) -> str:
    """Numbers-only view: each panelist's probability, no reasoning."""
    return "\n".join(f"Panelist {chr(65 + i)}: probability {p:.2f}." for i, (p, _) in enumerate(answers))


def member_reasoning_text(answers: list) -> str:
    """Reasoning-only view: each panelist's reasoning with probability-like numbers withheld."""
    return "\n".join(f"Panelist {chr(65 + i)}: {redact_numbers(reasoning.strip()) or '(no reasoning given)'}"
                     for i, (_, reasoning) in enumerate(answers))
