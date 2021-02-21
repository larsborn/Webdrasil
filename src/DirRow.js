import React from 'react';
import WebdrasilApi from './WebdrasilApi';
import {toast} from 'react-toastify';
import Link from "./Link";
import DirLink from "./DirLink";
import PathUtils from "./PathUtils";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.clickDirectory = props.clickDirectory;
        this.path = props.path;
        this.filename = props.filename;
        this.isDir = props.isDir;
        this.isEmpty = props.isEmpty;
        this.state = {fileStatus: props.fileStatus}

        this.pathUtils = new PathUtils();
    }

    render() {
        const full_file_path = this.pathUtils.join(this.path, this.filename);
        let content = this.filename;
        if (this.isDir) {
            if (! this.isEmpty) {
                content = <DirLink dir={full_file_path} caption={this.filename} loadFunc={() => {
                    this.clickDirectory(this.filename);
                }}/>;
            }
        } else if (this.state.fileStatus === 'IN_PROGRESS') {
            content = <div>{content} <i>processing...</i></div>;
        } else if (this.state.fileStatus === 'MISSING') {
            content = <div>{content} <Link onClick={() => {
                this.setState({fileStatus: 'IN_PROGRESS'});
                new WebdrasilApi().download(full_file_path).catch((err) => {
                    toast('Cannot schedule file for download.');
                    this.setState({fileStatus: 'MISSING'});
                });
            }}>schedule download</Link></div>;
        }

        return <li key={this.filename}>{content}</li>;
    }
}
