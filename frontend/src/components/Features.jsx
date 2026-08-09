import "./Features.css";
import FeatureCard from "./FeatureCard";

function Features() {

  const features = [
    {
      icon: "✦",
      title: "Personalized Questions",
      description:
        "Questions are generated based on the candidate's skills, curriculum, and technical background."
    },
    {
      icon: "◈",
      title: "AI Answer Evaluation",
      description:
        "Every answer is evaluated for relevance, technical depth, strengths, and knowledge gaps."
    },
    {
      icon: "⌁",
      title: "RAG Powered",
      description:
        "Relevant knowledge is retrieved from the knowledge base to improve answer evaluation."
    },
    {
      icon: "◎",
      title: "Smart Feedback",
      description:
        "Get actionable feedback and identify the technical areas you need to improve."
    }
  ];

  return (
    <section className="features-section" id="features">

      <div className="section-heading">

        <div className="section-badge">
          ✦ INTELLIGENT INTERVIEWING
        </div>

        <h2>
          Everything you need to
          <span> ace your interview.</span>
        </h2>

        <p>
          An AI-powered interview experience designed
          to help you practice, improve, and perform better.
        </p>

      </div>

      <div className="features-grid">

        {features.map((feature, index) => (
          <FeatureCard
            key={index}
            icon={feature.icon}
            title={feature.title}
            description={feature.description}
          />
        ))}

      </div>

    </section>
  );
}

export default Features;