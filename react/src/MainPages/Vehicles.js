import React, { useState, useEffect, useRef } from 'react';
import Navbar from '../Shared/Navbar';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { ConnectorTypeGetAll, VehicleInfoGetByUser } from '../API/API';

export default function Vehicles() {
    const userEmail = localStorage.getItem("user_email");

    const [vehicleName, setVehicleName] = useState('');
    const [vehicleModel, setVehicleModel] = useState('');
    const [vehicleSN, setVehicleSN] = useState('');
    const [selectedConnector, setSelectedConnector] = useState(null);
    function clearFormFields() {
        setVehicleName('');
        setVehicleModel('');
        setVehicleSN('');
        setSelectedConnector(connectorInfo[0].name_short);
    }

    const [connectorInfo, setConnectorInfo] = useState();
    const [userVehicleInfo, setUserVehicleInfo] = useState();

    const [displayPopup, setDisplayPopup] = useState(false);

    // Function that loads all connectors. Called on page load, populates connectorInfo.
    // Used in connector type dropdown.
    async function fetchAllConnectors() {
        const response = await ConnectorTypeGetAll(userEmail);

        // If success returned, store connector information
        if (response.success) {
            setConnectorInfo(response['content']);
        } else {
            toast.error(<div>{response.api_response}</div>);
            setConnectorInfo([]);
        }
    }

    // Function that loads all user vehicles. Called on page load, populates userVehicleInfo.
    // Used in main page.
    async function fetchAllUserVehicles() {
        const response = await VehicleInfoGetByUser(userEmail);

        // If success returned, store vehicle information
        if (response.success) {
            setUserVehicleInfo(response['content']);
        } else {
            toast.error(<div>{response.api_response}</div>);
            setUserVehicleInfo([]);
        }
    }

    // fetch all required data for population
    useEffect(() => {
        fetchAllConnectors();
        fetchAllUserVehicles();
    }, []);

    // once connectorInfo loaded, update selectedConnector
    useEffect(() => {
        connectorInfo && setSelectedConnector(connectorInfo[0].name_short);
    }, [connectorInfo]);

    // Component that formats vehicle information for display in main page. Reads from userVehicleInfo.
    function UserVehicles() {
        let options = [];

        for (var i = 0; i < userVehicleInfo.length; i++) {
            let id = userVehicleInfo[i].id;

            options.push(
                <div className="flex bg-white rounded-lg py-4 px-10" key={userVehicleInfo[i].id}>
                    <div className="w-4/5">
                        <div className="font-bold text-xl">{userVehicleInfo[i].name}</div>
                        <div>
                            <div>Model: {userVehicleInfo[i].model}</div>
                            <div>S/N: {userVehicleInfo[i].vehicle_sn}</div>
                            <div>Connector: {userVehicleInfo[i].connector_type}</div>
                        </div>
                    </div>
                    <div className="w-1/5 flex justify-center items-center">
                        <button id={id}
                            className="bg-red-400 hover:bg-red-300 p-5 rounded-full text-white"
                            onClick={() => handleRemove(id)}>
                            <i className="fas fa-trash fa-xl" style={{ color: "#ffffff" }}></i>
                        </button>
                    </div>
                </div>
            )
        }
        return options;
    }

    // Component that formats connector information for display in dropdown. Reads from connectorInfo.
    function ConnectorChoices() {
        let options = [];

        for (var i = 0; i < connectorInfo.length; i++) {
            options.push(
                <option className="border-0 px-3 py-3 text-gray-700" key={connectorInfo[i].id}
                    value={connectorInfo[i].name_short}>{connectorInfo[i].name_short}</option>
            );
        }
        return options;
    }

    // Function that adds a new vehicle. Called upon form submission.
    async function handleCreate(e) {
        e.preventDefault();

        // Forms POST header
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: userEmail, vehicle_name: vehicleName,
                vehicle_model: vehicleModel, vehicle_sn: vehicleSN, vehicle_connector: selectedConnector
            })
        };

        // Store response
        let response;
        await fetch('/api/add_vehicle', requestOptions)
            .then(res => res.json())
            .then(data => { response = data })
            .catch(err => console.log(err));

        // result is boolean of status
        if (response.success) {
            toast.success(response.api_response);
            setDisplayPopup(!displayPopup);
            clearFormFields();
            fetchAllUserVehicles();
        } else {
            toast.error(response.reason);
        }
    }

    // Function that removes a vehicle. Called upon corresponding button selection.
    async function handleRemove(vehicleId) {
        if (!window.confirm("remove car?")) {
            //do nothing if cancel confirmation
            return;
        }

        // Forms POST header
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_vehicle: vehicleId
            })
        };

        // Store response
        let response;
        await fetch('/api/remove_vehicle', requestOptions)
            .then(res => res.json())
            .then(data => { response = data })
            .catch(err => console.log(err));

        // result is boolean of status
        if (response.success) {
            toast.success(response.api_response);
            fetchAllUserVehicles();
        } else {
            toast.error(response.reason);
        }
    }

    return (
        <div className="min-h-screen bg-gray-900"
        >
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
                <section className="w-full h-full">
                    <div className="relative container mx-auto px-4 h-full bg-gray-900 w-1/2">
                        <div className="h-40">
                            <div className="flex content-center items-center justify-center h-full w-full font-semibold text-3xl text-white">Vehicles</div>
                        </div>

                        <div className="space-y-4">
                            <div className="flex justify-end">
                                <button className="bg-green-400 hover:bg-green-500 py-2 px-5 rounded-lg"
                                    onClick={() => setDisplayPopup(!displayPopup)}
                                    style={{ transition: "all .15s ease" }}>
                                    Add new vehicle</button>
                            </div>
                            {userVehicleInfo && <UserVehicles />}
                        </div>
                    </div>
                </section>
            </main>

            {/*
            Modal with overlay
            whether displayed or not depends on displayPopup, toggled by button, form submission or clicking outside of window
            e.currentTarget === e.target ensures that child elements dont trigger modal toggling
            */}
            <div
                className="fixed inset-0 bg-gray-900 bg-opacity-50 overflow-y-auto h-full w-full"
                id="my-modal"
                onClick={(e) => e.currentTarget === e.target ? setDisplayPopup(!displayPopup) : undefined}
                style={{ display: displayPopup ? "block" : "none" }}>
                {/*Modal content*/}
                <div
                    className="relative top-24 mx-auto p-5 border w-96 shadow-lg rounded-md bg-gray-200"
                >

                    <div className="flex-auto px-4 lg:px-10 py-10 pt-0 mt-6">
                        <div className="text-center mb-3">
                            <h6 className="text-gray-600 text-sm font-bold">
                                Add a new vehicle
                            </h6>
                        </div>
                        <form onSubmit={handleCreate}>
                            <div className="relative w-full mb-3">
                                <label
                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                    htmlFor="vNameInput"
                                >
                                    Vehicle Name
                                </label>
                                <input
                                    id="vNameInput"
                                    type="text"
                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                    style={{ transition: "all .15s ease" }}
                                    value={vehicleName} onChange={(event) => setVehicleName(event.target.value)}
                                />
                            </div>

                            <div className="relative w-full mb-3">
                                <label
                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                    htmlFor="vModelInput"
                                >
                                    Vehicle Model
                                </label>
                                <input
                                    id="vModelInput"
                                    type="text"
                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                    style={{ transition: "all .15s ease" }}
                                    value={vehicleModel} onChange={(event) => setVehicleModel(event.target.value)}
                                />
                            </div>

                            <div className="relative w-full mb-3">
                                <label
                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                    htmlFor="vSNInput"
                                >
                                    Vehicle S/N
                                </label>
                                <input
                                    id="vSNInput"
                                    type="text"
                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                    style={{ transition: "all .15s ease" }}
                                    value={vehicleSN} onChange={(event) => setVehicleSN(event.target.value)}
                                />
                            </div>

                            <div className="relative w-full mb-3">
                                <label
                                    className="block uppercase text-gray-700 text-xs font-bold mb-2"
                                    htmlFor="connectorTypeInput"
                                >
                                    Connector Type
                                </label>
                                <select
                                    id="connectorTypeInput"
                                    type="text"
                                    className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                    style={{ transition: "all .15s ease" }}
                                    value={(connectorInfo && selectedConnector) || ""}
                                    onChange={(event) => setSelectedConnector(event.target.value)}
                                >
                                    {connectorInfo && <ConnectorChoices />}
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
                        <p className="mt-2 text-center text-gray-700 text-sm italic">Click outside to close</p>
                    </div>
                </div>

            </div>
        </div>
    );
}
