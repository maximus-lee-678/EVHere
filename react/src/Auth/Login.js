// https://www.digitalocean.com/community/tutorials/how-to-add-login-authentication-to-react-applications
// https://stackoverflow.com/questions/41956465/how-to-create-multiple-page-app-using-react

import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    function authenticate(username, password) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username, password: password })
        };
        fetch('http://localhost:5000/login', requestOptions)
            .then(res => res.json())
            .then(data => { console.log(data.username); })
            .catch(err => console.log(err));
    }

    function handleLogin(e) {
        e.preventDefault();
        authenticate(username, password);
        console.log('You clicked submit.');
    }

    return (
        <div className="login-page">
            <h1>Login</h1>
            <form onSubmit={handleLogin}>
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input type="text" id="username" value={username} onChange={(event) => setUsername(event.target.value)}/>
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" value={password} onChange={(event) => setPassword(event.target.value)}/>
                </div>
                <button type="submit">Login</button>
            </form>
            <div className="create-account">
                <p>Don't have an account?</p>
                <Link to="/Register">Create one</Link>
            </div>
        </div>
    )
}
