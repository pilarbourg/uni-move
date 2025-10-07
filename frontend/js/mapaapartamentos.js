// ----------------- MAPA -----------------
const map = L.map("map").setView([40.4168, -3.7038], 12);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19 }).addTo(map);

// Icono personalizado (ruta relativa correcta desde /pages)
const apartmentIcon = new L.Icon({
  iconUrl: "../assets/images/marker-icon-2x-green.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

// Estado
let ALL_APARTMENTS = [];
let markers = [];

// ----------------- FETCH -----------------
async function loadApartments() {
  const res = await fetch("/api/apartamentos");
  const text = await res.text();

  if (!res.ok) {
    console.error("HTTP", res.status, text);
    throw new Error(`HTTP ${res.status}`);
  }
  try {
    ALL_APARTMENTS = JSON.parse(text);
  } catch (e) {
    console.error("Respuesta NO JSON:", text);
    throw e;
  }
}

// ----------------- RENDER -----------------
function clearMarkers() {
  markers.forEach(m => map.removeLayer(m));
  markers = [];
}

function render(apartments) {
  // Lista (similar a universidades)
  const ul = document.getElementById("results");
  ul.innerHTML = "";

  // Ordenar por precio ascendente (si existe)
  const sorted = [...apartments].sort((a, b) => (a.precio ?? Infinity) - (b.precio ?? Infinity));

  sorted.forEach(a => {
    const li = document.createElement("li");
    const precioStr = a.precio ? `${a.precio} €` : "Precio no disponible";
    const barrioStr = a.barrio || "Barrio desconocido";
    li.textContent = `${a.titulo || "Apartamento"} — ${barrioStr} — ${precioStr}`;
    ul.appendChild(li);
  });

  // Mapa
  clearMarkers();
  const bounds = [];
  sorted.forEach(a => {
    if (typeof a.latitude !== "number" || typeof a.longitude !== "number") return;
    const m = L.marker([a.latitude, a.longitude], { icon: apartmentIcon })
      .addTo(map)
      .bindPopup(
        `<b>${a.titulo || "Apartamento"}</b><br>` +
        `${a.barrio || "Barrio desconocido"}<br>` +
        `${a.precio ? a.precio + " €" : "Precio no disponible"}<br>` +
        `${a.tamano_m2 ? a.tamano_m2 + " m²" : ""}`
      );
    markers.push(m);
    bounds.push([a.latitude, a.longitude]);
  });
  if (bounds.length) map.fitBounds(bounds, { padding: [30, 30] });
}

// ----------------- FILTRO (como en universidades) -----------------
function applyFilter() {
  const barrio = document.getElementById("barrioInput").value.trim().toLowerCase();
  const presupuesto = document.getElementById("presupuestoInput").value.trim();
  const maxPrice = presupuesto ? Number(presupuesto) : null;

  let results = ALL_APARTMENTS;

  if (barrio) {
    results = results.filter(a => (a.barrio || "").toLowerCase().includes(barrio));
  }
  if (maxPrice != null && !Number.isNaN(maxPrice)) {
    results = results.filter(a => typeof a.precio === "number" && a.precio <= maxPrice);
  }

  if (results.length === 0) {
    document.getElementById("results").innerHTML = "<li>No apartments match your filters</li>";
    clearMarkers();
    return;
  }

  render(results);
}

// ----------------- INIT -----------------
async function init() {
  try {
    await loadApartments();
    render(ALL_APARTMENTS); // primera carga sin filtros
  } catch (e) {
    alert("No se pudieron cargar los apartamentos. Revisa la consola.");
  }

  document.getElementById("showApartmentsBtn").addEventListener("click", e => {
    e.preventDefault();
    applyFilter();
  });
  // También con Enter en los inputs
  ["barrioInput", "presupuestoInput"].forEach(id => {
    const el = document.getElementById(id);
    el.addEventListener("keydown", ev => { if (ev.key === "Enter") applyFilter(); });
  });
}

init();
