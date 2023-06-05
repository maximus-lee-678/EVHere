// https://www.digitalocean.com/community/tutorials/how-to-add-login-authentication-to-react-applications

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../shared/Navbar';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function Vehicles() {
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
                    <div className="absolute top-0 w-full h-full bg-gray-900 min-h-screen"></div>
                    <div className="container mx-auto px-4 h-full">
                        <div className="flex content-center items-center justify-center h-full">
                            <div className="w-full lg:w-4/12 px-4">
                                <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-gray-300 border-0">
                                    <div className="flex-auto px-4 lg:px-10 py-10 pt-0 mt-6">
                                        <div className="text-center mb-3">
                                            <h6 className="text-gray-600 text-sm font-bold">
                                                Current Vehicles
                                            </h6>
                                        </div>
                                        <div className="relative w-full">
                                            <li>Vehicle name 1 (Model - S/N)</li>
                                            <li>Vehicle name 2 (Model - S/N)</li>
                                        </div>
                                    </div>
                                </div>
                                <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-gray-300 border-0">
                                    <div className="flex-auto px-4 lg:px-10 py-10 pt-0 mt-6">
                                        <div className="text-center mb-3">
                                            <h6 className="text-gray-600 text-sm font-bold">
                                                Add a new vehicle
                                            </h6>
                                        </div>
                                        <form>
                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    for="vNameInput"
                                                >
                                                    Vehicle Name
                                                </label>
                                                <input
                                                    id="vNameInput"
                                                    type="text"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    style={{ transition: "all .15s ease" }}
                                                />
                                            </div>

                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    for="vModelInput"
                                                >
                                                    Vehicle Model
                                                </label>
                                                <input
                                                    id="vModelInput"
                                                    type="text"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    style={{ transition: "all .15s ease" }}
                                                />
                                            </div>

                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    for="vSNInput"
                                                >
                                                    Vehicle S/N
                                                </label>
                                                <input
                                                    id="vSNInput"
                                                    type="text"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    style={{ transition: "all .15s ease" }}
                                                />
                                            </div>

                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    for="chargerTypeInput"
                                                >
                                                    Charger Type (AC/DC/Dual) {/*either of these 3 answers will be accepted*/}
                                                </label>
                                                <select
                                                    id="chargerTypeInput"
                                                    type="text"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    <option className="border-0 px-3 py-3 text-gray-700" value="AC">AC</option>
                                                    <option className="border-0 px-3 py-3 text-gray-700" value="DC">DC</option>
                                                    <option className="border-0 px-3 py-3 text-gray-700" value="Dual">Dual (AC/DC)</option>
                                                </select>
                                            </div>

                                            <div className="text-center mt-6">
                                                <button
                                                    className="bg-gray-900 text-white hover:bg-gray-700 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full"
                                                    type="submit"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Add new vehicle
                                                </button>
                                            </div>
                                        </form>
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
