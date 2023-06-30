// React imports
import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { DateTime } from 'luxon';

// Standard imports
import Navbar from "../SharedComponents/Navbar";
import BarChart from "./Barchart";
import PieChart from "./Piechart";
import { FormatDateTime, GetDateDiffString } from '../Utils/Time';

// API endpoints imports
import { ChargeHistoryGet } from '../API/API';

export default function ChargingHistory() {
    const userEmail = localStorage.getItem("user_email");

    const [chargeHistoryDetails, setChargeHistoryDetails] = useState(null);

    // Function that gets user's historical charges. Called on page load, populates chargeHistoryDetails.
    const fetchUserChargeHistory = useCallback(async () => {
        const Response = await ChargeHistoryGet(userEmail, 'complete');

        // result is boolean of status
        if (Response.status === 'success' && Response.data !== null) {
            setChargeHistoryDetails(Response.data);
        }
    }, [userEmail]);

    useEffect(() => {
        fetchUserChargeHistory();
    }, [fetchUserChargeHistory]);


    window.onclick = function (event) {
        if (event.target === document.getElementById("charge-details")) {
            document.getElementById("charge-details").style.display = "none";
        }
    }

    return (
        <div className="min-h-screen bg-gray-900"
            style={{
                backgroundImage:
                    "url('battery.png')",
                backgroundSize: "100%",
                backgroundRepeat: "repeat"
            }}>
            <Navbar transparent />
            <div className="relative container mx-auto px-4 h-full bg-gray-900">
                {/* Header */}
                <div className="h-40">
                    <div className="flex content-center items-center justify-center h-full w-full font-semibold text-3xl text-white">Charging History</div>
                </div>
                <div className="w-fit flex flex-row">
                    <button className="bg-white rounded-t-md px-4 py-4"
                        id="overview-tab-btn"
                        onClick={showOverview}
                    >Overview</button>

                    <button className="bg-gray-300 rounded-t-md px-4 py-4"
                        id="history-tab-btn"
                        onClick={showHistory}
                    >History</button>
                </div>


                <div className="px-4 py-2 md:px-10 mx-auto w-full flex flex-col items-center bg-white">
                    <div id="overview-tab-content" className="w-full block">
                        <BarChart />
                        <PieChart />
                    </div>

                    <div id="history-tab-content" className="hidden w-full xl:w-8/12 mb-12 xl:mb-0 px-4 self-center">

                        {/*Recent entries table*/}
                        <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
                            <div className="rounded-t mb-0 px-4 py-3 border-0">
                                <div className="flex flex-wrap items-center">
                                    <div className="relative w-full px-4 max-w-full flex-grow flex-1">
                                        <h3 className="font-semibold text-base text-blueGray-700">
                                            Most recent
                                        </h3>
                                    </div>
                                </div>
                            </div>
                            <div className="block w-full overflow-x-auto">
                                {/* Table */}
                                <table className="items-center w-full bg-transparent border-collapse">
                                    <thead>
                                        <tr>
                                            <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                                                Date / Time
                                            </th>
                                            <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                                                Location
                                            </th>
                                            <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                                                Charged
                                            </th>
                                            <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                                                Amount paid
                                            </th>
                                            <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                                                1/6/2023, 2pm
                                            </th>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Shell Recharge Punggol
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                50% -&gt; 60%
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                $5
                                            </td>

                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                <button
                                                    className="text-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none"
                                                    type="button"
                                                    onClick={showModal}
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Details
                                                </button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                                                31/5/2023, 8pm
                                            </th>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Jalan Kayu URA Carpark
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                0% -&gt; 75%
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                $13
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                <button
                                                    className="text-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none"
                                                    type="button"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Details
                                                </button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                                                Row 3
                                            </th>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Location name
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Percentage
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Price
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                <button
                                                    className="text-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none"
                                                    type="button"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Details
                                                </button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                                                Row 4
                                            </th>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Location name
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Percentage
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Price
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                <button
                                                    className="text-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none"
                                                    type="button"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Details
                                                </button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                                                Row 5
                                            </th>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Location name
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Percentage
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Price
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                <button
                                                    className="text-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none"
                                                    type="button"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Details
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>


                        {/*By year table*/}
                        <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
                            <div className="rounded-t mb-0 px-4 py-3 border-0">
                                <div className="flex flex-wrap items-center">
                                    <div className="relative w-full px-4 max-w-full flex items-center">
                                        <button onClick={decreaseYear}><i className="fa-solid fa-chevron-left"></i></button>
                                        <h3 className="font-semibold text-base text-blueGray-700 px-3" id="yearNo">
                                            2023
                                        </h3>
                                        <button onClick={increaseYear}><i className="fa-solid fa-chevron-right"></i></button>
                                    </div>
                                </div>
                            </div>
                            <div className="block w-full overflow-x-auto">
                                {/* Table */}
                                <table className="items-center w-full bg-transparent border-collapse">
                                    <thead>
                                        <tr>
                                            <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                                                Date / Time
                                            </th>
                                            <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                                                Location
                                            </th>
                                            <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                                                Charged
                                            </th>
                                            <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                                                Amount paid
                                            </th>
                                            <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                                                1/6/2023, 2pm
                                            </th>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Shell Recharge Punggol
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                50% -&gt; 60%
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                $5
                                            </td>

                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                <button
                                                    className="text-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none"
                                                    type="button"
                                                    onClick={showModal}
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Details
                                                </button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                                                31/5/2023, 8pm
                                            </th>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Jalan Kayu URA Carpark
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                0% -&gt; 75%
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                $13
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                <button
                                                    className="text-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none"
                                                    type="button"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Details
                                                </button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                                                Row 3
                                            </th>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Location name
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Percentage
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Price
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                <button
                                                    className="text-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none"
                                                    type="button"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Details
                                                </button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                                                Row 4
                                            </th>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Location name
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Percentage
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Price
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                <button
                                                    className="text-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none"
                                                    type="button"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Details
                                                </button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                                                Row 5
                                            </th>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Location name
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Percentage
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                Price
                                            </td>
                                            <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                                <button
                                                    className="text-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none"
                                                    type="button"
                                                    style={{ transition: "all .15s ease" }}
                                                >
                                                    Details
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                </div>
            </div>


            {/*Modal with overlay*/}
            <div
                className="fixed hidden inset-0 bg-gray-900 bg-opacity-50 overflow-y-auto h-full w-full"
                id="charge-details">
                {/*Modal content*/}
                <div
                    className="relative top-24 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
                >
                    <div className="mt-3 text-center">
                        <h3 className="text-lg leading-6 font-medium text-gray-900">1/6/2023, 2pm</h3>
                        <div className="mt-2 px-7 py-3 space-y-5">
                            {/*Vehicle charging details*/}
                            <div>
                                <p>Vehicle: (Vehicle name)</p>
                                <p>Time: 2pm - 2.25pm (25 min)</p>
                                <p>Starting battery percentage: 50%</p>
                                <p>Ending battery percentage: 60%</p>
                                <p>Total price: $20.00</p>
                            </div>

                            {/*Charger details*/}
                            <div>

                                <p>Charger: (Charger name)</p>
                                <p>Charger type: DC</p>
                                <p>Charger connector: XX</p>
                                <p>Location: XX</p>
                                <p>Rate: $1.50/kWh</p>
                            </div>
                            <div className="flex justify-center items-center">
                                <button className="bg-red-400 hover:bg-red-900 px-3 py-2 mr-2 rounded-full text-white">
                                    <i className="fas fa-heart" style={{ color: "#ffffff" }}></i> Add charger to favourites
                                </button>
                            </div>
                            <p className="text-gray-400 text-sm italic">Click outside to close</p>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );

    function showModal() {
        let modal = document.getElementById("charge-details");
        modal.style.display = "block";
    }

    function showOverview() {
        let overviewTab = document.getElementById("overview-tab-content")
        let historyTab = document.getElementById("history-tab-content")
        overviewTab.classList.replace("hidden", "block");
        historyTab.classList.replace("block", "hidden");
        document.getElementById("overview-tab-btn").classList.replace("bg-gray-300", "bg-white")
        document.getElementById("history-tab-btn").classList.replace("bg-white", "bg-gray-300")
    }

    function showHistory() {
        let overviewTab = document.getElementById("overview-tab-content")
        let historyTab = document.getElementById("history-tab-content")
        overviewTab.classList.replace("block", "hidden");
        historyTab.classList.replace("hidden", "block");
        document.getElementById("overview-tab-btn").classList.replace("bg-white", "bg-gray-300")
        document.getElementById("history-tab-btn").classList.replace("bg-gray-300", "bg-white")
    }

    function increaseYear() {
        let yearHeader = document.getElementById("yearNo");
        let yearNoInt = parseInt(yearHeader.innerText);
        yearHeader.innerText = yearNoInt + 1;
    }

    function decreaseYear() {
        let yearHeader = document.getElementById("yearNo");
        let yearNoInt = parseInt(yearHeader.innerText);
        yearHeader.innerText = yearNoInt - 1;
    }



}
