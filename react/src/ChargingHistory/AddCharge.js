import React, { useState, useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { VehicleInfoGetByUser, ChargerGetAllWithEmail, ChargeHistoryAdd } from '../API/API';

export default function AddCharge() {
    const userEmail = localStorage.getItem("user_email");

    const [selectedVehicleId, setSelectedVehicleId] = useState(null);
    const [selectedVehicleConnector, setSelectedVehicleConnector] = useState(null);
    const [selectedCharger, setSelectedCharger] = useState('');
    let firstCharger;
    const [batteryPercentage, setBatteryPercentage] = useState('');

    const [userVehicleInfo, setUserVehicleInfo] = useState();
    const [allChargerInfo, setAllChargerInfo] = useState();

    // Function that loads all user vehicles. Called on page load, populates userVehicleInfo.
    // Used in main page.
    async function fetchAllUserVehicles() {
        const response = await VehicleInfoGetByUser(userEmail);

        // If success returned, store vehicle information
        if (response.success) {
            setUserVehicleInfo(response['content']);
        } else {
            toast.error(<div>{response.api_response}</div>);
        }
    }

    // Function that loads all chargers. Called on page load, populates allChargerInfo.
    async function fetchAllChargers() {
        const response = await ChargerGetAllWithEmail(userEmail);

        // If success returned, store charger information
        if (response.success) {
            setAllChargerInfo(response['content'])
        } else {
            toast.error(<div>{response.api_response}</div>);
        }
    }

    useEffect(() => {
        fetchAllUserVehicles();
        fetchAllChargers();
    }, []);

    // once userVehicleInfo loaded, update selectedConnector and Id
    useEffect(() => {
        userVehicleInfo && setSelectedVehicleId(userVehicleInfo[0].id);
        userVehicleInfo && setSelectedVehicleConnector(userVehicleInfo[0].connector_type);
    }, [userVehicleInfo]);

    // Component that formats vehicle information for display in dropdown. Reads from userVehicleInfo.
    // When value is read, vehicle id is returned.
    function VehicleChoices() {
        let options = [];

        for (var i = 0; i < userVehicleInfo.length; i++) {
            options.push(
                <option className="border-0 px-3 py-3 text-gray-700" key={userVehicleInfo[i].id}
                    value={userVehicleInfo[i].id} data-connector-type={userVehicleInfo[i].connector_type}>
                    {userVehicleInfo[i].name} ({userVehicleInfo[i].vehicle_sn})
                </option>
            );
        }

        return options;
    }

    // Component that formats charger information for display in dropdown. Reads from allChargerInfo.
    // When value is read, charger id is returned.
    // Only adds chargers that contain a connector specified by selectedVehicleConnector.
    function ChargerChoices() {
        let options = [], hasSetInitial = false;

        for (var i = 0; i < allChargerInfo.length; i++) {
            let connector_types_array = allChargerInfo[i].connector_types;

            if (!connector_types_array.includes(selectedVehicleConnector)) {
                continue;
            }

            if (!hasSetInitial) {
                hasSetInitial = true;
                firstCharger = allChargerInfo[i].id;
            }

            options.push(
                <option className="border-0 px-3 py-3 text-gray-700" key={allChargerInfo[i].id}
                    value={allChargerInfo[i].id}>{allChargerInfo[i].name}</option>
            );
        }

        return options;
    }

    // Function that starts a charge. Called upon form submission.
    async function handleStart(e) {
        e.preventDefault();

        const response = await ChargeHistoryAdd(userEmail, selectedVehicleId, selectedCharger || firstCharger, batteryPercentage);

        // result is boolean of status
        if (response.success) {
            toast.success(response.api_response);
        } else {
            toast.error(response.reason);
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
                                    <form onSubmit={handleStart}>
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
                                                value={(userVehicleInfo && selectedVehicleId) || ""}
                                                onChange={(event) => {
                                                    setSelectedVehicleId(event.target.value);
                                                    setSelectedVehicleConnector(event.target.selectedOptions[0].getAttribute('data-connector-type'));
                                                }}
                                            >
                                                {userVehicleInfo && <VehicleChoices />}
                                            </select>
                                        </div>

                                        {/* <div className="relative w-full mb-3">
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
                                        </div> */}

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
                                                value={batteryPercentage} onChange={(event) => setBatteryPercentage(event.target.value)}
                                            />
                                        </div>

                                        {/* <div className="relative w-full mb-3">
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
                                        </div> */}

                                        {/* <div className="relative w-full mb-3">
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
                                        </div> */}

                                        <div className="relative w-full mb-3">
                                            <label
                                                className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                                for="vInput"
                                            >
                                                Charger Name
                                            </label>
                                            <select
                                                id="vInput"
                                                className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                                style={{ transition: "all .15s ease" }}
                                                value={(allChargerInfo && selectedCharger) || ""}
                                                onChange={(event) => setSelectedCharger(event.target.value)}
                                            >
                                                {allChargerInfo && <ChargerChoices />}
                                            </select>
                                        </div>

                                        <div className="text-center mt-6">
                                            <button
                                                className="bg-gray-900 text-white hover:bg-gray-700 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full"
                                                type="submit"
                                                style={{ transition: "all .15s ease" }}
                                            >
                                                "Start" Charge
                                            </button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section >
        </div>
    )
}