import React from 'react';
import './Footer.css';

const Footer = () => (
    <footer className="footer">
        <p>&copy; 2024 BCG. All rights reserved.</p>
        <ul className="footer-links">
            <li><a href="/privacy">Privacy Policy</a></li>
            <li><a href="/terms">Terms of Service</a></li>
        </ul>
    </footer>
);

export default Footer;
