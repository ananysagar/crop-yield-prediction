import React from "react";
import "./Dashboard.css";
import { Link } from "react-router-dom";

function Dashboard() {
  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Welcome to the Dashboard</h1>
      <div className="dashboard-card">
        <h2 className="section-title">Quick Actions</h2>
        <div className="action-cards">
          <div className="action-card">
            <h3>Predict Crops</h3>
            <p>Get predictions for your crop yield</p>
            <Link to="/predict" className="action-button">
              Start Prediction
            </Link>
          </div>
          <div className="action-card">
            <h3>View Services</h3>
            <p>Check our available services</p>
            <button className="action-button">View Services</button>
          </div>
          <div className="action-card">
            <h3>Learn More</h3>
            <p>Learn about our platform</p>
            <Link to="/about" className="action-button">
              About Us
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
