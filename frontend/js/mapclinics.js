// Initialize map
const map = L.map("map").setView([40.4168, -3.7038], 13);

// Add tile layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);

// Globals
let universitySelect = document.getElementById("universitySelect");
let radiusSelect = document.getElementById("radiusSelect");
let universityMarker = null;
let clinicMarkers = [];

// Fetch universities
async function fetchUniversities() {
  try {
    const res = await fetch("http://127.0.0.1:5000/universities");
    const universities = await res.json();

    universitySelect.innerHTML = "";
    universities.forEach((u) => {
      const option = document.createElement("option");
      option.value = u.id;
      option.textContent = u.name;
      option.dataset.lat = u.latitude;
      option.dataset.lng = u.longitude;
      universitySelect.appendChild(option);
    });

    console.log("Universities loaded:", universities);
  } catch (err) {
    console.error("Error fetching universities:", err);
  }
}

// Fetch clinics near selected university
async function fetchClinics() {
  const selected = universitySelect.options[universitySelect.selectedIndex];
  if (!selected) {
    alert("Please select a university first.");
    return;
  }

  const universityId = selected.value;
  const radius = radiusSelect.value;

  console.log("Fetching clinics for:", universityId, "radius:", radius);

  try {
    const res = await fetch(
      `http://127.0.0.1:5000/universities/${universityId}/clinics?radius=${radius}`
    );
    const clinics = await res.json();

    console.log("Clinics response:", clinics);

    // Clear old markers
    clinicMarkers.forEach((m) => map.removeLayer(m));
    clinicMarkers = [];

    if (universityMarker) {
      map.removeLayer(universityMarker);
    }

    // University marker
    const uniLat = parseFloat(selected.dataset.lat);
    const uniLng = parseFloat(selected.dataset.lng);
    universityMarker = L.marker([uniLat, uniLng]).addTo(map);
    universityMarker.bindPopup(selected.textContent).openPopup();

    // Clinics markers
    clinics.forEach((clinic) => {
      const marker = L.marker([clinic.latitude, clinic.longitude]).addTo(map);
      marker.bindPopup(
        `<b>${clinic.name}</b><br>Distance: ${clinic.distance_km} km`
      );
      clinicMarkers.push(marker);
    });

    // Adjust view
    const allCoords = [
      [uniLat, uniLng],
      ...clinics.map((c) => [c.latitude, c.longitude]),
    ];
    if (allCoords.length > 0) {
      map.fitBounds(allCoords, { padding: [50, 50] });
    }
  } catch (err) {
    console.error("Error fetching clinics:", err);
  }
}

// Button listener
document.getElementById("showClinicsBtn").addEventListener("click", (e) => {
  e.preventDefault();
  fetchClinics();
});

// Init
fetchUniversities();
