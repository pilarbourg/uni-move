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

// Step 1: Define GitHub icons
var redIcon = new L.Icon({
	iconUrl: 'assets\images\marker-icon-2x-red.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

var blueIcon = new L.Icon({
	iconUrl: 'assets\imagesmarker-icon-2x-blue.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

// Fetch universities
async function fetchUniversities() {
  try {
    const res = await fetch("http://127.0.0.1:5000/universities");
    const universities = await res.json();

    universitySelect.innerHTML = "";
    universities.forEach(u => {
      const option = document.createElement("option");
      option.value = JSON.stringify({ lat: u.latitude, lng: u.longitude, id: u.id, name: u.name });
      option.textContent = u.name;
      universitySelect.appendChild(option);
    });
  } catch (err) {
    console.error("Error fetching universities:", err);
  }
}

// Fetch clinics
async function fetchClinics() {
  const selected = universitySelect.value;
  if (!selected) return alert("Select a university!");
  const uni = JSON.parse(selected);
  const radius = radiusSelect.value;

  try {
    const res = await fetch(`http://127.0.0.1:5000/universities/${uni.id}/clinics?radius=${radius}`);
    const clinics = await res.json();

    // Clear old markers
    if (universityMarker) map.removeLayer(universityMarker);
    clinicMarkers.forEach(m => map.removeLayer(m));
    clinicMarkers = [];

    // Step 3: University marker with redIcon
    universityMarker = L.marker([parseFloat(uni.lat), parseFloat(uni.lng)], { icon: redIcon })
      .addTo(map)
      .bindPopup(`<b>${uni.name}</b>`).openPopup();

    // Step 3: Clinic markers with blueIcon
    clinics.forEach(c => {
      const marker = L.marker([parseFloat(c.latitude), parseFloat(c.longitude)], { icon: blueIcon })
        .addTo(map)
        .bindPopup(`<b>${c.name}</b><br>Distance: ${c.distance_km} km`);
      clinicMarkers.push(marker);
    });

    // Adjust map view
    const allCoords = [[parseFloat(uni.lat), parseFloat(uni.lng)], ...clinics.map(c => [parseFloat(c.latitude), parseFloat(c.longitude)])];
    if (allCoords.length > 0) map.fitBounds(allCoords, { padding: [50,50] });
    else map.setView([parseFloat(uni.lat), parseFloat(uni.lng)], 14);

  } catch (err) {
    console.error("Error fetching clinics:", err);
  }
}

// Button listener
document.getElementById("showClinicsBtn").addEventListener("click", e => {
  e.preventDefault();
  fetchClinics();
});

// Initialize
fetchUniversities();