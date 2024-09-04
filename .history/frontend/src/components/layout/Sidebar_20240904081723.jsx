import React from 'react';
import './Sidebar.css';
import { FaRobot, FaChartLine } from 'react-icons/fa';

const Sidebar = () => {
    return (
        <aside className="sidebar">
            <div className="sidebar-item">
                <FaRobot className="sidebar-icon" />
                <p>Chatbot</p>
            </div>
            <div className="sidebar-item">
                <FaChartLine className="sidebar-icon" />
                <p>Financial Insights</p>
            </div>
        </aside>
    );
}

export default Sidebar;
