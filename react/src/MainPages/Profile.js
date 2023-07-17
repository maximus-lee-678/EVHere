import React, { useState } from 'react';
import Navbar from "../SharedComponents/Navbar";
import { CardButton, CardContent } from '../SharedComponents/Card';
import Form, { FormInputField } from '../SharedComponents/Form';

export default function Profile() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [fullName, setFullName] = useState('');

    return (
        <div className="min-h-screen bg-gray-900">
            <Navbar transparent />
            <main>
                <div className="relative container mx-auto px-4 h-full bg-gray-900">
                    <div className="h-40">
                        <div className="flex content-center items-center justify-center h-full w-full font-semibold text-3xl text-white">Profile</div>
                    </div>
                </div>

                <div className="relative mx-auto py-5 px-3 bg-white w-11/12 md:w-1/2 rounded-lg space-y-4">
                    <CardContent>
                        <div className="flex md:px-4">
                            <FormInputField
                            value={fullName} 
                            elementName="Full name"
                            icon="id-card"
                            id="fullname" 
                            placeholder="Full name here"
                            onChange={(event) => setFullName(event.target.value)}/>
                        </div>
                        <div className="flex md:px-4">
                            <FormInputField
                            value={username} 
                            elementName="Username"
                            icon="user"
                            id="username" 
                            placeholder="Username here"
                            onChange={(event) => setUsername(event.target.value)}/>
                        </div>
                        <div className="flex md:px-4">
                            <FormInputField 
                            value={email} 
                            elementName="Email"
                            icon="envelope"
                            id="email" 
                            placeholder="Email address here"
                            onChange={(event) => setEmail(event.target.value)}/>
                        </div>
                        
                        <div className="flex items-center md:px-4">
                            <FormInputField type="tel"
                            value={phoneNumber}
                            elementName="Phone number"
                            icon="phone"
                            id="phoneNumber"
                            placeholder="Phone number here"
                            onChange={(event) => setPhoneNumber(event.target.value)}/>
                        </div>
                    </CardContent>

                    <CardButton text="Save profile" icon="edit" color="green" onClick="editFunction" id="userID"></CardButton>
                    <CardButton text="Delete account" icon="trash" color="red" onClick="deleteFunction" id="userID"></CardButton>
                </div>
                
            </main>
        </div>
    );
}