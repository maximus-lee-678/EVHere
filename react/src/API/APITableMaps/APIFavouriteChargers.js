import { GenerateHeader, GetResponse } from '../APIBase';

export const FavouriteChargerGet = async (email) => {
    return GetResponse('/api/get_favourite_chargers',
        GenerateHeader({ email: email }));
}

export const FavouriteChargerAdd = async (email, IDCharger) => {
    return GetResponse('/api/add_favourite_charger',
        GenerateHeader({ email: email, id_charger: IDCharger }));
}

export const FavouriteChargerRemove = async (email, IDCharger) => {
    return GetResponse('/api/remove_favourite_charger',
        GenerateHeader({ email: email, id_charger: IDCharger }));
}