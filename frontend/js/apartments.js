const searchBtn = document.getElementById("searchBtn");
  const precioInput = document.getElementById("precioInput");
  const resultsCard = document.getElementById("resultsCard");
  const resultsList = document.getElementById("resultsList");

  function render(apts) {
    resultsCard.style.display = "block";
    resultsList.innerHTML = "";

    if (!apts || apts.length === 0) {
      resultsList.innerHTML = "<p>No apartments found.</p>";
      return;
    }

    apts.forEach(a => {
      const card = document.createElement("div");
      card.className = "apt-card";

      card.innerHTML = `
        <img src="${a.thumbnail}" />
        <h3>${a.title}</h3>
        <p><strong>Price:</strong> ${a.price}</p>
        <p><strong>Rooms:</strong> ${a.rooms ?? "?"}</p>
        <p><strong>Baths:</strong> ${a.bathrooms ?? "?"}</p>
        <p><strong>Size:</strong> ${a.size ?? "?"} m²</p>
        <a href="${a.url}" target="_blank" style="color:#1a4d8f;">View on Idealista</a>
      `;

      resultsList.appendChild(card);
    });
  }

  async function search() {
    const precio = precioInput.value.trim();

    if (!precio) {
      alert("Enter a maximum price.");
      return;
    }

    const res = await fetch("http://127.0.0.1:8080/idealista/properties");
    const data = await res.json();

    const filtered = data.filter(a => {
      const price = parseFloat(a.price);
      return !isNaN(price) && price <= precio;
    });

    render(filtered);
  }

  searchBtn.addEventListener("click", search);