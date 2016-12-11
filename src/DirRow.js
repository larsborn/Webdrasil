import React from 'react';
import {FaFolderO, FaFolder} from 'react-icons/lib/fa';

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.clickDirectory = props.clickDirectory;
        this.clickDownload = props.clickDownload;
        this.filename = props.filename;
        this.isDir = props.isDir;
        this.isEmpty = props.isEmpty;
        this.fileStatus = props.fileStatus;
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
        else if (this.fileStatus === 'IN_PROGRESS') {
            content = <div>{content} <i>processing...</i></div>;
        }
        else if (this.fileStatus === 'MISSING') {
            content = <div>{content} <a onClick={(event) => {
                this.clickDownload(this.filename);
                event.preventDefault();
            }} href="#">download</a></div>;
        }

        return <li key={this.filename}>{content}</li>;
    }
}
