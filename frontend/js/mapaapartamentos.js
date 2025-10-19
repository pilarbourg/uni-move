const map = L.map("map").setView([40.4168, -3.7038], 12);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19 }).addTo(map);

const redIcon = new L.Icon({
  iconUrl: "../assets/images/marker-icon-2x-red.png",
  iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34],
});

let markers = [];

function clearMarkers() { markers.forEach(m => map.removeLayer(m)); markers = []; }

function render(list) {
  clearMarkers();
  const container = document.getElementById("apartmentsList");
  container.innerHTML = "";

  list.forEach(a => {
    const lat = parseFloat(a.latitud);
    const lng = parseFloat(a.longitud);
    if (isFinite(lat) && isFinite(lng)) {
      const marker = L.marker([lat, lng], { icon: redIcon })
        .addTo(map)
        .bindPopup(`<b>${a.titulo}</b><br>${a.barrio ?? ""}<br><b>${a.precio ?? "?"} €</b><br>${a.tamano_m2 ?? "?"} m²`);
      markers.push(marker);
    }
    const card = document.createElement("div");
    card.className = "clinic-card"; // reutilizamos estilos de clínicas
    card.innerHTML = `
      <h3>${a.titulo ?? "Apartment"}</h3>
      <p><b>Neighborhood:</b> ${a.barrio ?? "N/A"}</p>
      <p><b>Price:</b> ${a.precio ?? "N/A"} €</p>
      <p><b>Size:</b> ${a.tamano_m2 ?? "N/A"} m²</p>
      <p><b>Furnished:</b> ${a.amueblado ? "Yes" : "No"}</p>
    `;
    container.appendChild(card);
  });

  const coords = list
    .map(a => [parseFloat(a.latitud), parseFloat(a.longitud)])
    .filter(([la, lo]) => isFinite(la) && isFinite(lo));
  if (coords.length) map.fitBounds(coords, { padding: [50, 50] });
}

async function fetchAll() {
  const res = await fetch("http://127.0.0.1:8080/get_apartments");
  render(await res.json());
}

async function filter() {
  const barrio = document.getElementById("barrioInput").value.trim();
  const precio = document.getElementById("precioInput").value.trim();
  let url = "";

  if (barrio && precio) {
    url = `http://127.0.0.1:8080/get_apartments_by_barrio_price?barrio=${encodeURIComponent(barrio)}&presupuesto=${precio}`;
  } else if (barrio) {
    url = `http://127.0.0.1:8080/get_apartments_by_barrio/${encodeURIComponent(barrio)}`;
  } else if (precio) {
    url = `http://127.0.0.1:8080/get_apartments_by_price/${precio}`;
  } else {
    return fetchAll();
  }

  const res = await fetch(url);
  render(await res.json());
}

document.getElementById("showApartmentsBtn").addEventListener("click", (e) => {
  e.preventDefault();
  filter();
});

fetchAll();
