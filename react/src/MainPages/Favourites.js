import React, { useState, useEffect } from 'react';
import Navbar from "../Shared/Navbar";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

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
        fetchFavouriteChargers()
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
                <div className="flex py-4 px-10 bg-white rounded-lg">
                    <div className="w-4/5">
                        <div className="font-bold text-xl">{favouriteChargerInfo[i].name}</div>
                        <div>Provider: {favouriteChargerInfo[i].provider}</div>
                        <div>Power: {favouriteChargerInfo[i].kilowatts || 0} kW</div>
                        <div>Connectors: {favouriteChargerInfo[i].connectors}</div>
                        <div>Location: {favouriteChargerInfo[i].address}</div>
                        <div>Hours: {favouriteChargerInfo[i].twenty_four_hours === 'TRUE' ? '24 hours' : 'not 24 hours'}</div>
                    </div>
                    <div className="w-1/5 flex justify-center items-center">
                        <button id={id}
                            className="bg-red-400 hover:bg-red-300 p-5 rounded-full text-white"
                            onClick={() => handleFavouriteRemove(id)}>
                            <i className="fas fa-heart-broken fa-xl" style={{ color: "#ffffff" }}></i>
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
                backgroundImage:
                    "url('battery.png')",
                backgroundSize: "100%",
                backgroundRepeat: "repeat"
            }}>
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
