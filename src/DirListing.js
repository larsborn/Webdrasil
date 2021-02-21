import React from 'react';
import loading from './image/ajax-loader.gif'
import WebdrasilApi from './WebdrasilApi';
import DirRow from './DirRow';
import Link from "./Link";
import DirLink from "./DirLink";

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

    componentWillMount() {
        this.loadPathContent(decodeURIComponent(document.location.hash.substr(1)));
    }

    componentDidMount() {
    }

    renderDirectoryUp() {
        if (this.state.path === '') return '';
        return <li><DirLink
            caption=".." dir={this.dirname(this.state.path)}
            loadFunc={this.loadPathContent.bind(this)}/></li>
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
                    clickDirectory={() => {
                        this.loadPathContent(this.join(this.state.path, row.filename))
                    }}
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
        if (! path) return ret;
        let spl = path.split('/');
        spl.forEach((part, i) => {
            untilNow.push(part)
            const path = untilNow.join('/');
            ret.push(<span key={untilNow.join('/')}>
                /{
                this.isLastElement(i, spl) ? <span>{part}</span>
                    : <DirLink caption={part} dir={path} loadFunc={this.loadPathContent.bind(this)}/>}
            </span>);
        });
        return ret;
    }

    render() {
        return <div>
            <div>Current Directory: {this.renderPath(this.state.path)}</div>
            {this.renderListing()}
        </div>;
    }
}