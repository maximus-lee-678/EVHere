export const ChargeHistoryAdd = async (Email, IDVehicleInfo, IDCharger, BatteryPercentage) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: Email, id_vehicle_info: IDVehicleInfo,
            id_charger: IDCharger, battery_percentage: BatteryPercentage
        })
    };

    // Store response
    let response;
    await fetch('/api/start_charge', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}

export const ChargeHistoryGet = async (Email) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: Email })
    };

    // Store response
    let response;
    await fetch('/api/get_charge_current', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}