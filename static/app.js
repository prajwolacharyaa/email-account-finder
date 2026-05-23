const form = document.querySelector("#scan-form");
const emailInput = document.querySelector("#email");
const resultsBody = document.querySelector("#results-body");
const loader = document.querySelector("#loader");
const message = document.querySelector("#message");
const exportCsv = document.querySelector("#export-csv");
const exportPdf = document.querySelector("#export-pdf");
const historyList = document.querySelector("#history-list");

let lastEmail = "";

function setLoading(isLoading) {
  loader.classList.toggle("hidden", !isLoading);
  document.querySelector("#scan-button").disabled = isLoading;
}

function showMessage(text) {
  message.textContent = text;
  message.classList.toggle("hidden", !text);
}

function statusClass(status) {
  return status.toLowerCase().replace(/\s+/g, "-");
}

function renderResults(results) {
  resultsBody.innerHTML = "";

  for (const result of results) {
    const row = document.createElement("tr");
    const link = result.link === "-"
      ? "-"
      : `<a href="${result.link}" target="_blank" rel="noreferrer">${result.link}</a>`;

    row.innerHTML = `
      <td>${result.website}</td>
      <td><span class="badge ${statusClass(result.status)}">${result.status}</span></td>
      <td>${link}</td>
      <td>${result.method}</td>
      <td>${result.note}</td>
    `;
    resultsBody.appendChild(row);
  }
}

async function loadHistory() {
  const response = await fetch("/api/history");
  const history = await response.json();

  if (!history.length) {
    historyList.innerHTML = '<p class="empty">No checks yet.</p>';
    return;
  }

  historyList.innerHTML = "";
  for (const item of history.slice(0, 8)) {
    const div = document.createElement("div");
    const date = new Date(item.scanned_at);
    div.className = "history-item";
    div.innerHTML = `
      <span class="history-email">${item.email}</span>
      <span class="history-time">${date.toLocaleString()}</span>
    `;
    historyList.appendChild(div);
  }
}

async function scanEmail(email) {
  setLoading(true);
  showMessage("");

  try {
    const response = await fetch("/api/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Scan failed.");
    }

    lastEmail = data.email;
    renderResults(data.results);
    exportCsv.disabled = false;
    exportPdf.disabled = false;
    await loadHistory();
  } catch (error) {
    showMessage(error.message);
  } finally {
    setLoading(false);
  }
}

async function exportResults(type) {
  if (!lastEmail) return;

  const response = await fetch(`/api/export/${type}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: lastEmail }),
  });

  if (!response.ok) {
    const data = await response.json();
    showMessage(data.error || "Export failed.");
    return;
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `account_finder.${type}`;
  link.click();
  window.URL.revokeObjectURL(url);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  scanEmail(emailInput.value);
});

exportCsv.addEventListener("click", () => exportResults("csv"));
exportPdf.addEventListener("click", () => exportResults("pdf"));

loadHistory();
