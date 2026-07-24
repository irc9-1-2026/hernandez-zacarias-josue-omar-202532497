// ---------------------------------------------------------------------------
// Estado y referencias
// ---------------------------------------------------------------------------
let modoActual = "buscar";

const entrada = document.getElementById("entrada");
const selectCategoria = document.getElementById("selectCategoria");
const btnBuscar = document.getElementById("btnBuscar");
const btnAleatorio = document.getElementById("btnAleatorio");
const resultados = document.getElementById("resultados");
const estado = document.getElementById("estado");
const modal = document.getElementById("modal");
const modalCuerpo = document.getElementById("modalCuerpo");
const cerrarModal = document.getElementById("cerrarModal");

// ---------------------------------------------------------------------------
// Cambio de pestañas
// ---------------------------------------------------------------------------
document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("activo"));
    tab.classList.add("activo");
    modoActual = tab.dataset.modo;

    if (modoActual === "categoria") {
      entrada.classList.add("oculto");
      selectCategoria.classList.remove("oculto");
      cargarCategorias();
    } else {
      entrada.classList.remove("oculto");
      selectCategoria.classList.add("oculto");
      entrada.placeholder =
        modoActual === "buscar"
          ? "Ej: Margarita, Mojito..."
          : "Ej: Vodka, Gin, Lemon...";
    }
  });
});

// ---------------------------------------------------------------------------
// Cargar categorías en el select
// ---------------------------------------------------------------------------
async function cargarCategorias() {
  if (selectCategoria.options.length > 0) return;
  try {
    const r = await fetch("/api/categorias");
    const data = await r.json();
    data.categorias.forEach((c) => {
      const opt = document.createElement("option");
      opt.value = c;
      opt.textContent = c;
      selectCategoria.appendChild(opt);
    });
  } catch (e) {
    estado.textContent = "No se pudieron cargar las categorías.";
  }
}

// ---------------------------------------------------------------------------
// Buscar
// ---------------------------------------------------------------------------
async function buscar() {
  let url;
  if (modoActual === "buscar") {
    const q = entrada.value.trim();
    if (!q) return (estado.textContent = "Escribe algo para buscar.");
    url = `/api/buscar?nombre=${encodeURIComponent(q)}`;
  } else if (modoActual === "ingrediente") {
    const q = entrada.value.trim();
    if (!q) return (estado.textContent = "Escribe un ingrediente.");
    url = `/api/ingrediente?nombre=${encodeURIComponent(q)}`;
  } else {
    const q = selectCategoria.value;
    url = `/api/categoria?nombre=${encodeURIComponent(q)}`;
  }

  estado.textContent = "Buscando...";
  resultados.innerHTML = "";

  try {
    const r = await fetch(url);
    const data = await r.json();
    const items = data.resultados || [];

    if (items.length === 0) {
      estado.textContent = "Sin resultados 🥲";
      return;
    }

    estado.textContent = `${items.length} resultado(s)`;
    pintarTarjetas(items);
  } catch (e) {
    estado.textContent = "Error al consultar la API.";
  }
}

// ---------------------------------------------------------------------------
// Pintar tarjetas
// ---------------------------------------------------------------------------
function pintarTarjetas(items) {
  resultados.innerHTML = "";
  items.forEach((it) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <img src="${it.imagen}" alt="${it.nombre}" loading="lazy" />
      <div class="card-info">
        <h3>${it.nombre}</h3>
        ${it.categoria ? `<span>${it.categoria}</span>` : ""}
      </div>
    `;
    card.addEventListener("click", () => abrirDetalle(it.id));
    resultados.appendChild(card);
  });
}

// ---------------------------------------------------------------------------
// Detalle en modal
// ---------------------------------------------------------------------------
async function abrirDetalle(id) {
  modal.classList.remove("oculto");
  modalCuerpo.innerHTML = "<p style='text-align:center'>Cargando...</p>";

  try {
    const r = await fetch(`/api/detalle/${id}`);
    const d = await r.json();

    const ingredientes = d.ingredientes
      .map((i) => `<li>${i}</li>`)
      .join("");

    modalCuerpo.innerHTML = `
      <img src="${d.imagen}" alt="${d.nombre}" />
      <h2>${d.nombre}</h2>
      <div class="badges">
        ${d.categoria ? `<span class="badge">${d.categoria}</span>` : ""}
        ${d.tipo ? `<span class="badge">${d.tipo}</span>` : ""}
        ${d.vaso ? `<span class="badge">${d.vaso}</span>` : ""}
      </div>
      <h4>Ingredientes</h4>
      <ul class="ingredientes">${ingredientes}</ul>
      <h4>Preparación</h4>
      <p class="instrucciones">${d.instrucciones || "No disponible."}</p>
    `;
  } catch (e) {
    modalCuerpo.innerHTML = "<p>Error al cargar el detalle.</p>";
  }
}

// ---------------------------------------------------------------------------
// Aleatorio
// ---------------------------------------------------------------------------
async function aleatorio() {
  estado.textContent = "Buscando un cóctel sorpresa...";
  try {
    const r = await fetch("/api/aleatorio");
    const d = await r.json();
    estado.textContent = "";
    abrirDetalleDirecto(d);
  } catch (e) {
    estado.textContent = "Error al obtener cóctel aleatorio.";
  }
}

function abrirDetalleDirecto(d) {
  modal.classList.remove("oculto");
  const ingredientes = d.ingredientes.map((i) => `<li>${i}</li>`).join("");
  modalCuerpo.innerHTML = `
    <img src="${d.imagen}" alt="${d.nombre}" />
    <h2>${d.nombre}</h2>
    <div class="badges">
      ${d.categoria ? `<span class="badge">${d.categoria}</span>` : ""}
      ${d.tipo ? `<span class="badge">${d.tipo}</span>` : ""}
      ${d.vaso ? `<span class="badge">${d.vaso}</span>` : ""}
    </div>
    <h4>Ingredientes</h4>
    <ul class="ingredientes">${ingredientes}</ul>
    <h4>Preparación</h4>
    <p class="instrucciones">${d.instrucciones || "No disponible."}</p>
  `;
}

// ---------------------------------------------------------------------------
// Eventos
// ---------------------------------------------------------------------------
btnBuscar.addEventListener("click", buscar);
btnAleatorio.addEventListener("click", aleatorio);
entrada.addEventListener("keypress", (e) => {
  if (e.key === "Enter") buscar();
});
cerrarModal.addEventListener("click", () => modal.classList.add("oculto"));
modal.addEventListener("click", (e) => {
  if (e.target === modal) modal.classList.add("oculto");
});
