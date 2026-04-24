# matching.py - Core logic for matching user needs to experts in the database
# This module defines the scoring algorithm that evaluates how well each person in the database matches the structured context extracted from the user's conversation. It considers factors like skill matches, domain relevance, experience alignment, and availability. The main function is find_matches, which returns a ranked list of direct and supporting matches based on the calculated scores.
# The scoring is designed to be transparent and explainable, with reasons for each match that can be used in the response formatting to help the user understand why each expert was recommended.
# The main functions are:
# - score_person: Calculates a relevance score for a single person based on the structured context and their profile
# - find_matches: Iterates through all people in the database, scores them, and returns the top matches categorized as direct or supporting based on domain relevance.

import re
from config import people_col, debug

SKILL_GROUPS = {
    "backend": ["nodejs", "python", "apis", "microservices", "databases", "sql", "system design"],
    "frontend": ["react", "javascript", "typescript", "css", "html", "vue", "angular", "nextjs"],
    "design": ["figma", "ui design", "user experience", "prototyping", "visual design", "branding", "ux", "design systems", "user research", "wireframing"],
    "ux": ["user experience", "user research", "figma", "prototyping", "wireframing", "usability testing"],
    "game design": ["game design", "game development", "unity", "unreal", "level design", "game mechanics", "2d games", "3d games", "game engine", "game physics"],
    "gaming": ["game design", "game development", "unity", "unreal", "game mechanics", "2d games", "level design", "nodejs", "python", "react"],
    "data": ["sql", "python", "data pipelines", "data engineering", "etl", "spark", "hadoop", "databases"],
    "analytics": ["analytics", "reporting", "data analysis", "excel", "tableau", "power bi", "sql", "dashboards"],
    "ml": ["machine learning", "ml", "prediction models", "statistics", "sklearn", "tensorflow", "pytorch", "deep learning", "neural networks"],
    "ai": ["nlp", "llms", "machine learning", "ml", "python", "ai products", "generative ai", "transformers"],
    "devops": ["aws", "docker", "kubernetes", "ci/cd", "terraform", "ansible", "gcp", "azure", "linux"],
    "infra": ["aws", "docker", "kubernetes", "ci/cd", "terraform", "gcp", "azure"],
    "security": ["cybersecurity", "auth systems", "encryption", "risk analysis", "penetration testing", "compliance", "pci-dss", "oauth", "sso"],
    "growth": ["growth hacking", "a/b testing", "funnels", "retention", "activation", "referral programs", "product led growth", "plg"],
    "marketing": ["marketing", "seo", "content strategy", "paid acquisition", "email marketing", "social media", "brand strategy", "influencer marketing"],
    "product": ["product strategy", "roadmapping", "user research", "product roadmap", "feature prioritization", "okrs", "kpis", "go to market"],
    "fullstack": ["react", "nodejs", "apis", "databases", "javascript", "python", "sql"],
    "hr": ["recruitment", "onboarding", "training", "performance reviews", "culture", "talent acquisition", "employee engagement"],
    "consultant": ["product strategy", "system design", "roadmapping", "game design", "user research", "game mechanics", "architecture", "technical advisory"],
}

DOMAIN_SYNONYMS = {
    "fintech": ["fintech", "finance", "payments", "banking", "insurance"],
    "ecommerce": ["ecommerce", "e-commerce", "retail", "marketplace", "d2c"],
    "saas": ["saas", "b2b", "b2b saas", "software"],
    "ai": ["ai", "ai products", "automation", "machine learning"],
    "automation": ["automation", "ai products", "ai"],
    "marketing": ["marketing", "growth", "digital marketing"],
    "hr": ["hr", "corporate", "recruitment", "people ops"],
    "education": ["education", "edtech", "education tech", "e-learning"],
    "startup": ["startup", "early stage"],
    "mobile": ["mobile apps", "consumer apps", "ios", "android"],
    "enterprise": ["enterprise", "b2b", "corporate"],
    "gaming": ["gaming", "game development"],
    "healthcare": ["healthcare", "health tech", "medtech"],
    "real estate": ["real estate", "proptech"],
    "logistics": ["logistics", "supply chain", "shipping"],
}

NEED_ALIASES = {
    "developer": "fullstack",
    "dev": "fullstack",
    "engineer": "backend",
    "coder": "fullstack",
    "programmer": "fullstack",
    "ui": "design",
    "ux": "design",
    "ui/ux": "design",
    "game dev": "game design",
    "game developer": "game design",
    "game": "game design",
    "games": "game design",
    "data science": "ml",
    "data scientist": "ml",
    "machine learning": "ml",
    "artificial intelligence": "ai",
    "cloud": "devops",
    "infrastructure": "devops",
    "ops": "devops",
    "seo": "marketing",
    "content": "marketing",
    "ads": "marketing",
    "acquisition": "growth",
    "retention": "growth",
    "pm": "product",
    "product manager": "product",
    "strategy": "product",
    "architect": "backend",
    "architecture": "backend",
    "database": "data",
    "db": "data",
    "api": "backend",
    "mobile": "frontend",
    "app": "fullstack",
    "advisor": "consultant",
    "adviser": "consultant",
}

DOMAIN_KEYWORDS = {
    "gaming":    ["game", "gaming", "2d", "3d", "shooter", "level", "mechanics", "unity", "unreal"],
    "fintech":   ["payment", "banking", "finance", "transaction", "fraud", "compliance"],
    "ecommerce": ["cart", "checkout", "inventory", "storefront", "product", "order"],
    "saas":      ["subscription", "activation", "retention", "onboarding", "b2b"],
    "ai":        ["model", "training", "inference", "llm", "nlp", "pipeline"],
    "marketing": ["campaign", "acquisition", "seo", "content", "funnel", "brand"],
    "hr":        ["hiring", "recruitment", "onboarding", "talent", "culture"],
    "education": ["learning", "curriculum", "student", "teacher", "course"],
    "security":  ["auth", "encryption", "compliance", "vulnerability", "fraud"],
    "healthcare": ["patient", "clinical", "health", "medical", "hipaa"],
}


def normalize_list(val):
    if not val:
        return []
    if isinstance(val, str):
        return [val.lower().strip()]
    return [str(v).lower().strip() for v in val]


def normalize_experience(exp):
    if not exp:
        return 0
    if isinstance(exp, list):
        return min(len(exp), 10)
    if isinstance(exp, str):
        nums = re.findall(r"\d+", exp)
        return int(nums[0]) if nums else 1
    return 0


def normalize_availability(av):
    if not av:
        return 0
    av = str(av).lower()
    if "high" in av:
        return 10
    if "medium" in av:
        return 6
    return 3


def resolve_needs(raw_needs):
    resolved = []
    for need in raw_needs:
        need_lower = need.lower().strip()
        if need_lower in NEED_ALIASES:
            canonical = NEED_ALIASES[need_lower]
            if canonical not in resolved:
                resolved.append(canonical)
        elif need_lower in SKILL_GROUPS:
            if need_lower not in resolved:
                resolved.append(need_lower)
        else:
            if need_lower not in resolved:
                resolved.append(need_lower)
    return resolved


def score_person(person, structured):
    score = 0
    reasons = []

    raw_needs = normalize_list(structured.get("needs", []))
    needs = resolve_needs(raw_needs)

    domain  = (structured.get("domain") or "").lower().strip()
    stage   = (structured.get("stage") or "").lower()
    urgency = (structured.get("urgency") or "").lower()
    goal    = (structured.get("goal") or "").lower()

    p_skills   = normalize_list(person.get("skills"))
    p_domains  = normalize_list(person.get("domains"))
    p_tags     = normalize_list(person.get("tags"))
    p_role     = (person.get("role") or "").lower()
    p_exp_list = person.get("experience", [])

    exp_score  = normalize_experience(p_exp_list)
    avail_score = normalize_availability(person.get("availability"))

    # 1. EXACT SKILL MATCH
    matched_skills = set()
    for need in needs:
        for skill in p_skills:
            if need == skill:
                if skill not in matched_skills:
                    score += 40
                    matched_skills.add(skill)
                    reasons.append(f"exact skill match: '{skill}'")

    # 2. SEMANTIC SKILL MATCH
    for need in needs:
        for exp_skill in SKILL_GROUPS.get(need, []):
            for skill in p_skills:
                if exp_skill == skill:
                    if skill not in matched_skills:
                        score += 25
                        matched_skills.add(skill)
                        reasons.append(f"'{skill}' fits need '{need}'")

    # 3. DOMAIN MATCH — tiered
    domain_matched = False
    if domain:
        for pd in p_domains:
            if domain == pd:
                score += 35
                reasons.append(f"exact domain match: '{pd}'")
                domain_matched = True
                break
            elif domain in pd or pd in domain:
                score += 20
                reasons.append(f"domain '{pd}' closely matches '{domain}'")
                domain_matched = True
                break
        if not domain_matched:
            for syn in DOMAIN_SYNONYMS.get(domain, []):
                for pd in p_domains:
                    if syn == pd or syn in pd:
                        score += 8
                        reasons.append(f"domain '{pd}' loosely relates to '{domain}'")
                        domain_matched = True
                        break
                if domain_matched:
                    break

    # 4. TAG SIGNALS
    for need in needs:
        for tag in p_tags:
            if need == tag:
                score += 12
                reasons.append(f"tag '{tag}' exactly matches '{need}'")
            elif need in tag.split("-"):
                score += 5
                reasons.append(f"tag '{tag}' partially relates to '{need}'")

    # 5. EXPERIENCE TEXT RELEVANCE
    problem_text = (structured.get("problem") or "").lower()
    keywords = set(re.findall(r"\b\w{4,}\b", problem_text + " " + domain + " " + goal))
    keywords.update(needs)
    keywords.update(DOMAIN_KEYWORDS.get(domain, []))

    scored_entries = set()
    for i, exp_entry in enumerate(p_exp_list):
        exp_lower = exp_entry.lower()
        for kw in keywords:
            if kw in exp_lower and i not in scored_entries:
                score += 8
                scored_entries.add(i)
                reasons.append(f"experience mentions '{kw}'")
                break

    # 6. ROLE RELEVANCE
    for need in needs:
        need_words = set(need.split())
        role_words = set(p_role.split())
        if need_words.issubset(role_words):
            score += 15
            reasons.append(f"role '{p_role}' covers '{need}'")
        elif need_words & role_words and len(need_words) > 1:
            score += 5
            reasons.append(f"role '{p_role}' partially covers '{need}'")

    # 7. AVAILABILITY × URGENCY
    if urgency == "high" and avail_score >= 10:
        score += 15
        reasons.append("high availability matches high urgency")
    elif urgency == "high" and avail_score >= 6:
        score += 8
        reasons.append("medium availability for urgent request")
    elif urgency == "medium" and avail_score >= 10:
        score += 8
        reasons.append("high availability suits medium urgency")
    else:
        score += avail_score

    # 8. EXPERIENCE DEPTH
    score += exp_score * 2
    if exp_score > 0:
        reasons.append(f"{exp_score} experience entries")

    # 9. STAGE FIT
    if stage in ["mvp", "idea"] and "startup" in p_domains:
        score += 8
        reasons.append("startup experience fits early stage")
    if stage == "scaling" and any(t in p_tags for t in ["scalability", "infra", "backend"]):
        score += 12
        reasons.append("scaling stage — infra experience valuable")

    # 10. GOAL RELEVANCE
    if goal:
        goal_keywords = set(re.findall(r"\b\w{4,}\b", goal))
        for i, exp_entry in enumerate(p_exp_list):
            if i in scored_entries:
                continue
            for kw in goal_keywords:
                if kw in exp_entry.lower():
                    score += 6
                    reasons.append(f"experience aligns with goal '{kw}'")
                    break

    return score, reasons


def find_matches(structured):
    people = list(people_col.find({}))
    debug("TOTAL PEOPLE IN DB", len(people))

    domain = (structured.get("domain") or "").lower().strip()
    direct = []
    supporting = []

    for p in people:
        score, reasons = score_person(p, structured)
        debug(f"SCORE: {p.get('name')}", f"{score} | {reasons}")
        if score <= 0:
            continue

        p_domains = normalize_list(p.get("domains"))
        is_direct = False

        if domain:
            if domain in p_domains:
                is_direct = True
            else:
                for syn in DOMAIN_SYNONYMS.get(domain, []):
                    if any(syn == pd for pd in p_domains):
                        is_direct = True
                        break

        entry = {"person": p, "score": score, "reasons": reasons}
        if is_direct:
            direct.append(entry)
        else:
            supporting.append(entry)

    direct.sort(key=lambda x: x["score"], reverse=True)
    supporting.sort(key=lambda x: x["score"], reverse=True)

    debug("DIRECT MATCHES", [(m["person"]["name"], m["score"]) for m in direct[:5]])
    debug("SUPPORTING MATCHES", [(m["person"]["name"], m["score"]) for m in supporting[:5]])

    return direct[:5], supporting[:5]