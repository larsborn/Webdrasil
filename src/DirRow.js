import React from 'react';
import WebdrasilApi from './WebdrasilApi';
import {toast} from 'react-toastify';

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.clickDirectory = props.clickDirectory;
        this.path = props.path;
        this.filename = props.filename;
        this.isDir = props.isDir;
        this.isEmpty = props.isEmpty;
        this.state = {fileStatus: props.fileStatus}
    }

    join(a, b) {
        return `${a}/${b}`
    }

    render() {
        let content = this.filename;
        if (this.isDir) {
            if (!this.isEmpty) {
                content = <a onClick={(event) => {
                    this.clickDirectory(this.filename);
                    event.preventDefault();
                }} href="#">{content}</a>;
            }
        }
        else if (this.state.fileStatus === 'IN_PROGRESS') {
            content = <div>{content} <i>processing...</i></div>;
        }
        else if (this.state.fileStatus === 'MISSING') {
            content = <div>{content} <a onClick={(event) => {
                this.setState({fileStatus: 'IN_PROGRESS'});
                new WebdrasilApi().download(this.join(this.path, this.filename)).catch((err) => {
                    toast('Cannot schedule file for download.');
                    this.setState({fileStatus: 'MISSING'});
                });
                event.preventDefault();
            }} href="#">schedule download</a></div>;
        }

        return <li key={this.filename}>{content}</li>;
    }
}
