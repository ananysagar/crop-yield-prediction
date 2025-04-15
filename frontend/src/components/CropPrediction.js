import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";
import "./CropPrediction.css"; // Make sure CSS is imported

const CropPrediction = () => {
  const [formData, setFormData] = useState({
    location: "",
    soil_type: "",
    area: "",
  });
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  // const [cropDetails, setCropDetails] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    //setCropDetails(null);

    try {
      const response = await api.predictCrop(formData);
      if (response.error) {
        setError(response.error);
      } else {
        setPrediction(response);
        // After getting prediction, fetch crop details
        // if (response.prediction) {
        //     try {
        //         const cropInfo = await fetch(`/templates/${response.prediction.toLowerCase()}.html`);
        //         const cropText = await cropInfo.text();
        //         setCropDetails(cropText);
        //     } catch (err) {
        //         console.log('Could not load crop details');
        //     }
        // }
      }
    } catch (err) {
      setError("Failed to get prediction. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-container">
      <div className="prediction-form">
        <h2>Crop Prediction</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="location">Location</label>
            <select
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              required
            >
              <option value="">Select Location</option>
              <option value="Mangalore">Mangalore</option>
              <option value="Kodagu">Kodagu</option>
              <option value="kasaragodu">Kasargod</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="soilType">Soil Type</label>
            <select
              id="soilType"
              name="soil_type"
              value={formData.soil_type}
              onChange={handleChange}
              required
            >
              <option value="">Select Soil Type</option>
              <option value="Coastal alluvials">Coastal alluvials</option>
              <option value="Laterite soil">Laterite soil</option>
              <option value="Dark brown alayey soil">
                Dark brown alayey soil
              </option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="area">Area (in acres)</label>
            <input
              type="number"
              id="area"
              name="area"
              value={formData.area}
              onChange={handleChange}
              required
              placeholder="Enter area in acres"
              min="1"
            />
          </div>
          <button type="submit" className="predict-button" disabled={loading}>
            {loading ? "Predicting..." : "Predict Crop"}
          </button>
        </form>

        {prediction && (
          <div className="prediction-result">
            <h3>Prediction Results</h3>
            <div className="result-item">
              <span className="label">Recommended Crop:</span>
              <span className="value">{prediction.prediction}</span>
            </div>
            {prediction.price && (
              <div className="result-item">
                <span className="label">Estimated Price:</span>
                <span className="value">₹{prediction.price}</span>
              </div>
            )}
            <div className="result-item">
              <span className="label">Alternative Crop:</span>
              <span className="value">{prediction.prediction1}</span>
            </div>
            {prediction.price1 && (
              <div className="result-item">
                <span className="label">Alternative Estimated Price:</span>
                <span className="value">₹{prediction.price1}</span>
              </div>
            )}
          </div>
        )}

        {/* {cropDetails && (
                    <div className="crop-details">
                        <h3>Crop Information</h3>
                        <div dangerouslySetInnerHTML={{ __html: cropDetails }} />
                    </div>
                )} */}
      </div>
    </div>
  );
};

export default CropPrediction;
