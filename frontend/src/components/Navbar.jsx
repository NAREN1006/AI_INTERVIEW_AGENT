import "./Navbar.css";
import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  return (
    <nav className="navbar">
      <div className="navbar-container">

        {/* Logo */}
        <div className="brand">
          <div className="brand-icon">✦</div>

          <div>
            <div className="brand-name">InterviewAI</div>
            <div className="brand-subtitle">
              Intelligent Interview Platform
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
          <a href="#Dashboard"></a>


          {/* Dashboard */}
          <button
            className="nav-link-button"
            onClick={() => navigate("/dashboard")}
          >
            Dashboard
          </button>
        </div>

        {/* Button */}
        <button
          className="nav-button"
          onClick={() => navigate("/interview")}
        >
          Start Interview
          <span>→</span>
        </button>

      </div>
    </nav>
  );
}

export default Navbar;