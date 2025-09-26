const map = L.map("map").setView([40.4168, -3.7038], 13);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);

let universitySelect = document.getElementById("universitySelect");
let radiusSelect = document.getElementById("radiusSelect");
let universityMarker = null;
let clinicMarkers = [];

async function fetchUniversities() {
  try {
    const res = await fetch("http://127.0.0.1:5000/universities");
    const universities = await res.json();

    universitySelect.innerHTML = "";
    universities.forEach(u => {
      const option = document.createElement("option");
      option.value = u.id;
      option.textContent = u.name;
      option.dataset.lat = u.latitude;
      option.dataset.lng = u.longitude;
      universitySelect.appendChild(option);
    });
  } catch (err) {
    console.error(err);
  }
}

async function fetchClinics() {
  const selected = universitySelect.options[universitySelect.selectedIndex];
  if (!selected) return alert("Please select a university first.");

  const uniLat = parseFloat(selected.dataset.lat);
  const uniLng = parseFloat(selected.dataset.lng);
  const uniId = selected.value;
  const radius = radiusSelect.value;

  try {
    const res = await fetch(`http://127.0.0.1:5000/universities/${uniId}/clinics?radius=${radius}`);
    const clinics = await res.json();

    // Clear old markers
    if (universityMarker) map.removeLayer(universityMarker);
    clinicMarkers.forEach(m => map.removeLayer(m));
    clinicMarkers = [];

    // 🔴 University marker inline
    universityMarker = L.marker([uniLat, uniLng], {
      icon: new L.Icon({
        iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
        shadowUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      })
    }).addTo(map).bindPopup(`<b>${selected.textContent}</b>`).openPopup();

    // 🔵 Clinics markers inline
    clinics.forEach(c => {
      const marker = L.marker([parseFloat(c.latitude), parseFloat(c.longitude)], {
        icon: new L.Icon({
          iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png",
          shadowUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png",
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        })
      }).addTo(map).bindPopup(`<b>${c.name}</b><br>Distance: ${c.distance_km} km`);
      clinicMarkers.push(marker);
    });

    // Fit map to markers
    const allCoords = [[uniLat, uniLng], ...clinics.map(c => [parseFloat(c.latitude), parseFloat(c.longitude)])];
    if (allCoords.length > 0) map.fitBounds(allCoords, { padding: [50, 50] });
    else map.setView([uniLat, uniLng], 14);

  } catch (err) {
    console.error(err);
  }
}

document.getElementById("showClinicsBtn").addEventListener("click", e => {
  e.preventDefault();
  fetchClinics();
});

fetchUniversities();