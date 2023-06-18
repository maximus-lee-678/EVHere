// https://www.digitalocean.com/community/tutorials/how-to-add-login-authentication-to-react-applications

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../Shared/Navbar';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { UserInfoLogin } from '../API/API';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    // Handler for login form submission. Transforms email and password from useStates into POST fields
    // and sends it to backend. Receives a JSON and acts based on response result.
    async function handleLogin(e) {
        e.preventDefault();

        const response = await UserInfoLogin(email, password);

        // If success returned, change pages
        if (response.success) {
            // store the user in localStorage
            localStorage.setItem('user_email', email);

            // reload page
            window.location.replace('/');
        } else {
            toast.error(<div>{response.api_response}<br />{response.reason}</div>);
        }
    }

    return (
        <div>
            <ToastContainer position="top-center"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
                theme="colored" />
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
                                                    for="emailInput"
                                                >
                                                    Email
                                                </label>
                                                <input
                                                    id="emailInput"
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
                                                    for="passwordInput"
                                                >
                                                    Password
                                                </label>
                                                <input
                                                    id="passwordInput"
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
    )
}
