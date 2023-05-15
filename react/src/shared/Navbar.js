import React, { useState } from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
    const [loggedIn, setLoggedIn] = useState('');

    if (loggedIn == '') {
        //not logged in
        if (localStorage.getItem("user_email") != "" && localStorage.getItem("user_email") == null) {
            setLoggedIn("false");
        }
        //if logged in
        else {
            setLoggedIn("true");
        }
    }
   


    return (
        <nav class="flex items-center justify-between flex-wrap bg-cyan-500 p-5">
            <div class="flex items-center flex-shrink-0 text-white mr-6">
                <span class="font-semibold text-xl tracking-tight">EVHere</span>
            </div>
            <div class="block lg:hidden">
                <button class="flex items-center px-3 py-2 border rounded text-cyan-200 border-cyan-400 hover:text-white hover:border-white" onClick={menuButtonClicked}>
                    <svg class="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><title>Menu</title><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" /></svg>
                </button>
            </div>
            <div id="menu" class="hidden w-full flex-grow lg:flex lg:items-center lg:w-auto">
                <div class="text-sm lg:flex-grow">
                    <a href="#responsive-header" class="block mt-4 lg:inline-block lg:mt-0 text-cyan-200 hover:text-white mr-4">
                        Docs
                    </a>
                    <a href="#responsive-header" class="block mt-4 lg:inline-block lg:mt-0 text-cyan-200 hover:text-white mr-4">
                        Examples
                    </a>
                    <a href="#responsive-header" class="block mt-4 lg:inline-block lg:mt-0 text-cyan-200 hover:text-white mr-4">
                        Blog
                    </a>
                    <a href="#responsive-header" class="block mt-4 lg:inline-block lg:mt-0 text-cyan-200 hover:text-white mr-4">
                        Examples
                    </a>
                    <a href="#responsive-header" class="block mt-4 lg:inline-block lg:mt-0 text-cyan-200 hover:text-white">
                        Blog
                    </a>
                </div>
                <div>
                    <Link to="/Register" id="signupButton" class={
                        loggedIn == "true" ? "hidden text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0 mr-4" : "inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0 mr-4"
                    }>Sign up</Link>
                    <Link to="/Login" id="loginButton" class={
                        loggedIn == "true" ? "hidden text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0 mr-4" : "inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0 mr-4"
                    }>Login</Link>
                    <button id="logoutButton" onClick={handleLogout} class={
                        loggedIn == "false" ? "hidden text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0 mr-4" : "inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0 mr-4"
                    }>Logout</button>
                </div>
            </div>
        </nav>
    )
}

function handleLogout() {
    console.log(localStorage.getItem("user_email"));
    localStorage.removeItem("user_email");

    // reload page
    window.location.reload();
}


function menuButtonClicked() {
    const menu = document.getElementById("menu");
    menu.classList.toggle("hidden");
    console.log(menu.classList);
}



