// src/pages/ContactPage.jsx
import React from 'react';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import Sidebar from '../components/layout/Sidebar';
import '../assets/css/main.css'; // Importing the main CSS for global styles

const ContactPage = () => {
    return (
        <div className="main-layout">
            <Header />
            <Sidebar />
            <div className="main-layout__content-container">
                <main className="main-layout__main-content">
                    <h1>Contact Us</h1>
                    <p>Get in touch with us for any inquiries or support.</p>
                </main>
            </div>
            <Footer />
        </div>
    );
};

export default ContactPage;
