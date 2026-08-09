def build_curriculum_map(curriculum):
    curriculum_map = {}

    for day in curriculum["days"]:
        curriculum_map[day["day"]] = {
            "day": day["day"],
            "title": day["title"],
            "type": day.get("type"),
            "tools": day.get("tools", []),
            "objectives": day.get("objectives", [])
        }

    return curriculum_map


def get_relevant_curriculum_days(candidate_profile, curriculum):
    curriculum_map = build_curriculum_map(curriculum)

    selected_days = []

    # Passed topics
    for mission in candidate_profile["passed_topics"]:
        day = mission["day"]

        if day in curriculum_map:
            selected_days.append({
                **curriculum_map[day],
                "candidate_status": "passed",
                "attempts": mission.get("attempts", 1)
            })

    # Skipped topics
    for mission in candidate_profile["skipped_topics"]:
        day = mission["day"]

        if day in curriculum_map:
            selected_days.append({
                **curriculum_map[day],
                "candidate_status": "skipped",
                "attempts": 0
            })

    return selected_days