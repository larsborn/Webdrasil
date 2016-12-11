import React from 'react';
import {FaFolderO, FaFolder} from 'react-icons/lib/fa';

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.clickDirectory = props.clickDirectory;
        this.clickDownload = props.clickDownload;
        this.filename = props.filename;
        this.is_dir = props.is_dir;
        this.is_empty = props.is_empty;
        this.file_status = props.file_status;
    }

    render() {
        let content = this.filename;
        if (this.is_dir) {
            if (!this.is_empty) {
                content = <a onClick={(event) => {
                    this.clickDirectory(this.filename);
                    event.preventDefault();
                }} href="#">{content}</a>;
            }
        }
        else if (this.file_status === 'IN_PROGRESS') {
            content = <div>{content} <i>processing...</i></div>;
        }
        else if (this.file_status === 'MISSING') {
            content = <div>{content} <a onClick={(event) => {
                this.clickDownload(this.filename);
                event.preventDefault();
            }} href="#">download</a></div>;
        }

        return <li key={this.filename}>{content}</li>;
    }
}
