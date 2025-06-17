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
  const [cropDetails, setCropDetails] = useState(null);

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
    setCropDetails(null);

    try {
      const response = await api.predictCrop(formData);
      if (response.error) {
        setError(response.error);
      } else {
        setPrediction(response);
        // After getting prediction, fetch details for both crops
        const fetchCropInfo = async (cropName) => {
          try {
            const cropInfo = await fetch(
              `http://localhost:5000/api/crop-info/${cropName.toLowerCase()}`,
              {
                credentials: "include",
              }
            );
            const cropData = await cropInfo.json();
            if (!cropData.error) {
              return cropData.content;
            }
            return null;
          } catch (err) {
            console.log(`Could not load details for ${cropName}:`, err);
            return null;
          }
        };

        // Fetch both crop details
        const fetchBothCrops = async () => {
          const mainCropInfo = await fetchCropInfo(response.prediction);
          const altCropInfo =
            response.prediction1 !== "N/A"
              ? await fetchCropInfo(response.prediction1)
              : null;

          setCropDetails({
            main: mainCropInfo,
            alternative: altCropInfo,
          });
        };

        fetchBothCrops();
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
            <div className="result-grid">
              <div className="result-card">
                <h4>Primary Crop</h4>
                <p>
                  <strong>Crop:</strong> {prediction.prediction}
                </p>
                {prediction.price && (
                  <p>
                    <strong>Estimated Price:</strong> ₹{prediction.price}
                  </p>
                )}
              </div>

              <div className="result-card">
                <h4>Alternative Crop</h4>
                <p>
                  <strong>Crop:</strong> {prediction.prediction1}
                </p>
                {prediction.price1 && prediction.prediction1 !== "N/A" && (
                  <p>
                    <strong>Estimated Price:</strong> ₹{prediction.price1}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {cropDetails && (
          <div className="crop-info-section">
            {cropDetails.main && (
              <div className="crop-card">
                <h3>🌱 Primary Crop Information - {prediction.prediction}</h3>
                <div
                  className="crop-content"
                  dangerouslySetInnerHTML={{ __html: cropDetails.main }}
                />
              </div>
            )}

            {cropDetails.alternative && prediction.prediction1 !== "N/A" && (
              <div className="crop-card">
                <h3>
                  🌿 Alternative Crop Information - {prediction.prediction1}
                </h3>
                <div
                  className="crop-content"
                  dangerouslySetInnerHTML={{ __html: cropDetails.alternative }}
                />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default CropPrediction;
