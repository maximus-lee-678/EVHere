// React imports
import React, { useState, useEffect, useCallback } from 'react';

// Standard imports
import Navbar from '../SharedComponents/Navbar';
import Toast, { toast } from '../SharedComponents/Toast';
import Map from "../Map/Map";

// API endpoints imports
import { VehicleInfoGetByUser } from '../API/API';

export default function Recommendations() {
    const userEmail = localStorage.getItem("user_email");

    const [userVehicleInfo, setUserVehicleInfo] = useState();
    const [selectedVehicleId, setSelectedVehicleId] = useState('');

    // Function that loads all user vehicles. Called on page load, populates userVehicleInfo.
    // Used in main page.
    const fetchAllUserVehicles = useCallback(async () => {
        const response = await VehicleInfoGetByUser(userEmail);

        // If success returned, store vehicle information
        if (response.status === 'success') {
            setUserVehicleInfo(response['data']);
        } else {
            toast.error(<div>{response.message}<br />{response.reason}</div>);
            setUserVehicleInfo([]);
        }
    }, [userEmail]);

    useEffect(() => {
        fetchAllUserVehicles();
    }, [fetchAllUserVehicles]);

    var optionsList = [{
        text: "No vehicles available",
        value: "No vehicles available"
    }];

    if (userVehicleInfo != null || userVehicleInfo != undefined) {
        optionsList = [];
        populateOptionsList();
    }

    function populateOptionsList() {
        if (userVehicleInfo != null || userVehicleInfo != undefined || userVehicleInfo.length !== 0) {
            document.getElementById("vehicleName").disabled = false;

            optionsList.push(
                {
                    text: "Show all markers",
                    value: ""
                }
            )

            for (var i = 0; i < userVehicleInfo.length; i++) {
                let id = userVehicleInfo[i].id;

                optionsList.push(
                    {
                        text: userVehicleInfo[i].name + " - " + userVehicleInfo[i].model + " (" + userVehicleInfo[i].vehicle_sn + ")",
                        value: userVehicleInfo[i].id
                    }
                )
            }

        }

        optionsList = optionsList.sort((a, b) => {
            if (a.text != "Show all markers" && b.text != "Show all markers") {
                if (a.text < b.text) {
                    return -1;
                }
                if (a.text > b.text) {
                    return 1;
                }
                return 0;
            }
        });
    }

    function updateValue(value) {
        setSelectedVehicleId(value);
    }

    // const filterMarkers = useCallback(() => {

    //     console.log(selectedVehicleId, "was selected!!");
    // }, [selectedVehicleId]);

    const [recommendationsOpen, setRecommendationsOpen] = useState(false);

    return (
        <div className="min-h-screen bg-gray-900 "
        >
            <Toast />
            <Navbar transparent />

            <main>
                <section className="w-full h-full">
                    <div className="relative container mx-auto px-4 h-full bg-gray-900">
                        <div className="md:h-40 pt-16 pb-8">
                            <div className="flex content-center items-center justify-center h-full w-full font-semibold text-3xl text-white">Map</div>
                        </div>
                        <div className="md:grid md:grid-cols-3">
                            <div className="bg-white px-7 md:col-span-1 md:h-[70vh] h-min py-3">
                                <div className="md:mt-6 md:h-24 flex">
                                    <div className="flex content-center items-center justify-center h-full w-full font-semibold lg:text-2xl text-xl">Recommended</div>
                                    <button className="md:hidden"
                                        onClick={() => setRecommendationsOpen(!recommendationsOpen)}>
                                        {
                                            <i className="fas fa-angle-down"></i>
                                        }
                                    </button>
                                </div>
                                <div className={"mb-2 mt-6 md:block" + (recommendationsOpen ? " block rounded" : " hidden")}>
                                    <div className="lg:mb-12 mb-2">
                                        <label className="block uppercase text-gray-700 text-xs font-bold mb-2">
                                            Vehicle
                                        </label>
                                        <SelectVehicles optionList={optionsList} onSelected={updateValue} />
                                    </div>

                                    <div className="grid lg:gap-4 gap-2 lg:text-base text-sm">
                                        <button id="nearest-charger-button" className="p-2 rounded-md hover:bg-gray-200 grid grid-cols-8 text-left">
                                            <div className="h-full mt-2">
                                                <i className="fas fa-map-marker-alt fa-2xl"></i>
                                            </div>

                                            <div className="ml-4 col-span-7">
                                                <div className="uppercase text-gray-700 font-bold">Nearest to me:</div>
                                                <div id="nearest-charger-name">
                                                    --
                                                </div>
                                            </div>
                                        </button>


                                        <button id="best-value-charger-button" className="p-2 rounded-md hover:bg-gray-200 cursor-pointer grid grid-cols-8 text-left">
                                            <div className="h-full mt-2">
                                                <i className="fas fa-map-marker-alt fa-2xl"></i>
                                            </div>

                                            <div className="ml-4 col-span-7">
                                                <div className="uppercase text-gray-700 font-bold">Best value for money:</div>
                                                <div id="best-value-charger-name">
                                                    --
                                                </div>
                                            </div>
                                        </button>
                                    </div>
                                </div>

                            </div>

                            <div className="row-span-2 md:col-span-2">
                                <Map desiredZoom={11} mapWidth={"100%"} mapHeight={"70vh"} userVehicleInfo={userVehicleInfo} selectedVehicleId={selectedVehicleId} />
                            </div>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}


function SelectVehicles({ optionList, onSelected }) {
    const [value, setValue] = useState();

    function updateValue({ target }) {
        setValue(target.value);
        if (onSelected) {
            onSelected(target.value);
        }
    };

    return (
        <>
            <select
                id="vehicleName"
                disabled
                className="border-0 px-3 py-3 text-gray-700 bg-white rounded text-sm focus:outline-none focus:ring w-full"
                style={{ transition: "all .15s ease" }}
                defaultValue="No vehicles available"
                value={value}
                onChange={updateValue}
            >
                {optionList.map((option) => (
                    <option value={option.value} key={option.value}>
                        {option.text}
                    </option>
                ))}
            </select>
        </>
    );
}
