import * as axios from 'axios';

function WebdrasilApi() {
    let baseUrl = (location.hostname === 'localhost' ? 'http://localhost:3001' : '') + '/api/';

    this.list = function (path) {
        return axios.get(baseUrl + 'list?dir=' + encodeURIComponent(path));
    };

    this.download = function (path) {
        return axios.post(baseUrl + 'download?file=' + encodeURIComponent(path));
    };
}

export default WebdrasilApi;
