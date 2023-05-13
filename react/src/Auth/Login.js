// https://www.digitalocean.com/community/tutorials/how-to-add-login-authentication-to-react-applications

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

        <form class="w-full max-w-sm mx-auto mt-6" onSubmit={handleLogin}>
            <div class="md:flex md:items-center mb-6">
                <div class="md:w-1/3">
                    <label class="block text-gray-500 font-bold md:text-left mb-1 md:mb-0 pr-4" for="inline-usename">
                        Username
                    </label>
                </div>
                <div class="md:w-2/3">
                    <input value={username} onChange={(event) => setUsername(event.target.value)} class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-cyan-500" id="inline-full-name" type="text" placeholder="janeDoe" />
                </div>
            </div>
            <div class="md:flex md:items-center mb-6">
                <div class="md:w-1/3">
                    <label class="block text-gray-500 font-bold md:text-left mb-1 md:mb-0 pr-4" for="inline-password">
                        Password
                    </label>
                </div>
                <div class="md:w-2/3">
                    <input value={password} onChange={(event) => setPassword(event.target.value)} class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-cyan-500" id="inline-password" type="password" placeholder="******************" />
                </div>
            </div>
            <div class="md:flex md:items-center">
                <div class="mx-auto">
                    <button class="shadow bg-cyan-500 hover:bg-cyan-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded" type="submit">
                        Login
                    </button>
                </div>
            </div>

            <div class="md:flex md:content-center">
                <Link to="/Register" class="mx-auto text-cyan-500 hover:text-cyan-400">Don't have an account?</Link>
            </div>
        </form>

        /*<div className="login-page">
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
        </div>*/
    )
}
