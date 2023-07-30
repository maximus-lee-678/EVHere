// React imports
import React, { useState, useEffect, useCallback } from 'react';

// Standard imports
import Toast, { toast } from '../SharedComponents/Toast';
import Form, { FormButton, FormInputSelect } from '../SharedComponents/Form';

// API endpoints imports
import { VehicleInfoGetByUser, ChargerGetAllWithEmail, ChargeHistoryAdd } from '../API/API';

export default function AddCharge() {
    const userEmail = localStorage.getItem("user_email");

    const [selectedVehicleId, setSelectedVehicleId] = useState(null);
    const [selectedVehicleConnectorId, setSelectedVehicleConnectorId] = useState(null);
    const [selectedChargerId, setSelectedCharger] = useState(null);
    const [selectedChargerConnectorId, setSelectedChargerConnectorId] = useState(null);
    let defaultChargerId, defaultChargerConnectorId;

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

    // once userVehicleInfo loaded, update selectedVehicleId and selectedVehicleConnectorId
    useEffect(() => {
        userVehicleInfo && setSelectedVehicleId(userVehicleInfo[0].id);
        userVehicleInfo && setSelectedVehicleConnectorId(userVehicleInfo[0].connector.id);
    }, [userVehicleInfo]);

    // Component that formats vehicle information for display in dropdown. Reads from userVehicleInfo.
    // When value is read, vehicle id is returned.
    function VehicleChoices() {
        let options = [];

        for (var i = 0; i < userVehicleInfo.length; i++) {
            options.push(
                <option className="border-0 px-3 py-3 text-gray-700" key={userVehicleInfo[i].id}
                    value={userVehicleInfo[i].id} data-connector-id={userVehicleInfo[i].connector.id}>
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
            let connectors_json = allChargerInfo[i].available_connector;

            let flag;
            for (var j = 0; j < connectors_json.length; j++) {
                flag = false;

                // matching connector_type ids
                if (connectors_json[j].connector_type.id === selectedVehicleConnectorId) {
                    flag = true;
                    break;
                }
            }
            if (!flag) {
                continue;
            }

            if (!hasSetInitial) {
                hasSetInitial = true;
                defaultChargerId = allChargerInfo[i].id;
            }

            options.push(
                <option className="border-0 px-3 py-3 text-gray-700" key={allChargerInfo[i].id}
                    value={allChargerInfo[i].id}>{allChargerInfo[i].name}</option>
            );
        }

        return options;
    }

    // Component that formats charger connector information for display in dropdown. Reads from allChargerInfo.
    // When value is read, charger connector id (not connector type id) is returned.
    function ConnectorChoices() {
        let options = [], hasSetInitial = false, connectors;

        if (selectedChargerId) {
            connectors = allChargerInfo.filter(obj => { return obj.id === selectedChargerId })[0].available_connector;
        } else {
            connectors = allChargerInfo[0].available_connector;
        }

        for (var i = 0; i < connectors.length; i++) {
            if (connectors[i].connector_type.id !== selectedVehicleConnectorId) {
                continue;
            }

            if (!hasSetInitial) {
                hasSetInitial = true;
                defaultChargerConnectorId = connectors[i].id;
            }

            options.push(
                <option className="border-0 px-3 py-3 text-gray-700" key={connectors[i].id}
                    value={connectors[i].id}>{connectors[i].connector_type.name_connector} {'<' + connectors[i].id + '>'}</option>
            );
        }

        return options;
    }

    // Function that starts a charge. Called upon form submission.
    async function handleStart(e) {
        e.preventDefault();

        const response = await ChargeHistoryAdd(userEmail, selectedVehicleId,
            selectedChargerId || defaultChargerId, selectedChargerConnectorId || defaultChargerConnectorId);

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
            <div className="absolute w-full h-full bg-gray-900">
                <Form elementName="Add new Charging History" onSubmit={handleStart} backgroundImageURL="battery.png">
                    <FormInputSelect elementName="Vehicle" id="vehicle"
                        value={(userVehicleInfo && selectedVehicleId) || ""}
                        options={userVehicleInfo && <VehicleChoices />}
                        onChange={(event) => {
                            setSelectedVehicleId(event.target.value);
                            setSelectedVehicleConnectorId(event.target.selectedOptions[0].getAttribute('data-connector-id'));
                        }}
                    />

                    <FormInputSelect elementName="Charger Name" id="charger"
                        value={(allChargerInfo && selectedChargerId) || ""}
                        options={allChargerInfo && <ChargerChoices />}
                        onChange={(event) => {
                            setSelectedCharger(event.target.value);
                        }}
                    />

                    <FormInputSelect elementName="Charger Connector" id="charger-connector"
                        value={(allChargerInfo && selectedChargerConnectorId) || ""}
                        options={(allChargerInfo && <ConnectorChoices />)}
                        onChange={(event) => setSelectedChargerConnectorId(event.target.value)}
                    />

                    <FormButton elementName={"\"Start\" Charge"} />
                </Form>

            </div>
        </div>
    )
}