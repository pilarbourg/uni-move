const map = L.map("librariesMap").setView([40.4168, -3.7038], 12);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);

var blueIcon = new L.Icon({
    iconUrl: '../assets/images/marker-icon-2x-blue.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34]
});

let libraryMarkers = [];

fetch("http://localhost:8080/api/libraries")
  .then((res) => res.json())
  .then((libraries) => {
    const list = document.getElementById("library-list");

    libraries.forEach((lib) => {
      const li = document.createElement("li");
      li.className = "library-card";
      li.innerHTML = `
        <h4>${lib.name}</h4>
        <p><i>${lib.address.street || ""}, ${lib.address.locality || ""}</i></p>
        <p><strong>Services:</strong> ${lib.services || "Not available"}</p>
        <p><strong>Description:</strong> ${lib.description || "No description"}</p>
        ${lib.link ? `<a href="${lib.link}" target="_blank">Visit Website</a>` : ""}
      `;
      list.appendChild(li);

      if (lib.latitude && lib.longitude) {
        const marker = L.marker([lib.latitude, lib.longitude], { icon: blueIcon })
          .addTo(map)
          .bindPopup(`
            <b>${lib.name}</b><br>
            ${lib.address.street || ""}, ${lib.address.locality || ""}<br>
            <strong>Services:</strong> ${lib.services || "Not available"}<br>
            ${lib.link ? `<a href="${lib.link}" target="_blank">Website</a>` : ""}
          `);
        libraryMarkers.push(marker);
      }
    });

    if (libraryMarkers.length > 0) {
      const bounds = L.latLngBounds(libraryMarkers.map((m) => m.getLatLng()));
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  })
  .catch((err) => console.error("Error fetching libraries:", err));