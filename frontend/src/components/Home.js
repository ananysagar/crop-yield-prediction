import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

const Home = () => {
  return (
    <div className="home-hero">
      <div className="home-container">
        <div className="overlay">
          <h1 className="hero-title">Maximize Your Farm's Potential</h1>
          <p className="hero-subtitle">
            Predict the best crops for your land based on your environmental
            data.
          </p>
          <div className="hero-buttons">
            <Link to="/login" className="hero-button1">
              Get Started
            </Link>
            <Link to="/" className="hero-button2">
              Learn More
            </Link>
          </div>
        </div>
        <div className="hero-image">
          <img
            src="/heroImage.png"
            alt="hero-image"
            className="home-image"
            width={450}
            height={500}
          />
        </div>
      </div>
    </div>
  );
};

export default Home;
