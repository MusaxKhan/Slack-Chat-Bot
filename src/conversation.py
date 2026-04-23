# conversation.py - Manages the conversation flow and context extraction for the Slack Co-Pilot
# It defines the logic for determining when enough context has been gathered from the user,
# and what the next question to ask should be. It uses a predefined queue of questions and checks the
# structured context to decide what to ask next.


from config import MIN_QUESTIONS, MAX_QUESTIONS

QUESTION_QUEUE = [
    {
        "field": "problem",
        "required": True,
        "check": lambda s: bool(s.get("problem", "").strip()),
        "ask": "What's the core problem or challenge you're trying to solve?"
    },
    {
        "field": "domain",
        "required": True,
        "check": lambda s: bool(s.get("domain", "").strip()),
        "ask": "What industry or domain is this for — e.g. gaming, fintech, SaaS, ecommerce, AI, marketing?"
    },
    {
        "field": "needs",
        "required": True,
        "check": lambda s: len(s.get("needs", [])) > 0,
        "ask": "What kind of expertise do you need — e.g. backend, frontend, design, data, growth, security, or a mix?"
    },
    {
        "field": "stage",
        "required": False,
        "check": lambda s: bool(s.get("stage", "").strip()),
        "ask": "What stage is this at — early idea, building an MVP, already live, or scaling?"
    },
    {
        "field": "goal",
        "required": False,
        "check": lambda s: bool(s.get("goal", "").strip()),
        "ask": "What does success look like for you — what outcome are you working toward?"
    },
    {
        "field": "urgency",
        "required": False,
        "check": lambda s: bool(s.get("urgency", "").strip()),
        "ask": "How urgent is this — do you need someone immediately, or is there flexibility on timing?"
    },
    {
        "field": "team_size",
        "required": False,
        "check": lambda s: bool(s.get("team_size", "").strip()),
        "ask": "Who's currently on this — are you working solo, or do you have a team already?"
    },
    {
        "field": "constraints",
        "required": False,
        "check": lambda s: bool(s.get("constraints", "").strip()),
        "ask": "Any constraints I should factor in — budget, timeline, specific tech stack preferences?"
    },
    {
        "field": "tried_before",
        "required": False,
        "check": lambda s: bool(s.get("tried_before", "").strip()),
        "ask": "Have you already tried anything to solve this, or is there an approach you've ruled out?"
    },
]

REQUIRED_FIELDS = [q["field"] for q in QUESTION_QUEUE if q["required"]]
ENRICHMENT_FIELDS = [q["field"] for q in QUESTION_QUEUE if not q["required"]]


def count_filled_enrichment(structured):
    count = 0
    for f in ENRICHMENT_FIELDS:
        val = structured.get(f)
        if val and (
            (isinstance(val, str) and val.strip()) or
            (isinstance(val, list) and len(val) > 0)
        ):
            count += 1
    return count


def has_enough_context(structured, questions_asked):
    if questions_asked < MIN_QUESTIONS:
        return False
    if questions_asked >= MAX_QUESTIONS:
        return True
    for field in REQUIRED_FIELDS:
        val = structured.get(field)
        if not val or (isinstance(val, list) and len(val) == 0) or (isinstance(val, str) and not val.strip()):
            return False
    return count_filled_enrichment(structured) >= 4


def get_next_question_field(structured, asked_fields):
    for q in QUESTION_QUEUE:
        if q["field"] not in asked_fields and not q["check"](structured):
            return q["field"], q["ask"]
    return None, None