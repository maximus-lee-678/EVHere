import React from 'react';

export default function Form(props) {
    const { elementName, onSubmit, backgroundImageURL, popup, children } = props;

    if (popup) {
        return (
            <div className="relative top-24 mx-auto p-5 border w-96 shadow-lg rounded-md bg-gray-200">
                <div className="flex-auto px-4 lg:px-10 py-10 pt-0 mt-6">
                    <div className="text-center mb-3">
                        <h6 className="text-gray-600 text-sm font-bold">
                            {elementName}
                        </h6>
                    </div>
                    <form onSubmit={onSubmit}>
                        {children}
                    </form>
                </div>
            </div>
        );
    };

    return (
        <section className="absolute w-full h-full">
            <div className="absolute top-0 w-full h-full bg-gray-900 min-h-screen"
                style={{
                    backgroundImage:
                        `url('${backgroundImageURL}')`,
                    backgroundSize: "100%",
                    backgroundRepeat: "no-repeat"
                }}></div>
            <div className="container mx-auto px-4 h-full">
                <div className="flex content-center items-center justify-center h-full">
                    <div className="w-full lg:w-4/12 px-4">
                        <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-gray-300 border-0">
                            <div className="flex-auto px-4 lg:px-10 py-10 pt-0 mt-6">
                                <div className="text-center mb-3">
                                    <h6 className="text-gray-600 text-sm font-bold">
                                        {elementName}
                                    </h6>
                                </div>
                                <form onSubmit={onSubmit}>
                                    {children}
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    );
};

export function FormInputField(props) {
    const { elementName, icon, id, type, value, placeholder, onChange } = props;

    return (
        <div className="relative w-full mb-3">
            <label
                className="block uppercase text-gray-700 text-xs font-bold mb-2"
                htmlFor={id}
            >
                <i className={icon != null ? "fas fa-" + icon + " mr-2" : "hidden"}></i>
                {elementName}
            </label>
            <input
                id={id}
                type={type || "text"}
                className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                style={{ transition: "all .15s ease" }}
                value={value}
                placeholder={placeholder}
                onChange={onChange}
            />
        </div>
    );
};

export function FormInputSelect(props) {
    const { elementName, id, value, onChange, options } = props;

    return (
        <div className="relative w-full mb-3">
            <label
                className="block uppercase text-gray-700 text-xs font-bold mb-2"
                htmlFor={id}
            >
                {elementName}
            </label>
            <select
                id={id}
                className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                style={{ transition: "all .15s ease" }}
                value={value}
                onChange={onChange}
            >
                {options}
            </select>
        </div>
    );
};

export function FormButton(props) {
    const { elementName } = props;

    return (
        <div className="text-center mt-6">
            <button
                className="bg-gray-900 text-white hover:bg-gray-700 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full"
                type="submit"
                style={{ transition: "all .15s ease" }}
            >
                {elementName}
            </button>
        </div>
    );
};