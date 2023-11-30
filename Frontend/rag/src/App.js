import React from 'react';
import './style.css'; 
import Chatbot from './chatbot';

function App() {
  return (
    <div className="App">
      <h1>The Culinary Coach-</h1><h5>A Resource Augmented Generation Application for Home Chefs</h5>
      <div className='container'><Chatbot /></div>
    </div>
  );
}

export default App;