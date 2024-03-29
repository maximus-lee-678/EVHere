// React imports
import React, { useState, useEffect, useCallback } from 'react';

// Standard imports
import Navbar from "../SharedComponents/Navbar";
import Toast, { toast } from '../SharedComponents/Toast';
import { CardContent, CardButton, DashboardCard, ChargingCard } from '../SharedComponents/Card';
import Form, { FormInputField } from '../SharedComponents/Form';

// API endpoints imports
import { UserInfoGet, UserInfoUpdate } from '../API/API';

export default function Profile() {
    const userEmail = localStorage.getItem("user_email");


    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [fullName, setFullName] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [newPasswordConfirm, setNewPasswordConfirm] = useState('');

    // Function that gets user's current charge. Called on page load, populates chargeCurrentDetails.
    const fetchUserInfo = useCallback(async () => {
        const response = await UserInfoGet(userEmail);

        // result is boolean of status
        if (response.status === 'success' && response.data !== null) {
            setUsername(response.data.username);
            setEmail(response.data.email);
            setPhoneNumber(response.data.phone_no);
            setFullName(response.data.full_name);
        }
    }, [userEmail]);

    useEffect(() => {
        fetchUserInfo();
    }, [fetchUserInfo]);

    // Function that updates user info. Called upon corresponding button selection.
    async function handleUpdate(event) {
        event.preventDefault();

        if (newPassword !== newPasswordConfirm) {
            toast.error(<div>Passwords do not match!</div>);
            return;
        }

        if (!window.confirm("Update account with these details?")) {
            //do nothing if cancel confirmation
            return;
        }

        const response = await UserInfoUpdate(userEmail, email, fullName,
            username, phoneNumber, newPassword);

        // result is boolean of status
        if (response.status === 'success') {
            toast.success(response.message);

            // store the user in localStorage
            localStorage.setItem('user_email', response.data);
        } else {
            toast.error(<div>{response.message}<br />{response.reason}</div>);
        }
    }

    return (
        <div className="min-h-screen bg-gray-900">
            <Toast />
            <Navbar transparent />

            <main>
                <div className="relative container mx-auto px-4 h-full bg-gray-900">
                    <div className="h-40">
                        <div className="flex content-center items-center justify-center h-full w-full font-semibold text-3xl text-white">Profile</div>
                    </div>
                </div>
                <Form>
                    <div className="flex md:px-4">
                        <FormInputField type="email"
                            value={email}
                            elementName="Email"
                            icon="envelope"
                            id="email"
                            placeholder="Enter Email Address . . ."
                            onChange={(event) => setEmail(event.target.value)} />
                    </div>
                    <div className="flex md:px-4">
                        <FormInputField
                            value={fullName}
                            elementName="Full name"
                            icon="id-card"
                            id="fullname"
                            placeholder="Enter Full Name . . ."
                            onChange={(event) => setFullName(event.target.value)} />
                    </div>
                    <div className="flex md:px-4">
                        <FormInputField
                            value={username}
                            elementName="Username"
                            icon="user"
                            id="username"
                            placeholder="Enter Username . . ."
                            onChange={(event) => setUsername(event.target.value)} />
                    </div>
                    <div className="flex items-center md:px-4">
                        <FormInputField type="tel"
                            value={phoneNumber}
                            elementName="Phone number"
                            icon="phone"
                            id="phone-number"
                            placeholder="Enter Phone Number . . ."
                            onChange={(event) => setPhoneNumber(event.target.value)} />
                    </div>
                    <div className="flex items-center md:px-4">
                        <FormInputField type="password"
                            value={newPassword}
                            elementName="Change Password"
                            icon="key"
                            id="password-new"
                            placeholder="Enter New Password . . ."
                            onChange={(event) => setNewPassword(event.target.value)} />
                    </div>
                    <div className="flex items-center md:px-4">
                        <FormInputField type="password"
                            value={newPasswordConfirm}
                            elementName="Confirm New Password"
                            icon="key"
                            id="password-new-confirm"
                            placeholder="Confirm New Password . . ."
                            onChange={(event) => setNewPasswordConfirm(event.target.value)} />
                    </div>

                    <CardButton text="Save Profile" icon="edit" color="green" onClick={(event) => handleUpdate(event)} id="profile-save"></CardButton>
                </Form>

            </main>
        </div>
    );
}