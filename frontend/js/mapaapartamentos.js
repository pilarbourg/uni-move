let apartments = [];

// CARGA INICIAL (todos)
async function loadAll() {
  const res = await fetch("http://127.0.0.1:5000/get_apartamentos");
  apartments = await res.json();
  render(apartments);   // tu función que pinta mapa + lista
}

// FILTRO (barrio + presupuesto)
async function applyFilter() {
  const barrio = document.getElementById("barrioInput").value.trim();
  const presupuesto = document.getElementById("presupuestoInput").value.trim();

  let url = "http://127.0.0.1:5000/get_apartamentos";
  if (barrio && presupuesto) {
    url = `http://127.0.0.1:5000/get_apartamentos_by_neighborhood_and_price?barrio=${encodeURIComponent(barrio)}&presupuesto=${encodeURIComponent(presupuesto)}`;
  } else if (presupuesto) {
    url = `http://127.0.0.1:5000/get_apartamentos_by_price/${encodeURIComponent(presupuesto)}`;
  }

  const res = await fetch(url);
  apartments = await res.json();
  render(apartments);
}

// Engancha eventos
document.getElementById("showApartmentsBtn").addEventListener("click", (e) => {
  e.preventDefault();
  applyFilter();
});

// Enter en inputs como en Universities
["barrioInput", "presupuestoInput"].forEach(id => {
  document.getElementById(id).addEventListener("keydown", ev => {
    if (ev.key === "Enter") applyFilter();
  });
});

// arranca
loadAll();

