# formatter.py - Responsible for formatting the response messages sent back to Slack
# This includes rendering the matched experts in a readable format, and generating the confirmation summary
# It defines functions like format_matches_response and generate_confirmation_summary, which take the structured context and match results to create user-friendly messages.
# The formatting is designed to be clear and engaging, using Slack's markdown and emojis to highlight key information.
# It also includes a helper function build_suggested_ask to create personalized suggestions for how the user can engage with each matched expert based on their role and the user's problem.
# The main functions are:
# - render_person: Formats a single matched person with their details and reasons for matching
# - format_matches_response: Combines multiple matches into a structured response message

def build_suggested_ask(person, structured):
    role = (person.get("role") or "").lower()
    problem = structured.get("problem", "your challenge")
    goal = structured.get("goal", "")
    context = f"{problem} — aiming to {goal}" if goal else problem

    if "engineer" in role or "developer" in role:
        return f"Ask them to review your architecture or lead technical implementation for {context}."
    if "designer" in role:
        return f"Ask them to audit your UX flows or prototype a solution for {context}."
    if "data" in role or "analyst" in role:
        return f"Ask them to analyze your data or build dashboards relevant to {context}."
    if "product" in role:
        return f"Ask them to map the product roadmap or user journey for {context}."
    if "growth" in role or "marketing" in role:
        return f"Ask them to run experiments or optimize your funnel for {context}."
    if "security" in role:
        return f"Ask them to audit your authentication and security posture for {context}."
    if "devops" in role:
        return f"Ask them to set up your deployment pipeline or infrastructure for {context}."
    if "hr" in role:
        return f"Ask them to structure your onboarding or hiring process for {context}."
    if "scientist" in role:
        return f"Ask them to build predictive models or run analysis for {context}."
    return f"Reach out to discuss how their experience maps to {context}."


def render_person(m, medal, structured):
    p = m["person"]
    score = m["score"]
    reasons = m["reasons"]

    skills_display = ", ".join(p.get("skills", []))
    availability = p.get("availability", "unknown")
    connections = p.get("connections", [])
    suggested_ask = build_suggested_ask(p, structured)

    top_reasons = []
    seen = set()
    for r in reasons:
        key = r.split("'")[1] if "'" in r else r
        if key not in seen:
            top_reasons.append(r)
            seen.add(key)
        if len(top_reasons) == 3:
            break

    block  = f"{medal} *{p.get('name')}* — _{p.get('role')}_\n"
    block += f"  • *Skills:* {skills_display}\n"
    block += f"  • *Availability:* {availability}\n"
    if connections:
        block += f"  • *Connected to:* {', '.join(connections)}\n"
    block += f"  • *Why they match:*\n"
    for r in top_reasons:
        block += f"      › {r}\n"
    block += f"  • *Suggested ask:* {suggested_ask}\n"
    block += f"  • *Match score:* `{score} pts`\n\n"
    return block


def format_matches_response(direct, supporting, structured):
    problem = structured.get("problem", "your challenge")
    domain  = structured.get("domain", "")
    needs   = structured.get("needs", [])

    medals = [
        ":first_place_medal:", ":second_place_medal:", ":third_place_medal:",
        ":four:", ":five:"
    ]

    header = (
        f":brain: *Matches for:* _{problem}_\n"
        f"Domain: `{domain}` | Needs: `{', '.join(needs)}`\n\n"
        f"{'─' * 40}\n\n"
    )

    # Section 1 — Direct
    if direct:
        body = f":dart: *Domain Experts — {domain.title()} Specialists*\n"
        body += f"_These people work directly in the `{domain}` space and match your needs:_\n\n"
        for i, m in enumerate(direct):
            body += render_person(m, medals[i] if i < len(medals) else f"{i+1}.", structured)
    else:
        body = (
            f":dart: *Domain Experts — {domain.title()} Specialists*\n"
            f"_No direct `{domain}` specialists found — see supporting matches below._\n\n"
        )

    body += f"{'─' * 40}\n\n"

    # Section 2 — Supporting
    if supporting:
        body += f":handshake: *Supporting Matches — Relevant Skills*\n"
        body += f"_These people don't specialize in `{domain}` but bring directly useful skills:_\n\n"
        for i, m in enumerate(supporting):
            body += render_person(m, medals[i] if i < len(medals) else f"{i+1}.", structured)
    else:
        body += (
            f":handshake: *Supporting Matches*\n"
            f"_No additional supporting matches found._\n\n"
        )

    footer = (
        f"{'─' * 40}\n"
        ":bulb: _Mention me again anytime to start a new search._"
    )

    return header + body + footer


def generate_confirmation_summary(structured):
    field_labels = {
        "problem":     "Problem",
        "domain":      "Domain",
        "needs":       "Expertise needed",
        "stage":       "Stage",
        "goal":        "Goal",
        "urgency":     "Urgency",
        "team_size":   "Team size",
        "constraints": "Constraints",
        "tried_before":"Already tried",
    }
    lines = []
    for f, label in field_labels.items():
        val = structured.get(f)
        if val and ((isinstance(val, str) and val.strip()) or (isinstance(val, list) and len(val) > 0)):
            display = ", ".join(val) if isinstance(val, list) else val
            lines.append(f"  • *{label}:* {display}")

    body = "\n".join(lines) if lines else "  • _(limited context — doing best-effort match)_"
    return (
        f":mag: *Here's what I understood — finding your matches now...*\n\n"
        f"{body}\n"
    )