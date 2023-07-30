// React imports
import React, { useState, useEffect, useCallback } from 'react';
import { DateTime } from 'luxon';

// Standard imports
import Navbar from '../SharedComponents/Navbar';
import Toast, { toast } from '../SharedComponents/Toast';
import { CardContent, CardButton } from '../SharedComponents/Card.js';
import { FormatDateTime } from '../Utils/Time';

// API endpoints imports
import { FavouriteChargerGet, FavouriteChargerRemove } from '../API/API';

export default function Favourites() {
    const userEmail = localStorage.getItem("user_email");
    const [favouriteChargerInfo, setFavouriteChargerInfo] = useState();

    // Function that loads user's favourited chargers. Called on page load, populates favouriteChargerInfo.
    const fetchFavouriteChargers = useCallback(async () => {
        const response = await FavouriteChargerGet(userEmail);

        // If success returned, store chargers
        if (response.status === 'success') {
            setFavouriteChargerInfo(response['data']);
        }
        else {
            toast.error(<div>{response.message}<br />{response.reason}</div>);
            setFavouriteChargerInfo([]);
        }
    }, [userEmail]);

    useEffect(() => {
        fetchFavouriteChargers();
    }, [fetchFavouriteChargers]);

    // Function that removes a user's favourited charger. Called when user clicks corresponding remove button.
    async function handleFavouriteRemove(IDCharger) {
        // Ugly confirmation prompt, TODO better
        // maybe can make a dialog that opens when button is clicked, then yes no goes to handle favourite?
        if (!window.confirm("Remove favourite charger?")) {
            //do nothing if cancel confirmation
            return;
        }

        const response = await FavouriteChargerRemove(userEmail, IDCharger);

        if (response.status === 'success') {
            toast.success("Removed from favourites!")
            fetchFavouriteChargers();
        } else {
            toast.error(<div>{response.message}<br />{response.reason}</div>);
        }

    }

    // Component that formats charger information for display. Reads from favouriteChargerInfo.
    function FormatFavourites() {
        let result = [];

        for (var i = 0; i < favouriteChargerInfo.length; i++) {
            let id = favouriteChargerInfo[i].id;
            var predictedValue = "";
            if (favouriteChargerInfo[i].rate_predicted != "") {
                //get time now, then get index for next hour
                //0 index is 12AM etc. so get the time then see next hour
                //then put this value in the popup value
                var timeNow = FormatDateTime(DateTime.now(), "T");

                var currentHour = parseInt(timeNow.split(":")[0]);

                var predictedArray = JSON.parse(favouriteChargerInfo[i].rate_predicted);

                predictedValue = predictedArray[currentHour + 1];

            }

            result.push(
                <div className="lg:flex py-4 lg:px-10 px-3 bg-white rounded-lg grid grid-rows-4" key={id}>
                    <div className="w-full md:w-4/5 row-span-3">
                        <CardContent elementName={favouriteChargerInfo[i].name}>
                            <div><span className="uppercase font-semibold text-sm">Location:</span> {favouriteChargerInfo[i].address}</div>
                            <div><span className="uppercase font-semibold text-sm">Solar Voltage In:</span> {favouriteChargerInfo[i].pv_voltage_in} V</div>
                            <div><span className="uppercase font-semibold text-sm">Solar Current In:</span> {favouriteChargerInfo[i].pv_current_in} A</div>
                            <div><span className="uppercase font-semibold text-sm">Solar Voltage Out:</span> {favouriteChargerInfo[i].pv_voltage_out} V</div>
                            <div><span className="uppercase font-semibold text-sm">Solar Current Out:</span> {favouriteChargerInfo[i].pv_current_out} A</div>
                            <div><span className="uppercase font-semibold text-sm">Price Rate:</span> ${favouriteChargerInfo[i].rate_current} / kWh</div>
                            <span className="uppercase font-semibold text-sm">Predicted Rate (Next Hour):</span> ${predictedValue !== "" ? predictedValue : "--"} / kWh
                        </CardContent>
                    </div>
                    <CardButton id={id} onClick={() => handleFavouriteRemove(id)} icon="heart-broken fa-lg" color="red"></CardButton>
                </div>
            )
        }

        return result;
    }

    return (
        <div className="min-h-screen bg-gray-900"
            style={{
                backgroundImage: "url('battery.png')",
                backgroundSize: "100%",
                backgroundRepeat: "repeat"
            }}>
            <Toast />
            <Navbar transparent />

            <main>
                <section className="w-full h-full">
                    <div className="relative container mx-auto px-4 h-full bg-gray-900">
                        <div className="h-40">
                            <div className="flex content-center items-center justify-center h-full w-full font-semibold text-3xl text-white">Your Favourite Chargers</div>
                        </div>
                        <div className="grid md:grid-cols-2 gap-4">
                            {favouriteChargerInfo && <FormatFavourites />}
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
