import { GenerateHeader, GetResponse } from '../APIBase';

export const ChargeHistoryAdd = async (email, IDVehicleInfo, IDCharger, IDChargerAvailableConnector) => {
    return GetResponse('/api/start_charge_history',
        GenerateHeader({
            email: email, id_vehicle_info: IDVehicleInfo,
            id_charger: IDCharger, id_charger_available_connector: IDChargerAvailableConnector
        }));
}

export const ChargeHistoryFinish = async (email, kWh) => {
    return GetResponse('/api/finish_charge_history',
        GenerateHeader({ email: email, energy_drawn: kWh }));
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