export const ChargerGetAllWithEmail = async (Email) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: Email })
    };

    // Store response
    let response;
    await fetch('/api/get_all_chargers', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}