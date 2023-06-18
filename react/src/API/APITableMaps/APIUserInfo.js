export const UserInfoLogin = async (Email, Password) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: Email, password: Password })
    };

    // Store response
    let response;
    await fetch('/api/login', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}

export const UserInfoRegister = async (Username, Password, Email, PhoneNumber, FullName) => {
    // Forms POST header
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: Username, password: Password,
            email: Email, phone_number: PhoneNumber, full_name: FullName
        })
    };

    // Store response
    let response;
    await fetch('/api/create_account', requestOptions)
        .then(res => res.json())
        .then(data => { response = data })
        .catch(err => console.log(err));

    return response;
}