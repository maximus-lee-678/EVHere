import { GenerateHeader, GetResponse } from '../APIBase';

export const UserInfoLogin = async (email, password) => {
    return GetResponse('/api/login',
        GenerateHeader({ email: email, password: password }));
}

export const UserInfoRegister = async (username, password, email, phoneNumber, fullName) => {
    return GetResponse('/api/create_account',
        GenerateHeader({
            username: username, password: password,
            email: email, phone_number: phoneNumber, full_name: fullName
        }));
}