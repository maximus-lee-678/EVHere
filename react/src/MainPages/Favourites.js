import React, { useState, useEffect } from 'react';
import Navbar from "../shared/Navbar";

export default function Favourites() {
    const userEmail = localStorage.getItem("user_email");
    const [favouriteChargerInfo, setFavouriteChargerInfo] = useState();

    // Function that loads user's favourited chargers. Called on page load, populates favouriteChargerInfo.
    async function fetchFavouriteChargers() {
        // Forms POST header
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: userEmail })
        };

        // JSON returns keys 'result' & 'content'
        await fetch('/api/get_favourite_chargers', requestOptions)
            .then(res => res.json())
            .then(data => {
                if ('content' in data) {
                    setFavouriteChargerInfo(data['content']);
                }
                else {
                    alert("No favourites found!");
                }
            })
            .catch(err => console.log(err));
    }

    useEffect(() => {
        fetchFavouriteChargers()
    }, []);

    // Component that formats charger information for display. Reads from favouriteChargerInfo.
    function FormatFavourites() {
        let result = [];

        for (var i = 0; i < favouriteChargerInfo.length; i++) {
            result.push(
                <div className="flex py-4 px-10 bg-white rounded-lg">
                    <div className="w-4/5">
                        <div className="font-bold text-xl">{favouriteChargerInfo[i].name}</div>
                        <div>Provider: {favouriteChargerInfo[i].provider}</div>
                        <div>Power: {favouriteChargerInfo[i].kilowatts || 0} kW</div>
                        <div>Connectors: {favouriteChargerInfo[i].connectors}</div>
                        <div>Location: {favouriteChargerInfo[i].address}</div>
                        <div>Hours: {favouriteChargerInfo[i].twenty_four_hours == 'TRUE' ? '24 hours' : 'not 24 hours'}</div>
                    </div>
                    <div className="w-1/5 flex justify-center items-center">
                        <button className="bg-red-400 hover:bg-red-900 p-5 rounded-full text-white">
                            <i className="fas fa-heart fa-xl" style={{ color: "#ffffff" }}></i>
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
