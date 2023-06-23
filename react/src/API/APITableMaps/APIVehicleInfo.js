export const VehicleInfoGetByUser = async (Email) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: Email })
    };

    // Store response
    let response;
    await fetch('/api/get_user_vehicles', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}

export const VehicleInfoGetById = async (VehicleId) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_vehicle: VehicleId })
    };

    // Store response
    let response;
    await fetch('/api/get_vehicle_by_id', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}

export const VehicleInfoAdd = async (Email, VehicleName, VehicleModel, VehicleSN, VehicleConnector) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: Email, vehicle_name: VehicleName, vehicle_model: VehicleModel,
            vehicle_sn: VehicleSN, vehicle_connector: VehicleConnector
        })
    };

    // Store response
    let response;
    await fetch('/api/add_vehicle', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}

export const VehicleInfoRemove = async (VehicleID) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_vehicle: VehicleID })
    };

    // Store response
    let response;
    await fetch('/api/remove_vehicle', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}
