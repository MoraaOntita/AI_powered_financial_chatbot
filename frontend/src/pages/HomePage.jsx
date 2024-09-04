// src/pages/HomePage.jsx
import React from 'react';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import Sidebar from '../components/layout/Sidebar';
import ChatbotIcon from '../components/chatbot/ChatbotIcon';
import '../assets/css/main.css'; // Importing the main CSS for global styles

const HomePage = () => {
    return (
        <div className="main-layout">
            <Header />
            <Sidebar />
            <div className="main-layout__content-container">
                <main className="main-layout__main-content">
                    <h1>Welcome to the BCG Chatbot!</h1>
                    <p>I'm here to assist you with financial questions about Microsoft, Tesla, and Apple.</p>
                </main>
            </div>
            <Footer />
            <ChatbotIcon />
        </div>
    );
};

export default HomePage;
