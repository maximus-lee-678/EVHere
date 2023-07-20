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

export const UserInfoGet = async (email) => {
    return GetResponse('/api/get_user_info',
        GenerateHeader({ email: email }));
}

export const UserInfoUpdate = async (email, emailNew, fullName, username, phoneNumber, password) => {
    return GetResponse('/api/update_user_info',
        GenerateHeader({
            email: email, email_new: emailNew, full_name: fullName,
            username: username, phone_number: phoneNumber, password: password
        }));
}