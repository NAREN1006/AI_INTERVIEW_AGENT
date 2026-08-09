import "./HowItWorks.css";

function HowItWorks() {
  const steps = [
    {
      number: "01",
      title: "Build Your Profile",
      description:
        "Your skills, experience, and technical background are analyzed to create a personalized interview profile.",
      icon: "◉",
    },
    {
      number: "02",
      title: "Generate Interview",
      description:
        "The system creates interview questions based on your profile and the relevant curriculum topics.",
      icon: "✦",
    },
    {
      number: "03",
      title: "Answer & Evaluate",
      description:
        "Your answers are evaluated using AI with relevant knowledge retrieved from the RAG pipeline.",
      icon: "⌁",
    },
    {
      number: "04",
      title: "Get Smart Feedback",
      description:
        "Receive your score, strengths, knowledge gaps, and personalized recommendations for improvement.",
      icon: "◎",
    },
  ];

  return (
    <section className="how-section" id="how-it-works">

      <div className="how-heading">

        <div className="section-badge">
          ✦ HOW IT WORKS
        </div>

        <h2>
          From preparation to
          <span> performance.</span>
        </h2>

        <p>
          A complete AI-powered interview workflow
          designed around your technical profile.
        </p>

      </div>

      <div className="steps-container">

        {steps.map((step, index) => (
          <div className="step-wrapper" key={step.number}>

            <div className="step-card">

              <div className="step-top">

                <span className="step-number">
                  {step.number}
                </span>

                <div className="step-icon">
                  {step.icon}
                </div>

              </div>

              <h3>{step.title}</h3>

              <p>{step.description}</p>

            </div>

            {index < steps.length - 1 && (
              <div className="step-connector">
                →
              </div>
            )}

          </div>
        ))}

      </div>

    </section>
  );
}

export default HowItWorks;