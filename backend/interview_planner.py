def build_interview_plan(candidate_profile, relevant_days):
    """
    Build a personalized interview plan from
    the candidate's learning history.

    Each curriculum day appears only once.
    """

    high_attempt_days = {
        topic["day"]
        for topic in candidate_profile.get(
            "high_attempt_topics", []
        )
    }

    skipped_days = {
        topic["day"]
        for topic in candidate_profile.get(
            "skipped_topics", []
        )
    }

    priority_days = []

    # =====================================================
    # 1. HIGH PRIORITY - MULTIPLE ATTEMPTS
    # =====================================================

    for day in relevant_days:

        if day["day"] in high_attempt_days:

            priority_days.append({
                **day,
                "priority": "HIGH",
                "reason": "Multiple attempts required",
                "question_type": "conceptual"
            })

    # =====================================================
    # 2. HIGH PRIORITY - SKIPPED TOPICS
    # =====================================================

    for day in relevant_days:

        if (
            day["day"] in skipped_days
            and day["day"] not in high_attempt_days
        ):

            priority_days.append({
                **day,
                "priority": "HIGH",
                "reason": "Topic was skipped",
                "question_type": "conceptual"
            })

    # =====================================================
    # 3. NORMAL PRIORITY - OTHER TOPICS
    # =====================================================

    for day in relevant_days:

        if (
            day["day"] not in high_attempt_days
            and day["day"] not in skipped_days
        ):

            priority_days.append({
                **day,
                "priority": "NORMAL",
                "reason": "Completed topic",
                "question_type": "practical"
            })

    # =====================================================
    # 4. REMOVE DUPLICATE DAYS
    # =====================================================

    unique_days = {}

    for topic in priority_days:

        day_number = topic["day"]

        if day_number not in unique_days:
            unique_days[day_number] = topic

    # =====================================================
    # 5. RETURN FINAL PLAN
    # =====================================================

    return list(unique_days.values())