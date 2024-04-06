export const sendRequest = (action, currentPage, data = null) => {
    // Base URL for the API
    const baseUrl = 'http://127.0.0.1:5000';

    // Determine the endpoint based on the currentPage
    let endpoint = '';
    switch (currentPage) {
        case 'categories':
            endpoint = '/category/';
            break;
        case 'goods':
        case 'goods_in_store': // Assuming both cases use the same endpoint for simplicity
            endpoint = '/product/';
            break;
        default:
            console.error('Unknown currentPage:', currentPage);
            return Promise.reject(new Error('Unknown currentPage'));
    }

    // Construct the URL differently for DELETE requests when data is expected to be part of the URL
    let url;
    if (action.toLowerCase() === 'delete' && data !== null) {
        url = `${baseUrl}${endpoint}${data}`; // For DELETE, append data (e.g., ID) to the URL
    } else {
        url = `${baseUrl}${endpoint}`;
    }

    // Configure the request options
    const options = {
        method: action,
        url: url,
    };

    // For methods other than DELETE that require data, include it in the request
    if (['post', 'put', 'patch'].includes(action.toLowerCase()) && data) {
        options.data = data;
    }

    // Perform the request using axios
    return axios(options)
        .then(response => {
            console.log(`${action.toUpperCase()} request to ${url} successful:`, response.data);
            return response.data; // Resolve the promise with response data
        })
        .catch(error => {
            console.error(`${action.toUpperCase()} request to ${url} failed:`, error);
            throw error; // Reject the promise with the error
        });
}