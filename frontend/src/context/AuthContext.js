import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await api.getUser();
                if (response.username) {
                    setUser(response);
                }
            } catch (error) {
                console.error('Auth check failed:', error);
            } finally {
                setLoading(false);
            }
        };
        checkAuth();
    }, []);

    const login = async (username, password) => {
        try {
            const response = await api.login(username, password);
            if (response.message === 'Login successful') {
                setUser({ username: response.username });
                return { success: true };
            }
            return { success: false, error: response.error };
        } catch (error) {
            return { success: false, error: 'Login failed' };
        }
    };

    const register = async (userData) => {
        try {
            const response = await api.register(userData);
            if (response.message === 'User registered successfully') {
                return { success: true };
            }
            return { success: false, error: response.error };
        } catch (error) {
            return { success: false, error: 'Registration failed' };
        }
    };

    const logout = async () => {
        try {
            await api.logout();
            setUser(null);
            return { success: true };
        } catch (error) {
            return { success: false, error: 'Logout failed' };
        }
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}; 