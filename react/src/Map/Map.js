import React, { useState, useMemo, useEffect } from 'react';
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
    const [responseChargerInfo, setResponseChargerInfo] = useState();

    useEffect(() => {
        fetch_charger()

        async function fetch_charger() {
            await fetch('http://localhost:5000/get_chargers')
                .then(res => res.json())
                .then(data => { setResponseChargerInfo(data) })
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

        for (var i = 0; i < responseChargerInfo.length; i++) {
            result.push(
                <Marker position={[responseChargerInfo[i].lat, responseChargerInfo[i].long]}
                    icon={new Icon({ iconUrl: markerIconPng, iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [0, -30] })}>
                    <Popup>
                        {responseChargerInfo[i].name}
                        <br />
                        <button class="shadow bg-cyan-500 hover:bg-cyan-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded">
                            ⭐
                        </button>
                    </Popup>
                </Marker>
            )
        }
        return result;
    }

    let mapMarkers = [];
    function OverlayRender() {
        const zoomLevel = GetZoomLevel();

        const map = useMap();
        for (var i = 0; i < mapMarkers.length; i++) {
            map.removeLayer(mapMarkers[i]);
        }

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
            return responseChargerInfo && RenderMarkers();
        }
        if (zoomLevel >= 13) {  // District Level
            return <GeoJSON data={geoJsonSubzone} key={Date.now()} onEachFeature={onEachFeature} />;
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