export const ConnectorTypeGetAll = async () => {
    // Forms GET header
    const requestOptions = {
        method: 'GEt',
        headers: { 'Content-Type': 'application/json' }
    };

    // Store response
    let response;
    // JSON returns keys 'result' & 'content'
    await fetch('/api/get_all_connectors', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}