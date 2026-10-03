<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { LocateFixed, MapPin, Route as RouteIcon } from "lucide-vue-next";
import {
  LngLatBounds,
  Map as MapLibreMap,
  Marker,
  NavigationControl,
  Popup,
  type StyleSpecification,
} from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

import {
  fetchOSRMRoute,
  getCityCoordinates,
  reverseGeocode,
  type Coordinates,
  type GeocodedLocation,
} from "@/utils/geo";

const props = withDefaults(
  defineProps<{
    mode?: "picker" | "route" | "view";
    initialLocation?: Coordinates;
    routeStops?: Array<{ name: string; lat?: number; lon?: number }>;
    height?: string;
    aspectRatio?: string;
    interactive?: boolean;
    label?: string;
  }>(),
  {
    mode: "picker",
    initialLocation: undefined,
    routeStops: () => [],
    height: undefined,
    aspectRatio: "16/12",
    interactive: true,
    label: undefined,
  },
);

const emit = defineEmits<{
  select: [location: GeocodedLocation];
}>();

const containerStyle = computed(() => {
  if (props.height) {
    return { height: props.height };
  }
  const ratio = (props.aspectRatio || "16/12").replace(":", " / ");
  return {
    aspectRatio: ratio,
    minHeight: "360px",
    maxHeight: "680px",
  };
});

const mapContainer = ref<HTMLDivElement | null>(null);
let map: MapLibreMap | null = null;
let activeMarker: Marker | null = null;
let routeMarkers: Marker[] = [];
let resizeObserver: ResizeObserver | null = null;

const isLocating = ref(false);
const selectedAddress = ref<string>("");
const routeInfo = ref<{ distanceKm: number; durationMin: number } | null>(null);

// OpenStreetMap standard style (100% full coverage in Korea & Uzbekistan, no watermark)
const MAP_STYLE: StyleSpecification = {
  version: 8,
  sources: {
    "osm-tiles": {
      type: "raster",
      tiles: [
        "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
      ],
      tileSize: 256,
      attribution: "© OpenStreetMap contributors",
    },
  },
  layers: [
    {
      id: "osm-tiles-layer",
      type: "raster",
      source: "osm-tiles",
      minzoom: 0,
      maxzoom: 19,
    },
  ],
};

function createMarkerElement(type: "start" | "waypoint" | "end" | "picker", label?: string | number): HTMLElement {
  const el = document.createElement("div");
  el.className = "flex items-center justify-center cursor-pointer transition-transform hover:scale-110";

  if (type === "picker") {
    el.innerHTML = `
      <div class="relative flex items-center justify-center">
        <div class="absolute -bottom-1 h-3 w-3 rounded-full bg-black/30 blur-[2px]"></div>
        <div class="flex h-10 w-10 items-center justify-center rounded-full bg-yulda-black text-white shadow-xl ring-4 ring-yulda-yellow">
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 21s-8-7.5-8-12a8 8 0 1116 0c0 4.5-8 12-8 12z" />
            <circle cx="12" cy="9" r="2.5" fill="currentColor" />
          </svg>
        </div>
      </div>
    `;
  } else if (type === "start") {
    el.innerHTML = `
      <div class="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-500 font-bold text-xs text-white shadow-lg ring-2 ring-white">
        A
      </div>
    `;
  } else if (type === "end") {
    el.innerHTML = `
      <div class="flex h-8 w-8 items-center justify-center rounded-full bg-yulda-black font-bold text-xs text-white shadow-lg ring-2 ring-yulda-yellow">
        B
      </div>
    `;
  } else {
    el.innerHTML = `
      <div class="flex h-7 w-7 items-center justify-center rounded-full bg-yulda-yellow font-bold text-xs text-yulda-black shadow-md ring-2 ring-white">
        ${label ?? "•"}
      </div>
    `;
  }
  return el;
}

async function setPickerLocation(lat: number, lon: number, addressName?: string, emitEvent = true) {
  if (!map) return;

  if (activeMarker) {
    activeMarker.setLngLat([lon, lat]);
  } else {
    const el = createMarkerElement("picker");
    const marker = new Marker({ element: el, draggable: props.mode === "picker" })
      .setLngLat([lon, lat])
      .addTo(map);
    activeMarker = marker;

    marker.on("dragend", async () => {
      const lngLat = marker.getLngLat();
      const geo = await reverseGeocode(lngLat.lat, lngLat.lng);
      selectedAddress.value = geo.name;
      emit("select", geo);
    });
  }

  if (addressName) {
    selectedAddress.value = addressName;
    if (emitEvent) {
      emit("select", { name: addressName, lat, lon });
    }
  } else {
    const geo = await reverseGeocode(lat, lon);
    selectedAddress.value = geo.name;
    if (emitEvent) {
      emit("select", geo);
    }
  }
}

async function handleUseMyLocation() {
  if (!navigator.geolocation) {
    alert("Brauzeringiz geolokatsiyani qo'llab-quvvatlamaydi.");
    return;
  }
  isLocating.value = true;
  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      isLocating.value = false;
      const { latitude, longitude } = pos.coords;
      if (map) {
        map.flyTo({
          center: [longitude, latitude],
          zoom: 15,
          speed: 1.8,
          curve: 1.2,
        });
      }
      await setPickerLocation(latitude, longitude);
    },
    (err) => {
      isLocating.value = false;
      console.warn("Geolocation error:", err.message);
      alert("Lokatsiyani aniqlashga ruxsat berilmadi.");
    },
    { enableHighAccuracy: true, timeout: 10000 },
  );
}

async function renderRoute(stops: Array<{ name: string; lat?: number; lon?: number }>) {
  if (!map) return;

  // Clear existing markers & route layer
  routeMarkers.forEach((m) => m.remove());
  routeMarkers = [];

  if (map.getSource("route")) {
    if (map.getLayer("route-casing")) map.removeLayer("route-casing");
    if (map.getLayer("route-line")) map.removeLayer("route-line");
    map.removeSource("route");
  }

  const validPoints: [number, number][] = [];
  stops.forEach((stop, idx) => {
    let lat = stop.lat;
    let lon = stop.lon;
    if (!lat || !lon) {
      const cityCoords = getCityCoordinates(stop.name);
      if (cityCoords) {
        lat = cityCoords.lat;
        lon = cityCoords.lon;
      }
    }
    if (lat && lon && map) {
      validPoints.push([lon, lat]);
      const type = idx === 0 ? "start" : idx === stops.length - 1 ? "end" : "waypoint";
      const el = createMarkerElement(type, idx);
      const marker = new Marker({ element: el })
        .setLngLat([lon, lat])
        .setPopup(new Popup({ offset: 12 }).setText(stop.name))
        .addTo(map);
      routeMarkers.push(marker);
    }
  });

  if (validPoints.length >= 2 && map) {
    const routeData = await fetchOSRMRoute(validPoints);
    let lineCoordinates: [number, number][] = validPoints;

    if (routeData) {
      lineCoordinates = routeData.coordinates;
      routeInfo.value = {
        distanceKm: routeData.distanceKm,
        durationMin: routeData.durationMin,
      };
    } else {
      routeInfo.value = null;
    }

    map.addSource("route", {
      type: "geojson",
      data: {
        type: "Feature",
        properties: {},
        geometry: {
          type: "LineString",
          coordinates: lineCoordinates,
        },
      },
    });

    // Sleek route line styling with subtle glow casing
    map.addLayer({
      id: "route-casing",
      type: "line",
      source: "route",
      layout: {
        "line-join": "round",
        "line-cap": "round",
      },
      paint: {
        "line-color": "#FFD600",
        "line-width": 7,
        "line-opacity": 0.8,
      },
    });

    map.addLayer({
      id: "route-line",
      type: "line",
      source: "route",
      layout: {
        "line-join": "round",
        "line-cap": "round",
      },
      paint: {
        "line-color": "#121212",
        "line-width": 4,
      },
    });

    // Fit map bounds to show full route
    const bounds = new LngLatBounds();
    validPoints.forEach((pt) => bounds.extend(pt));
    map.fitBounds(bounds, {
      padding: { top: 80, bottom: 50, left: 60, right: 60 },
      maxZoom: 14,
      duration: 1000,
    });
  }
}

onMounted(() => {
  if (!mapContainer.value) return;

  const defaultCenter = props.initialLocation
    ? [props.initialLocation.lon, props.initialLocation.lat]
    : [127.4897, 36.6424]; // Center of Korea (Cheongju area)

  const instance = new MapLibreMap({
    container: mapContainer.value,
    style: MAP_STYLE,
    center: defaultCenter as [number, number],
    zoom: props.initialLocation ? 14 : 7,
    interactive: props.interactive,
    attributionControl: false,
  });

  instance.addControl(new NavigationControl({ showCompass: false }), "bottom-right");

  instance.on("load", () => {
    map = instance;
    if (props.mode === "picker" && props.initialLocation) {
      setPickerLocation(props.initialLocation.lat, props.initialLocation.lon, undefined, false);
    } else if (props.mode === "route" && props.routeStops.length) {
      renderRoute(props.routeStops);
    }

    if (props.mode === "picker") {
      instance.on("click", async (e) => {
        const { lat, lng } = e.lngLat;
        await setPickerLocation(lat, lng);
      });
    }
  });

  map = instance;

  if (mapContainer.value) {
    resizeObserver = new ResizeObserver(() => {
      map?.resize();
    });
    resizeObserver.observe(mapContainer.value);
  }
});

watch(
  () => props.routeStops,
  (newStops) => {
    if (props.mode === "route" && map && map.isStyleLoaded()) {
      renderRoute(newStops);
    }
  },
  { deep: true },
);

watch(
  () => props.initialLocation,
  (newLoc) => {
    if (newLoc && map) {
      map.flyTo({ center: [newLoc.lon, newLoc.lat], zoom: 14 });
      setPickerLocation(newLoc.lat, newLoc.lon, undefined, false);
    }
  },
);

onBeforeUnmount(() => {
  if (resizeObserver) {
    resizeObserver.disconnect();
    resizeObserver = null;
  }
  if (map) {
    map.remove();
    map = null;
  }
});
</script>

<template>
  <div class="relative w-full overflow-hidden rounded-2xl border border-yulda-gray-200 bg-yulda-gray-100 shadow-sm">
    <!-- Top Bar / Label & Action Controls -->
    <div
      v-if="label || mode === 'picker'"
      class="absolute left-3 top-3 z-10 flex max-w-[calc(100%-24px)] flex-wrap items-center gap-2"
    >
      <div v-if="label" class="rounded-xl bg-white/90 px-3 py-1.5 text-xs font-semibold text-yulda-black shadow-md backdrop-blur">
        {{ label }}
      </div>

      <!-- Use My Location Button -->
      <button
        v-if="mode === 'picker'"
        type="button"
        class="flex items-center gap-1.5 rounded-xl bg-yulda-black px-3 py-1.5 text-xs font-semibold text-white shadow-lg transition-transform hover:scale-105 active:scale-95"
        :disabled="isLocating"
        @click="handleUseMyLocation"
      >
        <LocateFixed class="h-3.5 w-3.5 text-yulda-yellow" :class="{ 'animate-spin': isLocating }" />
        <span>{{ isLocating ? "Aniqlanmoqda..." : "Mening lokatsiyam (GPS)" }}</span>
      </button>
    </div>

    <!-- Route HUD Card (Distance & Duration) -->
    <div
      v-if="mode === 'route' && routeInfo"
      class="absolute left-3 top-3 z-10 flex items-center gap-3 rounded-xl bg-white/95 px-4 py-2.5 shadow-lg backdrop-blur"
    >
      <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-yulda-yellow text-yulda-black font-bold">
        <RouteIcon class="h-4 w-4" />
      </div>
      <div>
        <p class="text-xs font-medium text-yulda-gray-500">Avto yo'nalish masofasi</p>
        <p class="text-sm font-bold text-yulda-black">
          {{ routeInfo.distanceKm }} km
          <span class="text-xs font-normal text-yulda-gray-500">
            (~{{ Math.floor(routeInfo.durationMin / 60) > 0 ? `${Math.floor(routeInfo.durationMin / 60)}s ` : '' }}{{ routeInfo.durationMin % 60 }}daq)
          </span>
        </p>
      </div>
    </div>

    <!-- Selected Address Notification Badge (Picker mode) -->
    <div
      v-if="mode === 'picker' && selectedAddress"
      class="absolute bottom-3 left-3 right-16 z-10 truncate rounded-xl bg-white/95 px-3 py-2 text-xs font-medium text-yulda-black shadow-md backdrop-blur"
    >
      <div class="flex items-center gap-1.5 truncate">
        <MapPin class="h-3.5 w-3.5 flex-shrink-0 text-emerald-600" />
        <span class="truncate">{{ selectedAddress }}</span>
      </div>
    </div>

    <!-- Map Canvas Element -->
    <div ref="mapContainer" class="w-full" :style="containerStyle" />
  </div>
</template>

<style>
/* Clean MapLibre controls */
.maplibregl-ctrl-group {
  border-radius: 12px !important;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
  border: 1px solid #e5e7eb !important;
}
.maplibregl-ctrl button {
  width: 32px !important;
  height: 32px !important;
}
</style>
