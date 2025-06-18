import { useState, useEffect, useRef } from "react";
import { MapContext } from "./components/MapContext";
import { ExternalEndpoints } from "./external_services/endpoints";
import "maplibre-gl/dist/maplibre-gl.css";
import "./controller.css";
import maplibregl from "maplibre-gl";
import TitleBar from "./components/Titlebar";
import EnergyInfo from "./components/EnergyInfo";

export default function App() {
  const mapRef = useRef<HTMLDivElement | null>(null);
  const [map, setMap] = useState<maplibregl.Map | null>(null);

  useEffect(() => {
    if (!mapRef.current) return;

    if (mapRef.current && !map) {
      const instance = new maplibregl.Map({
        container: mapRef.current,
        style: ExternalEndpoints.mapStyle,
        center: [0, 0],
        zoom: 2,
      });
      instance.on("click", async (e) => {
        const { lng, lat } = e.lngLat;
        console.log(lng, lat);
        instance.flyTo({
          center: [lng, lat],
          zoom: 5,
          essential: true,
        });
      });

      instance.addControl(new maplibregl.NavigationControl({ showCompass: true }), "bottom-left");
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
