import React from 'react';
import Navbar from "../SharedComponents/Navbar";
import { CardButton, CardContent } from '../SharedComponents/Card';

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

                <div className="relative top-24 mx-auto py-5 px-3 bg-white w-11/12 md:w-1/2 rounded-lg text-center space-y-4">
                    <CardContent elementName="Full Name">
                        <div>
                            <i className="fas fa-user mr-2"></i>
                            (Username here)
                        </div>
                        <div>
                            <i className="fas fa-envelope mr-2"></i>
                            (Email address here)
                        </div>
                        
                        <div>
                            <i className="fas fa-phone mr-2"></i>
                            (Phone number here)
                        </div>
                    </CardContent>

                    <CardButton text="Delete account" icon="trash" color="red" onClick="deleteFunction" id="userID"></CardButton>
                </div>
                
            </main>
        </div>
    );
}