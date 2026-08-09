# =====================================================
# AI INTERVIEW ENGINE
# =====================================================

def get_score(evaluation):
    """
    Safely extract the evaluation score.
    """

    if not isinstance(evaluation, dict):
        return 0

    score = evaluation.get("score", 0)

    try:
        return float(score)
    except (TypeError, ValueError):
        return 0


def generate_adaptive_question(topic, evaluation):
    """
    Generate the next question based on
    the candidate's previous answer quality.
    """

    title = topic.get(
        "title",
        "this topic",
    )

    score = get_score(evaluation)

    # ---------------------------------------------
    # Strong answer
    # ---------------------------------------------

    if score >= 80:

        return (
            f"Good explanation. Let's go deeper into {title}. "
            f"Can you explain a challenging real-world problem "
            f"you could solve using {title}, and how you would "
            f"design the solution?"
        )

    # ---------------------------------------------
    # Moderate answer
    # ---------------------------------------------

    if score >= 50:

        return (
            f"Let's explore {title} further. "
            f"Can you explain how you would apply {title} "
            f"in a practical project and what challenges "
            f"you might face?"
        )

    # ---------------------------------------------
    # Weak answer
    # ---------------------------------------------

    return (
        f"Let's revisit {title}. "
        f"Can you explain the basic concepts of "
        f"{title} and give a simple example?"
    )


def generate_next_question(
    current_topic,
    evaluation,
    next_topic=None,
):
    """
    Decide whether to ask an adaptive follow-up
    or move to the next interview topic.
    """

    score = get_score(evaluation)

    # Strong or moderate answer:
    # move to the next planned topic.
    if next_topic is not None:

        return {
            "question": None,
            "move_to_next_topic": True,
            "reason": (
                "Candidate demonstrated sufficient "
                f"understanding with score {score}."
            ),
        }

    # No next topic:
    # generate an adaptive follow-up.
    question = generate_adaptive_question(
        current_topic,
        evaluation,
    )

    return {
        "question": question,
        "move_to_next_topic": False,
        "reason": (
            f"No next topic available. "
            f"Adaptive follow-up generated from score {score}."
        ),
    }