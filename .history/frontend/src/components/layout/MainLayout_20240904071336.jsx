import React from 'react';
import Header from './Header';
import Footer from './Footer';
import Sidebar from './Sidebar';
import './MainLayout.css';

const MainLayout = ({ children }) => (
    <div className="main-layout">
        <Header />
        <div className="main-content">
            <Sidebar />
            <div className="content-area">
                {children}
            </div>
        </div>
        <Footer />
    </div>
);

export default MainLayout;
