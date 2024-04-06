// #region request management

console.log('sendRequest.js loaded');
export const sendRequest = (action, currentPage, data = null) => {
    // Base URL for the API
    const baseUrl = 'http://127.0.0.1:5000';

    // Determine the endpoint based on the currentPage
    let endpoint = '';
    if (currentPage === 'categories') {
        endpoint = '/category/';
    } else if (currentPage === 'goods') {
        endpoint = '/product/';
    } else if (currentPage === 'goods_in_store') {
        endpoint = '/product/';
    }
    // Construct the full URL
    const url = `${baseUrl}${endpoint}`;

    // Configure the request options
    const options = {
        method: action,
        url: url,
    };

    // Include data for methods that require it (e.g., POST, PUT, PATCH)
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

// #endregion