import React, { useState, useMemo, useEffect } from 'react';
import Navbar from "../shared/Navbar";
export default function Charger() {
    const [chargerID, setChargerID] = useState('');

    useEffect(() => {
        // Get the current URL search parameters
        const searchParams = new URLSearchParams(window.location.search);

        // Read the value of the 'id' parameter
        setChargerID(searchParams.get('id'));
    }, []);

    return (
            <main>
                <h1>Charger {chargerID}</h1>
            </main>
    );
}