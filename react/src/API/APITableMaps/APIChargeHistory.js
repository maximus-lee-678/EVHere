import { GenerateHeader, GetResponse } from '../APIBase';

export const ChargeHistoryAdd = async (email, IDVehicleInfo, IDCharger, batteryPercentage) => {
    return GetResponse('/api/start_charge_history',
        GenerateHeader({
            email: email, id_vehicle_info: IDVehicleInfo,
            id_charger: IDCharger, battery_percentage: batteryPercentage
        }));
}

export const ChargeHistoryFinish = async (email, batteryPercentage, amountPayable) => {
    return GetResponse('/api/finish_charge_history',
        GenerateHeader({ email: email, battery_percentage: batteryPercentage, amount_payable: amountPayable }));
}

export const ChargeHistoryGet = async (email, filter) => {
    // Acceptable values for Filter
    if (filter !== 'in_progress' && filter !== 'complete' && filter !== 'all') {
        return;
    }

    return GetResponse('/api/get_charge_history',
        GenerateHeader({ email: email, filter: filter }));
}

export const ChargeHistoryActiveGet = async (email) => {
    return GetResponse('/api/get_charge_history_active',
        GenerateHeader({ email: email }));
}