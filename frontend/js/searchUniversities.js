// Datos de ejemplo (Sin conexión a BBDD)
const universities = [
    {
        name: "Universidad Complutense de Madrid",
        ranking: 1,
        degrees: ["Economics", "Computer Science", "Law"]
    },
    {
        name: "Universidad Autónoma de Madrid",
        ranking: 2,
        degrees: ["Medicine", "Biology", "Economics"]
    },
    {
        name: "Universidad Carlos III de Madrid",
        ranking: 3,
        degrees: ["Computer Science", "Business", "Economics"]
    },
    {
        name: "Universidad Politécnica de Madrid",
        ranking: 4,
        degrees: ["Engineering", "Architecture", "Computer Science"]
    }
];

// Función que se ejecuta al hacer click en Search
function search() {
    const input = document.getElementById("degree").value.trim();
    const resultsList = document.getElementById("results");
    resultsList.innerHTML = ""; // limpiar resultados anteriores

    if (!input) {
        resultsList.innerHTML = "<li>Please enter a degree</li>";
        return;
    }

    // Filtrar universidades que ofrezcan el grado buscado
    const results = universities.filter(u =>
        u.degrees.some(d => d.toLowerCase() === input.toLowerCase())
    );

    if (results.length === 0) {
        resultsList.innerHTML = `<li>No universities found for "${input}"</li>`;
        return;
    }

    // Ordenar por ranking
    results.sort((a, b) => a.ranking - b.ranking);

    // Mostrar en pantalla
    results.forEach(u => {
        const li = document.createElement("li");
        li.textContent = `${u.name} (Ranking: ${u.ranking})`;
        resultsList.appendChild(li);
    });
}
