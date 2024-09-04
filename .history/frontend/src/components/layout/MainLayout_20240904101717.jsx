import React from 'react';
import Header from './Header';
import Footer from './Footer';
import Sidebar from './Sidebar';
import ChatbotIcon from '../chatbot/ChatbotIcon';
import './MainLayout.css';

const MainLayout = ({ children }) => {
    return (
        <div className="main-layout">
            <Header />
            <div className="content-container">
                <Sidebar />
                <main className="main-content">
                    {children}
                </main>
            </div>
            <Footer />
            <ChatbotIcon />
        </div>
    );
};

export default MainLayout;
