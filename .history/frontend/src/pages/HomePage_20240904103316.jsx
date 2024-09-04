import React, { useState } from 'react';
import { postQuestion } from '../utils/api';
import { validateQuestion } from '../utils/validators';
import { formatCurrency } from '../utils/formatters';

const HomePage = () => {
    const [question, setQuestion] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = async () => {
        if (validateQuestion(question)) {
            try {
                const data = await postQuestion(question);
                setResponse(data.answer);
            } catch (error) {
                setResponse('An error occurred while fetching the response.');
            }
        } else {
            setResponse('Please enter a valid question.');
        }
    };

    return (
        <div>
            <textarea 
                value={question} 
                onChange={(e) => setQuestion(e.target.value)} 
                placeholder="Ask me something..."
            />
            <button onClick={handleSubmit}>Send</button>
            <p>{response}</p>
        </div>
    );
};

export default HomePage;
