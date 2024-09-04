import React from 'react';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import Sidebar from '../components/layout/Sidebar';
import ChatbotIcon from '../components/chatbot/ChatbotIcon';  // Import ChatbotIcon

const MainLayout = ({ children }) => {
    return (
        <div className="main-layout">
            <Header />
            <Sidebar />
            <div className="content">
                {children}
            </div>
            <ChatbotIcon />  {/* Add ChatbotIcon here */}
            <Footer />
        </div>
    );
};

export default MainLayout;
