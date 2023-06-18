export const FavouriteChargerGet = async (Email) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: Email })
    };

    // Store response
    let response;
    // JSON returns keys 'result' & 'content'
    await fetch('/api/get_favourite_chargers', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}

export const FavouriteChargerAdd = async (Email, IDCharger) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: Email, id_charger: IDCharger })
    };

    // Store response
    let response;
    await fetch('/api/add_favourite_charger', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}

export const FavouriteChargerRemove = async (Email, IDCharger) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: Email, id_charger: IDCharger })
    };

    // Store response
    let response;
    await fetch('/api/remove_favourite_charger', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}