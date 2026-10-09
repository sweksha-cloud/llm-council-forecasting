"""
Prompts used for every forecast. Single models and council members get the
SAME forecast prompt, so deliberation is the only difference between a
single model's answer and the council's.

Bump PROMPT_ID whenever a prompt changes; it's saved with every forecast.
"""

PROMPT_ID = "v1"

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
{{"probability": <number between 0 and 1>, "reasoning": "<2-4 sentences>"}}"""

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
{{"probability": <number between 0 and 1>, "reasoning": "<2-4 sentences>"}}"""

# Structured-output schema passed to Ollama so replies come back as JSON.
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "probability": {"type": "number"},
        "reasoning": {"type": "string"},
    },
    "required": ["probability", "reasoning"],
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
