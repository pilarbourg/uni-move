const searchBtn = document.getElementById("searchBtn");
const barrioInput = document.getElementById("barrioInput");
const precioInput = document.getElementById("precioInput");
const resultsList = document.getElementById("resultsList");
const resultsCard = document.getElementById("resultsCard");

// Función principal de búsqueda
async function searchApartments() {
  const barrio = barrioInput.value.trim();
  const precio = precioInput.value.trim();

  resultsList.innerHTML = "";
  resultsCard.style.display = "block";

  // Validación básica
  if (!barrio && !precio) {
    resultsList.innerHTML = `<p style="color:red;">Please enter a neighborhood or price.</p>`;
    return;
  }

  let url = "";

  if (barrio && precio) {
    url = `http://127.0.0.1:5000/get_apartments_by_barrio_price?barrio=${encodeURIComponent(
      barrio
    )}&presupuesto=${precio}`;
  } else if (barrio) {
    url = `http://127.0.0.1:5000/get_apartments_by_barrio/${encodeURIComponent(barrio)}`;
  } else if (precio) {
    url = `http://127.0.0.1:5000/get_apartments_by_price/${precio}`;
  }

  try {
    const res = await fetch(url);
    const data = await res.json();

    if (!Array.isArray(data) || data.length === 0) {
      resultsList.innerHTML = "<p>No apartments found for this search.</p>";
      return;
    }

    // Mostrar resultados en tarjetas
    data.forEach((a) => {
      const card = document.createElement("div");
      card.className = "apartment-card";
      card.innerHTML = `
        <h3>${a.titulo}</h3>
        <p><b>🏘️ Neighborhood:</b> ${a.barrio ?? "N/A"}</p>
        <p><b>💰 Price:</b> ${a.precio} €</p>
        <p><b>📏 Size:</b> ${a.tamano_m2} m²</p>
        <p><b>🛋️ Furnished:</b> ${a.amueblado ? "Yes" : "No"}</p>
      `;
      resultsList.appendChild(card);
    });
  } catch (err) {
    console.error("Error fetching apartments:", err);
    resultsList.innerHTML = `<p style="color:red;">Error connecting to server.</p>`;
  }
}

searchBtn.addEventListener("click", searchApartments);
barrioInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") searchApartments();
});
precioInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") searchApartments();
});
