import React, { useState, useMemo, useEffect } from 'react';
import Navbar from "../Shared/Navbar";
import Map from "../Map/Map";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function Recommendations() {
    const userEmail = localStorage.getItem("user_email");

    const [userVehicleInfo, setUserVehicleInfo] = useState();

    // Function that loads all user vehicles. Called on page load, populates userVehicleInfo.
    // Used in main page.
    async function fetchAllUserVehicles() {
        // Forms GET header
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: userEmail })
        };

        // Store response
        let response;
        await fetch('/api/get_user_vehicles', requestOptions)
            .then(res => res.json())
            .then(data => { response = data })
            .catch(err => console.log(err));

        // If success returned, store connector information
        if (response.success) {
            setUserVehicleInfo(response['content']);
        } else {
            toast.error(<div>{response.api_response}</div>);
            setUserVehicleInfo([]);
            console.log("test",userVehicleInfo);
        }
    }

    // fetch all required data for population
    useEffect(() => {
        fetchAllUserVehicles();
    }, []);


    // Component that formats vehicle information for display in main page. Reads from userVehicleInfo.
    function UserVehicles() {
        let options = [];
        
        if (userVehicleInfo.length == 0) {
            options.push(
                <option value="No vehicles available">No vehicles available</option>
            )
        }
        else {
            document.getElementById("vehicleName").disabled = false;

            for (var i = 0; i < userVehicleInfo.length; i++) {
                let id = userVehicleInfo[i].id;
    
                options.push(
                    <option className="border-0 px-3 py-3 text-gray-700" value={userVehicleInfo[i].name}>{userVehicleInfo[i].name}</option>
                )
            }
        }
        
        return options;
    }

    return (
        <div className="min-h-screen bg-gray-900 "
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
                    <div className="relative container mx-auto px-4 h-full bg-gray-900">
                        <div className="h-40">
                            <div className="flex content-center items-center justify-center h-full w-full font-semibold text-3xl text-white">Map</div>
                        </div>
                        <div className="grid grid-cols-3">
                            <div className="bg-white col-span-1 px-7 max-h-[70vh]">
                                <div className="h-24">
                                    <div className="flex content-center items-center justify-center h-full w-full font-semibold text-2xl">Recommended</div>
                                </div>
                                <div>
                                    <div className="mb-12">
                                        <label className="block uppercase text-gray-700 text-xs font-bold mb-2">
                                            Vehicle
                                        </label>
                                        <select
                                            id="vehicleName"
                                            disabled
                                            className="border-0 px-3 py-3 text-gray-700 bg-white rounded text-sm focus:outline-none focus:ring w-full"
                                            style={{ transition: "all .15s ease" }}
                                            defaultValue="No vehicles available"
                                        >
                                            {userVehicleInfo && <UserVehicles/> }
                                            
                                        </select>
                                    </div>

                                    <div className="grid lg:gap-4 gap-2">
                                        <div className="p-2 rounded-md hover:bg-gray-200 cursor-pointer grid grid-cols-8">
                                            <div className="h-full mt-2">
                                                <i className="fas fa-map-marker-alt fa-2xl"></i>
                                            </div>

                                            <div className="ml-4 col-span-7">
                                                <div className="uppercase text-gray-700 font-bold">Nearest to me:</div>
                                                <div>
                                                    Bukit Merah / Telok Blangah Rise / Blk 32
                                                </div>
                                            </div>
                                        </div>


                                        <div className="p-2 rounded-md hover:bg-gray-200 cursor-pointer grid grid-cols-8">
                                            <div className="h-full mt-2">
                                                <i className="fas fa-map-marker-alt fa-2xl"></i>
                                            </div>

                                            <div className="ml-4 col-span-7">
                                                <div className="uppercase text-gray-700 font-bold">Fastest charging speed:</div>
                                                <div>
                                                    Shell Recharge Punggol
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>

                            <div className="col-span-2">
                                <Map desiredZoom={11} mapWidth={"100%"} mapHeight={"70vh"} />
                            </div>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
