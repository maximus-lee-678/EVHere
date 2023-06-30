// React imports
import React, { useState, useEffect, useCallback } from 'react';

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
    const fetchUserCurrentCharge = useCallback(async () => {
        const response = await ChargeCurrentGet(userEmail);

        response['data'] ? setHasChargeCurrent(true) : setHasChargeCurrent(false);
    }, [userEmail]);

    useEffect(() => {
        fetchUserCurrentCharge()
    }, [fetchUserCurrentCharge]);

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
