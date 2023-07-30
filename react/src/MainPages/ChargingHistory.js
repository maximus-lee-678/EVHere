// React imports
import React, { useState, useEffect, useCallback } from 'react';
import { DateTime } from 'luxon';

// Standard imports
import Navbar from "../SharedComponents/Navbar";
import BarChart from "./Barchart";
import { FormatDateTime, GetDateDiffString } from '../Utils/Time';
import Toast, { toast } from '../SharedComponents/Toast';

// API endpoints imports
import { ChargeHistoryGet, FavouriteChargerAdd, FavouriteChargerRemove } from '../API/API';

export default function ChargingHistory() {
    const userEmail = localStorage.getItem("user_email");

    const [chargeHistoryDetails, setChargeHistoryDetails] = useState(null);

    const [dataTimeSpent, setDataTimeSpent] = useState([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
    const [dataExpenses, setDataExpenses] = useState([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
    const [dataCharged, setDataCharged] = useState([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
    
    // Function that gets user's historical charges. Called on page load, populates chargeHistoryDetails.
    const fetchUserChargeHistory = useCallback(async () => {
        const response = await ChargeHistoryGet(userEmail, 'complete');

        // result is boolean of status
        if (response.status === 'success' && response.data !== null) {
            setChargeHistoryDetails(response.data);
        }
    }, [userEmail]);

    useEffect(() => {
        fetchUserChargeHistory();
    }, [fetchUserChargeHistory]);

    const calculateGraphData = useCallback(() => {
        var timeSpent = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        var expenses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        var charged = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        for (var i = 0; i < chargeHistoryDetails.length; i++) {
            if (FormatDateTime(chargeHistoryDetails[i].time_start, "yyyy") === String(DateTime.now().year)) {
                timeSpent[FormatDateTime(chargeHistoryDetails[i].time_start, "L") - 1] = parseInt(timeSpent[FormatDateTime(chargeHistoryDetails[i].time_start, "L") - 1]) +
                    parseInt(GetDateDiffString(chargeHistoryDetails[i].time_start, chargeHistoryDetails[i].time_end, ["minutes"]).split(" ")[0]);

                var roundedExpenses = round(parseFloat(expenses[FormatDateTime(chargeHistoryDetails[i].time_start, "L") - 1]) +
                    parseFloat(chargeHistoryDetails[i].amount_payable), 2);

                expenses[FormatDateTime(chargeHistoryDetails[i].time_start, "L") - 1] = roundedExpenses;
                charged[FormatDateTime(chargeHistoryDetails[i].time_start, "L") - 1] = parseFloat(charged[FormatDateTime(chargeHistoryDetails[i].time_start, "L") - 1]) +
                    parseFloat(chargeHistoryDetails[i].total_energy_drawn);
            }

        }

        // for 0 values not to be drawn on graph - example
        /* expenses.forEach((item, index) => {
            if (item == 0) {
                expenses[index] = null;
            }
        }) */

        setDataExpenses(expenses);
        setDataTimeSpent(timeSpent);
        setDataCharged(charged);
    }, [chargeHistoryDetails]);


    useEffect(() => {
        if (chargeHistoryDetails !== null && chargeHistoryDetails.length > 0) {
            calculateGraphData();
        }
    }, [chargeHistoryDetails, calculateGraphData]);


    window.onclick = function (event) {
        if (event.target === document.getElementById("charge-details")) {
            document.getElementById("charge-details").classList.replace("block", "hidden");
        }
    }

    async function handleFavourite(IDCharger, operation) {
        // Ugly confirmation prompt, TODO better
        //maybe can make a dialog that opens when button is clicked, then yes no goes to handle favourite?
        if (!window.confirm(operation + " favourite charger?")) {
            //do nothing if cancel confirmation
            return;
        }

        let response;
        // Pick API endpoint
        if (operation === "add") {
            response = await FavouriteChargerAdd(userEmail, IDCharger);
        } else if (operation === "remove") {
            response = await FavouriteChargerRemove(userEmail, IDCharger);
        } else {
            return;
        }

        // If operation successful, reload user charge history
        // Which reloads modal
        if (response.status === 'success') {
            fetchUserChargeHistory();
            //close modal and show toast accordingly
            if (operation === "add") {
                document.getElementById("charge-details").classList.replace("block", "hidden");
                toast.success("Added to favourites!");
            }
            if (operation === "remove") {
                document.getElementById("charge-details").classList.replace("block", "hidden");
                toast.success("Removed from favourites!");
            }
        }
        else {
            toast.error(<div>{response.message}<br />{response.reason}</div>);
        }
    }

    function round(value, decimals) {
        return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals).toFixed(decimals);
    }

    function FormatChargeHistoryDetails() {
        let result = [];

        for (var i = 0; i < chargeHistoryDetails.length; i++) {
            let id = chargeHistoryDetails[i].id;

            result.push(
                <tr key={id}>
                    <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                        {FormatDateTime(chargeHistoryDetails[i].time_start)}
                    </th>
                    <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                        {chargeHistoryDetails[i].charger.name}
                    </td>
                    <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                        {chargeHistoryDetails[i].vehicle.name}
                    </td>
                    <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                        {chargeHistoryDetails[i].total_energy_drawn} kWh
                    </td>
                    <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                        ${round(chargeHistoryDetails[i].amount_payable, 2)}
                    </td>

                    <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                        <button
                            className="text-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none"
                            type="button"
                            onClick={showModal}
                            id={id}
                            style={{ transition: "all .15s ease" }}
                        >
                            Details
                        </button>
                    </td>
                </tr>
            )
        }

        return result.reverse();
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
            <Toast />
            <div className="relative container mx-auto px-0 md:px-4 h-screen bg-gray-900">
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


                <div className="px-0 py-2 md:px-10 mx-auto w-full flex flex-col items-center bg-white">
                    <div id="overview-tab-content" className="w-full block">
                        <BarChart dataTimeSpent={dataTimeSpent} dataExpenses={dataExpenses} dataCharged={dataCharged} />
                    </div>

                    <div id="history-tab-content" className="hidden w-full mb-12 xl:mb-0 px-4 self-center">

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
                                                Vehicle
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
                                        {chargeHistoryDetails && <FormatChargeHistoryDetails />}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                    </div>
                </div>


                {/*Modal with overlay*/}
                <div
                    className="fixed hidden inset-0 bg-gray-900 bg-opacity-50 h-full"
                    id="charge-details">
                    {/*Modal content*/}
                    <div
                        className="relative mx-auto w-fit max-w-screen top-24 p-5 border shadow-lg rounded-md bg-white"
                    >
                        <div className="mt-3 text-center w-fit">
                            <h3 className="text-lg leading-6 font-medium text-gray-900" id="date">1/6/2023, 2pm</h3>
                            <div className="mt-2 px-7 py-3 space-y-5">
                                {/*Vehicle charging details*/}
                                <div>
                                    <p>Vehicle: <span id="vehicle">(Vehicle name)</span></p>
                                    <p>Time: <span id="duration">2pm - 2.25pm (25 min)</span></p>
                                    <p>Charged: <span id="charged">0 kWh</span></p>
                                    <p>Total price: <span id="paid">$0.00</span></p>
                                </div>

                                {/*Charger details*/}
                                <div>

                                    <p>Charger: <span id="charger-name">(Charger name)</span></p>
                                    <p>Connector used: <span id="connector-used">XX</span></p>
                                    <p>Location: <span id="location">XX</span></p>
                                    <p>Rate: <span id="rate">$1.50/kWh</span></p>
                                    <p>Predicted rate (Next hour): <span id="predicted-rate">$-- / kwh</span></p>
                                </div>
                                <div className="flex justify-center items-center" id="favourite-button-div">
                                    <button id="favourite-button" className="bg-red-400 hover:bg-red-900 px-3 py-2 mr-2 rounded-full text-white">
                                        <i className="fas fa-heart" style={{ color: "#ffffff" }}></i> Add charger to favourites
                                    </button>
                                </div>
                                <p className="text-gray-400 text-sm italic">Click outside to close</p>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );

    function showModal(e) {
        let modal = document.getElementById("charge-details");
        modal.classList.replace("hidden", "block");

        let record = chargeHistoryDetails.find(rec => rec.id === e.target.id)

        document.getElementById("date").innerHTML = FormatDateTime(record.time_start);
        document.getElementById("vehicle").innerHTML = record.vehicle.name + " - " + record.vehicle.model + " (" + record.vehicle.vehicle_sn + ")";
        document.getElementById("duration").innerHTML = FormatDateTime(record.time_start, "t") + " - " + FormatDateTime(record.time_end, "t") + "<br/><span class='text-sm'>(" + GetDateDiffString(record.time_start, record.time_end, ["hours", "minutes", "seconds"]) + ")</span>    ";
        document.getElementById("charged").innerHTML = record.total_energy_drawn + " kWh";
        document.getElementById("paid").innerHTML = "$" + round(record.amount_payable, 2);

        document.getElementById("charger-name").innerHTML = record.charger.name;
        document.getElementById("connector-used").innerHTML = record.vehicle.connector.name_connector;
        document.getElementById("location").innerHTML = record.charger.address;
        document.getElementById("rate").innerHTML = "$" + record.charger.rate_current + " / kWh";

        var predictedValue = "";
        if (record.charger.rate_predicted !== "") {
            //get time now, then get index for next hour
            //0 index is 12AM etc. so get the time then see next hour
            //then put this value in the popup value
            var timeNow = FormatDateTime(DateTime.now(), "T");

            var currentHour = parseInt(timeNow.split(":")[0]);

            var predictedArray = JSON.parse(record.charger.rate_predicted);

            predictedValue = predictedArray[currentHour + 1];

        }

        document.getElementById("predicted-rate").innerHTML = "$" + predictedValue + " / kWh";

        if (record.charger.is_favourite === true) {
            document.getElementById("favourite-button-div").innerHTML = `<button id='favourite-button' class='bg-red-400 hover:bg-red-300 px-3 py-2 mr-2 rounded-full text-white'><i class='fas fa-trash'></i> Remove favourite</button>`;
            document.getElementById("favourite-button").addEventListener("click", () => handleFavourite(record.charger.id, 'remove'));
        }
        else {
            document.getElementById("favourite-button-div").innerHTML = "<button id='favourite-button' class='bg-red-400 hover:bg-red-900 px-3 py-2 mr-2 rounded-full text-white'><i class='fas fa-heart'></i> Add to favourites</button>";
            document.getElementById("favourite-button").addEventListener("click", () => handleFavourite(record.charger.id, 'add'));

        }

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

}
