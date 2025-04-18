import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

const Home = () => {
  return (
    <div className="home-container">
      <nav className="navbar">
        <div className="navbar-brand">Crop Yield Prediction</div>
        <div className="navbar-links">
          <Link to="/login" className="nav-link">
            Login
          </Link>
          <Link to="/register" className="nav-link">
            Signup
          </Link>
        </div>
      </nav>
      <div className="home-content">
        <h1>Welcome to Crop Yield Prediction</h1>
        <p>Predict the best crops for your land and maximize your yield.</p>
      </div>
    </div>
  );
};

export default Home;
