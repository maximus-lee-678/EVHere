// https://www.digitalocean.com/community/tutorials/how-to-add-login-authentication-to-react-applications

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../shared/Navbar';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loginError, setLoginError] = useState('');

    // Handler for login form submission. Transforms email and password from useStates into POST fields
    // and sends it to backend. Receives a JSON and acts based on response result.
    async function handleLogin(e) {
        e.preventDefault();

        // Forms POST header
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password })
        };

        // Store response
        let response;
        await fetch('/api/login', requestOptions)
            .then(res => res.json())
            .then(data => { response = data })
            .catch(err => console.log(err));

        // result is boolean of status
        if (response.result) {
            // store the user in localStorage
            localStorage.setItem('user_email', email);

            // reload page
            window.location.replace('/');
        } else {
            // setLoginError useState for use with popup error
            // TODO
            setLoginError(response.description);
            alert(response.description);
        }
    }

    return (
        <div>
            <Navbar transparent />
            <main>
                <section className="absolute w-full h-full">
                    <div
                        className="absolute top-0 w-full h-full bg-gray-900"
                        style={{
                            backgroundImage:
                                "url('login-register.png')",
                            backgroundSize: "100%",
                            backgroundRepeat: "no-repeat"
                        }}
                    ></div>
                    <div className="container mx-auto px-4 h-full">
                        <div className="flex content-center items-center justify-center h-full">
                            <div className="w-full lg:w-4/12 px-4">
                                <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-gray-300 border-0">
                                    <div className="flex-auto px-4 lg:px-10 py-10 pt-0 mt-6">
                                        <div className="text-center mb-3">
                                            <h6 className="text-gray-600 text-sm font-bold">
                                                Sign in with
                                            </h6>
                                        </div>
                                        <form onSubmit={handleLogin}>
                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    htmlFor="grid-password"
                                                >
                                                    Email
                                                </label>
                                                <input
                                                    type="email"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    placeholder="janeDoe@email.com"
                                                    style={{ transition: "all .15s ease" }}
                                                    value={email} onChange={(event) => setEmail(event.target.value)}
                                                />
                                            </div>

                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    htmlFor="grid-password"
                                                >
                                                    Password
                                                </label>
                                                <input
                                                    type="password"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    placeholder="******************"
                                                    style={{ transition: "all .15s ease" }}
                                                    value={password} onChange={(event) => setPassword(event.target.value)}
                                                />
                                            </div>

                                            <div className="text-center mt-6">
                                                <button
                                                    className="bg-gray-900 text-white hover:bg-gray-700 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full"
                                                    type="submit"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Sign In
                                                </button>
                                            </div>
                                        </form>
                                        <div className='text-center'>
                                            <Link to="/Register" className="mt-6 text-gray-900 hover:text-gray-700">
                                                Don't have an account? Create one.
                                            </Link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section >
            </main >
        </div>

        /*<div>
            <Navbar/>
            <form class="w-full max-w-sm mx-auto mt-6" onSubmit={handleLogin}>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/3">
                        <label class="block text-gray-500 font-bold md:text-left mb-1 md:mb-0 pr-4" for="inline-username">
                            Email
                        </label>
                    </div>
                    <div class="md:w-2/3">
                        <input value={email} onChange={(event) => setEmail(event.target.value)} class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-cyan-500" id="inline-username" type="text" placeholder="janeDoe@email.com" />
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
        </div>*/

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
