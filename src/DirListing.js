import React from 'react';
import path from 'path';
import loading from './image/ajax-loader.gif'
import WebdrasilApi from './WebdrasilApi';
import DirRow from './DirRow';

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {dirListing: null, path: ''}
    }

    loadDirectoryContent(filename) {
        let nextPath = filename === '..' ? path.dirname(this.state.path) : path.join(this.state.path, filename);
        if (nextPath === '.') nextPath = '/';
        this.setState({dirListing: null, path: nextPath});
        new WebdrasilApi().list(nextPath).then((response) => {
            this.setState({
                dirListing: response.data.sort((a, b) => {
                    return a.filename.toLowerCase().localeCompare(b.filename.toLowerCase());
                })
            })
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
        if (this.state.path === '/') return '';
        return <li><a href="#" onClick={(event) => {
            this.loadDirectoryContent('..');
            event.preventDefault();
        }}>..</a></li>
    }

    renderListing() {
        if (this.state.dirListing === null) return <div><img src={loading} alt="loading"/></div>

        return <ul>
            {this.renderDirectoryUp()}
            {this.state.dirListing.map((row) => {
                return <DirRow
                    key={row.filename}
                    filename={row.filename}
                    isDir={row.is_dir}
                    isEmpty={row.is_empty}
                    fileStatus={row.file_status}
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