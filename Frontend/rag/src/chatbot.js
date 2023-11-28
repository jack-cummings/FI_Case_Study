import React, { useState, useRef, useEffect} from 'react';

const Chatbot = () => {
  const [messages, setMessages] = useState([{ text: 'Welcome! How can I help you?', isUser: false }]);
  const [input, setInput] = useState('');
  const [context_window, setContextWindow] = useState('Your Context will apear here, use the chat to continue!')
  const [documents, setDocuments] = useState([])


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

  const StyledSubstring = ({full_text, substring, defaultStyle, substringStyle}) => {

    //  Opperating under the assumption that there is only occurance of substring (only highlights first)
    let raw 

    if (full_text === 'Your Context will apear here, use the chat to continue!') {
      raw = full_text.split(substring)
    }
    else {
      raw = full_text.split(substring)
      raw.splice(1,0,substring)
      console.log('hit')
      
    }

    // console.log(parts)
    console.log(substring)

    const substringRef = useRef(null);

    useEffect(() => {
      // Scroll to the substringRef on page load
      if (substringRef.current) {
        substringRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    }, []);

    return (
      <p>
        {raw.map((part, index) => (
          <span 
            key={index} 
            ref={part === substring ? substringRef : null}
            style={part === substring ? substringStyle : defaultStyle}>
            {part} 
            </span>
          ))}
        </p>
      );
    };


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
    setContextWindow(answerObj.context)
    // const focus_text = 'A taco'
    // // const ProcessedContext = await processContext(focus_text,answerObj.context)
    // const ProcessedContext = await HighlightedSubstring(answerObj.context,focus_text)
    // setContextWindow(ProcessedContext)
    setDocuments([
      ...documents,
      {urls:answerObj.url}
    ])
    setInput('');
  };


  return (
    <div className="layout-container">
      <div className="chatbot">
        {/* Chatbot window */}
        <h1>Chatbot</h1>
        <div className="chatbot-messages">
          {messages.map((msg, index) => (
            <div key={index} className={msg.isUser ? 'user-message' : 'bot-message'}>
              {msg.text}
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="chatbot-form">
          <textarea
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={handleInput}
          />
          <button type="submit">Send</button>
        </form>
      </div>

      <div className="middle-panel">
        <h1>Context Window</h1>
        <div className="context-window">
          {/* <p>{context_window}</p> */}
          <div>
            <h1>Styled Substring</h1>
            <StyledSubstring
              full_text={context_window}
              substring= 'These instances predate the theory that the first mention of the word "taco" in Mexico was in the 1891 novel Los bandidos de Río Frío by Manuel Payno.'
              substringStyle={{ fontWeight: 'bold', color: '#009688' }}
              defaultStyle={{ fontWeight: 'normal', color: 'white' }}
            />
          </div>

        </div>
      </div>

      <div className="file-explorer">
        <h1>Document History</h1>
      {documents.map((doc, index) => (
      <div className='container'><div><a href={doc.urls} key={index} className='file-object'> {doc.urls}</a></div></div>))}
      </div>

      
    </div>
  );
};

export default Chatbot;


