// Params:
// dictionary> key-values
export const GenerateHeader = (dictionary) => {
    if (dictionary !== undefined) {
        // Forms POST header
        return {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dictionary)
        };
    } else {
        return {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        };
    }

}

// Params:
// apiURL> api endpoint, e.g. /api/example
export const GetResponse = async (apiURL, requestOptions) => {
    let response;

    await fetch(apiURL, requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}