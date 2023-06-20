// React imports
import React, { useState, useEffect } from 'react';

// Standard imports
import Navbar from '../SharedComponents/Navbar';
import Toast, { toast } from '../SharedComponents/Toast';

// API endpoints imports
import { FavouriteChargerGet, FavouriteChargerRemove } from '../API/API';

export default function Favourites() {
    const userEmail = localStorage.getItem("user_email");
    const [favouriteChargerInfo, setFavouriteChargerInfo] = useState();

    // Function that loads user's favourited chargers. Called on page load, populates favouriteChargerInfo.
    async function fetchFavouriteChargers() {
        const response = await FavouriteChargerGet(userEmail);

        // If success returned, store chargers
        if (response.success) {
            setFavouriteChargerInfo(response['content']);
        }
        else {
            toast.error(<div>{response.api_response}<br />{response.reason}</div>);
            setFavouriteChargerInfo([]);
        }
    }

    useEffect(() => {
        fetchFavouriteChargers();
    }, []);

    // Function that removes a user's favourited charger. Called when user clicks corresponding remove button.
    async function handleFavouriteRemove(IDCharger) {
        // Ugly confirmation prompt, TODO better
        // maybe can make a dialog that opens when button is clicked, then yes no goes to handle favourite?
        if (!window.confirm("Remove favourite charger?")) {
            //do nothing if cancel confirmation
            return;
        }

        const response = await FavouriteChargerRemove(userEmail, IDCharger);

        if (response.success) {
            toast.success("Removed from favourites!")
            fetchFavouriteChargers();
        } else {
            toast.error(<div>{response.api_response}<br />{response.reason}</div>);
        }

    }

    // Component that formats charger information for display. Reads from favouriteChargerInfo.
    function FormatFavourites() {
        let result = [];

        for (var i = 0; i < favouriteChargerInfo.length; i++) {
            let id = favouriteChargerInfo[i].id;

            result.push(
                <div className="lg:flex py-4 lg:px-10 px-3 bg-white rounded-lg grid grid-rows-4">
                    <div className="lg:w-4/5 row-span-3">
                        <div className="font-bold text-xl">{favouriteChargerInfo[i].name}</div>
                        <div><span className="uppercase font-semibold text-sm">Provider:</span> {favouriteChargerInfo[i].provider}</div>
                        <div><span className="uppercase font-semibold text-sm">Power:</span> {favouriteChargerInfo[i].kilowatts || 0} kW</div>
                        <div><span className="uppercase font-semibold text-sm">Connectors:</span> {favouriteChargerInfo[i].connectors}</div>
                        <div><span className="uppercase font-semibold text-sm">Location:</span> {favouriteChargerInfo[i].address}</div>
                        <div><span className="uppercase font-semibold text-sm">Hours:</span> {favouriteChargerInfo[i].twenty_four_hours === 'TRUE' ? '24 hours' : 'Not 24 hours'}</div>
                    </div>
                    <div className="lg:w-1/5 flex justify-center lg:items-center">
                        <button id={id}
                            className="bg-red-400 hover:bg-red-300 px-5 py-4 rounded-full text-white max-h-14"
                            onClick={() => handleFavouriteRemove(id)}>
                            <i className="fas fa-heart-broken fa-lg" style={{ color: "#ffffff" }}></i>
                        </button>
                    </div>
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
                        <div className="grid grid-cols-2 gap-4">
                            {favouriteChargerInfo && <FormatFavourites />}
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
