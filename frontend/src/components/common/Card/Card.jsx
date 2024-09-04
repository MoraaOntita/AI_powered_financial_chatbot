import React from 'react';
import './Card.css';

const Card = ({ title, content, footer }) => (
    <div className="card">
        <div className="card-header">
            <h2>{title}</h2>
        </div>
        <div className="card-content">
            {content}
        </div>
        {footer && <div className="card-footer">{footer}</div>}
    </div>
);

export default Card;
