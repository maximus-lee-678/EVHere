// React imports
import React, { useState, useEffect, useCallback } from 'react';
import { DateTime } from 'luxon';

// Standard imports
import Toast, { toast } from '../SharedComponents/Toast';
import { FormatDateTime } from '../Utils/Time';

// API endpoints imports
import { ChargerGetAllWithEmail, FavouriteChargerAdd, FavouriteChargerRemove } from '../API/API';

// Leaflet imports
import { Icon, LatLng, divIcon, marker } from 'leaflet'
import { MapContainer, TileLayer, useMap, useMapEvents, Marker, Popup, GeoJSON } from 'react-leaflet';
import "leaflet/dist/leaflet.css";
import markerIconPng from "./marker-icon.png";
import markerIconFavouritePng from "./marker-icon-favourite.png";
import geoJsonSubzone from "./2-planning-area.json";
import geoJsonRegion from "./master-plan-2019-region-boundary-no-sea-geojson.json";

//navigation import
import Route from "./Route";
import routeIconPng from "./route-icon.png"

import GeometryUtil from 'leaflet-geometryutil';

// This component renders a map centered on singapore. Pass in properties to change the kind of returns you get.
//
// Supported Props:[
// desiredZoom: how zoomed in the map initially is, the smaller the value the more zoomed out.
// mapWidth: how wide the map is. (%)
// mapHeight: how tall the map is. (html measurements e.g. vh)
// ] See defaults below.
export default function Map(props) {
    const singaporeCenter = [1.3521, 103.8198];
    const defaultZoom = 12;
    const defaultWidth = "100%";
    const defaultHeight = "70vh";

    const districtZoomThreshold = 12;
    const displayMarkersThreshold = 14;

    const userEmail = localStorage.getItem("user_email");
    const [allChargerInfo, setAllChargerInfo] = useState();

    //const for navigation
    const [sourceLocation, setSourceLocation] = useState({});
    const [destinationLocation, setDestinationLocation] = useState({});
    const [geolocationMsg, setGeolocationMsg] = useState("Awaiting permission");
    const { userVehicleInfo, selectedVehicleId } = props;

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
        fetchAllChargers();
    }, [fetchAllChargers]);

    async function handleFavourite(IDCharger, operation) {
        // Ugly confirmation prompt, TODO better
        //maybe can make a dialog that opens when button is clicked, then yes no goes to handle favourite?
        if (!window.confirm(operation + " favourite charger?")) {
            //do nothing if cancel confirmation
            return;
        }

        let response;
        // Pick API endpoint
        if (operation === "add") {
            response = await FavouriteChargerAdd(userEmail, IDCharger);
        } else if (operation === "remove") {
            response = await FavouriteChargerRemove(userEmail, IDCharger);
        } else {
            return;
        }

        // If operation successful, reload charger information
        // Which reloads markers
        if (response.status === 'success') {
            fetchAllChargers();
            if (operation === "add") {
                toast.success("Added to favourites!")
            }
            if (operation === "remove") {
                toast.success("Removed from favourites!")
            }
        }
        else {
            toast.error(<div>{response.message}<br />{response.reason}</div>);
        }
    }

    // Returns zoom level of map.
    function GetZoomLevel() {
        const [zoomLevel, setZoomLevel] = useState(-1);

        // Attach zoomend event handler
        const mapEvents = useMapEvents({
            zoomend: () => {
                setZoomLevel(mapEvents.getZoom());
            },
        });

        // If zoomLevel "uninitialised", init it
        if (zoomLevel <= -1) {
            setZoomLevel(mapEvents.getZoom());
        }

        return zoomLevel;
    }


    var markersToRender = [];
    // Component that formats charger information into markers for display. Reads from allChargerInfo.
    function RenderMarkers() {
        const map = useMap();

        let result = [];
        // console.log("selectedId", selectedVehicleId);

        //if user has selected their vehicle
        if (selectedVehicleId !== "" && document.getElementById("vehicleName").value !== "Show all markers") {
            var selectedVehicle = userVehicleInfo.find(vehicle => vehicle.id === selectedVehicleId);
            markersToRender = [];


            //check for their vehicle connector
            allChargerInfo.forEach(charger => {
                charger.available_connector.forEach(connector => {
                    if (connector.connector_type.id === selectedVehicle.connector.id) {
                        markersToRender.push(charger);
                    }
                })
            });

            // console.log("IN SELECTED", markersToRender);

            //check map's existing layers, markers
            map.eachLayer(function (layer) {
                if (layer._latlng !== undefined) {
                    if (layer._latlng.lat !== undefined && layer._latlng.lng !== undefined) {
                        //remove them if doesnt match with markersToRender latlng, and also doesnt match with sourceLocation
                        if (markersToRender.find(marker => marker.latitude === layer._latlng.lat && marker.longitude === layer._latlng.lng) === undefined) {
                            if (layer._latlng.lat !== sourceLocation.lat && layer._latlng.lng !== sourceLocation.lng) {
                                map.removeLayer(layer);
                            }
                        }
                    }
                }
            })
        }
        else {
            markersToRender = allChargerInfo;
        }

        for (var i = 0; i < markersToRender.length; i++) {
            // this is necessary for event handler to work, using allChargerInfo[i] directly causes it to go out of bound for some reason
            let id = markersToRender[i].id;
            let favourite = markersToRender[i].is_favourite;
            let lat = markersToRender[i].latitude;
            let lng = markersToRender[i].longitude;

            var predictedValue = "";
            if (markersToRender[i].rate_predicted != "") {
                //get time now, then get index for next hour
                //0 index is 12AM etc. so get the time then see next hour
                //then put this value in the popup value
                var timeNow = FormatDateTime(DateTime.now(), "T");

                var currentHour = parseInt(timeNow.split(":")[0]);

                var predictedArray = JSON.parse(markersToRender[i].rate_predicted);

                predictedValue = predictedArray[currentHour + 1];

            }

            result.push(
                <Marker position={[markersToRender[i].latitude, markersToRender[i].longitude]}
                    icon={markersToRender[i].is_favourite === false ?
                        new Icon({ iconUrl: markerIconPng, iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [0, -30] }) :
                        new Icon({ iconUrl: markerIconFavouritePng, iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [0, -30] })}
                    key={markersToRender[i].id}>
                    <Popup>
                        <div className="pb-1">
                            <span className="font-semibold text-sm">Name:</span> {markersToRender[i].name}
                            <br />
                            <span className="font-semibold text-sm">Address:</span> {markersToRender[i].address}
                            <br />
                            <span className="font-semibold text-sm">Solar Voltage In:</span> {markersToRender[i].pv_voltage_in} V
                            <br />
                            <span className="font-semibold text-sm">Solar Current In:</span> {markersToRender[i].pv_current_in} A
                            <br />
                            <span className="font-semibold text-sm">Solar Voltage Out:</span> {markersToRender[i].pv_voltage_out} V
                            <br />
                            <span className="font-semibold text-sm">Solar Current Out:</span> {markersToRender[i].pv_current_out} A
                            <br />
                            <span className="font-semibold text-sm">Price Rate:</span> ${markersToRender[i].rate_current} / kWh
                            <br />
                            <span className="font-semibold text-sm">Predicted Rate (Next Hour):</span> ${predictedValue !== "" ? predictedValue : "--"} / kWh
                        </div>
                        <button id={markersToRender[i].id}
                            onClick={() => handleFavourite(id, favourite === false ? 'add' : 'remove')}
                            className={(markersToRender[i].is_favourite === false ? "hover:bg-red-900" : "hover:bg-red-300")
                                + " bg-red-400 px-3 py-2 mr-2 rounded-full text-white"}
                        >
                            {markersToRender[i].is_favourite === false ? <i className="fas fa-heart" style={{ color: "#ffffff" }}></i> : <i className="fas fa-heart-broken" style={{ color: "#ffffff" }}></i>}
                            {markersToRender[i].is_favourite === false ? ' Add to favourites' : ' Remove favourite'}
                        </button>
                        <button id={markersToRender[i].id}
                            onClick={() => navigate(lat, lng)}
                            className={(geolocationMsg !== "Permission granted" ? "hidden " : "") + "bg-green-400 hover:bg-green-900 px-3 py-2 rounded-full text-white"}>
                            Go
                            <i className="fas fa-location-arrow pl-1"></i>
                        </button>
                    </Popup>
                </Marker>
            )
        }
        return result;
    }

    let mapMarkers = [];
    // Component that overlays region information and markers on map.
    function OverlayRender() {
        const zoomLevel = GetZoomLevel();

        // Get bounds of map on map change.
        // TODO optimise markers displayed only within screen
        const mapEvents = useMapEvents({
            dragend: (e) => handleMapEvent(e),
            zoomend: (e) => handleMapEvent(e),
        });
        const handleMapEvent = (e) => {
            console.log("mapCenter", e.target.getCenter());
            console.log("map bounds", e.target.getBounds());
        };

        // Remove all old markers
        const map = useMap();
        for (var i = 0; i < mapMarkers.length; i++) {
            map.removeLayer(mapMarkers[i]);
        }

        // displays district name in region centre, currently not used
        // use by placing in onEachFeature={onEachFeature} in GeoJSON
        const onEachFeature = (feature, layer) => {
            const label = divIcon({
                className: 'label',
                html: feature.properties.name,
                iconSize: [100, 40],
            });

            const center = layer.getBounds().getCenter();
            const newMarker = marker(center, { icon: label });

            mapMarkers.push(newMarker);
            newMarker.addTo(map);
        };

        //if location allowed, set view as current location
        navigator.geolocation.getCurrentPosition((position) => location(map, position.coords.latitude, position.coords.longitude), function (error) { setGeolocationMsg(error.message) });

        // Return geoJSON overlay depending on zoom level
        if (zoomLevel >= displayMarkersThreshold) {// No overlay, only markers
            return allChargerInfo && <div><RenderMarkers /></div>;
        }
        if (zoomLevel >= districtZoomThreshold) {  // District Level
            return allChargerInfo && <div><GeoJSON data={geoJsonSubzone} key={Date.now()} /></div>;
        }
        else {                                     // Region Level
            return <GeoJSON data={geoJsonRegion} key={Date.now()} />;
        }
    }


    function PopulateRecommendations() {

        const map = useMap();

        var markersArray = [];
        var markersCoordsArray = [];
        for (var i = 0; i < markersToRender.length; i++) {
            markersArray.push(markersToRender[i]);
            var coords = [markersToRender[i].latitude, markersToRender[i].longitude]
            markersCoordsArray.push(coords);
        }


        if (geolocationMsg === "Permission granted" && sourceLocation != null) {

            if (markersArray.length > 0) {
                //for nearest charger

                var nearest = GeometryUtil.closest(map, markersCoordsArray, [sourceLocation.lat, sourceLocation.lng], true);

                var nearestMarker = markersArray.find(element => element.latitude === nearest.lat && element.longitude === nearest.lng);

                // console.log("nearestMarker", nearestMarker);

                document.getElementById("nearest-charger-name").innerText = nearestMarker.name;
                document.getElementById("nearest-charger-button").addEventListener("click", () => {
                    map.panTo(new LatLng(nearestMarker.latitude, nearestMarker.longitude));
                });


                //for best value charger
                var prices = [];

                markersArray.forEach(item => {
                    prices.push(item.rate_current);
                });

                var valueMarker = markersArray.find(element => element.rate_current === Math.min.apply(Math, prices));

                // console.log("valueMarker", valueMarker);
                document.getElementById("best-value-charger-name").innerText = valueMarker.name;
                document.getElementById("best-value-charger-button").addEventListener("click", () => {
                    map.panTo(new LatLng(valueMarker.latitude, valueMarker.longitude));
                });


            }

        }
        else {
            document.getElementById("nearest-charger-name").innerText = "-- (" + geolocationMsg + ")";
            document.getElementById("best-value-charger-name").innerText = "-- (" + geolocationMsg + ")";
        }

    }


    function location(map, lat, lng) {

        const center = new LatLng(lat, lng);

        let children = Array.from(map._panes.markerPane.children);

        //check for existing location marker
        //if no location marker has been added
        if (children.find(child => child.src === routeIconPng) === undefined) {
            //check that source location is not the same as new location
            if (sourceLocation.lat !== center.lat && sourceLocation.lng !== center.lng) {
                setSourceLocation(center);

                map.setView(center, 24);

                setGeolocationMsg("Permission granted");

                const newMarker = marker(center, { icon: new Icon({ iconUrl: routeIconPng, iconSize: [41, 41], iconAnchor: [20, 41] }) });
                newMarker.addTo(map);
            }
        }
    }

    function navigate(destinationLat, destinationLng) {
        // console.log(destinationLat);
        // console.log(destinationLng);

        setDestinationLocation(new LatLng(destinationLat, destinationLng));
        // console.log(destinationLocation);
    }

    return (
        <>
            <Toast />

            <MapContainer center={singaporeCenter} zoom={props.desiredZoom || defaultZoom} scrollWheelZoom={true}
                style={{ width: props.mapWidth || defaultWidth, height: props.mapHeight || defaultHeight }}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {<OverlayRender />  /* Must be rendered as a component to be a considered descendant of MapContainer */}
                {allChargerInfo && <PopulateRecommendations />}
                <Route source={sourceLocation} destination={destinationLocation} />
            </MapContainer>
        </>
    );
}