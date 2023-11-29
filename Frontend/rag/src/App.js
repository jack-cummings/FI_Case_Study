import React from 'react';
import './style.css'; 
import Chatbot from './chatbot';

function App() {
  return (
    <div className="App">
      <h1>The Coulinary Coach-</h1><h5>A Resource Augment Generation Application for home chefs</h5>
      <div className='container'><Chatbot /></div>
    </div>
  );
}

export default App;