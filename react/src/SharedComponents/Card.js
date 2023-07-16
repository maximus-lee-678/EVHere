import React from 'react';
import { Link } from 'react-router-dom';

export function CardContent(props) {
    const { elementName, children } = props;


    return (
        <div>
            <div className="font-bold text-xl">{elementName}</div>
            <div>
                {children}
            </div>
        </div>
    );
};

export function CardButton(props) {
    const { id, onClick, color, icon, text } = props;

    return (
        <div className="flex justify-center items-center">
            <button id={id}
                className={"bg-" + color + "-400 hover:bg-" + color + "-300  px-5 py-4 rounded-full text-white max-h-14"}
                onClick={() => onClick(id)}
            >
                <i className={"fas fa-" + icon}></i>
                <span className={text != null ? "ml-2" : ""}>{text}</span>
            </button>
        </div>
    );
};


export function DashboardCard(props) {
    const { elementName, children, link, icon, lower, color } = props;

    const colorVariants = {
        blueHover: 'hover:bg-blue-50',
        blueBG: 'bg-blue-400',
        redHover: 'hover:bg-red-50',
        redBG: 'bg-red-400',
        greenHover: 'hover:bg-green-50',
        greenBG: 'bg-green-400',
    }

    // console.log("wtf", colorVariants[color + "Hover"]);

    if (lower) {
        return (
            <div className="md:pt-6 w-full md:w-4/12 px-4 text-center">
                <Link to={link} className={`${colorVariants[color + "Hover"]} relative flex flex-col min-w-0 break-words bg-white cursor-pointer w-full mb-8 shadow-lg rounded-lg`}>
                    <div className="px-4 py-5 flex-auto">
                        <div className={`${colorVariants[color + "BG"]} text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full`}>
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
            <Link to={link} className={`${colorVariants[color + "Hover"]} relative flex flex-col min-w-0 break-words bg-white cursor-pointer w-full mb-8 shadow-lg rounded-lg`}>
                <div className="px-4 py-5 flex-auto">
                    <div className={`${colorVariants[color + "BG"]} text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full`}>
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
};

export function ChargingCard(props) {
    const { elementName, vName, SN, currEnergyDrawn, startTime, timeElapsed } = props;
    return (
        <div className="container mx-auto px-4 -mt-52">
            <div className="flex justify-center w-full">
                <div className="w-full md:w-1/2 px-4">
                    <div className="relative flex flex-col min-w-0 break-words bg-lime-100 mb-8 shadow-lg rounded-lg">
                        <div className="px-4 py-5 flex-auto">
                            <h6 className="text-lg font-semibold uppercase text-center">{elementName}</h6>

                            <div className="space-y-1 grid grid-cols-2 text-center">
                                <div>Vehicle: {vName} ({SN})</div>
                                <div>Energy Drawn: {currEnergyDrawn}</div>
                                <div>Started at: {startTime}</div>
                                <div>Time elapsed: {timeElapsed}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}