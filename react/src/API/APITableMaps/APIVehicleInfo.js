import { GenerateHeader, GetResponse } from '../APIBase';

export const VehicleInfoGetByUser = async (email) => {
    return GetResponse('/api/get_user_vehicles',
        GenerateHeader({ email: email }));
}

export const VehicleInfoGetById = async (IDVehicle) => {
    return GetResponse('/api/get_vehicle_by_id',
        GenerateHeader({ id_vehicle: IDVehicle }));
}

export const VehicleInfoAdd = async (email, vehicleName, vehicleModel, vehicleSN, vehicleConnector) => {
    return GetResponse('/api/add_vehicle',
        GenerateHeader({
            email: email, vehicle_name: vehicleName, vehicle_model: vehicleModel,
            vehicle_sn: vehicleSN, vehicle_connector: vehicleConnector
        }));
}

export const VehicleInfoRemove = async (IDVehicle) => {
    return GetResponse('/api/remove_vehicle',
    GenerateHeader({ id_vehicle: IDVehicle }));
}
