export async function sendRequest(action, currentPage, id = null, data = null, sortBy = null, sortOrder = null) {
    // Base URL for the API
    const baseUrl = 'http://127.0.0.1:5000';

    // Determine the endpoint based on the currentPage
    let endpoint = '';
    switch (currentPage) {
        case 'categories':
            endpoint = '/category/';
            break;
        case 'goods':
            endpoint = '/product/';
            break;
        case 'goods_in_store':
            endpoint = '/store-product/';
            break;
        default:
            console.error('Unknown currentPage:', currentPage);
            return Promise.reject(new Error('Unknown currentPage'));
    }

    // Construct the URL
    let url = `${baseUrl}${endpoint}`;
    if (['delete', 'put'].includes(action.toLowerCase()) && id !== null) {
        url += `${id}`; // For DELETE and PUT, append id to the URL
    } else if (sortBy) {
        url += `?sort=${sortBy}&order=${sortOrder}`; // Append sorting query parameter if sort is provided
    }
    console.log('URL:', url);

    // Configure the request options
    const options = {
        method: action,
        url: url,
    };

    // For methods other than DELETE that require data, include it in the request
    if (['post', 'put', 'patch'].includes(action.toLowerCase()) && data) {
        options.data = data;
        // Axios POST, PUT, PATCH requests expect 'data' field, not 'body'
        options.headers = { 'Content-Type': 'application/json' };
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
