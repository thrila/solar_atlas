import { useState, useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import { MapContext } from "./components/MapContext";
import { ExternalEndpoints } from "./external_services/endpoints";
import TitleBar from "./components/Titlebar";
import EnergyInfo from "./components/EnergyInfo";
import PopupPortal from "./components/PopupPortal";
import solarData from "../sample.json";
import "maplibre-gl/dist/maplibre-gl.css";
import "./controller.css";
import type { SolarEstimation } from "./types/index";

export default function App() {
  const mapRef = useRef<HTMLDivElement | null>(null);
  const [map, setMap] = useState<maplibregl.Map | null>(null);
  const [showPanel, setShowPanel] = useState(false);
  const [locationSolarInfo, setLocationSolarInfo] = useState<SolarEstimation>(solarData);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!mapRef.current) return;

    //NOTE: try and get location
    if (mapRef.current && !map) {
      const instance = new maplibregl.Map({
        container: mapRef.current,
        style: ExternalEndpoints.mapStyle,
        center: [32, 15],
        zoom: 2,
      });
      // instance.on("click", async (e) => {
      //   const { lng, lat } = e.lngLat;
      //   console.log(lng, lat);
      //   instance.flyTo({
      //     center: [lng, lat],
      //     zoom: 5,
      //     essential: true,
      //   });
      //   setShowPanel(() => true);
      // });

      instance.addControl(new maplibregl.NavigationControl({ showCompass: true }), "bottom-left");
      setMap(instance);
    }
  }, []);

  useEffect(() => {
    const setHeight = () => {
      if (mapRef.current) {
        mapRef.current.style.height = `${window.innerHeight}px`;
      }
    };

    setHeight();
    window.addEventListener("resize", setHeight);
    return () => window.removeEventListener("resize", setHeight);
  }, []);

  return (
    <MapContext.Provider value={map}>
      <TitleBar
        setShowPanel={setShowPanel}
        setLocationSolarInfo={setLocationSolarInfo}
        setLoading={setLoading}
      />

      <PopupPortal>
        <div
          className={`fixed md:top-1/3  top-1/2 right-0  w-[24rem] px-5 transition-transform duration-700
                  ${showPanel ? "translate-x-0" : "translate-x-full"}`}
        >
          <EnergyInfo data={locationSolarInfo} loading={loading} />
        </div>
      </PopupPortal>
      <div ref={mapRef} style={{ width: "100vw" }} />
    </MapContext.Provider>
  );
}
