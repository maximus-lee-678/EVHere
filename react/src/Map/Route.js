import { useEffect } from "react";
import L from "leaflet";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import "leaflet-routing-machine";
import { useMap } from "react-leaflet";

L.Marker.prototype.options.icon = L.icon({
    iconUrl: "https://upload.wikimedia.org/wikipedia/commons/5/59/Empty.png?20091205084734"
});

const Route = ({ source, destination }) => {
    const map = useMap();

    useEffect(() => {
        if (!map) return;

        if (source?.lat !== undefined && destination?.lat !== undefined) {
            const routingControl = L.Routing.control({
                waypoints: [
                    L.latLng(source.lat, source.lng),
                    L.latLng(destination.lat, destination.lng)
                ],
                routeWhileDragging: true,
                lineOptions: {
                    styles: [{ color: "#6FA1EC", weight: 4 }]
                },
                show: true,
                showAlternatives: true,
                addWaypoints: true,
                fitSelectedRoutes: true,
                draggableWaypoints: false,
                showWaypoints: false,
            }).addTo(map);

            return () => map.removeControl(routingControl);
        }



    }, [map, source, destination]);

    return null;
}

export default Route;