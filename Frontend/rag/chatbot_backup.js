import React, { useState, useRef, useEffect} from 'react';

const Chatbot = () => {
  const [messages, setMessages] = useState([{ text: 'Welcome! How can I help you?', isUser: false, isLoading: false }]);
  const [input, setInput] = useState('');
  const [context_window, setContextWindow] = useState('Your Context will apear here, use the chat to continue!')
  const [documents, setDocuments] = useState([])
  const [title, setTitle] = useState()
  const [focus_text, setFocusText] = useState('')
  const [isQuery, setIsQuery] = useState(false)

  // componets
  const RenderChatWindow = () => {
    const startRef = useRef(null);

    return (
      <div className="chatbot" >
      {/* Chatbot window */}
      <h1>Ask</h1>
      <p>Ask a question related to your coulinary needs</p>
      <div className="chatbot-messages-container">
        <div className="chatbot-messages">
        {messages.map((msg, index) => (
            <div key={index} className={msg.isUser ? 'user-message' : 'bot-message'}>
            {msg.isLoading === false ? (
                <div>{msg.text}</div>
            ) : (
              <div>
                <small>Retrieving Information</small>
               <div className="typing-animation">
                <span>.</span>
                <span>.</span>
                <span>.</span>
              </div>
            </div>
            )
            }
        </div>
          ))}
      </div>
      <form onSubmit={handleSubmit} className="chatbot-form">
        <textarea
          type="text"
          placeholder="Type your question here..."
          value={input}
          onChange={handleInput}
          ref={startRef}
        />
        <button type="submit">Send</button>
      </form>
      </div>
    </div>
    )
  }

  const RenderDocWindow = () => {
    return (
    <div className="middle-panel">
    <h1>Review</h1>
    <p>Review the relvent source doucmentation</p>
    <div className="context-window">
      <div>
        <h3>{title}</h3><br></br>
        <StyledSubstring
          full_text={context_window}
          substring= {focus_text}
          substringStyle={{fontWeight: 'bold', color: '#009688', backgroundColor: '#333'}}
          defaultStyle={{fontWeight: 'normal', color: 'white' }}
        />
      </div>
      {/* <iframe src="https://en.wikipedia.org/wiki/Boston_Red_Sox#:~:text=The%20Red%20Sox%20were%20a%20dominant%20team%20in%20the%20new%20league%2C"></iframe> */}
    </div>
  </div>
    );
  };

  const RenderFileWindow = () => {
    return (
    <div className="file-explorer">
    <h1>Revisit</h1>
    <p>Visit the documents you previosly viewd</p>
     <div className='file-explorer-container'>
        {documents.map((doc, index) => (
    <div className='container'><div><a href={doc.urls[0][0]} key={index} className='file-object'> {doc.urls[0][0]}</a></div></div>))}
    </div>
  </div>
    )
  }
  

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
      const doc_text = full_text[0]
      console.log('here')
      console.log(doc_text)
      raw = doc_text.split(substring)
      raw.splice(1,0,substring)
      console.log(raw)
      
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
    setInput('');
    setMessages([
      ...messages,
      { text: input, isUser: true, isLoading: false },
      { text: 'thinking', isUser: false, isLoading: true }
    ])
    const answerObj = await callAPI(input)
    setIsQuery(true)
    setMessages(
      [
      ...messages,
      { text: input, isUser: true, isLoading: false },
      {text: answerObj.content, isUser:false, isLoading: false},
    ]);
    setContextWindow(answerObj.full_text)
    setDocuments([
      ...documents,
      {urls:answerObj.urls}
    ])
    console.log(documents)
    setTitle(answerObj.urls);
    setFocusText(answerObj.context[0]);
  };

  const layoutContainerStyle = {
    justifyContent: isQuery ? 'space-between' : 'center',
  };

  return (
    <div className="layout-container" style={layoutContainerStyle}>
      <RenderChatWindow></RenderChatWindow>
      {isQuery && <RenderDocWindow></RenderDocWindow>}
      {isQuery && <RenderFileWindow></RenderFileWindow>}
    </div>
    
  );
};

export default Chatbot;


