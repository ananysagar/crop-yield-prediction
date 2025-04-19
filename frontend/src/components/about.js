import React from "react";
import "./about.css";

function About() {
  return (
    <div className="about-container">
      <div className="about-card">
        <h1>About Agriculture Crop Prediction</h1>

        <section className="about-section">
          <h2>Our Mission</h2>
          <p>
            We aim to help farmers make better decisions through data-driven
            predictions and insights.
          </p>
        </section>

        <section className="about-section">
          <h2>What We Do</h2>
          <p>
            Our platform uses advanced algorithms to predict crop yields and
            provide personalized recommendations based on various factors
            including:
          </p>
          <ul>
            <li>Soil conditions</li>
            <li>Weather patterns</li>
            <li>Historical data</li>
            <li>Local agricultural practices</li>
          </ul>
        </section>

        <section className="about-section">
          <h2>Why Choose Us</h2>
          <div className="features">
            <div className="feature-card">
              <h3>Accurate Predictions</h3>
              <p>
                Using advanced machine learning algorithms for precise results
              </p>
            </div>
            <div className="feature-card">
              <h3>Easy to Use</h3>
              <p>Simple interface designed for farmers</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default About;
