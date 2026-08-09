import "./Hero.css";
import { useNavigate } from "react-router-dom";

function Hero() {
  const navigate = useNavigate();

  return (
    <section className="hero" id="home">

      {/* Background glow */}
      <div className="hero-glow glow-one"></div>
      <div className="hero-glow glow-two"></div>

      <div className="hero-container">

        {/* Left side */}
        <div className="hero-content">

          <div className="hero-badge">
            <span className="pulse-dot"></span>
            AI-POWERED TECHNICAL INTERVIEW PLATFORM
          </div>

          <h1>
            Your next interview
            <br />

            <span className="gradient-text">
              starts here.
            </span>
          </h1>

          <p className="hero-description">
            Practice technical interviews with an intelligent AI
            interviewer that creates personalized questions,
            evaluates your answers, and gives actionable feedback.
          </p>

          <div className="hero-buttons">

            {/* START INTERVIEW BUTTON */}
            <button
              className="primary-button"
              onClick={() => navigate("/interview")}
            >
              <span>🚀</span>
              Start Interview
              <span>→</span>
            </button>

            {/* EXPLORE FEATURES BUTTON */}
            <button
              className="secondary-button"
              onClick={() =>
                document
                  .getElementById("features")
                  ?.scrollIntoView({
                    behavior: "smooth",
                  })
              }
            >
              Explore Features
              <span>↓</span>
            </button>

          </div>

          <div className="hero-trust">

            <div className="trust-avatars">
              <span>AI</span>
              <span>ML</span>
              <span>RAG</span>
            </div>

            <p>
              Personalized • Intelligent • AI Powered
            </p>

          </div>

        </div>

        {/* Right side - Interview Preview */}
        <div className="hero-visual">

          <div className="floating-card card-top">

            <span className="floating-icon">
              ✦
            </span>

            <div>
              <strong>AI Evaluation</strong>
              <small>Answer analyzed</small>
            </div>

            <span className="check">
              ✓
            </span>

          </div>

          <div className="interview-window">

            <div className="window-header">

              <div className="window-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>

              <div className="window-title">
                AI Interview Session
              </div>

              <div className="live">
                <span></span>
                LIVE
              </div>

            </div>

            <div className="window-body">

              <div className="question-label">
                QUESTION 01
              </div>

              <h3>
                Explain how you would design
                a scalable RAG system.
              </h3>

              <div className="topic-tag">
                <span>✦</span>
                Generative AI
              </div>

              <div className="progress-section">

                <div className="progress-info">
                  <span>Interview Progress</span>
                  <span>1 / 8</span>
                </div>

                <div className="progress-bar">
                  <div></div>
                </div>

              </div>

              <div className="ai-status">

                <div className="ai-orb">
                  ✦
                </div>

                <div>
                  <strong>AI Interviewer</strong>
                  <p>
                    Listening to your response...
                  </p>
                </div>

                <div className="sound-bars">
                  <span></span>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

              </div>

            </div>

          </div>

          <div className="floating-card card-bottom">

            <div className="score-circle">
              92
            </div>

            <div>
              <strong>Strong Answer</strong>
              <small>AI confidence score</small>
            </div>

            <span className="sparkle">
              ✦
            </span>

          </div>

        </div>

      </div>

    </section>
  );
}

export default Hero;

