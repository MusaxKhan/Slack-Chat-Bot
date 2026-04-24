# app.py - Main application logic for the Slack Co-Pilot
# app.py contains the core flow of the Slack bot, including:
# - Handling incoming messages and maintaining conversation state
# - Extracting structured context from the conversation using the LLM
# - Determining when enough context has been gathered to find matches
# - Finding matches based on the structured context
# - Formatting and sending the response back to Slack

import re
from flask import request
from config import bolt_app, flask_app, handler, USER_STATE, debug
from llm import extract_structured_context, generate_clarifying_question
from conversation import has_enough_context, get_next_question_field
from matching import find_matches
from formatter import format_matches_response, generate_confirmation_summary


@bolt_app.event("app_mention")
def handle_mention(event, say):
    user_id = event["user"]
    raw_text = event.get("text", "")
    text = re.sub(r"<@[A-Z0-9]+>", "", raw_text).strip()

    debug("USER INPUT", f"user={user_id} | text={text}")

    # =========================
    # RESTART HANDLER
    # =========================
    restart_commands = ["restart", "start over", "reset", "begin again"]

    if any(cmd in text.lower() for cmd in restart_commands):
        USER_STATE[user_id] = {
            "turns": [],
            "structured": {},
            "phase": "gathering",
            "asked_fields": set(),
            "questions_asked": 0
        }

        say(
            ":arrows_counterclockwise: Starting fresh.\n\n"
            "Tell me what you're trying to build or solve — "
            "I'll find the right people in your network to help.\n\n"
            "_What's the challenge you're working on?_"
        )
        return

    is_new_session = user_id not in USER_STATE or USER_STATE[user_id]["phase"] == "done"

    if is_new_session:
        USER_STATE[user_id] = {
            "turns": [],
            "structured": {},
            "phase": "gathering",
            "asked_fields": set(),
            "questions_asked": 0
        }
        greeting = (
            ":wave: Hey! I'm your *Smart Connector Co-pilot*.\n\n"
            "Tell me what you're trying to build or solve — "
            "I'll find the right people in your network to help.\n\n"
            "_What's the challenge you're working on?_"
        )
        say(greeting)
        if text:
            USER_STATE[user_id]["turns"].append({"role": "user", "content": text})
        else:
            return

    state = USER_STATE[user_id]

    if not is_new_session and text:
        state["turns"].append({"role": "user", "content": text})

    structured = extract_structured_context(state["turns"])
    state["structured"] = structured
    debug("STRUCTURED CONTEXT", structured)
    debug("QUESTIONS ASKED", state["questions_asked"])

    if has_enough_context(structured, state["questions_asked"]):
        state["phase"] = "done"
        say(generate_confirmation_summary(structured))
        direct, supporting = find_matches(structured)
        say(format_matches_response(direct, supporting, structured))
        return

    field, fallback = get_next_question_field(structured, state["asked_fields"])

    if field is None:
        state["phase"] = "done"
        say(generate_confirmation_summary(structured))
        direct, supporting = find_matches(structured)
        say(format_matches_response(direct, supporting, structured))
        return

    state["asked_fields"].add(field)
    state["questions_asked"] += 1

    question = generate_clarifying_question(state["turns"], structured, field, fallback)
    state["turns"].append({"role": "assistant", "content": question})
    say(question)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


if __name__ == "__main__":
    print("🚀 Smart Connector Co-pilot running on port 3000...")
    flask_app.run(port=3000, debug=True)