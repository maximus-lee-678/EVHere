import React, { useState, useMemo, useEffect } from 'react';
import Navbar from "../shared/Navbar";
import Map from "../Map/Map";

export default function Recommendations() {
    return (
        <div className="min-h-screen bg-gray-900 "
            style={{
                backgroundImage:
                    "url('favourites.png')",
                backgroundSize: "100%",
                backgroundRepeat: "repeat"
            }}>
            <Navbar transparent />
            <main>
                <section className="bg-gray-900 w-full h-full">
                    <div className="relative container mx-auto px-4 h-full">
                        <div className="h-40">
                            <div className="flex content-center items-center justify-center h-full w-full font-semibold text-3xl text-white">Get recommendations on the go</div>
                        </div>
                        <div className="grid">
                            <Map />
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
