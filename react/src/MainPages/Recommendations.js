import React, { useState, useMemo, useEffect } from 'react';
import Navbar from "../shared/Navbar";
import Map from "../Map/Map";

export default function Recommendations() {
    return (
        <div className="min-h-screen bg-gray-900 "
        >
            <Navbar transparent />
            <main>
                <section className="bg-gray-900 w-full h-full">
                    <div className="relative container mx-auto px-4 h-full">
                        <div className="h-40">
                            <div className="flex content-center items-center justify-center h-full w-full font-semibold text-3xl text-white">Map</div>
                        </div>
                        <div className="grid grid-cols-3">
                            <div className="bg-white col-span-1 px-7">
                                <div className="h-24">
                                    <div className="flex content-center items-center justify-center h-full w-full font-semibold text-2xl">Recommended</div>
                                </div>
                                <div>
                                    <div className="mb-12">
                                        <label className="block uppercase text-gray-700 text-xs font-bold mb-2">
                                            Vehicle
                                        </label>
                                        <div>(Vehicle name)</div>
                                    </div>
                                    <div className="grid gap-4">
                                        <div className="p-2 rounded-md hover:bg-gray-200 cursor-pointer">
                                            <div className="inline-flex h-full align-middle">
                                                <i className="fas fa-map-marker-alt fa-2xl"></i>
                                            </div>

                                            <div className="ml-4 inline-block">
                                                <div className="uppercase text-gray-700 font-bold">Best value for money:</div>
                                                <div>
                                                    Charger name
                                                </div>
                                            </div>
                                        </div>
                                        <div className="p-2 rounded-md hover:bg-gray-200 cursor-pointer">
                                            <div className="inline-flex h-full align-middle">
                                                <i className="fas fa-map-marker-alt fa-2xl"></i>
                                            </div>

                                            <div className="ml-4 inline-block">
                                                <div className="uppercase text-gray-700 font-bold">Nearest to me:</div>
                                                <div>
                                                    Charger name
                                                </div>
                                            </div>
                                        </div>
                                        <div className="p-2 rounded-md hover:bg-gray-200 cursor-pointer">
                                            <div className="inline-flex h-full align-middle">
                                                <i className="fas fa-map-marker-alt fa-2xl"></i>
                                            </div>

                                            <div className="ml-4 inline-block">
                                                <div className="uppercase text-gray-700 font-bold">Fastest charging speed:</div>
                                                <div>
                                                    Charger name
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>

                            <div className="col-span-2">
                                <Map />
                            </div>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
