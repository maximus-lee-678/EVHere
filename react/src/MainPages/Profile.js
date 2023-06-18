import React from 'react';
import Navbar from "../Shared/Navbar";
export default function Profile() {


    return (
        <div className="min-h-screen bg-gray-900">
            <Navbar transparent />
            <main>
                <div className="relative container mx-auto px-4 h-full bg-gray-900">
                    <div className="h-40">
                        <div className="flex content-center items-center justify-center h-full w-full font-semibold text-3xl text-white">Profile</div>
                    </div>
                </div>
            </main>
        </div>
    );
}