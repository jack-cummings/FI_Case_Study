import React, { useState } from 'react';

const Chatbot = () => {
  const [messages, setMessages] = useState([{ text: 'Welcome! How can I help you?', isUser: false }]);
  const [input, setInput] = useState('');
  const [context_window, setContextWindow] = useState('Your Context will apear here, use the chat to continue!')
  const [documents, setDocuments] = useState('')
  // const [isLoading, setIsLoading] = useState(true);

  const callAPI = async (question_input) => {
    const apiUrl = 'http://0.0.0.0:4242/inference';
    const data = {'text': question_input};
    console.log(JSON.stringify(data))
  
    try {
      const response = await fetch(apiUrl, {method: 'POST',
                                            headers: {'Content-Type': 'application/json'},
                                            body: JSON.stringify(data)});
  
      if (!response.ok) {throw new Error('No 200');}
  
      const answerObj = await response.json();
      console.log('Response data:', answerObj);
      return answerObj
    } 
    
    catch (error) {
      console.error('Error in POST:', error);
    }}; // end call api


  const handleInput = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input) return;
    console.log(input)
    const answerObj = await callAPI(input)
    setMessages(
      [
      ...messages,
      { text: input, isUser: true },
      {text: answerObj.content, isUser:false},
    ]);
    console.log(answerObj.context)
    setContextWindow(answerObj.context)
    console.log(context_window)
    setInput('');
  };


  return (
    <div className="layout-container">
      <div className="chatbot">
        {/* Chatbot window */}
        <div className="chatbot-messages">
          {messages.map((msg, index) => (
            <div key={index} className={msg.isUser ? 'user-message' : 'bot-message'}>
              {msg.text}
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="chatbot-form">
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={handleInput}
          />
          <button type="submit">Send</button>
        </form>
      </div>

      <div className="middle-panel">
        <div className="scrollable-content">
          {/* {Array.from({ length: 50 }, (_, i) => (
            <p key={i}>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
              incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
              exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            </p>
          ))} */}
          <p>{context_window}</p>
        </div>
      </div>

      <div className="file-explorer">
        {/* Windows File Explorer-like view */}
        {/* Implement the file explorer content here */}
      </div>
    </div>
  );
};

export default Chatbot;


