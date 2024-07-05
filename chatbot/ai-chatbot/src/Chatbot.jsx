import React, { useState } from 'react';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    const sendMessage = async () => {
        try {
            console.log("Sending message:", input);
            const response = await fetch("http://localhost:8000/chatbot/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: input })
            });

            const data = await response.json();
            console.log("Received response:", data);

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
        <div>
            <div>
                {messages.map((msg, index) => (
                    <div key={index} className={msg.from === "user" ? "user-message" : "bot-message"}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <input 
                value={input} 
                onChange={(e) => setInput(e.target.value)} 
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()} 
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default Chatbot;
