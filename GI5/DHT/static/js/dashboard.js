const API_URL = "/latest/";

function formatValue(value, suffix) {
  if (value === undefined || value === null) {
    return "--";
  }
  return `${value.toFixed ? value.toFixed(1) : value} ${suffix}`.trim();
}

async function refreshDashboard() {
  try {
    const response = await fetch(API_URL, { cache: "no-store" });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    const timestamp = data.timestamp ? new Date(data.timestamp).toLocaleString() : "--";

    document.getElementById("temp-value").textContent = formatValue(data.temperature, "°C");
    document.getElementById("hum-value").textContent = formatValue(data.humidity, "%");

    document.getElementById("temp-time").textContent = timestamp;
    document.getElementById("hum-time").textContent = timestamp;
  } catch (error) {
    console.error("Dashboard refresh error:", error);
    document.getElementById("temp-value").textContent = "--";
    document.getElementById("hum-value").textContent = "--";
    document.getElementById("temp-time").textContent = "Erreur de chargement";
    document.getElementById("hum-time").textContent = "Erreur de chargement";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  refreshDashboard();
  setInterval(refreshDashboard, 20000);
});

