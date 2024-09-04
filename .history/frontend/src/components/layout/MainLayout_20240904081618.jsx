import React from 'react';
import './MainLayout.css';
import Header from '../common/Header';
import Footer from '../common/Footer';
import Sidebar from '../common/Sidebar';

const MainLayout = ({ children }) => {
    return (
        <div className="main-layout">
            <Header />
            <div className="content-area">
                <Sidebar />
                <main className="main-content">
                    {children}
                </main>
            </div>
            <Footer />
        </div>
    );
}

export default MainLayout;
