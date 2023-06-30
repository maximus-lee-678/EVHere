import { GenerateHeader, GetResponse } from '../APIBase';

export const ChargerGetAllWithEmail = async (email) => {
    return GetResponse('/api/get_all_chargers',
    GenerateHeader({ email: email }));
}