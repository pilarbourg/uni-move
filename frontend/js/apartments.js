const results = document.getElementById("results");
const priceInput = document.getElementById("priceInput");
const searchBtn = document.getElementById("searchBtn");
const resetBtn = document.getElementById("resetBtn");

async function loadApartments() {
    const res = await fetch("http://127.0.0.1:8080/api/idealista/properties");
    const data = await res.json();
    render(data);
}

function render(apts) {
    results.innerHTML = apts.length ? "" : "<p>No apartments found</p>";

    apts.forEach(a => {
        results.innerHTML += `
        <div class="ap-card">
            <img src="${a.thumbnail || 'no_photo.jpg'}">
            <h3>${a.title}</h3>
            <p><b>Price:</b> ${a.price} €</p>
            <p><b>Rooms:</b> ${a.rooms ?? '—'}</p>
            <p><b>Baths:</b> ${a.bathrooms ?? '—'}</p>
            <p><b>Size:</b> ${a.size ?? '—'} m²</p>
            <a href="${a.url}" target="_blank">View on Idealista</a>
        </div>`;
    });
}

function search() {
    const max = priceInput.value;
    if (!max) return alert("Enter a price");

    fetch("http://127.0.0.1:8080/api/idealista/properties")
    .then(r => r.json())
    .then(data => render(data.filter(a => parseFloat(a.price) <= max)));
}

searchBtn.onclick = search;
resetBtn.onclick = loadApartments;

loadApartments();
