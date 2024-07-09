import React, { useState } from 'react';
import './Chatbot.css'; // Import the CSS file

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    const sendMessage = async () => {
        try {
            const response = await fetch("http://localhost:8000/chatbot/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: input })
            });

            const data = await response.json();

            if (data.response) {
                setMessages([...messages, { text: input, from: "user" }, { text: data.response, from: "bot" }]);
            } else {
                console.error("No response text found");
            }
            setInput("");
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    return (
        <div className="chat-container">
            <div className="message-box">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.from === "user" ? "user-message" : "bot-message"}`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <div className="input-container">
                <input 
                    value={input} 
                    onChange={(e) => setInput(e.target.value)} 
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()} 
                />
                <button onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
};

export default Chatbot;
