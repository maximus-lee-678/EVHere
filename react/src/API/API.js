import { UserInfoLogin, UserInfoRegister } from './APITableMaps/APIUserInfo';
import { VehicleInfoGetByUser, VehicleInfoGetById, VehicleInfoAdd, VehicleInfoRemove } from './APITableMaps/APIVehicleInfo';
import { ChargerGetAllWithEmail } from './APITableMaps/APICharger';
import { ChargeCurrentGet } from './APITableMaps/APIChargeCurrent';
import { ChargeHistoryAdd, ChargeHistoryFinish, ChargeHistoryGet } from './APITableMaps/APIChargeHistory';
import { FavouriteChargerGet, FavouriteChargerAdd, FavouriteChargerRemove } from './APITableMaps/APIFavouriteChargers';
import { ConnectorTypeGetAll } from './APITableMaps/APIConnectorType';

export { UserInfoLogin, UserInfoRegister };
export { VehicleInfoGetByUser, VehicleInfoGetById, VehicleInfoAdd, VehicleInfoRemove };
export { ChargerGetAllWithEmail };
export { ChargeCurrentGet };
export { ChargeHistoryAdd, ChargeHistoryFinish, ChargeHistoryGet };
export { FavouriteChargerGet, FavouriteChargerAdd, FavouriteChargerRemove };
export { ConnectorTypeGetAll };
