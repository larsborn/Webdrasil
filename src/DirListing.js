import React from 'react';
import path from 'path';
import loading from './image/ajax-loader.gif'
import WebdrasilApi from './WebdrasilApi';
import DirRow from './DirRow';

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {content: null, path: ''}
    }

    loadDirectoryContent(filename) {
        let nextPath = filename == '..' ? path.dirname(this.state.path) : path.join(this.state.path, filename);
        if (nextPath === '.') nextPath = '/';
        this.setState({content: null, path: nextPath});
        new WebdrasilApi().list(nextPath, (response) => {
            this.setState({content: response.data})
        });
    }

    clickDownload(filename) {
        new WebdrasilApi().download(path.join(this.state.path, filename));
    }

    componentWillMount() {
        this.loadDirectoryContent('');
    }

    componentDidMount() {
    }

    renderDirectoryUp() {
        if (this.state.path === '') return '';
        return <li><a href="#" onClick={(event) => {
            this.loadDirectoryContent('..');
            event.preventDefault();
        }}>..</a></li>
    }

    renderListing() {
        if (this.state.content === null) return <div><img src={loading} alt="loading"/></div>

        return <ul>
            { this.renderDirectoryUp()}
            {this.state.content.map((row) => {
                return <DirRow
                    key={row.filename}
                    filename={row.filename}
                    is_dir={row.is_dir}
                    is_empty={row.is_empty}
                    file_status={row.file_status}
                    clickDirectory={this.loadDirectoryContent.bind(this)}
                    clickDownload={this.clickDownload.bind(this)}
                />
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