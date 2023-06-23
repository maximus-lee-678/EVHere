// React imports
import React, { useState, useEffect } from 'react';

// Standard imports
import Navbar from '../SharedComponents/Navbar';
import Toast, { toast } from '../SharedComponents/Toast';

// API endpoints imports
import { ChargeCurrentGet } from '../API/API';

// Component imports
import AddCharge from './AddCharge';
import FinishCharge from './FinishCharge';

export default function AddChargingHistory() {
    const userEmail = localStorage.getItem("user_email");

    const [hasChargeCurrent, setHasChargeCurrent] = useState();

    // Function that checks if user has a current charge. Called on page load, populates hasChargeCurrent.
    async function fetchUserCurrentCharge() {
        const response = await ChargeCurrentGet(userEmail);

        response['data'] ? setHasChargeCurrent(true) : setHasChargeCurrent(false);
    }

    useEffect(() => {
        fetchUserCurrentCharge();
    }, []);

    return (
        <div>
            <Toast />
            <Navbar transparent />

            <main>
                {hasChargeCurrent && hasChargeCurrent ? <FinishCharge /> : <AddCharge />}
            </main >
        </div>
    )
}
