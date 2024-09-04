import React from 'react';
import './ChatWindow.css';

const ChatWindow = () => {
    return (
        <div className="chat-window">
            <div className="chat-header">
                <h2>BCG Chatbot</h2>
                {/* Add close button or any header content */}
            </div>
            <div className="chat-body">
                {/* Chat messages will go here */}
            </div>
            <div className="chat-footer">
                <textarea placeholder="Type your message..."></textarea>
                <button>Send</button>
            </div>
        </div>
    );
};

export default ChatWindow;
