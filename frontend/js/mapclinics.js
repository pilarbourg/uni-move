const map = L.map("map").setView([40.4168, -3.7038], 13);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);

let universitySelect = document.getElementById("universitySelect");
let radiusSelect = document.getElementById("radiusSelect");
let universityMarker = null;
let clinicMarkers = [];

const redIcon = new L.Icon({
  iconUrl: "../assets/images/marker-icon-2x-red.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

const blueIcon = new L.Icon({
  iconUrl: "../assets/images/marker-icon-2x-blue.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

async function fetchUniversities() {
  try {
    const res = await fetch("http://127.0.0.1:8080/universities");
    const universities = await res.json();

    universitySelect.innerHTML = "";
    universities.forEach((u) => {
      const option = document.createElement("option");
      option.value = JSON.stringify({
        lat: u.latitude,
        lng: u.longitude,
        id: u.id,
        name: u.name,
      });
      option.textContent = u.name;
      universitySelect.appendChild(option);
    });
  } catch (err) {
    console.error("Error fetching universities:", err);
  }
}

async function fetchClinics() {
  const selected = universitySelect.value;
  if (!selected) return alert("Select a university!");
  const uni = JSON.parse(selected);
  const radius = radiusSelect.value;

  try {
    const res = await fetch(
      `http://127.0.0.1:8080/universities/${uni.id}/clinics?radius=${radius}`
    );
    const clinics = await res.json();

    if (!clinics || clinics.length === 0) {
      alert("No clinics found in this area.");
      return;
    }

    if (universityMarker) map.removeLayer(universityMarker);
    clinicMarkers.forEach((m) => map.removeLayer(m));
    clinicMarkers = [];

    universityMarker = L.marker([parseFloat(uni.lat), parseFloat(uni.lng)], {
      icon: redIcon,
    }).addTo(map)
      .bindPopup(`<b>${uni.name}</b>`)
      .openPopup();

    const listContainer = document.getElementById("clinic-list");
    listContainer.innerHTML = "<h3>Nearby Clinics</h3>";

    clinics.forEach((c) => {
      const schedule = c.schedule || "Not provided";
      const publicTransport = c.publicTransport || "Not provided";
      const phone = c.phoneNumber || "Not provided";
      const email = c.email || "Not provided";

      const marker = L.marker([c.latitude, c.longitude], { icon: blueIcon })
        .addTo(map)
        .bindPopup(`
          <b>${c.name}</b><br>
          <b>Schedule:</b> ${schedule}<br>
          <b>Public Transport:</b> ${publicTransport}<br>
          <b>Phone:</b> ${phone}<br>
          <b>Email:</b> ${email}
        `);
      clinicMarkers.push(marker);

      const div = document.createElement("div");
      div.classList.add("clinic-item");
      div.innerHTML = `
        <h4>${c.name}</h4>
        <p><b>Schedule:</b> ${schedule}</p>
        <p><b>Public Transport:</b> ${publicTransport}</p>
        <p><b>Phone:</b> ${phone}</p>
        <p><b>Email:</b> ${email}</p>
      `;

      div.addEventListener("click", () => {
        clinicMarkers.forEach((m) => map.removeLayer(m));
        clinicMarkers = [];

        const singleMarker = L.marker([c.latitude, c.longitude], { icon: blueIcon })
          .addTo(map)
          .bindPopup(`
            <b>${c.name}</b><br>
            <b>Schedule:</b> ${schedule}<br>
            <b>Public Transport:</b> ${publicTransport}<br>
            <b>Phone:</b> ${phone}<br>
            <b>Email:</b> ${email}
          `)
          .openPopup();

        clinicMarkers.push(singleMarker);
        map.setView([c.latitude, c.longitude], 16);

        singleMarker.on("popupclose", () => {
          map.removeLayer(singleMarker);
          clinicMarkers = [];

          clinics.forEach((clinic) => {
            const sch = clinic.schedule || "Not provided";
            const pt = clinic.publicTransport || "Not provided";
            const ph = clinic.phoneNumber || "Not provided";
            const em = clinic.email || "Not provided";

            const m = L.marker([clinic.latitude, clinic.longitude], { icon: blueIcon })
              .addTo(map)
              .bindPopup(`
                <b>${clinic.name}</b><br>
                <b>Schedule:</b> ${sch}<br>
                <b>Public Transport:</b> ${pt}<br>
                <b>Phone:</b> ${ph}<br>
                <b>Email:</b> ${em}
              `);
            clinicMarkers.push(m);
          });

          const allCoords = [
            [parseFloat(uni.lat), parseFloat(uni.lng)],
            ...clinics.map((c) => [parseFloat(c.latitude), parseFloat(c.longitude)]),
          ];
          map.fitBounds(allCoords, { padding: [50, 50] });
        });
      });

      listContainer.appendChild(div);
    });

    const allCoords = [
      [parseFloat(uni.lat), parseFloat(uni.lng)],
      ...clinics.map((c) => [parseFloat(c.latitude), parseFloat(c.longitude)]),
    ];
    map.fitBounds(allCoords, { padding: [50, 50] });

  } catch (err) {
    console.error("Error fetching clinics:", err);
  }
}

document.getElementById("showClinicsBtn").addEventListener("click", (e) => {
  e.preventDefault();
  fetchClinics();
});

fetchUniversities();
