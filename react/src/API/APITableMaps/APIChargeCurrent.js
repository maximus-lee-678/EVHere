import { GenerateHeader, GetResponse } from '../APIBase';

export const ChargeCurrentGet = async (email) => {
    return GetResponse('/api/get_charge_current',
        GenerateHeader({ email: email }));
}