<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { LocateFixed, MapPin, RotateCcw, Route as RouteIcon } from "lucide-vue-next";
import {
  LngLatBounds,
  Map as MapLibreMap,
  Marker,
  NavigationControl,
  Popup,
  setWorkerUrl,
  type StyleSpecification,
} from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url";

setWorkerUrl(workerUrl);

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
    initialCoords?: Coordinates;
    routeStops?: Array<{ name: string; lat?: number; lon?: number }>;
    height?: string;
    aspectRatio?: string;
    interactive?: boolean;
    label?: string;
  }>(),
  {
    mode: "picker",
    initialLocation: undefined,
    initialCoords: undefined,
    routeStops: () => [],
    height: undefined,
    aspectRatio: "16/10",
    interactive: true,
    label: undefined,
  },
);

const emit = defineEmits<{
  select: [location: GeocodedLocation];
}>();

const effectiveLocation = computed(() => props.initialLocation || props.initialCoords);

const containerStyle = computed(() => {
  if (props.height) {
    return { height: props.height };
  }
  const ratio = (props.aspectRatio || "16/10").replace(":", " / ");
  return {
    aspectRatio: ratio,
    minHeight: "340px",
    maxHeight: "620px",
  };
});

const mapContainer = ref<HTMLDivElement | null>(null);
const canvasEl = ref<HTMLCanvasElement | null>(null);
let map: MapLibreMap | null = null;
let activeMarker: Marker | null = null;
let routeMarkers: Marker[] = [];
let resizeObserver: ResizeObserver | null = null;
let savedRouteBounds: LngLatBounds | null = null;
let routeGeoPoints: [number, number][] = []; // [lon, lat] for canvas redraw
let dashOffset = 0;
let animFrameId: number | null = null;

const isLocating = ref(false);
const selectedAddress = ref<string>("");
const routeInfo = ref<{ distanceKm: number; durationMin: number } | null>(null);

const { locale } = useI18n();

const routeSummary = computed(() => {
  if (!routeInfo.value) return null;

  const from = props.routeStops[0]?.name?.trim() || "A";
  const to = props.routeStops[props.routeStops.length - 1]?.name?.trim() || "B";
  const points = `${from} > ${to}`;

  const dist = `${routeInfo.value.distanceKm} km`;

  const hours = Math.floor(routeInfo.value.durationMin / 60);
  const mins = routeInfo.value.durationMin % 60;
  let duration = "";
  if (hours > 0 && mins > 0) {
    duration = `${hours} h, ${mins} m`;
  } else if (hours > 0) {
    duration = `${hours} h`;
  } else if (mins > 0) {
    duration = `${mins} m`;
  }

  const details = duration ? `${dist} - ${duration}` : dist;
  return {
    points,
    details,
  };
});

const recenterTitle = computed(() => {
  if (locale.value === "ru") return "Центрировать карту / Сбросить масштаб";
  if (locale.value === "en") return "Recenter map / Reset zoom";
  if (locale.value === "ko") return "지도 중심 맞추기 / 확대 복원";
  return "Xaritani markazga keltirish / Masshtabni tiklash";
});

const gpsButtonText = computed(() => {
  if (isLocating.value) {
    if (locale.value === "ru") return "Определение...";
    if (locale.value === "en") return "Locating...";
    if (locale.value === "ko") return "위치 확인 중...";
    return "Aniqlanmoqda...";
  }
  if (locale.value === "ru") return "Мое местоположение (GPS)";
  if (locale.value === "en") return "My Location (GPS)";
  if (locale.value === "ko") return "내 위치 (GPS)";
  return "Mening lokatsiyam (GPS)";
});

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
      <div class="flex h-8 w-8 items-center justify-center rounded-full bg-yulda-black font-bold text-xs text-white shadow-lg ring-2 ring-yulda-yellow">
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

// ─── Canvas overlay: draw dashed A→B line (like Kakao/Naver) ─────────────
function drawDashedLine() {
  if (!canvasEl.value || !map || routeGeoPoints.length < 2) return;

  const canvas = canvasEl.value;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const container = map.getContainer();
  const w = container.clientWidth;
  const h = container.clientHeight;
  if (canvas.width !== w) canvas.width = w;
  if (canvas.height !== h) canvas.height = h;

  ctx.clearRect(0, 0, w, h);

  // Project geo coords → screen pixels
  const pixels = routeGeoPoints.map((pt) => {
    const p = map!.project(pt as [number, number]);
    return { x: p.x, y: p.y };
  });

  // Marker radius in px (markers are h-8 w-8 = 32px → radius 16px + 2px ring = 18px)
  const MARKER_RADIUS = 18;

  // Build offset pixels: shift start outward toward next point, end outward toward prev point
  const pts = pixels.map((p) => ({ ...p }));
  if (pts.length >= 2) {
    // Offset start point: move away from center toward pts[1]
    const dx0 = pts[1].x - pts[0].x;
    const dy0 = pts[1].y - pts[0].y;
    const len0 = Math.sqrt(dx0 * dx0 + dy0 * dy0) || 1;
    pts[0] = { x: pts[0].x + (dx0 / len0) * MARKER_RADIUS, y: pts[0].y + (dy0 / len0) * MARKER_RADIUS };

    // Offset end point: move away from center toward pts[n-2]
    const last = pts.length - 1;
    const dx1 = pts[last - 1].x - pts[last].x;
    const dy1 = pts[last - 1].y - pts[last].y;
    const len1 = Math.sqrt(dx1 * dx1 + dy1 * dy1) || 1;
    pts[last] = { x: pts[last].x + (dx1 / len1) * MARKER_RADIUS, y: pts[last].y + (dy1 / len1) * MARKER_RADIUS };
  }

  // Compute quadratic bezier control point: midpoint + 10% perpendicular offset
  const start = pts[0];
  const end = pts[pts.length - 1];
  const mid = { x: (start.x + end.x) / 2, y: (start.y + end.y) / 2 };
  const totalLen = Math.sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2);
  // Perpendicular direction (rotate 90°)
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  const len = totalLen || 1;
  const curveOffset = totalLen * 0.10;
  const cx = mid.x + (dy / len) * curveOffset;
  const cy = mid.y - (dx / len) * curveOffset;

  function drawCurvedPath() {
    ctx!.moveTo(start.x, start.y);
    ctx!.quadraticCurveTo(cx, cy, end.x, end.y);
  }

  // 1. Dark outer casing
  ctx.beginPath();
  drawCurvedPath();
  ctx.strokeStyle = "rgba(18, 18, 18, 0.85)";
  ctx.lineWidth = 7;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.setLineDash([]);
  ctx.stroke();

  // 2. Yellow dashed line on top
  ctx.beginPath();
  drawCurvedPath();
  ctx.strokeStyle = "#FFD600";
  ctx.lineWidth = 3.5;
  ctx.lineCap = "butt";
  ctx.lineJoin = "round";
  ctx.setLineDash([16, 11]);
  ctx.lineDashOffset = -dashOffset;
  ctx.stroke();
  ctx.setLineDash([]);
}

function startDashAnimation() {
  if (animFrameId !== null) cancelAnimationFrame(animFrameId);
  const DASH_CYCLE = 27; // 16 dash + 11 gap
  function tick() {
    dashOffset = (dashOffset + 0.5) % DASH_CYCLE;
    drawDashedLine();
    animFrameId = requestAnimationFrame(tick);
  }
  animFrameId = requestAnimationFrame(tick);
}

function stopDashAnimation() {
  if (animFrameId !== null) {
    cancelAnimationFrame(animFrameId);
    animFrameId = null;
  }
}

function clearCanvas() {
  stopDashAnimation();
  routeGeoPoints = [];
  dashOffset = 0;
  if (!canvasEl.value) return;
  const ctx = canvasEl.value.getContext("2d");
  if (ctx) ctx.clearRect(0, 0, canvasEl.value.width, canvasEl.value.height);
}

function bindMapRedraw() {
  if (!map) return;
  const redraw = () => drawDashedLine();
  map.on("move", redraw);
  map.on("zoom", redraw);
  map.on("rotate", redraw);
  map.on("pitch", redraw);
  map.on("resize", redraw);
  map.on("render", redraw);
}
// ─────────────────────────────────────────────────────────────────────────

async function renderRoute(stops: Array<{ name: string; lat?: number; lon?: number }>) {
  if (!map) return;

  // Clear existing markers & canvas line
  routeMarkers.forEach((m) => m.remove());
  routeMarkers = [];
  clearCanvas();
  routeInfo.value = null;

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

  if (validPoints.length === 1 && map) {
    savedRouteBounds = null;
    map.flyTo({ center: validPoints[0], zoom: 12, duration: 800 });
  }

  if (validPoints.length >= 2 && map) {
    // Store points for canvas redraw on pan/zoom
    routeGeoPoints = validPoints;

    // Fit map to show full route
    const bounds = new LngLatBounds();
    validPoints.forEach((pt) => bounds.extend(pt));
    savedRouteBounds = bounds;
    map.fitBounds(bounds, {
      padding: { top: 80, bottom: 50, left: 60, right: 60 },
      maxZoom: 14,
      duration: 1000,
    });

    // Draw immediately and again after fly animation finishes
    drawDashedLine();
    setTimeout(() => startDashAnimation(), 100);

    // Fetch OSRM for HUD
    fetchOSRMRoute(validPoints).then((routeData) => {
      if (routeData) {
        routeInfo.value = {
          distanceKm: routeData.distanceKm,
          durationMin: routeData.durationMin,
        };
      }
    }).catch(() => {});
  }
}

function handleRecenter() {
  if (!map) return;

  if (props.mode === "route") {
    if (savedRouteBounds) {
      map.fitBounds(savedRouteBounds, {
        padding: { top: 80, bottom: 50, left: 60, right: 60 },
        maxZoom: 14,
        duration: 800,
      });
      return;
    }
    if (props.routeStops.length >= 2) {
      renderRoute(props.routeStops);
      return;
    }
  }

  const targetCoords = activeMarker
    ? { lat: activeMarker.getLngLat().lat, lon: activeMarker.getLngLat().lng }
    : effectiveLocation.value;

  if (targetCoords) {
    map.flyTo({
      center: [targetCoords.lon, targetCoords.lat],
      zoom: 14,
      essential: true,
      duration: 800,
    });
    return;
  }

  // Default: Center of Korea
  map.flyTo({
    center: [127.4897, 36.6424],
    zoom: 7,
    essential: true,
    duration: 800,
  });
}

onMounted(() => {
  if (!mapContainer.value) return;

  const defaultCenter = effectiveLocation.value
    ? [effectiveLocation.value.lon, effectiveLocation.value.lat]
    : [127.4897, 36.6424]; // Center of Korea (Cheongju area)

  const instance = new MapLibreMap({
    container: mapContainer.value,
    style: MAP_STYLE,
    center: defaultCenter as [number, number],
    zoom: effectiveLocation.value ? 14 : 7,
    interactive: props.interactive,
    attributionControl: false,
  });

  instance.addControl(new NavigationControl({ showCompass: false }), "bottom-right");

  instance.on("load", () => {
    map = instance;
    bindMapRedraw();

    if ((props.mode === "picker" || props.mode === "view") && effectiveLocation.value) {
      setPickerLocation(effectiveLocation.value.lat, effectiveLocation.value.lon, undefined, false);
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
      drawDashedLine();
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
  effectiveLocation,
  (newLoc) => {
    if (newLoc && map) {
      map.flyTo({ center: [newLoc.lon, newLoc.lat], zoom: 14 });
      setPickerLocation(newLoc.lat, newLoc.lon, undefined, false);
    }
  },
);

onBeforeUnmount(() => {
  stopDashAnimation();
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
        <span>{{ gpsButtonText }}</span>
      </button>
    </div>

    <!-- Route HUD Card (Compact, universal: Seoul > Busan (393 km - 4 h, 35 m)) -->
    <div
      v-if="mode === 'route' && routeInfo && routeSummary"
      class="absolute left-3 top-3 z-10 flex items-center gap-2.5 rounded-xl border border-yulda-gray-200/90 bg-white/95 px-3.5 py-2 shadow-lg backdrop-blur"
    >
      <div class="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg bg-yulda-yellow text-yulda-black font-bold">
        <RouteIcon class="h-3.5 w-3.5" />
      </div>
      <div class="flex flex-wrap items-center gap-1.5 text-xs font-bold text-yulda-black">
        <span>{{ routeSummary.points }}</span>
        <span class="font-medium text-yulda-gray-500">({{ routeSummary.details }})</span>
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

    <!-- Floating Recenter / Reset View Button (Positioned above + / - zoom buttons) -->
    <div class="absolute bottom-[86px] right-[10px] z-10">
      <button
        type="button"
        class="group flex h-[32px] w-[32px] items-center justify-center rounded-xl border border-yulda-gray-200 bg-white text-yulda-gray-700 shadow-md transition-all hover:bg-yulda-yellow hover:text-yulda-black hover:scale-105 active:scale-95"
        :title="recenterTitle"
        @click="handleRecenter"
      >
        <RotateCcw class="h-4 w-4 transition-transform duration-300 group-hover:-rotate-90" />
      </button>
    </div>

    <!-- Map Canvas Element -->
    <div ref="mapContainer" class="w-full" :style="containerStyle" />

    <!-- Canvas overlay for dashed A→B line (drawn via Canvas 2D API, like Kakao/Naver) -->
    <canvas
      ref="canvasEl"
      class="pointer-events-none absolute inset-0"
      style="z-index: 5;"
    />
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
