export interface Coordinates {
  lat: number;
  lon: number;
}

export interface GeocodedLocation {
  name: string;
  city?: string;
  country?: string;
  lat: number;
  lon: number;
  display_name?: string;
}

export const CITY_COORDINATES: Record<string, Coordinates> = {
  seoul: { lat: 37.5665, lon: 126.978 },
  incheon: { lat: 37.4563, lon: 126.7052 },
  busan: { lat: 35.1796, lon: 129.0756 },
  daegu: { lat: 35.8714, lon: 128.6014 },
  cheongju: { lat: 36.6424, lon: 127.4897 },
  cheonan: { lat: 36.8151, lon: 127.1522 },
  ansan: { lat: 37.3219, lon: 126.8309 },
  suwon: { lat: 37.2636, lon: 127.0286 },
  baran: { lat: 37.1325, lon: 126.9209 },
  hyangnam: { lat: 37.1325, lon: 126.9209 },
  pyeongtaek: { lat: 36.9921, lon: 127.1128 },
  gimhae: { lat: 35.2285, lon: 128.8893 },
  gwangju: { lat: 35.1595, lon: 126.8526 },
  daejeon: { lat: 36.3504, lon: 127.3845 },
  ulsan: { lat: 35.5384, lon: 129.3114 },
  tashkent: { lat: 41.2995, lon: 69.2401 },
  toshkent: { lat: 41.2995, lon: 69.2401 },
  samarkand: { lat: 39.627, lon: 66.975 },
  samarqand: { lat: 39.627, lon: 66.975 },
  andijan: { lat: 40.7821, lon: 72.3442 },
  andijon: { lat: 40.7821, lon: 72.3442 },
  namangan: { lat: 40.9983, lon: 71.6726 },
  fergana: { lat: 40.3842, lon: 71.7843 },
  fargona: { lat: 40.3842, lon: 71.7843 },
  bukhara: { lat: 39.7747, lon: 64.4217 },
  buxoro: { lat: 39.7747, lon: 64.4217 },
};

export function getCityCoordinates(cityName: string): Coordinates | null {
  const normalized = cityName.trim().toLowerCase();
  for (const [key, coords] of Object.entries(CITY_COORDINATES)) {
    if (normalized.includes(key) || key.includes(normalized)) {
      return coords;
    }
  }
  return null;
}

export async function reverseGeocode(lat: number, lon: number): Promise<GeocodedLocation> {
  try {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&accept-language=en,uz,ko`,
      {
        headers: {
          "Accept": "application/json",
        },
      },
    );
    if (!res.ok) throw new Error("Reverse geocode failed");
    const data = await res.json();
    const addr = data.address || {};
    const city =
      addr.city ||
      addr.town ||
      addr.county ||
      addr.suburb ||
      addr.state ||
      "Unknown";
    const name = addr.road ? `${city}, ${addr.road}` : city;
    return {
      name,
      city,
      country: addr.country_code?.toUpperCase(),
      lat,
      lon,
      display_name: data.display_name,
    };
  } catch {
    return {
      name: `${lat.toFixed(4)}, ${lon.toFixed(4)}`,
      lat,
      lon,
    };
  }
}

export async function fetchOSRMRoute(
  coordinates: [number, number][],
): Promise<{ coordinates: [number, number][]; distanceKm: number; durationMin: number } | null> {
  if (coordinates.length < 2) return null;
  try {
    const coordsString = coordinates.map(([lon, lat]) => `${lon},${lat}`).join(";");
    const url = `https://router.project-osrm.org/route/v1/driving/${coordsString}?overview=full&geometries=geojson`;
    const res = await fetch(url);
    if (!res.ok) return null;
    const json = await res.json();
    if (json.code !== "Ok" || !json.routes?.length) return null;
    const route = json.routes[0];
    return {
      coordinates: route.geometry.coordinates,
      distanceKm: Math.round(route.distance / 1000),
      durationMin: Math.round(route.duration / 60),
    };
  } catch {
    return null;
  }
}
