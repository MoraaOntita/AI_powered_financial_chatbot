import React from 'react';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <img 
                src="/assets/images/backrounds/footer-background.jpeg" 
                alt="Footer Background" 
                className="footer-background" 
            />
            <p className="footer-text">© 2024 Boston Consulting Group. All rights reserved.</p>
        </footer>
    );
}

export default Footer;
