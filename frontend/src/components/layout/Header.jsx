import React from 'react';
import './Header.css';

const Header = () => (
    <header className="header">
        <div className="logo">
            <img src="/assets/images/bcg-logo.png" alt="BCG Logo" />
        </div>
        <nav className="nav">
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
        </nav>
    </header>
);

export default Header;
