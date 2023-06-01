import React from 'react';
import Navbar from "../shared/Navbar";

export default function Favourites() {
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

                            <div className="flex py-4 px-10 bg-white rounded-lg">
                                <div className="w-4/5">
                                    <div className="font-bold text-xl">Jalan Kayu URA Carpark</div>
                                    <div>Brand: Charge+</div>
                                    <div>Type: Combo 2 (DC30.0)</div>
                                    <div>Rate: $0.5582/kWh</div>
                                    <div>Location: Opp Jln tari Lilin Singapore 799487, Lot 7, Lot 6</div>
                                    <div>Hours: 24 hours</div>
                                </div>
                                <div className="w-1/5 flex justify-center items-center">
                                    <button className="bg-red-400 hover:bg-red-900 p-5 rounded-full text-white">
                                        <i className="fas fa-heart fa-xl" style={{ color: "#ffffff" }}></i>
                                    </button>
                                </div>
                            </div>
                            <div className="flex py-4 px-10 bg-white rounded-lg">
                                <div className="w-4/5">
                                    <div className="font-bold text-xl">Shell Recharge Punggol</div>
                                    <div>Brand: Shell Recharge / Greenlots</div>
                                    <div>Type: Type 2 (AC43.0)</div>
                                    <div>Rate: $0.55/kWh</div>
                                    <div>Location: 821 Punggol Rd Singapore 829169</div>
                                    <div>Hours: 24 hours</div>
                                </div>
                                <div className="w-1/5 flex justify-center items-center">
                                    <button className="bg-red-400 hover:bg-red-900 p-5 rounded-full text-white">
                                        <i className="fas fa-heart fa-xl" style={{ color: "#ffffff" }}></i>
                                    </button>
                                </div>
                            </div>
                            <div className="flex py-4 px-10 bg-white rounded-lg">
                                <div className="w-4/5">
                                    <div className="font-bold text-xl">Bukit Merah / Telok Blangah Rise / Blk 32</div>
                                    <div>Brand: Bluecharge</div>
                                    <div>Type: Type 2 (AC3.7)</div>
                                    <div>Rate: $1.0/h</div>
                                    <div>Location: 32 Telok Blangah Rise Singapore 090032</div>
                                    <div>Hours: 24 hours</div>
                                </div>
                                <div className="w-1/5 flex justify-center items-center">
                                    <button className="bg-red-400 hover:bg-red-900 p-5 rounded-full text-white">
                                        <i className="fas fa-heart fa-xl" style={{ color: "#ffffff" }}></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
