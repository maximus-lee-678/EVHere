import React, { useState, useEffect } from 'react';
import Navbar from '../shared/Navbar';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import AddCharge from '../ChargingHistory/AddCharge';
import FinishCharge from '../ChargingHistory/FinishCharge';

export default function AddChargingHistory() {
    const userEmail = localStorage.getItem("user_email");

    const [hasChargeCurrent, setHasChargeCurrent] = useState();

    // Function that checks if user has a current charge. Called on page load, populates hasChargeCurrent.
    async function fetchUserCurrentCharge() {
        // Forms GET header
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: userEmail })
        };

        // Store response
        let response;
        await fetch('/api/get_charge_current', requestOptions)
            .then(res => res.json())
            .then(data => { response = data })
            .catch(err => console.log(err));

        // Store success status: if user has a current charge it will successfully retrieve it, and vice versa.
        setHasChargeCurrent(response.success);
    }

    useEffect(() => {
        fetchUserCurrentCharge();
    }, []);

    return (
        <div>
            <ToastContainer position="top-center"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
                theme="colored" />
            <Navbar transparent />
            <main>
                {hasChargeCurrent && hasChargeCurrent ? <FinishCharge /> : <AddCharge />}
            </main >
        </div>
    )
}
