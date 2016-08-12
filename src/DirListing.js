import React from 'react';
import * as axios from 'axios';
import loading from './image/ajax-loader.gif'

export default class extends React.Component {
    constructor(props) {
        super(props);

        this.state = {content: null, path: ''}
    }

    loadDirectoryContent() {
        axios.get('http://api.wallenborn.net/webdrasil/list.php?dir=' + this.state.path).then((response) => {
            let content = [];
            for (var i = 0; i < response.data.length; i++) {
                var row = response.data[i];
                row.key = i;
                content.push(row);
            }
            this.setState({content: content})
        });
    }

    componentWillMount() {
        this.loadDirectoryContent()
    }

    render() {
        let listing = this.state.content === null
            ? <div><img src={loading} alt="loading"/></div>
            : <ul>
            { this.state.path === '' ? '' : <li><a href="#" onClick={(event) => {
                let components = this.state.path.split('/');
                components.pop();
                this.setState({content: null, path: components.join('/') }, this.loadDirectoryContent);
                event.preventDefault();
            }}>..</a></li>}
            {this.state.content.map((row) => {
                return (
                    <li key={row.key}><a onClick={(event) => {
                        this.setState(
                            {content: null, path: this.state.path + '/' + row.name},
                            this.loadDirectoryContent
                        );
                        event.preventDefault();
                    }} href="#">{row.name}</a></li>
                );
            })}
        </ul>;
        return <div>
            <p>Current Directory: {this.state.path ? this.state.path : '/'}</p>
            {listing}
        </div>;
    }
}