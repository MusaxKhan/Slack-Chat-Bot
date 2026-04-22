# Smart Connector Co-pilot — Slack Bot
> A Slack-based intelligent agent that surfaces the right people to solve a problem through structured conversation and rule-based expert matching.

## Project Structure

```
smart-connector-copilot/
│
├── src/
│   ├── app.py              # Slack event handler + Flask route (entry point)
│   ├── config.py           # All service initialization (Slack, Groq, MongoDB)
│   ├── llm.py              # Groq LLM calls: field extraction + question phrasing
│   ├── conversation.py     # Question queue, session flow, context sufficiency logic
│   ├── matching.py         # Scoring engine, skill groups, domain maps (no LLM)
│   └── formatter.py        # Slack message formatting, two-tier output rendering
│
├── database/
│   └── seed.js             # MongoDB seed script — populates the people collection
│
├── .env                    # Environment variables (not committed)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Architecture Overview

```
User (@mentions bot)
        │
        ▼
  ┌─────────────┐
  │  app.py     │  Receives Slack event, manages per-user session state
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │   llm.py    │  Groq (LLaMA 3.1) extracts structured fields from conversation
  └──────┬──────┘     — problem, domain, needs, stage, urgency, goal, team_size,
         │               constraints, tried_before
         ▼
  ┌──────────────────┐
  │ conversation.py  │  Rules engine decides: do we have enough context?
  └──────┬───────────┘  If not → generate next clarifying question (LLM phrasing only)
         │              If yes → proceed to matching
         ▼
  ┌─────────────┐
  │ matching.py │  100% hand-coded scoring engine
  └──────┬──────┘  Queries MongoDB → scores every person → splits into two tiers
         │
         ▼
  ┌──────────────┐
  │ formatter.py │  Renders two-section Slack message:
  └──────────────┘   Domain Experts  +   Supporting Matches
```

---

## How the Agent Reasons

### Step 1 — Conversation Design

The bot engages the user through a **structured question queue** with 9 fields ordered by importance:

| Priority | Field | Required? |
|----------|-------|-----------|
| 1 | `problem` | ✅ Yes |
| 2 | `domain` | ✅ Yes |
| 3 | `needs` | ✅ Yes |
| 4 | `stage` | Optional |
| 5 | `goal` | Optional |
| 6 | `urgency` | Optional |
| 7 | `team_size` | Optional |
| 8 | `constraints` | Optional |
| 9 | `tried_before` | Optional |

**Rules governing the conversation:**
- Minimum **7 questions** are always asked — the bot never matches prematurely from 2 sentences
- Maximum **10 questions** — hard cap, forces a match regardless of missing fields
- Between 7–10: proceeds only if all 3 required fields + 4 enrichment fields are genuinely filled
- An `asked_fields` set tracks every field already asked — **no field is ever asked twice**
- The LLM is told explicitly what is already known before generating each question — preventing rephrasing of answered fields

### Step 2 — Structured Extraction (LLM, strict mode)

Groq (LLaMA 3.1-8b) extracts fields from the full conversation history. The prompt is **deliberately strict**:

> *"Do NOT infer, assume, or guess any field. If the user did not clearly state it in their own words, leave it empty."*

This prevents hallucinated fields like `urgency: high` or `goal: launch in 3 months` from thin input — a real failure mode that was identified and fixed during development.

### Step 3 — Matching Engine (100% Hand-Coded, No LLM)

The matching logic is entirely deterministic. Every point awarded is documented and traceable.

**10 scoring signals:**

| Signal | Points | Notes |
|--------|--------|-------|
| Exact skill match | 40 | String equality only — no substring tricks |
| Semantic skill match | 25 | Via curated `SKILL_GROUPS` per domain |
| Exact domain match | 35 | Person works in the exact requested domain |
| Domain close match | 20 | e.g. "finance" for "fintech" |
| Domain synonym match | 8 | Loose relation — intentionally low |
| Tag exact match | 12 | Person's tags match the stated need |
| Experience keyword | 8 | Domain-aware keywords injected per domain |
| Role relevance | 15 | All words of the need present in role title |
| Availability × Urgency | up to 15 | Amplified when urgency is high |
| Stage fit | up to 12 | Startup domain for MVP, infra tags for scaling |

**Key design decisions in matching:**

- `"system design"` does **not** match the need `"design"` — direct match requires exact string equality
- `"game design"` is a completely isolated skill group — never bleeds into generic `"design"` queries
- `"gaming"` domain synonyms are tight (`["gaming", "game development"]`) — no generic `"startup"` or `"mobile"` leaking in
- `NEED_ALIASES` resolves LLM extraction inconsistencies before scoring — `"game dev"` → `"game design"`, `"pm"` → `"product"`, etc.
- Domain-specific keyword injection enriches experience matching per domain (e.g. gaming queries look for `"unity"`, `"mechanics"`, `"2d"` in experience text)

### Step 4 — Two-Tier Output

Results are split into two ranked sections (5 each):

- **🎯 Domain Experts** — people whose `domains` field contains the exact requested domain or a tight synonym. These are specialists first.
- **🤝 Supporting Matches** — people with high skill/role scores but no direct domain overlap. Their raw score may be higher, but they never displace a domain specialist from the top section.

This prevents a generic backend engineer from outranking an actual game developer just because they have more keywords in their profile.

---

## Setup & Running

### Prerequisites

- Python 3.9+
- Node.js 18+ (for seed script)
- MongoDB installed locally
- A Slack workspace where you can install apps
- [ngrok](https://ngrok.com) account (free tier works)
- [Groq](https://console.groq.com) API key (free tier works)

---

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd smart-connector-copilot

pip install -r requirements.txt
```

**`requirements.txt`:**
```
slack-bolt
flask
pymongo
groq
python-dotenv
```

---

### 2. Environment Variables

Create a `.env` file in the root:

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
GROQ_API_KEY=your-groq-api-key
MONGO_URI=mongodb://localhost:27017
```

To get your Slack credentials:
1. Go to [api.slack.com/apps](https://api.slack.com/apps) → Create New App → From Manifest
2. Under **OAuth & Permissions** → copy `Bot User OAuth Token` → `SLACK_BOT_TOKEN`
3. Under **Basic Information** → copy `Signing Secret` → `SLACK_SIGNING_SECRET`
4. Add Bot Token Scopes: `app_mentions:read`, `chat:write`
5. Enable **Event Subscriptions** → Subscribe to `app_mention`

---

### 3. Database Setup

Start MongoDB (run this in its own terminal):

```bash
mongod --dbpath "C:\data\db"
```

> On first run, create the data directory if it doesn't exist:
> ```bash
> mkdir C:\data\db
> ```

Seed the database with mock people data:

```bash
cd database
node seed.js
```

This connects to `mongodb://localhost:27017`, creates the `slack_co_pilot` database, drops any existing `people` collection, and inserts all profiles covering every supported domain.

**Supported domains in seed data:**
`fintech` · `ecommerce` · `saas` · `ai` · `automation` · `marketing` · `hr` · `education` · `gaming` · `healthcare` · `enterprise` · `startup` · `mobile`

---

### 4. Running the Full Stack

These three processes must run **in parallel** — open three separate terminals:

**Terminal 1 — MongoDB**
```bash
mongod --dbpath "C:\data\db"
```

**Terminal 2 — Bot Server**
```bash
cd src
python app.py
```

**Terminal 3 — ngrok Tunnel**
```bash
ngrok http 3000
```

Once ngrok is running, copy the `https://` forwarding URL and paste it into your Slack app:

- Go to **Event Subscriptions** → Request URL → `https://your-ngrok-url/slack/events`
- Slack will send a challenge request — the bot must be running to verify it

---

### 5. Test the Bot

1. Invite the bot to a channel: `/invite @YourBotName`
2. Mention it: `@YourBotName I want to build something`
3. Answer its questions — it will ask 7–10 before returning matches
4. Mention it again after it finishes to start a fresh session

---

## What I Would Improve With More Time

### 1. Persistent Session Storage
Currently sessions live in `USER_STATE` — an in-memory Python dict. A server restart wipes all active conversations. With more time I'd move session state to MongoDB or Redis so conversations survive restarts and scale across multiple server instances.

### 2. LinkedIn / Web Profile Enrichment
The matching engine scores against static profile data. A real improvement would be to fetch live LinkedIn data or GitHub activity to verify that a person's claimed skills are active and current — not just listed on a profile from 3 years ago.

### 3. Smarter Need Extraction
The current LLM extraction is strict-mode to prevent hallucination, which sometimes means it under-extracts. A two-pass approach — first extract conservatively, then run a second pass specifically to infer domain from problem context — would improve coverage without introducing the hallucination problem.

### 4. Feedback Loop
After the bot returns matches, the user could react with ✅ or ❌ on each recommendation. That signal could feed back into the scoring weights over time, making the matcher learn which signals are actually predictive for this specific network.

### 5. Slot-Filling Instead of Strict Queue
The current question queue is linear. A slot-filling approach would let the bot ask multi-part questions when appropriate (e.g. *"What domain is this in, and what stage are you at?"*) reducing turn count for cooperative users while still probing thoroughly for minimal responders.

### 6. Team-Aware Matching
Right now the bot recommends individuals. A better version would detect when the user needs a multi-disciplinary team and surface a *set* of complementary people — e.g. "Here's a backend engineer, a designer, and a growth person who have worked together before" — using the `connections` field to prioritize people who already know each other.

### 7. Slack DM Support
Currently only works via `@mention` in channels. Adding DM support would make the workflow more natural — users could have a private conversation with the bot without broadcasting their problem to a channel.

---

## Defending the Approach

**Why hand-coded matching instead of LLM-based matching?**

LLM-based matching is a black box — you can't explain *why* someone was ranked first, and results shift between runs. For a tool that recommends real people for real problems, explainability and consistency matter. Every point in this system is traceable to a documented rule. During a walkthrough I can point to any match and explain exactly why that score was awarded.

**Why Groq/LLaMA for conversation but not matching?**

LLMs are excellent at understanding natural language and generating natural language — that's what they're used for here (extracting structured fields from freeform text, and phrasing questions conversationally). They're poor at consistent, auditable ranking logic. The split keeps each tool doing what it's actually good at.

**Why the two-tier output?**

A generic backend engineer with many keyword matches was outranking domain specialists in early testing. The two-tier design ensures that someone who actually works in gaming always appears before someone who merely has transferable skills — which is the correct prioritization for a network connector tool.

---