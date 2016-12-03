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
        let content = row.filename;
        if (row.is_dir) {
            if (!row.is_empty) {
                content = <a onClick={(event) => {
                    this.loadDirectoryContent(this.state.path + '/' + row.filename);
                    event.preventDefault();
                }} href="#">{content}</a>;
            }
        }
        else if (row.file_status == 'IN_PROGRESS') {
            content = <div>{content} <i>processing...</i></div>;
        }
        else if (row.file_status == 'MISSING') {
            content = <div>{content} <a href="#">download</a></div>;
        }

        return <li key={row.filename}>{content}</li>;
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