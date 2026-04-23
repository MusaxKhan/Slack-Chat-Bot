# llm.py - Handles interactions with the LLM for context extraction and question generation
# This module defines functions to call the LLM for two main purposes:
# 1. extract_structured_context: Given the conversation history, extract a structured representation of the user's problem, needs, and other relevant details.
# 2. generate_clarifying_question: When more information is needed, generate a natural language question to ask the user based on what is still missing from the structured context.
# The LLM calls are made through the Groq client, and the prompts are carefully designed to elicit the desired output while adhering to strict rules about what can be inferred or assumed. The responses are also parsed and validated to ensure they fit the expected format.

from config import groq_client, debug
import json
import re


def call_llm(messages, temperature=0.3, max_tokens=600):
    try:
        res = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        debug("LLM ERROR", str(e))
        return None


def extract_structured_context(turns):
    history_text = "\n".join([f"{t['role'].upper()}: {t['content']}" for t in turns])

    prompt = f"""
You are a strict information extractor. Extract ONLY what the user has EXPLICITLY stated.

CRITICAL RULES:
- Do NOT infer, assume, or guess any field
- Do NOT fill a field based on implications or common sense
- If the user did not clearly state it in their own words, leave it empty
- "needs" must only contain roles the user specifically asked for — do NOT add roles just because it's an app
- "urgency", "stage", "goal", "team_size", "constraints", "tried_before" must be EMPTY unless the user said so directly

Return ONLY a valid JSON object — no explanation, no markdown, no backticks.

Fields:
- "problem": what the user said they want to build or solve (string, "" if not stated)
- "domain": industry/domain only if user explicitly mentioned it (string, "" if not stated)
- "needs": ONLY functional roles the user explicitly asked for e.g. ["backend", "design"] (array, [] if not stated)
- "urgency": "high"/"medium"/"low" only if user mentioned timeline pressure (string, "" if not stated)
- "stage": "idea"/"mvp"/"scaling"/"production" only if user mentioned it (string, "" if not stated)
- "team_size": only if user described their team (string, "" if not stated)
- "constraints": only if user mentioned budget/time/tech constraints (string, "" if not stated)
- "goal": only if user described a success outcome (string, "" if not stated)
- "tried_before": only if user mentioned previous attempts (string, "" if not stated)

Conversation:
{history_text}

JSON:
"""

    raw = call_llm([{"role": "user", "content": prompt}], temperature=0)
    debug("RAW EXTRACTION", raw)

    if not raw:
        return {}

    try:
        match = re.search(r"\{.*\}", raw, re.S)
        if match:
            return json.loads(match.group())
    except Exception as e:
        debug("EXTRACTION PARSE ERROR", str(e))

    return {}


def generate_clarifying_question(turns, structured, field, fallback):
    already_known = []
    field_labels = {
        "problem": "problem",
        "domain": "domain",
        "needs": "expertise needed",
        "stage": "stage",
        "goal": "goal",
        "urgency": "urgency",
        "team_size": "team size",
        "constraints": "constraints",
        "tried_before": "what's been tried"
    }

    for f, label in field_labels.items():
        val = structured.get(f)
        if val and ((isinstance(val, str) and val.strip()) or (isinstance(val, list) and len(val) > 0)):
            display = ", ".join(val) if isinstance(val, list) else val
            already_known.append(f"{label}: {display}")

    known_str = "\n".join(already_known) if already_known else "Nothing confirmed yet."
    history_text = "\n".join([f"{t['role'].upper()}: {t['content']}" for t in turns[-8:]])

    prompt = f"""
You are a sharp, friendly Slack bot helping someone find the right expert in their network.

What you already know about this person's situation:
{known_str}

What you need to find out next: {field}
Reference question (rephrase naturally): "{fallback}"

Rules:
- Ask ONLY about "{field}" — one question, one topic
- Do NOT mention, repeat, or re-ask anything already listed above
- Sound like a curious, thoughtful colleague — not a form or chatbot
- One sentence only — no preamble, no "Great!", no "Sure!", no filler words
- No emoji, no numbering, no markdown

Recent conversation:
{history_text}

Your question:
"""

    question = call_llm([{"role": "user", "content": prompt}], temperature=0.45)
    return question if question else fallback