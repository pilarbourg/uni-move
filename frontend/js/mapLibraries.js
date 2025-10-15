const map = L.map("librariesMap").setView([40.4168, -3.7038], 12);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);

const blueIcon = new L.Icon({
  iconUrl: '../assets/images/marker-icon-2x-blue.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34]
});

let allLibraries = [];       
let allMarkers = [];         
let selectedMarker = null;   

const libraryList = document.getElementById("library-list");

function clearMarkers() {
  allMarkers.forEach(marker => map.removeLayer(marker));
  allMarkers = [];
  if (selectedMarker) {
    map.removeLayer(selectedMarker);
    selectedMarker = null;
  }
}

function showAllLibraries() {
  clearMarkers();
  allLibraries.forEach(lib => {
    const lat = parseFloat(lib.latitude);
    const lng = parseFloat(lib.longitude);
    if (!isNaN(lat) && !isNaN(lng)) {
      const marker = L.marker([lat, lng], { icon: blueIcon })
        .addTo(map)
        .bindPopup(`<b>${lib.name}</b><br>${lib.address.street || ""}, ${lib.address.locality || ""}`);
      allMarkers.push(marker);
    }
  });

  if (allMarkers.length > 0) {
    const bounds = L.latLngBounds(allMarkers.map(m => m.getLatLng()));
    map.fitBounds(bounds, { padding: [50, 50] });
  }
}

function showLibrary(lib) {
  clearMarkers();

  const lat = parseFloat(lib.latitude);
  const lng = parseFloat(lib.longitude);
  if (isNaN(lat) || isNaN(lng)) return;

  selectedMarker = L.marker([lat, lng], { icon: blueIcon }).addTo(map);

  selectedMarker.bindPopup(`<b>${lib.name}</b><br>${lib.address.street || ""}, ${lib.address.locality || ""}`)
    .openPopup();

  map.setView([lat, lng], 16, { animate: true });

  selectedMarker.on("popupclose", () => {
    showAllLibraries();
  });
}

fetch("http://localhost:8080/api/libraries")
  .then(res => res.json())
  .then(libraries => {
    allLibraries = libraries;

    libraries.forEach(lib => {
      const li = document.createElement("li");
      li.className = "library-card";
      li.innerHTML = `
        <h4>${lib.name}</h4>
        <p><i>${lib.address.street || ""}, ${lib.address.locality || ""}</i></p>
        <p><strong>Services:</strong> ${lib.services || "Not available"}</p>
        <p><strong>Description:</strong> ${lib.description || "No description"}</p>
        ${lib.link ? `<a href="${lib.link}" target="_blank">Visit Website</a>` : ""}
      `;
      libraryList.appendChild(li);

      li.addEventListener("click", () => {
        showLibrary(lib);
      });

      li.addEventListener("mouseenter", () => {
        li.style.cursor = "pointer";
      });
    });

    showAllLibraries();
  })
  .catch(err => console.error("Error fetching libraries:", err));

document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => map.invalidateSize(), 500);
});