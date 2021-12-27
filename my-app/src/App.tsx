import React from 'react';
import pythonImage from './pythonImage.png';
import fireImage from './fireImage.png';
import './App.css';
import {Link} from "react-router-dom";

const App = () => {
    return (
        <div className="App">
            <header className="App-header">
                <img src={pythonImage} className="App-logo" alt="logo"/>
                <p>Memory Consumption and Runtime Tracker for Python
                </p>
                <Link to="/Analysis" className="link">FlameGraph</Link>
                <Link to="/LargestConsumption" className="link">Top 10 Memory consuming frames!<img src={fireImage} className="Fire-logo" alt="logo"/></Link>

            </header>
        </div>


    );
}


export default App;
