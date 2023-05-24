import React, { useState, useMemo, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Icon, divIcon, marker } from 'leaflet'
import { MapContainer, TileLayer, useMap, useMapEvents, Marker, Popup, GeoJSON, Tooltip } from 'react-leaflet';

import "leaflet/dist/leaflet.css";
import markerIconPng from "leaflet/dist/images/marker-icon.png"
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

    const userEmail = localStorage.getItem("user_email");
    const [allChargerInfo, setAllChargerInfo] = useState();

    useEffect(() => {
        fetchAllChargers()

        async function fetchAllChargers() {
            // Forms POST header
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: userEmail })
            };

            await fetch('/api/get_all_chargers', requestOptions)
                .then(res => res.json())
                .then(data => { setAllChargerInfo(data) })
                .catch(err => console.log(err));
        }
    }, []);

    function GetZoomLevel() {
        const [zoomLevel, setZoomLevel] = useState(12); // initial zoom level provided for MapContainer

        const mapEvents = useMapEvents({
            zoomend: () => {
                setZoomLevel(mapEvents.getZoom());
            },
        });

        return zoomLevel;
    }

    function RenderMarkers() {
        let result = [];

        for (var i = 0; i < allChargerInfo.length; i++) {
            result.push(
                <Marker position={[allChargerInfo[i].lat, allChargerInfo[i].long]}
                    icon={new Icon({ iconUrl: markerIconPng, iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [0, -30] })}
                    key={allChargerInfo[i].lat + ", " + allChargerInfo[i].long}>
                    <Popup>
                        {allChargerInfo[i].name}
                        <br />
                        <Link to={`/Charger?id=${allChargerInfo[i].id}`}>
                            <button id={allChargerInfo[i].id}
                                className="shadow bg-cyan-500 hover:bg-cyan-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded"
                            >
                                ⓘ
                            </button>
                        </Link>
                    </Popup>
                </Marker>
            )
        }
        return result;
    }

    // function handleAddFavourite(e) {
    //     console.log(e.target.id);
    // }

    let mapMarkers = [];
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
        if (zoomLevel >= 15) {  // No overlay, only markers
            return allChargerInfo && <RenderMarkers />;
        }
        if (zoomLevel >= 13) {  // District Level and Markers
            return allChargerInfo && <div><RenderMarkers /><GeoJSON data={geoJsonSubzone} key={Date.now()} /></div>;
        }
        else {                  // Region Level
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