import React from 'react';
import loading from './image/ajax-loader.gif'
import WebdrasilApi from './WebdrasilApi';
import DirRow from './DirRow';
import Link from "./Link";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {dirListing: null, path: ''}
    }

    dirname(s) {
        const i = s.lastIndexOf('/');
        return i === -1 ? '' : s.substr(0, i);
    }

    join(a, b) {
        return a ? `${a}/${b}` : b;
    }

    loadPathContent(nextPath) {
        this.setState({dirListing: null, path: nextPath});
        document.location.hash = nextPath;
        new WebdrasilApi().list(nextPath).then((response) => {
            this.setState({
                dirListing: response.data.sort((a, b) => {
                    return a.filename.toLowerCase().localeCompare(b.filename.toLowerCase());
                })
            })
        }).catch((err) => {
            this.setState({error: err.response.statusText});
        });
    }

    loadDirectoryContent(filename) {
        let nextPath = filename === '..' ? this.dirname(this.state.path) : this.join(this.state.path, filename);
        if (nextPath === '.') nextPath = '/';
        this.loadPathContent(nextPath);
    }

    componentWillMount() {
        this.loadDirectoryContent(document.location.hash.substr(1));
    }

    componentDidMount() {
    }

    renderDirectoryUp() {
        if (this.state.path === '') return '';
        return <li><Link onClick={() => {
            this.loadDirectoryContent('..');
        }}>..</Link></li>
    }

    renderListing() {
        if (this.state.error) return <div>{this.state.error} - This should not have happened</div>;
        if (this.state.dirListing === null) return <div><img src={loading} alt="loading"/></div>;

        return <ul>
            {this.renderDirectoryUp()}
            {this.state.dirListing.map((row) => {
                return <DirRow
                    path={this.state.path}
                    key={row.filename}
                    filename={row.filename}
                    isDir={row.is_dir}
                    isEmpty={row.is_empty}
                    fileStatus={row.file_status}
                    clickDirectory={this.loadDirectoryContent.bind(this)}
                />
            })}
        </ul>
    }

    isLastElement(i, arr) {
        return i + 1 === arr.length;
    }

    renderPath(path) {
        let ret = [
            <span key="">{path === '' ? 'home' : <Link onClick={() => {
                this.loadPathContent('');
            }}>home</Link>}</span>
        ];
        let untilNow = [];
        let spl = path.split('/');
        spl.forEach((part, i) => {
            untilNow.push(part)
            const path = untilNow.join('/');
            ret.push(<span key={untilNow.join('/')}>
                /{this.isLastElement(i, spl) ? <span>{part}</span> : <Link onClick={() => {
                this.loadPathContent(path);
            }}>{part}</Link>}
            </span>);
        })
        return ret;
    }

    render() {
        return <div>
            <div>Current Directory: {this.renderPath(this.state.path)}</div>
            {this.renderListing()}
        </div>;
    }
}