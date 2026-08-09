import { useEffect, useMemo, useState } from "react";
import "./Dashboard.css";

const API_URL = "https://ai-interview-agent-s4da.onrender.com";

const ACTIVE_SESSION_KEY = "interviewSessionId";
const COMPLETED_SESSION_KEY = "completedInterviewSessionId";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // =====================================================
  // LOAD DASHBOARD
  // =====================================================

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError("");

      const sessionId =
        localStorage.getItem(COMPLETED_SESSION_KEY) ||
        localStorage.getItem(ACTIVE_SESSION_KEY);

      if (!sessionId) {
        setError(
          "No interview session found. Please complete an interview first."
        );
        return;
      }

      console.log(
        "Loading dashboard for session:",
        sessionId
      );

      const response = await fetch(
        `${API_URL}/api/candidate/dashboard/${sessionId}`
      );

      if (!response.ok) {
        throw new Error(
          `Backend error: ${response.status}`
        );
      }

      const data = await response.json();

      console.log("Dashboard data:", data);

      if (!data.success) {
        throw new Error(
          data.message || "Unable to load dashboard."
        );
      }

      setDashboard(data);

    } catch (err) {
      console.error(
        "Dashboard loading error:",
        err
      );

      setError(
        err.message ||
          "Unable to load interview dashboard."
      );

    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // CALCULATE TOPIC PERFORMANCE
  // =====================================================

  const topicPerformance = useMemo(() => {
    if (!dashboard?.questions) {
      return [];
    }

    const topicMap = {};

    dashboard.questions.forEach((item) => {
      const topic =
        item.evaluation?.topic ||
        item.topic ||
        `Day ${item.day}`;

      const score =
        Number(item.score) || 0;

      if (!topicMap[topic]) {
        topicMap[topic] = {
          topic,
          total: 0,
          count: 0,
        };
      }

      topicMap[topic].total += score;
      topicMap[topic].count += 1;
    });

    return Object.values(topicMap).map(
      (item) => ({
        topic: item.topic,
        score:
          item.count > 0
            ? Math.round(
                item.total / item.count
              )
            : 0,
      })
    );
  }, [dashboard]);

  // =====================================================
  // SCORE LABEL
  // =====================================================

  const getScoreLabel = (score) => {
    if (score >= 80) return "Excellent";
    if (score >= 60) return "Good";
    if (score >= 40) return "Needs Improvement";
    return "Needs Practice";
  };

  // =====================================================
  // SCORE CLASS
  // =====================================================

  const getScoreClass = (score) => {
    if (score >= 80) return "excellent";
    if (score >= 60) return "good";
    if (score >= 40) return "average";
    return "low";
  };

  // =====================================================
  // LOADING SCREEN
  // =====================================================

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-loading">

          <div className="loading-spinner">
            ✦
          </div>

          <h2>
            Loading your dashboard...
          </h2>

          <p>
            Preparing your interview performance report.
          </p>

        </div>
      </div>
    );
  }

  // =====================================================
  // ERROR
  // =====================================================

  if (error) {
    return (
      <div className="dashboard-page">

        <header className="dashboard-header">

          <div className="dashboard-brand">

            <div className="brand-icon">
              ✦
            </div>

            <div>
              <h2>
                AI Interview Agent
              </h2>

              <span>
                Candidate Dashboard
              </span>
            </div>

          </div>

        </header>

        <main className="dashboard-container">

          <div className="dashboard-error">

            <div className="error-icon">
              ⚠️
            </div>

            <h2>
              Unable to load dashboard
            </h2>

            <p>
              {error}
            </p>

            <button
              onClick={loadDashboard}
              className="retry-button"
            >
              Try Again
            </button>

          </div>

        </main>

      </div>
    );
  }

  // =====================================================
  // DATA
  // =====================================================

  const candidateName =
    dashboard?.candidate_name ||
    "Candidate";

  const averageScore =
    Number(dashboard?.average_score) || 0;

  const finalScore =
    Number(dashboard?.final_score) || 0;

  const totalQuestions =
    Number(dashboard?.total_questions) || 0;

  const completed =
    dashboard?.completed;

  const status =
    dashboard?.status || "Completed";

  const questions =
    dashboard?.questions || [];

  // =====================================================
  // MAIN DASHBOARD
  // =====================================================

  return (
    <div className="dashboard-page">

      {/* =================================================
          HEADER
      ================================================= */}

      <header className="dashboard-header">

        <div className="dashboard-brand">

          <div className="brand-icon">
            ✦
          </div>

          <div>
            <h2>
              AI Interview Agent
            </h2>

            <span>
              Candidate Dashboard
            </span>
          </div>

        </div>

        <div className="dashboard-status">

          <span className="status-dot"></span>

          {status}

        </div>

      </header>

      {/* =================================================
          CONTENT
      ================================================= */}

      <main className="dashboard-container">

        {/* =================================================
            WELCOME
        ================================================= */}

        <section className="dashboard-welcome">

          <div>

            <span className="welcome-label">
              INTERVIEW PERFORMANCE
            </span>

            <h1>
              Welcome, {candidateName}
            </h1>

            <p>
              Review your interview performance,
              strengths, and areas for improvement.
            </p>

          </div>

          <button
            className="refresh-button"
            onClick={loadDashboard}
          >
            ↻ Refresh
          </button>

        </section>

        {/* =================================================
            SUMMARY CARDS
        ================================================= */}

        <section className="dashboard-stats">

          {/* TOTAL QUESTIONS */}

          <div className="stat-card">

            <div className="stat-icon">
              ◉
            </div>

            <div>

              <span>
                Total Questions
              </span>

              <strong>
                {totalQuestions}
              </strong>

            </div>

          </div>

          {/* AVERAGE */}

          <div className="stat-card">

            <div className="stat-icon">
              ★
            </div>

            <div>

              <span>
                Average Score
              </span>

              <strong>
                {averageScore}/100
              </strong>

            </div>

          </div>

          {/* FINAL SCORE */}

          <div className="stat-card">

            <div className="stat-icon">
              ◆
            </div>

            <div>

              <span>
                Final Score
              </span>

              <strong>
                {finalScore}/100
              </strong>

            </div>

          </div>

          {/* STATUS */}

          <div className="stat-card">

            <div className="stat-icon">
              ✓
            </div>

            <div>

              <span>
                Status
              </span>

              <strong>
                {completed
                  ? "Completed"
                  : "In Progress"}
              </strong>

            </div>

          </div>

        </section>

        {/* =================================================
            PERFORMANCE OVERVIEW
        ================================================= */}

        <section className="performance-section">

          <div className="section-heading">

            <div>

              <span>
                OVERALL PERFORMANCE
              </span>

              <h2>
                Interview Score
              </h2>

            </div>

            <div
              className={`score-badge ${getScoreClass(
                finalScore
              )}`}
            >
              {getScoreLabel(finalScore)}
            </div>

          </div>

          <div className="score-overview">

            <div className="score-circle">

              <div>

                <strong>
                  {finalScore}
                </strong>

                <span>
                  /100
                </span>

              </div>

            </div>

            <div className="score-details">

              <h3>
                {getScoreLabel(finalScore)}
              </h3>

              <p>
                Your final score is based on the
                evaluation of your technical answers,
                relevance, depth, objectives, and
                practical understanding.
              </p>

              <div className="score-progress">

                <div
                  style={{
                    width: `${Math.min(
                      finalScore,
                      100
                    )}%`,
                  }}
                />

              </div>

              <span>
                {finalScore}% overall performance
              </span>

            </div>

          </div>

        </section>

        {/* =================================================
            TOPIC PERFORMANCE
        ================================================= */}

        <section className="performance-section">

          <div className="section-heading">

            <div>

              <span>
                TOPIC ANALYSIS
              </span>

              <h2>
                Performance by Topic
              </h2>

            </div>

          </div>

          {topicPerformance.length > 0 ? (

            <div className="topic-grid">

              {topicPerformance.map(
                (item, index) => {

                  const score =
                    Math.min(
                      Math.max(
                        Number(item.score) || 0,
                        0
                      ),
                      100
                    );

                  return (
                    <div
                      className="topic-card"
                      key={index}
                    >

                      <div className="topic-card-top">

                        <div>

                          <span>
                            TOPIC {String(
                              index + 1
                            ).padStart(2, "0")}
                          </span>

                          <h3>
                            {item.topic}
                          </h3>

                        </div>

                        <strong>
                          {score}
                        </strong>

                      </div>

                      <div className="topic-progress">

                        <div
                          className={getScoreClass(
                            score
                          )}
                          style={{
                            width:
                              `${score}%`,
                          }}
                        />

                      </div>

                      <div className="topic-card-bottom">

                        <span>
                          {score}/100
                        </span>

                        <span>
                          {getScoreLabel(score)}
                        </span>

                      </div>

                    </div>
                  );
                }
              )}

            </div>

          ) : (

            <div className="empty-state">
              No topic performance available.
            </div>

          )}

        </section>

        {/* =================================================
            INTERVIEW HISTORY
        ================================================= */}

        <section className="performance-section">

          <div className="section-heading">

            <div>

              <span>
                INTERVIEW HISTORY
              </span>

              <h2>
                Your Questions & Answers
              </h2>

            </div>

          </div>

          {questions.length > 0 ? (

            <div className="history-list">

              {questions.map(
                (item, index) => {

                  const score =
                    Math.min(
                      Math.max(
                        Number(item.score) || 0,
                        0
                      ),
                      100
                    );

                  return (
                    <article
                      className="history-card"
                      key={index}
                    >

                      {/* QUESTION HEADER */}

                      <div className="history-top">

                        <div className="history-number">

                          QUESTION{" "}
                          {String(
                            item.question_number ||
                              index + 1
                          ).padStart(2, "0")}

                        </div>

                        <div className="history-day">

                          Day {item.day}

                        </div>

                        <div
                          className={`history-score ${getScoreClass(
                            score
                          )}`}
                        >
                          {score}/100
                        </div>

                      </div>

                      {/* QUESTION */}

                      <div className="history-question">

                        <h3>
                          {item.question}
                        </h3>

                      </div>

                      {/* ANSWER */}

                      <div className="history-answer">

                        <span>
                          YOUR ANSWER
                        </span>

                        <p>
                          {item.answer ||
                            "No answer provided."}
                        </p>

                      </div>

                      {/* EVALUATION */}

                      {item.evaluation && (
                        <div className="history-evaluation">

                          <div className="evaluation-title">

                            <span>
                              AI EVALUATION
                            </span>

                            <strong>
                              Score: {score}/100
                            </strong>

                          </div>

                          {item.evaluation
                            .strengths
                            ?.length > 0 && (

                            <div className="evaluation-group">

                              <h4>
                                ✓ Strengths
                              </h4>

                              {item.evaluation.strengths.map(
                                (
                                  strength,
                                  strengthIndex
                                ) => (

                                  <p
                                    key={
                                      strengthIndex
                                    }
                                  >
                                    ✓ {strength}
                                  </p>

                                )
                              )}

                            </div>

                          )}

                          {item.evaluation
                            .gaps
                            ?.length > 0 && (

                            <div className="evaluation-group">

                              <h4>
                                Areas to improve
                              </h4>

                              {item.evaluation.gaps.map(
                                (
                                  gap,
                                  gapIndex
                                ) => (

                                  <p
                                    key={
                                      gapIndex
                                    }
                                  >
                                    • {gap}
                                  </p>

                                )
                              )}

                            </div>

                          )}

                        </div>
                      )}

                    </article>
                  );
                }
              )}

            </div>

          ) : (

            <div className="empty-state">
              No interview history available.
            </div>

          )}

        </section>

        {/* =================================================
            SESSION INFORMATION
        ================================================= */}

        <section className="session-card">

          <div>

            <span>
              SESSION ID
            </span>

            <strong>
              {dashboard?.session_id}
            </strong>

          </div>

          <div className="session-complete">

            <span className="status-dot"></span>

            Interview Saved Successfully

          </div>

        </section>

      </main>

    </div>
  );
}

export default Dashboard;