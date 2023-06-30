import { GenerateHeader, GetResponse } from '../APIBase';

export const ConnectorTypeGetAll = async () => {
    return GetResponse('/api/get_all_connectors',
        GenerateHeader());
}