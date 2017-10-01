import * as axios from 'axios';

function WebdrasilApi() {
    let baseUrl = (location.hostname === 'localhost' ? 'http://localhost:3001' : '') + '/api/';

    this.list = function (path) {
        return axios.get(baseUrl + 'list?dir=' + path);
    };

    this.download = function (path) {
        return axios.post(baseUrl + 'download?file=' + path);
    };
}

export default WebdrasilApi;
