document.getElementById("searchBtn").addEventListener("click", () => {
    const query = document.getElementById("search").value;

    // Llamada a la API
    fetch(`http://localhost:8000/api/centros?provincia=${query}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById("results");
            resultsDiv.innerHTML = "";

            data.centros.forEach(centro => {
                const centroElement = document.createElement("div");
                centroElement.textContent = `${centro.nombre} - ${centro.localidad}`;
                resultsDiv.appendChild(centroElement);
            });
        })
        .catch(error => console.error("Error al obtener los datos:", error));
});
