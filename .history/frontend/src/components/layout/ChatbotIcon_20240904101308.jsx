import React, { useState } from 'react';
import './ChatbotIcon.css';
import ChatWindow from './ChatWindow'; // Import the chat window component

const ChatbotIcon = () => {
    const [isChatOpen, setIsChatOpen] = useState(false);

    const toggleChatWindow = () => {
        setIsChatOpen(!isChatOpen);
    };

    return (
        <>
            <div className="chatbot-icon" onClick={toggleChatWindow}>
                {/* Insert your chatbot icon here */}
                <img src="/path-to-your-chatbot-icon.png" alt="Chatbot Icon" />
            </div>
            {isChatOpen && <ChatWindow />}
        </>
    );
};

export default ChatbotIcon;
