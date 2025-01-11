document.addEventListener("DOMContentLoaded", () => {
    fetch("/cves/list")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector("#cve-table tbody");
            data.forEach(cve => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${cve.cve_id}</td>
                    <td>${cve.description}</td>
                    <td>${new Date(cve.published_date).toLocaleDateString()}</td>
                    <td>${cve.base_score || "N/A"}</td>
                `;
                row.addEventListener("click", () => {
                    window.location.href = `/cve_details.html?cve_id=${cve.cve_id}`;
                });
                tableBody.appendChild(row);
            });
        })
        .catch(err => console.error("Error fetching data:", err));
});
