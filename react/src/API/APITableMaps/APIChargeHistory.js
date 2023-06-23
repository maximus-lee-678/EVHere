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
    await fetch('/api/start_charge_history', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}

export const ChargeHistoryFinish = async (Email, BatteryPercentage, AmountPayable) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: Email, battery_percentage: BatteryPercentage, amount_payable: AmountPayable
        })
    };

    // Store response
    let response;
    await fetch('/api/finish_charge_history', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}

export const ChargeHistoryGet = async (Email, Filter) => {
    // Acceptable values for Filter
    if(Filter != 'in_progress' && Filter != 'complete' && Filter != 'all'){
        return;
    }

    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: Email, filter: Filter
        })
    };

    // Store response
    let response;
    await fetch('/api/get_charge_history', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}