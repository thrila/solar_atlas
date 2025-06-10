export class ExternalEndpoints {
  static MAP_TOKEN = import.meta.env.VITE_MAP_TOKEN;
  static mapStyle = `https://api.maptiler.com/maps/darkmatter/style.json?key=${this.MAP_TOKEN}`;
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
      return null; // or throw err to bubble up
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
      return null; // or throw err to bubble up
    }
  }
}
