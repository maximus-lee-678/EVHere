import React, { useState, useMemo, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Icon, divIcon, marker } from 'leaflet'
import { MapContainer, TileLayer, useMap, useMapEvents, Marker, Popup, GeoJSON, Tooltip } from 'react-leaflet';

import "leaflet/dist/leaflet.css";
import markerIconPng from "./marker-icon.png"
import markerIconFavouritePng from "./marker-icon-favourite.png"
import geoJsonSubzone from "./2-planning-area.json"
import geoJsonRegion from "./master-plan-2019-region-boundary-no-sea-geojson.json"

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

    // Function that loads all chargers. Called on page load, populates allChargerInfo.
    async function fetchAllChargers() {
        // Forms POST header
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: userEmail })
        };

        // JSON returns keys 'result', 'type' & 'content'
        await fetch('/api/get_all_chargers', requestOptions)
            .then(res => res.json())
            .then(data => { setAllChargerInfo(data['content']) })
            .catch(err => console.log(err));
    }

    useEffect(() => {
        fetchAllChargers()
    }, []);

    async function handleFavourite(charger_id, operation) {
        // Ugly confirmation prompt, TODO better
        if(!window.confirm(operation + " favourite charger?")){
            return;
        }

        // Forms POST header
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: userEmail, charger_id: charger_id, action: operation })
        };

        // Store response (JSON returns key 'result')
        let response;
        await fetch('/api/modify_favourite_charger', requestOptions)
            .then(res => res.json())
            .then(data => { response = data['result'] })
            .catch(err => console.log(err));

        // If operation successful, reload charger information
        // Which reloads markers
        if(response == 'Favourite modified.'){
            fetchAllChargers();
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

    // Component that formats charger information into markers for display. Reads from allChargerInfo.
    function RenderMarkers() {
        let result = [];

        for (var i = 0; i < allChargerInfo.length; i++) {
            // this is necessary for event handler to work, using allChargerInfo[i] directly causes it to go out of bound for some reason
            let id = allChargerInfo[i].id;
            let favourite = allChargerInfo[i].is_favourite;

            result.push(
                <Marker position={[allChargerInfo[i].latitude, allChargerInfo[i].longitude]}
                    icon={allChargerInfo[i].is_favourite == 0 ?
                        new Icon({ iconUrl: markerIconPng, iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [0, -30] }) :
                        new Icon({ iconUrl: markerIconFavouritePng, iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [0, -30] })}
                    key={allChargerInfo[i].id}>
                    <Popup>
                        [Name] {allChargerInfo[i].name}
                        <br />
                        [Address] {allChargerInfo[i].address}
                        <br />
                        [Provider] {allChargerInfo[i].provider}
                        <br />
                        [Connectors] {allChargerInfo[i].connectors}
                        <br />
                        [Power] {allChargerInfo[i].kilowatts || 0} kW
                        <br />
                        [24/7] {allChargerInfo[i].twenty_four_hours}
                        <br />
                        <button id={allChargerInfo[i].id}
                            onClick={() => handleFavourite(id, favourite == 0 ? 'add' : 'remove')}
                            className="shadow bg-cyan-500 hover:bg-cyan-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded"
                        >
                            {allChargerInfo[i].is_favourite == 0 ? '❤️' : '🚫'}
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

    return (
        <MapContainer center={singaporeCenter} zoom={props.desiredZoom || defaultZoom} scrollWheelZoom={true}
            style={{ width: props.mapWidth || defaultWidth, height: props.mapHeight || defaultHeight }}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {<OverlayRender />  /* Must be rendered as a component to be a considered descendant of MapContainer */}
        </MapContainer>
    );
}