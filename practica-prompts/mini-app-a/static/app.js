const CATEGORY_COLORS = {
  Alimentación: "#56a878",
  Transporte: "#8095d0",
  Hogar: "#e5aa65",
  Ocio: "#b28acb",
  Salud: "#e27f78",
  Compras: "#52b7b2",
  Otros: "#a9b0aa",
};

const CATEGORY_ICONS = {
  Alimentación: "◒",
  Transporte: "↗",
  Hogar: "⌂",
  Ocio: "✳",
  Salud: "＋",
  Compras: "◇",
  Otros: "· · ·",
};

const numberFormat = new Intl.NumberFormat("es-ES", {
  style: "currency",
  currency: "EUR",
});
const dateFormat = new Intl.DateTimeFormat("es-ES", {
  day: "numeric",
  month: "short",
  year: "numeric",
});
function localDateString(date = new Date()) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

const currentMonth = localDateString().slice(0, 7);
const dialog = document.querySelector("#expense-dialog");
const form = document.querySelector("#expense-form");
const monthFilter = document.querySelector("#month-filter");
const categoryFilter = document.querySelector("#category-filter");
let expenses = [];

document.querySelector("#today-label").textContent = new Intl.DateTimeFormat(
  "es-ES",
  { month: "long", year: "numeric" },
).format(new Date()).toUpperCase();
document.querySelector("#spent_on").value = localDateString();
monthFilter.value = currentMonth;

async function request(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const detail = Array.isArray(body.detail)
      ? body.detail.map((issue) => issue.msg).join(" ")
      : body.detail;
    throw new Error(detail || "No se pudo completar la operación.");
  }
  return response.status === 204 ? null : response.json();
}

function showError(message) {
  document.querySelector("#form-error").textContent = message;
}

async function loadCategories() {
  const categories = await request("/api/categories");
  for (const category of categories) {
    const option = new Option(category, category);
    document.querySelector("#category").add(option);
    categoryFilter.add(new Option(category, category));
  }
}

async function loadExpenses() {
  const params = new URLSearchParams();
  if (monthFilter.value) params.set("month", monthFilter.value);
  if (categoryFilter.value) params.set("category", categoryFilter.value);
  expenses = await request(`/api/expenses?${params}`);
  render();
}

function render() {
  const list = document.querySelector("#expense-list");
  if (expenses.length === 0) {
    list.innerHTML = `
      <div class="empty-state">
        <div><div class="empty-icon">✳</div><strong>Aún no hay movimientos</strong>
        <p>Añade tu primer gasto para empezar.</p></div>
      </div>`;
  } else {
    list.innerHTML = expenses
      .slice(0, 6)
      .map((expense) => {
        const color = CATEGORY_COLORS[expense.category] || CATEGORY_COLORS.Otros;
        return `
          <div class="expense-row">
            <div class="expense-symbol" style="color:${color};background:${color}19">${CATEGORY_ICONS[expense.category] || "·"}</div>
            <div class="expense-main"><strong>${escapeHtml(expense.description)}</strong><span>${expense.category} · ${dateFormat.format(new Date(`${expense.spent_on}T12:00:00`))}</span></div>
            <div class="expense-amount">−${numberFormat.format(Number(expense.amount))}</div>
            <button class="delete-expense" type="button" aria-label="Eliminar ${escapeHtml(expense.description)}" data-id="${expense.id}">×</button>
          </div>`;
      })
      .join("");
  }
  renderSummary();
  renderCategories();
}

function renderSummary() {
  const monthExpenses = expenses.filter((expense) =>
    expense.spent_on.startsWith(monthFilter.value || currentMonth),
  );
  const total = monthExpenses.reduce((sum, expense) => sum + Number(expense.amount), 0);
  const totalsByCategory = new Map();
  for (const expense of monthExpenses) {
    totalsByCategory.set(
      expense.category,
      (totalsByCategory.get(expense.category) || 0) + Number(expense.amount),
    );
  }
  const top = [...totalsByCategory.entries()].sort((a, b) => b[1] - a[1])[0];
  document.querySelector("#month-total").textContent = numberFormat.format(total);
  document.querySelector("#month-count").textContent =
    `${monthExpenses.length} ${monthExpenses.length === 1 ? "gasto" : "gastos"}`;
  document.querySelector("#average-total").textContent = numberFormat.format(
    monthExpenses.length ? total / monthExpenses.length : 0,
  );
  document.querySelector("#top-category").textContent = top ? top[0] : "—";
  document.querySelector("#top-category-total").textContent = top
    ? `${numberFormat.format(top[1])} en la selección`
    : "Aún sin gastos";
}

function renderCategories() {
  const totals = new Map();
  for (const expense of expenses) {
    totals.set(
      expense.category,
      (totals.get(expense.category) || 0) + Number(expense.amount),
    );
  }
  const sorted = [...totals.entries()].sort((a, b) => b[1] - a[1]);
  const total = sorted.reduce((sum, [, amount]) => sum + amount, 0);
  let progress = 0;
  const segments = sorted.map(([category, amount]) => {
    const start = progress;
    progress += (amount / total) * 100;
    return `${CATEGORY_COLORS[category] || CATEGORY_COLORS.Otros} ${start}% ${progress}%`;
  });
  document.querySelector("#donut-chart").style.background = segments.length
    ? `conic-gradient(${segments.join(", ")})`
    : "#eef3ef";
  document.querySelector("#chart-total").textContent = numberFormat.format(total);
  document.querySelector("#chart-period").textContent = monthFilter.value
    ? new Intl.DateTimeFormat("es-ES", { month: "short", year: "numeric" })
        .format(new Date(`${monthFilter.value}-15T12:00:00`))
        .replace(".", "")
    : "Todos";
  document.querySelector("#category-legend").innerHTML = sorted.length
    ? sorted
        .map(
          ([category, amount]) => `
            <div class="legend-item"><span class="legend-dot" style="background:${CATEGORY_COLORS[category] || CATEGORY_COLORS.Otros}"></span>
            <span>${category}</span><strong>${numberFormat.format(amount)}</strong></div>`,
        )
        .join("")
    : '<div class="empty-state" style="min-height:auto;padding:5px">Añade gastos para ver el resumen.</div>';
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

document.querySelector("#open-form").addEventListener("click", () => {
  showError("");
  dialog.showModal();
  document.querySelector("#description").focus();
});
document.querySelector("#close-form").addEventListener("click", () => dialog.close());
monthFilter.addEventListener("change", () => loadExpenses().catch((error) => showError(error.message)));
categoryFilter.addEventListener("change", () => loadExpenses().catch((error) => showError(error.message)));
document.querySelector("#expense-list").addEventListener("click", async (event) => {
  const button = event.target.closest(".delete-expense");
  if (!button) return;
  try {
    await request(`/api/expenses/${button.dataset.id}`, { method: "DELETE" });
    await loadExpenses();
  } catch (error) {
    showError(error.message);
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  showError("");
  const payload = Object.fromEntries(new FormData(form));
  payload.amount = Number(payload.amount);
  try {
    await request("/api/expenses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    dialog.close();
    form.reset();
    document.querySelector("#spent_on").value = localDateString();
    monthFilter.value = currentMonth;
    categoryFilter.value = "";
    await loadExpenses();
  } catch (error) {
    showError(error.message);
  }
});

loadCategories()
  .then(loadExpenses)
  .catch((error) => {
    document.querySelector("#expense-list").innerHTML =
      `<div class="empty-state"><div><strong>No se pudo cargar la app</strong><p>${escapeHtml(error.message)}</p></div></div>`;
  });
