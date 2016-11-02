import React from 'react';
import * as axios from 'axios';
import loading from './image/ajax-loader.gif'
import {FaFolderO, FaFolder} from 'react-icons/lib/fa';

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {content: null, path: ''}
    }

    loadDirectoryContent(path) {
        this.setState({content: null, path: path});
        axios.get('http://webdrasil.nullteilerfrei.de/api/list?dir=' + path).then((response) => {
            this.setState({content: response.data})
        });
    }

    componentWillMount() {
        this.loadDirectoryContent('');
    }

    componentDidMount() {
    }

    renderDirectoryUp() {
        if (this.state.path === '') return '';
        return <li><a href="#" onClick={(event) => {
            let components = this.state.path.split('/');
            components.pop();
            this.loadDirectoryContent(components.join('/'));
            event.preventDefault();
        }}>..</a></li>
    }

    renderRowContent(row) {
        return <li key={row.filename}><a onClick={(event) => {
            this.loadDirectoryContent(this.state.path + '/' + row.filename);
            event.preventDefault();
        }} href="#">{row.filename}</a></li>;
    }

    renderListing() {
        if (this.state.content === null) return <div><img src={loading} alt="loading"/></div>

        return <ul>
            { this.renderDirectoryUp()}
            {this.state.content.map((row) => {
                return this.renderRowContent(row);
            })}
        </ul>
    }

    render() {
        return <div>
            <p>Current Directory: {this.state.path ? this.state.path : '/'}</p>
            {this.renderListing()}
        </div>;
    }
}