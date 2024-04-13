export async function sendRequest({
    action,
    currentPage,
    id = null,
    data = null,
    sortBy = null,
    sortOrder = null,
    searchColumn = null,
    searchValue = null
} = {}) {
    const baseUrl = 'http://127.0.0.1:5000';
    let endpoint;

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
            throw new Error(`Unknown currentPage: ${currentPage}`);
    }

    let url = new URL(`${baseUrl}${endpoint}`);

    if (action.toLowerCase() === 'delete' && id !== null) {
        url.pathname += id;
    } else {
        if (sortBy) {
            url.searchParams.append('sort', sortBy);
            url.searchParams.append('order', sortOrder ?? 'asc');
        }
        if (searchColumn && searchValue) {
            url.searchParams.append('search-column', searchColumn);
            url.searchParams.append('search-value', searchValue);
        }
    }

    console.log('URL:', url.href);

    const options = {
        method: action,
        url: url.href,
        headers: { 'Content-Type': 'application/json' },
        ...(data && { data })
    };

    try {
        const response = await axios(options);
        console.log(`${action.toUpperCase()} request to ${url.href} successful:`, response.data);
        return response.data;
    } catch (error) {
        console.error(`${action.toUpperCase()} request to ${url.href} failed:`, error);
        throw error;
    }
}
