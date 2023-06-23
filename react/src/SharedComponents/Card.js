import React from 'react';
import { Link } from 'react-router-dom';

export function CardContent(props) {
    const { elementName, type, children } = props;

    //favourite page cards
    if (type == "Charger") {
        return (
            <div className="lg:w-4/5 row-span-3">
                <div className="font-bold text-xl">{elementName}</div>
                <div>
                    {children}
                </div>
            </div>
        );
    }
    //vehicles page cards
    else if (type == "Vehicle") {
        return (
            <div className="w-4/5">
                <div className="font-bold text-xl">{elementName}</div>
                <div>
                    {children}
                </div>
            </div>
        )
    }
    //dashboard page cards
    else if (type == "Info") {
        const { link, color, icon, lower } = props;
        if (lower) {
            return (
                <div className="pt-6 w-full md:w-4/12 px-4 text-center">
                <Link to={link} className={"hover:bg-" + color + "-50 relative flex flex-col min-w-0 break-words bg-white cursor-pointer w-full mb-8 shadow-lg rounded-lg"}>
                  <div className="px-4 py-5 flex-auto">
                    <div className={"bg-" + color + "-400 text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full"}>
                      <i className={"fas fa-" + icon}></i>
                    </div>
                    <h6 className="text-xl font-semibold">{elementName}</h6>
                    <p className="mt-2 mb-4 text-gray-600">
                        {children}
                    </p>
                  </div>
                </Link>
            </div>
            )
        }
        return (
            <div className="w-full md:w-4/12 px-4 text-center">
                <Link to={link} className={"hover:bg-" + color + "-50 relative flex flex-col min-w-0 break-words bg-white cursor-pointer w-full mb-8 shadow-lg rounded-lg"}>
                  <div className="px-4 py-5 flex-auto">
                    <div className={"bg-" + color + "-400 text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full"}>
                      <i className={"fas fa-" + icon}></i>
                    </div>
                    <h6 className="text-xl font-semibold">{elementName}</h6>
                    <p className="mt-2 mb-4 text-gray-600">
                        {children}
                    </p>
                  </div>
                </Link>
            </div>
        );
    }
    else if (type == "CurrentCharging") {
        const { vName, SN, currPercent, startTime, timeElapsed } = props;
        return (
            <div className="container mx-auto px-4 -mt-52">
                <div className="flex justify-center w-full">
                <div className="w-full md:w-1/2 px-4">
                    <div className="relative flex flex-col min-w-0 break-words bg-lime-100 mb-8 shadow-lg rounded-lg">
                    <div className="px-4 py-5 flex-auto">
                        <h6 className="text-lg font-semibold uppercase text-center">{elementName}</h6>

                        <div className="space-y-1 grid grid-cols-2 text-center">
                        <div>Vehicle: {vName} ({SN})</div>
                        <div>Current percentage: {currPercent}</div>
                        <div>Started at: {startTime}</div>
                        <div>Time elapsed: {timeElapsed}</div>
                        </div>
                    </div>
                    </div>
                </div>
                </div>
            </div>
      )
    };

    
};

export function CardButton(props) {
    const { id, onClick, type, buttonName } = props;

    if (type == "Charger") {
        return (
            <div className="lg:w-1/5 flex justify-center lg:items-center">
                <button id={id}
                    className="bg-red-400 hover:bg-red-300 px-5 py-4 rounded-full text-white max-h-14"
                    onClick={() => onClick(id)}>
                    <i className="fas fa-heart-broken fa-lg" style={{ color: "#ffffff" }}></i>
                </button>
            </div>
        );
    }
    else if (type == "Vehicle") {
        return (
            <div className="w-1/5 flex justify-center items-center">
                <button id={id}
                    className="bg-red-400 hover:bg-red-300 px-5 py-4 rounded-full text-white"
                    onClick={() => onClick(id)}>
                    <i className="fas fa-trash fa-lg" style={{ color: "#ffffff" }}></i>
                </button>
            </div>
        );
    }
    else if (type == "Info") {

    }
};