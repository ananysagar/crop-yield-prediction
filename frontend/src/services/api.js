const API_BASE_URL = 'http://localhost:5000/api';

const api = {
    // Auth endpoints
    login: async (username, password) => {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ username, password }),
        });
        return response.json();
    },

    register: async (userData) => {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(userData),
        });
        return response.json();
    },

    logout: async () => {
        const response = await fetch(`${API_BASE_URL}/logout`, {
            method: 'POST',
            credentials: 'include',
        });
        return response.json();
    },

    getUser: async () => {
        const response = await fetch(`${API_BASE_URL}/user`, {
            credentials: 'include',
        });
        return response.json();
    },

    // Crop prediction endpoint
    predictCrop: async (predictionData) => {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(predictionData),
        });
        return response.json();
    },
};

export default api; 