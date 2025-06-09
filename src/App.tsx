import "maplibre-gl/dist/maplibre-gl.css";
import maplibregl from "maplibre-gl";
import { useEffect, useRef } from "react";
import TitleBar from "./components/Titlebar";

const MAP_TOKEN = import.meta.env.VITE_MAP_TOKEN;

export default function App() {
  const mapRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!mapRef.current) return;

    const map = new maplibregl.Map({
      container: mapRef.current,
      style: `https://api.maptiler.com/maps/darkmatter/style.json?key=${MAP_TOKEN}`,
      center: [0, 20],
      zoom: 2,
    });

    map.on("click", (e) => {
      console.log("Clicked:", e.lngLat);
    });

    return () => map.remove();
  }, []);

  return (
    <>
      <TitleBar />
      <div ref={mapRef} style={{ width: "100vw", height: "100vh" }} />
    </>
  );
}
