import React from 'react';
import '../assets/Header.css'
import  sc  from '../assets/space.jpg'
const Welcome = () => {
    return (
        <div className="container">
          <header className="header">
            <h1>Welcome</h1>
          </header>
          <main className="main">
            <button className="center-btn">Click Me</button>
            <img src={sc} alt="Center Image" className="center-img"/>
          </main>
        </div>
      );
};
export default Welcome;

