import React, { useState, useEffect, useRef } from 'react';
import Navbar from '../shared/Navbar';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function Vehicles() {
    const userEmail = localStorage.getItem("user_email");

    const [vehicleName, setVehicleName] = useState('');
    const [vehicleModel, setVehicleModel] = useState('');
    const [vehicleSN, setVehicleSN] = useState('');
    const connectorRef = useRef(null);

    const [connectorInfo, setConnectorInfo] = useState([]);

    // Function that loads all connectors. Called on page load, populates connectorInfo.
    // Used in connector type dropdown.
    async function fetchAllConnectors() {
        // Forms GET header
        const requestOptions = {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        };

        // Store response
        let response;
        await fetch('/api/get_all_connectors', requestOptions)
            .then(res => res.json())
            .then(data => { response = data })
            .catch(err => console.log(err));

        // If success returned, store connector information
        if (response.success) {
            setConnectorInfo(response['content']);
        } else {
            toast.error(<div>{response.api_response}</div>);
        }

    }

    useEffect(() => {
        fetchAllConnectors()
    }, []);

    // Function that adds a new vehicle. Called upon form submission.
    async function handleCreate(e) {
        e.preventDefault();

        // Forms POST header
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: userEmail, vehicle_name: vehicleName,
                vehicle_model: vehicleModel, vehicle_sn: vehicleSN, vehicle_connector: connectorRef.current.value
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
        } else {
            toast.error(response.reason.toString());
        }
    }

    // Component that formats connector information for display in dropdown. Reads from connectorInfo.
    function ConnectorChoices() {
        let options = [];

        for (var i = 0; i < connectorInfo.length; i++) {
            options.push(
                <option className="border-0 px-3 py-3 text-gray-700" value={connectorInfo[i].name_short}>{connectorInfo[i].name_short}</option>
            )
        }
        return options;
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
                                                    ref={connectorRef}
                                                >
                                                    <ConnectorChoices />
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
