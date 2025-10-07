// Inicializar mapa centrado en Madrid
const map = L.map("map").setView([40.4168, -3.7038], 12);

// Capa base
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);

// Icono personalizado
var apartmentIcon = new L.Icon({
  iconUrl: "/assets/images/marker-icon-2x-green.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

// Variables globales
let apartmentMarkers = [];

// Obtener apartamentos desde el backend
async function fetchApartments() {
  try {
    const res = await fetch("http://127.0.0.1:5000/apartamentos");
    const apartments = await res.json();

    // Limpiar marcadores anteriores
    apartmentMarkers.forEach((m) => map.removeLayer(m));
    apartmentMarkers = [];

    // Añadir marcadores al mapa
    apartments.forEach((apt) => {
      if (!apt.latitude || !apt.longitude) return; // saltar si faltan coords

      const marker = L.marker(
        [parseFloat(apt.latitude), parseFloat(apt.longitude)],
        { icon: apartmentIcon }
      )
        .addTo(map)
        .bindPopup(
          `<b>${apt.titulo}</b><br>${apt.barrio || "Barrio desconocido"}<br>
           ${apt.precio ? apt.precio + " €" : "Precio no disponible"}<br>
           ${apt.tamaño_m2 ? apt.tamaño_m2 + " m²" : ""}
          `
        );

      apartmentMarkers.push(marker);
    });

    // Centrar vista en los apartamentos cargados
    if (apartments.length > 0) {
      const coords = apartments
        .filter((a) => a.latitude && a.longitude)
        .map((a) => [a.latitude, a.longitude]);
      if (coords.length > 0) map.fitBounds(coords, { padding: [50, 50] });
    }
  } catch (err) {
    console.error("Error al obtener los apartamentos:", err);
  }
}

// Inicializar
fetchApartments();
