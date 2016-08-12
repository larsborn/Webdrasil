import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import DirListing from './DirListing'

class App extends Component {
    render() {
        return (
            <div className="App">
                <div className="App-header">
                    <img src={logo} className="App-logo" alt="logo"/>
                    <h2>Webdrasil</h2>
                </div>
                <DirListing/>
            </div>
        );
    }
}

export default App;
