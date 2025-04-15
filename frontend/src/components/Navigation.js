import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navigation = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        const result = await logout();
        if (result.success) {
            navigate('/login');
        }
    };

    return (
        <nav className="navigation">
            <div className="nav-container">
                <Link to="/" className="nav-brand">
                    Crop Prediction
                </Link>
                <div className="nav-links">
                    {user ? (
                        <>
                            <Link to="/dashboard" className="nav-link">
                                Dashboard
                            </Link>
                            <Link to="/predict" className="nav-link">
                                Predict
                            </Link>
                            <button onClick={handleLogout} className="nav-button">
                                Logout
                            </button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="nav-link">
                                Login
                            </Link>
                            <Link to="/register" className="nav-link">
                                Register
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navigation; 