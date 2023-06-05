// https://www.digitalocean.com/community/tutorials/how-to-add-login-authentication-to-react-applications

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../shared/Navbar';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function AddChargingHistory() {
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
                                                Add new charging history
                                            </h6>
                                        </div>
                                        <form>
                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    for="vInput"
                                                >
                                                    Vehicle
                                                </label>
                                                <select
                                                    id="vInput"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    <option value="Vehicle1Name">Vehicle 1 Name (S/N)</option>
                                                    <option value="Vehicle1Name">Vehicle 2 Name (S/N)</option>
                                                </select>
                                            </div>

                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    for="startDateTimeInput"
                                                >
                                                    Start date and time
                                                </label>
                                                <input
                                                    id="startDateTimeInput"
                                                    type="datetime-local"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    style={{ transition: "all .15s ease" }}
                                                />
                                            </div>

                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    for="endDateTimeInput"
                                                >
                                                    End date and time
                                                </label>
                                                <input
                                                    id="endDateTimeInput"
                                                    type="datetime-local"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    style={{ transition: "all .15s ease" }}
                                                />
                                            </div>

                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    for="startBattInput"
                                                >
                                                    Starting battery percentage
                                                </label>
                                                <input
                                                    id="startBattInput"
                                                    type="number"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    style={{ transition: "all .15s ease" }}
                                                />
                                            </div>

                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    for="endBattInput"
                                                >
                                                    Ending battery percentage
                                                </label>
                                                <input
                                                    id="endBattInput"
                                                    type="number"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    style={{ transition: "all .15s ease" }}
                                                />
                                            </div>

                                            <div className="relative w-full mb-3">
                                                <label
                                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                    for="chargerTypeInput"
                                                >
                                                    Total amount paid
                                                </label>
                                                <input
                                                    id="chargerTypeInput"
                                                    type="text"
                                                    placeholder="0.00"
                                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                    style={{ transition: "all .15s ease" }}
                                                />
                                            </div>

                                            <div className="text-center mt-6">
                                                <button
                                                    className="bg-gray-900 text-white hover:bg-gray-700 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full"
                                                    type="submit"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Add new charging history log
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
