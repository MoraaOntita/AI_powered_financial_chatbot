// src/pages/AboutPage.jsx
import React from 'react';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import Sidebar from '../components/layout/Sidebar';
import '../assets/css/main.css'; // Importing the main CSS for global styles

const AboutPage = () => {
    return (
        <div className="main-layout">
            <Header />
            <Sidebar />
            <div className="main-layout__content-container">
                <main className="main-layout__main-content">
                    <h1>About Us</h1>
                    <p>Learn more about the BCG Chatbot and our mission.</p>
                </main>
            </div>
            <Footer />
        </div>
    );
};

export default AboutPage;
