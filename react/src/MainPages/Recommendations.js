import React, { useState, useMemo, useEffect } from 'react';
import Navbar from "../Shared/Navbar";
import Map from "../Map/Map";

export default function Recommendations() {
    return (
        <div className="min-h-screen bg-gray-900 "
        >
            <Navbar transparent />
            <main>
                <section className="w-full h-full">
                    <div className="relative container mx-auto px-4 h-full bg-gray-900">
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
                                        <select
                                            id="vehicleName"
                                            className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                            style={{ transition: "all .15s ease" }}
                                        >
                                            <option className="border-0 px-3 py-3 text-gray-700" value="Vehicle1Name">Vehicle 1 Name (S/N)</option>
                                            <option className="border-0 px-3 py-3 text-gray-700" value="Vehicle2Name">Vehicle 2 Name (S/N)</option>
                                        </select>
                                    </div>
                                    <div className="grid gap-4">
                                        <div className="p-2 rounded-md hover:bg-gray-200 cursor-pointer">
                                            <div className="inline-flex h-full align-middle">
                                                <i className="fas fa-map-marker-alt fa-2xl"></i>
                                            </div>

                                            <div className="ml-4 inline-block">
                                                <div className="uppercase text-gray-700 font-bold">Best value for money:</div>
                                                <div>
                                                    Shell Recharge Punggol
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
                                                    Bukit Merah / Telok Blangah Rise / Blk 32
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
                                                    Shell Recharge Punggol
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>

                            <div className="col-span-2">
                                <Map desiredZoom={11} mapWidth={"100%"} mapHeight={"70vh"} />
                            </div>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
