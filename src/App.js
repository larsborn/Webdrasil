import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import DirListing from './DirListing'
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.min.css';

class App extends Component {
    render() {
        return <div className="App">
            <ToastContainer toastClassName="toast" progressClassName="transparent-progress"/>
            <div className="App-header">
                <img src={logo} className="App-logo" alt="logo"/>
                <h2>Webdrasil</h2>
            </div>
            <DirListing/>
        </div>;
    }
}

export default App;
