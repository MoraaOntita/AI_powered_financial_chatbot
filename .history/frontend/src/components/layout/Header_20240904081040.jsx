import React from 'react';
import './Header.css';

const Header = () => {
    return (
        <header className="header">
            <img 
                src="/assets/images/logos/BCG Logo.jpeg" 
                alt="BCG Logo" 
                className="header-logo" 
            />
            <h1 className="header-title">BCG Chatbot</h1>
        </header>
    );
}

export default Header;
