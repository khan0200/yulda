import { computed, ref } from "vue";
import { defineStore } from "pinia";

import { getCityCoordinates, reverseGeocode, type Coordinates } from "@/utils/geo";

function calculateHaversineDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371; // Earth's radius in km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

export const useUserLocationStore = defineStore("userLocation", () => {
  const isLocationEnabled = ref<boolean>(localStorage.getItem("yulda_location_enabled") === "true");
  const currentCity = ref<string>(localStorage.getItem("yulda_current_city") || "");
  const coords = ref<Coordinates | null>(
    localStorage.getItem("yulda_user_coords") ? JSON.parse(localStorage.getItem("yulda_user_coords")!) : null,
  );
  const isDetecting = ref(false);
  const onlyNearby = ref(false);

  const hasLocation = computed(() => Boolean(currentCity.value || coords.value));

  async function enableLocationWithGPS(): Promise<boolean> {
    if (!navigator.geolocation) return false;
    isDetecting.value = true;
    return new Promise((resolve) => {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const lat = position.coords.latitude;
          const lon = position.coords.longitude;
          coords.value = { lat, lon };
          isLocationEnabled.value = true;

          localStorage.setItem("yulda_location_enabled", "true");
          localStorage.setItem("yulda_user_coords", JSON.stringify({ lat, lon }));

          const geo = await reverseGeocode(lat, lon);
          if (geo.city) {
            currentCity.value = geo.city;
            localStorage.setItem("yulda_current_city", geo.city);
          }

          isDetecting.value = false;
          resolve(true);
        },
        (error) => {
          console.warn("Geolocation failed:", error.message);
          isDetecting.value = false;
          resolve(false);
        },
        { enableHighAccuracy: true, timeout: 10000 },
      );
    });
  }

  function setManualCity(city: string) {
    currentCity.value = city.trim();
    isLocationEnabled.value = true;
    localStorage.setItem("yulda_location_enabled", "true");
    localStorage.setItem("yulda_current_city", city.trim());

    const cityCoords = getCityCoordinates(city);
    if (cityCoords) {
      coords.value = cityCoords;
      localStorage.setItem("yulda_user_coords", JSON.stringify(cityCoords));
    }
  }

  function disableLocation() {
    isLocationEnabled.value = false;
    currentCity.value = "";
    coords.value = null;
    localStorage.removeItem("yulda_location_enabled");
    localStorage.removeItem("yulda_current_city");
    localStorage.removeItem("yulda_user_coords");
  }

  function getDistanceInfo(
    itemCoords?: { lat?: number; lon?: number } | [number, number] | null | undefined,
    itemCity?: string | null | undefined,
  ): { distanceKm: number | null; formatted: string; isNearby: boolean; isSameCity: boolean } {
    if (!isLocationEnabled.value || (!coords.value && !currentCity.value)) {
      return { distanceKm: null, formatted: "", isNearby: false, isSameCity: false };
    }

    let targetLat: number | null = null;
    let targetLon: number | null = null;

    if (Array.isArray(itemCoords) && itemCoords.length === 2) {
      targetLon = itemCoords[0];
      targetLat = itemCoords[1];
    } else if (itemCoords && "lat" in itemCoords && "lon" in itemCoords) {
      targetLat = itemCoords.lat ?? null;
      targetLon = itemCoords.lon ?? null;
    }

    if ((!targetLat || !targetLon) && itemCity) {
      const cityCoords = getCityCoordinates(itemCity);
      if (cityCoords) {
        targetLat = cityCoords.lat;
        targetLon = cityCoords.lon;
      }
    }

    const isSameCity = Boolean(
      currentCity.value &&
        itemCity &&
        (currentCity.value.toLowerCase().includes(itemCity.toLowerCase()) ||
          itemCity.toLowerCase().includes(currentCity.value.toLowerCase())),
    );

    if (coords.value && targetLat && targetLon) {
      const dist = calculateHaversineDistance(coords.value.lat, coords.value.lon, targetLat, targetLon);
      const isNearby = dist <= 30 || isSameCity;
      const formatted = dist < 1 ? `${Math.round(dist * 1000)} m yaqinda` : `${dist.toFixed(1)} km yaqinda`;
      return { distanceKm: dist, formatted, isNearby, isSameCity };
    }

    if (isSameCity) {
      return { distanceKm: 0, formatted: "Sizning shahringizda", isNearby: true, isSameCity: true };
    }

    return { distanceKm: null, formatted: "", isNearby: false, isSameCity: false };
  }

  function sortByProximity<T>(
    items: T[],
    getItemCoords: (item: T) => { lat?: number; lon?: number } | [number, number] | null | undefined,
    getItemCity: (item: T) => string | undefined | null,
  ): T[] {
    if (!isLocationEnabled.value) return items;

    return [...items].sort((a, b) => {
      const infoA = getDistanceInfo(getItemCoords(a), getItemCity(a));
      const infoB = getDistanceInfo(getItemCoords(b), getItemCity(b));

      // 1. Same city items first
      if (infoA.isSameCity && !infoB.isSameCity) return -1;
      if (!infoA.isSameCity && infoB.isSameCity) return 1;

      // 2. Closer distance items first (if both have distance)
      if (infoA.distanceKm !== null && infoB.distanceKm !== null) {
        return infoA.distanceKm - infoB.distanceKm;
      }

      // 3. Items with proximity data rank above items without
      if (infoA.distanceKm !== null && infoB.distanceKm === null) return -1;
      if (infoA.distanceKm === null && infoB.distanceKm !== null) return 1;

      return 0;
    });
  }

  return {
    isLocationEnabled,
    currentCity,
    coords,
    isDetecting,
    onlyNearby,
    hasLocation,
    enableLocationWithGPS,
    setManualCity,
    disableLocation,
    getDistanceInfo,
    sortByProximity,
  };
});
