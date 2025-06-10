import { useState, useEffect, useRef } from "react";
import { MapContext } from "./components/MapContext";
import "maplibre-gl/dist/maplibre-gl.css";
import maplibregl from "maplibre-gl";
import TitleBar from "./components/Titlebar";
import EnergyInfo from "./components/EnergyInfo";

const MAP_TOKEN = import.meta.env.VITE_MAP_TOKEN;

export default function App() {
  const mapRef = useRef<HTMLDivElement | null>(null);
  const [map, setMap] = useState<maplibregl.Map | null>(null);

  useEffect(() => {
    if (!mapRef.current) return;

    if (mapRef.current && !map) {
      const instance = new maplibregl.Map({
        container: mapRef.current,
        style: `https://api.maptiler.com/maps/darkmatter/style.json?key=${MAP_TOKEN}`,
        center: [0, 2],
        zoom: 2,
      });
      instance.on("click", async (e) => {
        const { lng, lat } = e.lngLat;

        // Optional: Reverse geocode
        const res = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`,
        );
        const data = await res.json();

        instance.flyTo({
          center: [lng, lat],
          zoom: 5,
          essential: true,
        });

        console.log("Clicked location info:", {
          lat,
          lng,
          address: data.display_name,
        });
      });

      setMap(instance);
    }
  }, []);

  return (
    <MapContext.Provider value={map}>
      <TitleBar />
      <EnergyInfo />
      <div ref={mapRef} style={{ width: "100vw", height: "100vh" }} />
    </MapContext.Provider>
  );
}
