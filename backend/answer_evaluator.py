
import re


# =====================================================
# TEXT NORMALIZATION
# =====================================================

def normalize_text(text):
    if not text:
        return set()

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s-]",
        " ",
        text
    )

    stop_words = {
        "the", "a", "an", "and", "or", "to", "of",
        "in", "on", "for", "with", "is", "are", "was",
        "were", "this", "that", "it", "from", "using",
        "use", "used", "would", "can", "i", "my",
        "be", "as", "by", "into", "their", "they",
        "then", "also", "such", "how", "what",
        "where", "when", "which", "than"
    }

    return {
        word
        for word in text.split()
        if len(word) > 2
        and word not in stop_words
    }


# =====================================================
# CONCEPT ALIASES
# =====================================================

CONCEPT_ALIASES = {

    "python": {
        "python",
        "programming",
        "coding",
        "code",
        "script",
        "program",
        "syntax",
        "function",
        "class",
        "exception",
        "module"
    },

    "machine learning": {
        "machine learning",
        "machine",
        "learning",
        "ml",
        "supervised",
        "unsupervised",
        "model",
        "training",
        "prediction",
        "classification",
        "regression",
        "clustering",
        "features",
        "dataset",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "rmse"
    },

    "nlp": {
        "nlp",
        "natural language",
        "language",
        "text",
        "textual",
        "tokenization",
        "tokens",
        "tfidf",
        "tf-idf",
        "embeddings",
        "embedding",
        "sentiment",
        "preprocessing",
        "stopword",
        "stop-word",
        "corpus",
        "transformer"
    },

    "react": {
        "react",
        "frontend",
        "component",
        "components",
        "ui",
        "interface",
        "jsx",
        "state",
        "props"
    },

    "fastapi": {
        "fastapi",
        "api",
        "backend",
        "endpoint",
        "rest",
        "server",
        "request",
        "response"
    },

    "git": {
        "git",
        "repository",
        "commit",
        "branch",
        "version",
        "control",
        "merge"
    },

    "github": {
        "github",
        "repository",
        "repo",
        "push",
        "publish",
        "remote"
    },

    "vite": {
        "vite",
        "frontend",
        "build",
        "development",
        "server"
    },

    "ollama": {
        "ollama",
        "local",
        "llm",
        "model",
        "ai",
        "assistant"
    },

    "pandas": {
        "pandas",
        "dataframe",
        "csv",
        "data",
        "processing",
        "cleaning",
        "missing",
        "columns"
    },

    "numpy": {
        "numpy",
        "array",
        "numerical",
        "computation",
        "matrix"
    },

    "scikit-learn": {
        "scikit",
        "sklearn",
        "classification",
        "regression",
        "training",
        "evaluation",
        "model",
        "machine",
        "learning"
    },

    "prompt engineering": {
        "prompt",
        "prompts",
        "prompting",
        "instruction",
        "instructions",
        "zero-shot",
        "few-shot",
        "chain-of-thought",
        "system prompt",
        "system prompts",
        "llm",
        "language model",
        "context",
        "role",
        "output format"
    },

    "docker": {
        "docker",
        "container",
        "containers",
        "image",
        "dockerfile",
        "containerization"
    },

    "kubernetes": {
        "kubernetes",
        "k8s",
        "cluster",
        "pod",
        "deployment",
        "service",
        "container"
    },

    "embeddings": {
        "embedding",
        "embeddings",
        "vector",
        "vectors",
        "semantic",
        "similarity",
        "sentence",
        "transformer"
    }
}


# =====================================================
# CONCEPT MATCHING
# =====================================================

def concept_matches(answer_words, text):

    text_lower = str(text).lower()

    matched_concepts = set()

    for concept, aliases in CONCEPT_ALIASES.items():

        for alias in aliases:

            if " " in alias:

                if alias in text_lower:
                    matched_concepts.add(concept)
                    break

            elif alias in answer_words:

                matched_concepts.add(concept)
                break

    return matched_concepts


# =====================================================
# TOPIC CONCEPTS
# =====================================================

def get_topic_concepts(title):

    title_lower = str(title).lower()

    concepts = set()

    for concept, aliases in CONCEPT_ALIASES.items():

        if concept in title_lower:

            concepts.add(concept)
            continue

        for alias in aliases:

            if alias in title_lower:

                concepts.add(concept)
                break

    return concepts


# =====================================================
# OBJECTIVE MATCHING
# =====================================================

def objective_match(
    answer_words,
    answer_text,
    objective,
    topic_title
):

    objective_words = normalize_text(
        objective
    )

    if not objective_words:
        return False

    matches = answer_words.intersection(
        objective_words
    )

    word_coverage = (
        len(matches) / len(objective_words)
    )

    topic_concepts = get_topic_concepts(
        topic_title
    )

    answer_concepts = concept_matches(
        answer_words,
        answer_text
    )

    objective_concepts = concept_matches(
        objective_words,
        objective
    )

    objective_concepts = (
        objective_concepts.intersection(
            topic_concepts
        )
    )

    answer_concepts = (
        answer_concepts.intersection(
            topic_concepts
        )
    )

    concept_overlap = (
        objective_concepts.intersection(
            answer_concepts
        )
    )

    if concept_overlap:
        return True

    if word_coverage >= 0.20:
        return True

    return False


# =====================================================
# TOOL MATCHING
# =====================================================

def tool_matches(
    answer_words,
    answer_text,
    tools
):

    matched_tools = []

    answer_lower = str(answer_text).lower()

    for tool in tools:

        tool_lower = str(tool).lower()

        if tool_lower in answer_lower:

            matched_tools.append(tool)
            continue

        tool_words = normalize_text(
            tool
        )

        if not tool_words:
            continue

        if tool_words.intersection(
            answer_words
        ):

            matched_tools.append(tool)

    return matched_tools


# =====================================================
# ANSWER DEPTH
# =====================================================

def calculate_depth_score(
    answer_words,
    answer_text
):

    word_count = len(answer_words)

    if word_count < 3:
        return 0.0

    if word_count < 8:
        return 0.2

    if word_count < 15:
        return 0.4

    if word_count < 25:
        return 0.6

    if word_count < 40:
        return 0.75

    if word_count < 60:
        return 0.85

    if word_count < 80:
        return 0.92

    return 1.0


# =====================================================
# RAG RELEVANCE
# =====================================================

def calculate_rag_score(
    answer_words,
    answer_text,
    context_text
):

    if not context_text:
        return 0.0, set()

    rag_words = normalize_text(
        context_text
    )

    if not rag_words:
        return 0.0, set()

    overlap = answer_words.intersection(
        rag_words
    )

    if not overlap:
        return 0.0, set()

    overlap_ratio = (
        len(overlap)
        / max(
            len(answer_words),
            1
        )
    )

    context_coverage = (
        len(overlap)
        / max(
            len(rag_words),
            1
        )
    )

    # Weighted RAG relevance.
    # Candidate answer should share meaningful
    # knowledge with the retrieved context.
    rag_score = (
        overlap_ratio * 0.7
        + min(context_coverage * 3, 1.0) * 0.3
    )

    return (
        min(rag_score, 1.0),
        overlap
    )


# =====================================================
# EVALUATE ANSWER
# =====================================================

def evaluate_answer(
    answer,
    topic,
    context=None
):

    if context is None:
        context = []

    # -------------------------------------------------
    # RAG CONTEXT
    # -------------------------------------------------

    if isinstance(context, list):

        context_text = " ".join(
            str(item)
            for item in context
        )

    else:

        context_text = str(context)

    # -------------------------------------------------
    # EMPTY ANSWER
    # -------------------------------------------------

    if not answer or not str(answer).strip():

        objectives = topic.get(
            "objectives",
            []
        )

        return {
            "score": 0,
            "strengths": [],
            "gaps": objectives,
            "matched_objectives": [],
            "missed_objectives": objectives,
            "matched_tools": [],
            "rag_score": 0,
            "rag_supported": False
        }

    # -------------------------------------------------
    # BASIC DATA
    # -------------------------------------------------

    answer_text = str(answer).strip()

    answer_words = normalize_text(
        answer_text
    )

    title = topic.get(
        "title",
        ""
    )

    tools = topic.get(
        "tools",
        []
    )

    objectives = topic.get(
        "objectives",
        []
    )

    # =================================================
    # VERY SHORT ANSWER
    # =================================================

    if len(answer_words) < 3:

        return {
            "score": 0,
            "strengths": [],
            "gaps": [
                f"Could explain: {objective}"
                for objective in objectives[:3]
            ],
            "matched_objectives": [],
            "missed_objectives": objectives,
            "matched_tools": [],
            "rag_score": 0,
            "rag_supported": False
        }

    # =================================================
    # TOPIC RELEVANCE
    # =================================================

    title_words = normalize_text(
        title
    )

    title_matches = (
        answer_words.intersection(
            title_words
        )
    )

    topic_concepts = get_topic_concepts(
        title
    )

    answer_concepts = concept_matches(
        answer_words,
        answer_text
    )

    concept_relevance = (
        topic_concepts.intersection(
            answer_concepts
        )
    )

    relevance_score = 1 if (
        title_matches
        or concept_relevance
    ) else 0

    # =================================================
    # OBJECTIVE MATCHING
    # =================================================

    matched_objectives = []

    missed_objectives = []

    for objective in objectives:

        matched = objective_match(
            answer_words,
            answer_text,
            objective,
            title
        )

        if matched:

            matched_objectives.append(
                objective
            )

        else:

            missed_objectives.append(
                objective
            )

    # =================================================
    # OBJECTIVE SCORE
    # =================================================

    if objectives:

        objective_score = (
            len(matched_objectives)
            / len(objectives)
        )

    else:

        objective_score = 0

    # =================================================
    # TOOL MATCHING
    # =================================================

    matched_tools = tool_matches(
        answer_words,
        answer_text,
        tools
    )

    if tools:

        tool_score = (
            len(matched_tools)
            / len(tools)
        )

    else:

        tool_score = 0

    # =================================================
    # ANSWER DEPTH
    # =================================================

    depth_score = calculate_depth_score(
        answer_words,
        answer_text
    )

    # =================================================
    # RAG SCORE
    # =================================================

    rag_score, rag_overlap = (
        calculate_rag_score(
            answer_words,
            answer_text,
            context_text
        )
    )

    rag_relevant = rag_score > 0

    # =================================================
    # COMPLETELY IRRELEVANT ANSWER
    # =================================================

    if relevance_score == 0:

        final_score = min(
            10,
            round(
                objective_score * 10
                + depth_score * 5
                + rag_score * 5,
                2
            )
        )

        return {

            "score": final_score,

            "strengths": [],

            "gaps": [
                f"Answer does not address {title}."
            ]
            + [
                f"Could explain: {objective}"
                for objective in missed_objectives[:2]
            ],

            "matched_objectives":
                matched_objectives,

            "missed_objectives":
                missed_objectives,

            "matched_tools":
                matched_tools,

            "rag_score":
                round(rag_score, 3),

            "rag_supported":
                rag_relevant
        }

    # =================================================
    # FINAL SCORE
    # =================================================
    #
    # Objective coverage = 50%
    # Topic relevance   = 15%
    # Tool knowledge    = 10%
    # Answer depth      = 15%
    # RAG alignment     = 10%
    #
    # Total = 100
    # =================================================

    final_score = (

        objective_score * 50

        + relevance_score * 15

        + tool_score * 10

        + depth_score * 15

        + rag_score * 10
    )

    final_score = round(
        min(
            final_score,
            100
        ),
        2
    )

    # =================================================
    # STRENGTHS
    # =================================================

    strengths = []

    if relevance_score:

        strengths.append(
            f"Answer is relevant to {title}."
        )

    if matched_objectives:

        strengths.append(
            f"Covered {len(matched_objectives)} "
            f"of {len(objectives)} "
            f"curriculum objectives."
        )

    if matched_tools:

        strengths.append(
            "Mentioned relevant tools: "
            + ", ".join(
                matched_tools[:5]
            )
        )

    if depth_score >= 0.85:

        strengths.append(
            "Provided a detailed explanation."
        )

    elif depth_score >= 0.6:

        strengths.append(
            "Provided a reasonably detailed explanation."
        )

    if rag_relevant:

        strengths.append(
            "Answer aligns with the retrieved "
            "knowledge context."
        )

    # =================================================
    # GAPS
    # =================================================

    gaps = []

    for objective in missed_objectives[:3]:

        gaps.append(
            f"Could explain: {objective}"
        )

    # =================================================
    # RAG GAP
    # =================================================

    if context_text and not rag_relevant:

        gaps.append(
            "Answer did not sufficiently align "
            "with the retrieved knowledge context."
        )

    # =================================================
    # FINAL RESULT
    # =================================================

    return {

        "score": final_score,

        "strengths": strengths,

        "gaps": gaps,

        "matched_objectives":
            matched_objectives,

        "missed_objectives":
            missed_objectives,

        "matched_tools":
            matched_tools,

        "rag_score":
            round(rag_score, 3),

        "rag_supported":
            rag_relevant,

        "rag_overlap_terms":
            sorted(list(rag_overlap))[:20]
    }

