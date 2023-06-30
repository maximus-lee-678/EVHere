// React imports
import React, { useState, useEffect, useCallback } from 'react';

// Standard imports
import Toast, { toast } from '../SharedComponents/Toast';
import Form, { FormButton, FormInputField, FormInputSelect } from '../SharedComponents/Form';

// API endpoints imports
import { VehicleInfoGetByUser, ChargerGetAllWithEmail, ChargeHistoryAdd } from '../API/API';

export default function AddCharge() {
    const userEmail = localStorage.getItem("user_email");

    const [selectedVehicleId, setSelectedVehicleId] = useState(null);
    const [selectedVehicleConnector, setSelectedVehicleConnector] = useState(null);
    const [selectedCharger, setSelectedCharger] = useState('');
    let firstCharger;
    const [batteryPercentage, setBatteryPercentage] = useState('');

    const [userVehicleInfo, setUserVehicleInfo] = useState();
    const [allChargerInfo, setAllChargerInfo] = useState();

    // Function that loads all user vehicles. Called on page load, populates userVehicleInfo.
    // Used in main page.
    const fetchAllUserVehicles = useCallback(async () => {
        const response = await VehicleInfoGetByUser(userEmail);

        // If success returned, store vehicle information
        if (response.status === 'success') {
            setUserVehicleInfo(response['data']);
        } else {
            toast.error(<div>{response.message}<br />{response.reason}</div>);
            setUserVehicleInfo([]);
        }
    }, [userEmail]);

    // Function that loads all chargers. Called on page load, populates allChargerInfo.
    const fetchAllChargers = useCallback(async () => {
        const response = await ChargerGetAllWithEmail(userEmail);

        // If success returned, store charger information
        if (response.status === 'success') {
            setAllChargerInfo(response['data'])
        } else {
            toast.error(<div>{response.message}<br />{response.reason}</div>);
        }
    }, [userEmail]);

    useEffect(() => {
        fetchAllUserVehicles();
        fetchAllChargers();
    }, [fetchAllUserVehicles, fetchAllChargers]);

    // once userVehicleInfo loaded, update selectedConnector and Id
    useEffect(() => {
        userVehicleInfo && setSelectedVehicleId(userVehicleInfo[0].id);
        userVehicleInfo && setSelectedVehicleConnector(userVehicleInfo[0].connector_type);
    }, [userVehicleInfo]);

    // Component that formats vehicle information for display in dropdown. Reads from userVehicleInfo.
    // When value is read, vehicle id is returned.
    function VehicleChoices() {
        let options = [];

        for (var i = 0; i < userVehicleInfo.length; i++) {
            options.push(
                <option className="border-0 px-3 py-3 text-gray-700" key={userVehicleInfo[i].id}
                    value={userVehicleInfo[i].id} data-connector-type={userVehicleInfo[i].connector_type}>
                    {userVehicleInfo[i].name} ({userVehicleInfo[i].vehicle_sn})
                </option>
            );
        }

        return options;
    }

    // Component that formats charger information for display in dropdown. Reads from allChargerInfo.
    // When value is read, charger id is returned.
    // Only adds chargers that contain a connector specified by selectedVehicleConnector.
    function ChargerChoices() {
        let options = [], hasSetInitial = false;

        for (var i = 0; i < allChargerInfo.length; i++) {
            let connector_types_array = allChargerInfo[i].connector_types;

            if (!connector_types_array.includes(selectedVehicleConnector)) {
                continue;
            }

            if (!hasSetInitial) {
                hasSetInitial = true;
                firstCharger = allChargerInfo[i].id;
            }

            options.push(
                <option className="border-0 px-3 py-3 text-gray-700" key={allChargerInfo[i].id}
                    value={allChargerInfo[i].id}>{allChargerInfo[i].name}</option>
            );
        }

        return options;
    }

    // Function that starts a charge. Called upon form submission.
    async function handleStart(e) {
        e.preventDefault();

        const response = await ChargeHistoryAdd(userEmail, selectedVehicleId, selectedCharger || firstCharger, batteryPercentage);

        // result is boolean of status
        if (response.status === 'success') {
            toast.success(response.message);
            // delay 2s
            await new Promise(resolve => setTimeout(resolve, 2000));

            // reload page
            window.location.replace('/');
        } else {
            toast.error(<div>{response.message}<br />{response.reason}</div>);
        }
    }

    return (
        <div>
            <Toast />

            <Form elementName="Add new Charging History" onSubmit={handleStart} backgroundImageURL="battery.png">
                <FormInputSelect elementName="Vehicle" id="vehicle"
                    value={(userVehicleInfo && selectedVehicleId) || ""}
                    options={userVehicleInfo && <VehicleChoices />}
                    onChange={(event) => {
                        setSelectedVehicleId(event.target.value);
                        setSelectedVehicleConnector(event.target.selectedOptions[0].getAttribute('data-connector-type'));
                    }}
                />

                <FormInputField elementName="Starting battery percentage" id="battery-start" placeholder="Select Battery Level . . ."
                    type="number" value={batteryPercentage}
                    onChange={(event) => setBatteryPercentage(event.target.value)}
                />

                <FormInputSelect elementName="Charger Name" id="charger"
                    value={(allChargerInfo && selectedCharger) || ""}
                    options={allChargerInfo && <ChargerChoices />}
                    onChange={(event) => setSelectedCharger(event.target.value)}
                />

                <FormButton elementName={"\"Start\" Charge"} />
            </Form>
        </div>
    )
}