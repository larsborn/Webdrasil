import React from 'react';
import WebdrasilApi from './WebdrasilApi';
import {toast} from 'react-toastify';

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.clickDirectory = props.clickDirectory;
        this.state = {
            filename: props.filename,
            isDir: props.isDir,
            isEmpty: props.isEmpty,
            fileStatus: props.fileStatus,
        };
    }

    render() {
        let content = this.state.filename;
        if (this.state.isDir) {
            if (!this.state.isEmpty) {
                content = <a onClick={(event) => {
                    this.clickDirectory(this.state.filename);
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
                new WebdrasilApi().download(this.state.filename).catch((err) => {
                    this.setState({fileStatus: 'MISSING'});
                    toast('Cannot schedule file for download.');
                });
                event.preventDefault();
            }} href="#">download</a></div>;
        }

        return <li key={this.state.filename}>{content}</li>;
    }
}
