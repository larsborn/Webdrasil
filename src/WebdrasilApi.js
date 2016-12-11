import * as axios from 'axios';

function WebdrasilApi() {
    var baseUrl = 'http://webdrasil.nullteilerfrei.de/api/';

    this.list = function (path, callback) {
        axios.get(baseUrl + 'list?dir=' + path).then(callback);
    };

    this.download = function (path) {
        axios.post(baseUrl + 'download?file=' + path);
    };
}

export default WebdrasilApi;
