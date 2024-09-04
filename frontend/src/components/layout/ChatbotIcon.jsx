import React from 'react';
import './ChatbotIcon.css';
import chatbotIcon from '../../assets/images/icons/chatbot-icon.png';

const ChatbotIcon = () => {
    const openChat = () => {
        // Functionality to open the chatbot window
        console.log("Chatbot icon clicked!");
    };

    return (
        <div className="chatbot-icon" onClick={openChat}>
            <img src={chatbotIcon} alt="Chatbot" />
        </div>
    );
};

export default ChatbotIcon;
