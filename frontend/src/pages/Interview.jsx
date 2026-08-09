import { useEffect, useRef, useState } from "react";
import "./Interview.css";

const API_URL = "http://127.0.0.1:8000";
const TOTAL_QUESTIONS = 8;

const ACTIVE_SESSION_KEY = "interviewSessionId";
const COMPLETED_SESSION_KEY = "completedInterviewSessionId";

function Interview() {
  const [answer, setAnswer] = useState("");
  const [question, setQuestion] = useState("");
  const [questionNumber, setQuestionNumber] = useState(1);

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const [done, setDone] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const [error, setError] = useState("");

  const interviewStarted = useRef(false);

  // =====================================================
  // ALWAYS CREATE A NEW INTERVIEW SESSION
  // =====================================================

  const [sessionId] = useState(() => {
    const newSessionId = `react-interview-${Date.now()}`;

    // Remove old session information
    localStorage.removeItem(ACTIVE_SESSION_KEY);
    localStorage.removeItem(COMPLETED_SESSION_KEY);

    // Save new session
    localStorage.setItem(
      ACTIVE_SESSION_KEY,
      newSessionId
    );

    console.log(
      "Created NEW interview session:",
      newSessionId
    );

    return newSessionId;
  });

  // =====================================================
  // START INTERVIEW
  // =====================================================

  useEffect(() => {
    if (interviewStarted.current) {
      return;
    }

    interviewStarted.current = true;

    startInterview();
  }, []);

  // =====================================================
  // START INTERVIEW REQUEST
  // =====================================================

  const startInterview = async () => {
    try {
      setLoading(true);
      setError("");

      console.log(
        "Starting interview:",
        sessionId
      );

      const response = await fetch(
        `${API_URL}/api/interview`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            sessionId: sessionId,
            candidate: null,
            message: null,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Backend error: ${response.status}`
        );
      }

      const data = await response.json();

      console.log(
        "Interview started:",
        data
      );

      const realSessionId =
        data.session_id ||
        data.sessionId ||
        sessionId;

      localStorage.setItem(
        ACTIVE_SESSION_KEY,
        realSessionId
      );

      setQuestion(
        data.reply || ""
      );

      setDone(
        Boolean(data.done)
      );

      if (data.feedback) {
        setFeedback(
          data.feedback
        );
      }

    } catch (err) {
      console.error(
        "Interview start error:",
        err
      );

      setError(
        "Unable to connect to the interview server. Please make sure FastAPI is running on port 8000."
      );

    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // SUBMIT ANSWER
  // =====================================================

  const submitAnswer = async () => {
    if (
      !answer.trim() ||
      submitting ||
      done
    ) {
      return;
    }

    try {
      setSubmitting(true);
      setError("");

      const currentAnswer =
        answer.trim();

      const currentSessionId =
        localStorage.getItem(
          ACTIVE_SESSION_KEY
        ) || sessionId;

      console.log(
        "Submitting answer:",
        currentAnswer
      );

      console.log(
        "Session:",
        currentSessionId
      );

      const response = await fetch(
        `${API_URL}/api/interview`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            sessionId:
              currentSessionId,

            candidate: null,

            message:
              currentAnswer,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Backend error: ${response.status}`
        );
      }

      const data =
        await response.json();

      console.log(
        "Backend response:",
        data
      );

      const realSessionId =
        data.session_id ||
        data.sessionId ||
        currentSessionId;

      localStorage.setItem(
        ACTIVE_SESSION_KEY,
        realSessionId
      );

      // Clear answer box
      setAnswer("");

      // =================================================
      // INTERVIEW COMPLETED
      // =================================================

      if (data.done) {
        console.log(
          "Interview completed."
        );

        localStorage.setItem(
          COMPLETED_SESSION_KEY,
          realSessionId
        );

        localStorage.setItem(
          ACTIVE_SESSION_KEY,
          realSessionId
        );

        setDone(true);

        setFeedback(
          data.feedback || null
        );

        return;
      }

      // =================================================
      // NEXT QUESTION
      // =================================================

      setQuestion(
        data.reply || ""
      );

      setQuestionNumber(
        previous =>
          Math.min(
            previous + 1,
            TOTAL_QUESTIONS
          )
      );

    } catch (err) {
      console.error(
        "Answer submission error:",
        err
      );

      setError(
        "Unable to submit your answer. Please check that the FastAPI server is running."
      );

    } finally {
      setSubmitting(false);
    }
  };

  // =====================================================
  // KEYBOARD SHORTCUT
  // =====================================================

  const handleKeyDown = event => {
    if (
      event.ctrlKey &&
      event.key === "Enter"
    ) {
      event.preventDefault();

      submitAnswer();
    }
  };

  // =====================================================
  // COMPLETED SCREEN
  // =====================================================

  if (done) {
    const completedSession =
      localStorage.getItem(
        COMPLETED_SESSION_KEY
      ) ||
      localStorage.getItem(
        ACTIVE_SESSION_KEY
      ) ||
      sessionId;

    return (
      <div className="interview-page">

        <header className="interview-header">

          <div className="interview-brand">

            <div className="brand-icon">
              ✦
            </div>

            <div>
              <h2>
                AI Interview Agent
              </h2>

              <span>
                Interview Completed
              </span>
            </div>

          </div>

          <div className="interview-status">

            <span className="status-dot"></span>

            Completed

          </div>

        </header>

        <main className="interview-container">

          <section className="question-card">

            <div className="question-top">

              <span className="question-number">
                INTERVIEW COMPLETE
              </span>

              <span className="topic-badge">
                ✓ Completed
              </span>

            </div>

            <h1>
              Great job! Your interview is complete.
            </h1>

            <div className="feedback-summary">

              <p>
                Your interview has been saved successfully.
              </p>

              <p>
                Session ID:
                <strong>
                  {" "}
                  {completedSession}
                </strong>
              </p>

            </div>

            {feedback && (
              <div className="feedback-summary">

                <p>
                  {feedback.summary ||
                    "Interview evaluation completed."}
                </p>

              </div>
            )}

          </section>

          {feedback && (
            <>

              {/* STRENGTHS */}

              <section className="answer-section">

                <div className="answer-header">

                  <div>

                    <h3>
                      Your Strengths
                    </h3>

                    <span>
                      Areas where you performed well
                    </span>

                  </div>

                </div>

                <div className="feedback-list">

                  {feedback.strengths?.length > 0 ? (

                    feedback.strengths.map(
                      (strength, index) => (

                        <div
                          className="feedback-item strength"
                          key={index}
                        >
                          ✓ {strength}
                        </div>

                      )
                    )

                  ) : (

                    <div className="feedback-item">
                      No strengths identified.
                    </div>

                  )}

                </div>

              </section>

              {/* GAPS */}

              <section className="answer-section">

                <div className="answer-header">

                  <div>

                    <h3>
                      Areas to Improve
                    </h3>

                    <span>
                      Topics that need more practice
                    </span>

                  </div>

                </div>

                <div className="feedback-list">

                  {feedback.gaps?.length > 0 ? (

                    feedback.gaps.map(
                      (gap, index) => (

                        <div
                          className="feedback-item gap"
                          key={index}
                        >
                          • {gap}
                        </div>

                      )
                    )

                  ) : (

                    <div className="feedback-item">
                      No major gaps identified.
                    </div>

                  )}

                </div>

              </section>

              {/* NEXT STEPS */}

              {feedback.next?.length > 0 && (

                <section className="answer-section">

                  <div className="answer-header">

                    <div>

                      <h3>
                        Next Steps
                      </h3>

                      <span>
                        Recommended preparation
                      </span>

                    </div>

                  </div>

                  <div className="feedback-list">

                    {feedback.next.map(
                      (item, index) => (

                        <div
                          className="feedback-item"
                          key={index}
                        >
                          → {item}
                        </div>

                      )
                    )}

                  </div>

                </section>

              )}

              {/* TOPIC PERFORMANCE */}

              {feedback.topic_feedback?.length > 0 && (

                <section className="answer-section">

                  <div className="answer-header">

                    <div>

                      <h3>
                        Topic Performance
                      </h3>

                      <span>
                        Your performance by topic
                      </span>

                    </div>

                  </div>

                  <div className="topic-feedback-grid">

                    {feedback.topic_feedback.map(
                      (topic, index) => {

                        const score =
                          Math.min(
                            Math.max(
                              Number(
                                topic.score
                              ) || 0,
                              0
                            ),
                            100
                          );

                        return (
                          <div
                            className="topic-result"
                            key={index}
                          >

                            <div className="topic-result-top">

                              <strong>
                                {topic.topic}
                              </strong>

                              <span>
                                {score}/100
                              </span>

                            </div>

                            <div className="topic-result-bar">

                              <div
                                style={{
                                  width:
                                    `${score}%`,
                                }}
                              />

                            </div>

                          </div>
                        );
                      }
                    )}

                  </div>

                </section>

              )}

            </>
          )}

        </main>

      </div>
    );
  }

  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {
    return (
      <div className="interview-page">

        <div className="loading-screen">

          <div className="loading-orb">
            ✦
          </div>

          <h2>
            Preparing your interview...
          </h2>

          <p>
            AI is creating your personalized questions.
          </p>

        </div>

      </div>
    );
  }

  // =====================================================
  // MAIN INTERVIEW
  // =====================================================

  return (
    <div className="interview-page">

      <header className="interview-header">

        <div className="interview-brand">

          <div className="brand-icon">
            ✦
          </div>

          <div>

            <h2>
              AI Interview Agent
            </h2>

            <span>
              Technical Interview Session
            </span>

          </div>

        </div>

        <div className="interview-status">

          <span className="status-dot"></span>

          AI Interviewer Online

        </div>

      </header>

      <main className="interview-container">

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {/* PROGRESS */}

        <div className="interview-progress">

          <div>

            <span>
              INTERVIEW PROGRESS
            </span>

            <strong>
              Question {questionNumber} of{" "}
              {TOTAL_QUESTIONS}
            </strong>

          </div>

          <div className="progress-percentage">

            {Math.round(
              Math.min(
                (questionNumber /
                  TOTAL_QUESTIONS) *
                  100,
                100
              )
            )}
            %

          </div>

        </div>

        <div className="progress-track">

          <div
            className="progress-value"
            style={{
              width:
                `${Math.min(
                  (questionNumber /
                    TOTAL_QUESTIONS) *
                    100,
                  100
                )}%`,
            }}
          />

        </div>

        {/* QUESTION */}

        <section className="question-card">

          <div className="question-top">

            <span className="question-number">

              QUESTION{" "}

              {String(
                questionNumber
              ).padStart(2, "0")}

            </span>

            <span className="topic-badge">
              AI Interview
            </span>

          </div>

          <h1>
            {question}
          </h1>

          <p className="question-hint">

            Take your time and explain your approach
            clearly. You can include examples from
            projects you have worked on.

          </p>

        </section>

        {/* ANSWER */}

        <section className="answer-section">

          <div className="answer-header">

            <div>

              <h3>
                Your Answer
              </h3>

              <span>
                Explain your approach in your own words.
              </span>

            </div>

            <span className="answer-count">
              {answer.length} characters
            </span>

          </div>

          <textarea
            value={answer}
            onChange={event =>
              setAnswer(
                event.target.value
              )
            }
            onKeyDown={handleKeyDown}
            placeholder="Start typing your answer here..."
            disabled={submitting}
          />

          <div className="answer-footer">

            <span>

              💡 Tip: Include concepts, tools,
              and a practical example.

              <br />

              Press Ctrl + Enter to submit.

            </span>

            <button
              className="submit-button"
              disabled={
                !answer.trim() ||
                submitting
              }
              onClick={submitAnswer}
            >

              {submitting
                ? "Evaluating..."
                : "Submit Answer"}

              <span>
                →
              </span>

            </button>

          </div>

        </section>

        {/* AI ASSISTANT */}

        <div className="ai-assistant">

          <div className="assistant-icon">
            ✦
          </div>

          <div>

            <strong>
              AI Interviewer
            </strong>

            <p>
              Your answer will be evaluated for relevance,
              technical depth, and practical understanding.
            </p>

          </div>

          <div className="assistant-wave">

            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>

          </div>

        </div>

      </main>

    </div>
  );
}

export default Interview;