const universitySelect = document.getElementById("universitySelect");
const radiusSelect = document.getElementById("radiusSelect");
let map, uniMarker, clinicMarkers = [];

// Initialize map
map = L.map("map").setView([20, 0], 2);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors"
}).addTo(map);

// Load universities from Flask backend
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
    console.error("Error fetching universities:", err);
  }
}

async function fetchClinics() {
  const selected = universitySelect.options[universitySelect.selectedIndex];
  if (!selected) return;

  const universityId = selected.value;
  const radius = radiusSelect.value;

  try {
    const res = await fetch(`http://127.0.0.1:5000/universities/${universityId}/clinics?radius=${radius}`);
    const clinics = await res.json();

    const uniLat = parseFloat(selected.dataset.lat);
    const uniLng = parseFloat(selected.dataset.lng);

    // Clear previous markers
    if (uniMarker) map.removeLayer(uniMarker);
    clinicMarkers.forEach(m => map.removeLayer(m));
    clinicMarkers = [];

    // University marker
    uniMarker = L.marker([uniLat, uniLng])
      .addTo(map)
      .bindPopup(`<b>${selected.textContent}</b>`)
      .openPopup();

    // Clinics markers
    clinics.forEach(clinic => {
      const marker = L.circleMarker([clinic.latitude, clinic.longitude], {
        color: "#d32f2f",
        radius: 8,
        fillOpacity: 0.8
      }).addTo(map).bindPopup(
        `<b>${clinic.name}</b><br>Distance: ${clinic.distance_km} km`
      );
      clinicMarkers.push(marker);
    });

    // Adjust map view
    const allCoords = [[uniLat, uniLng], ...clinics.map(c => [c.latitude, c.longitude])];
    map.fitBounds(allCoords, { padding: [50, 50] });
  } catch (err) {
    console.error("Error fetching clinics:", err);
  }
}

universitySelect.addEventListener("change", fetchClinics);
radiusSelect.addEventListener("change", fetchClinics);

// Load universities at start
fetchUniversities();
