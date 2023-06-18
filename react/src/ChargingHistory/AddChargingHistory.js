import React, { useState, useEffect } from 'react';
import Navbar from '../Shared/Navbar';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { ChargeHistoryGet } from '../API/API';

import AddCharge from './AddCharge';
import FinishCharge from './FinishCharge';

export default function AddChargingHistory() {
    const userEmail = localStorage.getItem("user_email");

    const [hasChargeCurrent, setHasChargeCurrent] = useState();

    // Function that checks if user has a current charge. Called on page load, populates hasChargeCurrent.
    async function fetchUserCurrentCharge() {
        // Store success status: if user has a current charge it will return success, and vice versa.
        setHasChargeCurrent(await ChargeHistoryGet(userEmail).success);
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
