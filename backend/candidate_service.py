def build_candidate_profile(candidate):
    """
    Build a candidate profile from the candidate JSON data.
    """

    member = candidate.get("member", candidate)
    missions = candidate.get("missions", [])
    signals = candidate.get("signals", {})

    passed = []
    failed = []
    skipped = []
    high_attempt_topics = []

    for mission in missions:

        if mission.get("skipped") is True:
            skipped.append(mission)
            continue

        if mission.get("passed") is True:
            passed.append(mission)

        elif mission.get("passed") is False:
            failed.append(mission)

        attempts = mission.get("attempts", 0)

        if attempts >= 3:
            high_attempt_topics.append(mission)

    return {
        "candidate": member,
        "passed_topics": passed,
        "failed_topics": failed,
        "skipped_topics": skipped,
        "high_attempt_topics": high_attempt_topics,
        "signals": signals,
    }