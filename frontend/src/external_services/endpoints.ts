import type { SolarEstimation, SolarDataType } from "../types/index";

export class ExternalEndpoints {
  static MAP_TOKEN = import.meta.env.VITE_MAP_TOKEN;
  static mapStyle = `https://api.maptiler.com/maps/darkmatter/style.json?key=${this.MAP_TOKEN}`;
  static BaseUrl: string = import.meta.env.VITE_BACKEND_URL;
  static Port: string = import.meta.env.VITE_BACKEND_PORT;
  static async getCoordinatesWithName(location: string) {
    try {
      const res = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}`,
      );

      if (!res.ok) throw new Error(`API error: ${res.status}`);

      const data = await res.json();

      if (data.length === 0) throw new Error("No coordinates found.");

      const { lat, lon } = data[0];
      return { lat: parseFloat(lat), lon: parseFloat(lon) };
    } catch (err) {
      console.error("getCoordinatesWithName failed:", err);
      return { lat: 0, lon: 0 };
    }
  }
  static async getCity(lng: number, lat: number) {
    try {
      const res = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`,
      );
      if (!res.ok) throw new Error(`API error: ${res.status}`);
      const data = await res.json();
      return data;
    } catch (err) {
      console.error("getCity:", err);
      return null;
    }
  }
  static async getLocationSuggestion(query: string) {
    try {
      const res = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${query}&limit=5`,
      );
      if (!res.ok) throw new Error(`API error: ${res.status}`);
      const data = await res.json();
      return data;
    } catch (err) {
      console.log(`getLocationSuggestion`, err);
      return null;
    }
  }
  static async getSolarData({
    long,
    lat,
    power,
    numberOfPanels,
  }: SolarDataType): Promise<SolarEstimation | null> {
    try {
      const res = await fetch(
        // NOTE: for local env add port
        `${this.BaseUrl}/v1/estimate_energy?long=${long}&lat=${lat}&panel_number=${numberOfPanels}&panel_output=${power}`,
        {
          method: "POST",
        },
      );

      if (!res.ok) {
        console.error(`Server error: ${res.status}`);
        return null;
      }

      const data: SolarEstimation = await res.json();
      return data;
    } catch (err) {
      console.error("Fetch error:", err);
      return null;
    }
  }
}
