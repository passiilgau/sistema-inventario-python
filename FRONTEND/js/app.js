/* =========================================================
   CONFIGURACIÓN
   Ajusta API_BASE_URL si tu backend corre en otro host/puerto.
========================================================= */
const API_BASE_URL = "http://127.0.0.1:8000";
const STOCK_BAJO_LIMITE = 5;

/* Estado en memoria de los productos cargados desde la API */
let productos = [];
let idEnEdicion = null; // null = modo "crear"
let idPendienteDeEliminar = null;

/* =========================================================
   REFERENCIAS AL DOM
========================================================= */
const apiStatusDot = document.getElementById("apiStatusDot");
const apiStatusText = document.getElementById("apiStatusText");

const cardTotalProductos = document.getElementById("cardTotalProductos");
const cardStockTotal = document.getElementById("cardStockTotal");
const cardStockBajo = document.getElementById("cardStockBajo");
const cardValorInventario = document.getElementById("cardValorInventario");

const searchInput = document.getElementById("searchInput");
const btnNuevoProducto = document.getElementById("btnNuevoProducto");

const feedbackContainer = document.getElementById("feedback");

const tableBody = document.getElementById("productosTableBody");
const tableEmptyState = document.getElementById("tableEmptyState");
const tableLoadingState = document.getElementById("tableLoadingState");

const modalOverlay = document.getElementById("modalOverlay");
const modalTitle = document.getElementById("modalTitle");
const productoForm = document.getElementById("productoForm");
const formModo = document.getElementById("formModo");
const formId = document.getElementById("formId");
const formNombre = document.getElementById("formNombre");
const formPrecio = document.getElementById("formPrecio");
const formStock = document.getElementById("formStock");
const formCategoria = document.getElementById("formCategoria");
const btnCerrarModal = document.getElementById("btnCerrarModal");
const btnCancelarForm = document.getElementById("btnCancelarForm");
const btnGuardarForm = document.getElementById("btnGuardarForm");

const confirmOverlay = document.getElementById("confirmOverlay");
const confirmMessage = document.getElementById("confirmMessage");
const btnCancelarConfirm = document.getElementById("btnCancelarConfirm");
const btnConfirmarEliminar = document.getElementById("btnConfirmarEliminar");

/* =========================================================
   UTILIDADES DE API
========================================================= */

/**
 * Envuelve fetch para centralizar manejo de errores HTTP y de red.
 * Lanza un Error con el mensaje que devuelve el backend (detail)
 * cuando la API responde con un status de error.
 */
async function apiFetch(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (errorDeRed) {
    throw new Error(
      "No se pudo conectar con la API. Verifica que el backend esté encendido " +
      "y que no haya un problema de CORS (revisa la consola del navegador)."
    );
  }

  let cuerpo = null;
  try {
    cuerpo = await response.json();
  } catch (_) {
    // Algunas respuestas (ej. DELETE) pueden no traer cuerpo JSON válido.
  }

  if (!response.ok) {
    const detalle = cuerpo && cuerpo.detail ? cuerpo.detail : `Error ${response.status}`;
    throw new Error(detalle);
  }

  return cuerpo;
}

async function verificarEstadoApi() {
  try {
    await apiFetch("/");
    apiStatusDot.classList.remove("api-status__dot--error");
    apiStatusDot.classList.add("api-status__dot--ok");
    apiStatusText.textContent = "API conectada";
  } catch (error) {
    apiStatusDot.classList.remove("api-status__dot--ok");
    apiStatusDot.classList.add("api-status__dot--error");
    apiStatusText.textContent = "API no disponible";
  }
}

/* =========================================================
   CARGA Y RENDERIZADO DE PRODUCTOS
========================================================= */

async function cargarProductos() {
  mostrarCargando(true);
  try {
    productos = await apiFetch("/productos");
    verificarEstadoApi(); // si la carga funcionó, la API está viva
    renderizarProductos();
    actualizarDashboard();
  } catch (error) {
    mostrarError(error.message);
    productos = [];
    renderizarProductos();
    actualizarDashboard();
  } finally {
    mostrarCargando(false);
  }
}

function mostrarCargando(estaCargando) {
  tableLoadingState.hidden = !estaCargando;
  if (estaCargando) {
    tableEmptyState.hidden = true;
  }
}

function obtenerProductosFiltrados() {
  const termino = searchInput.value.trim().toLowerCase();
  if (!termino) return productos;

  return productos.filter((producto) =>
    producto.nombre.toLowerCase().includes(termino) ||
    producto.categoria.toLowerCase().includes(termino) ||
    producto.id.toString().includes(termino) // <-- Esta es la validación nueva
  );
}

function renderizarProductos() {
  const lista = obtenerProductosFiltrados();

  tableBody.innerHTML = "";

  if (lista.length === 0) {
    tableEmptyState.hidden = false;
    tableEmptyState.textContent = productos.length === 0
      ? "No hay productos registrados todavía."
      : "Ningún producto coincide con la búsqueda.";
    return;
  }

  tableEmptyState.hidden = true;

  const filas = lista.map((producto) => crearFilaProducto(producto));
  filas.forEach((fila) => tableBody.appendChild(fila));
}

function crearFilaProducto(producto) {
  const fila = document.createElement("tr");

  fila.innerHTML = `
    <td class="col-id" data-label="ID">${producto.id}</td>
    <td class="col-nombre" data-label="Nombre">${escaparHtml(producto.nombre)}</td>
    <td class="col-precio" data-label="Precio">${formatearPrecio(producto.precio)}</td>
    <td class="col-stock" data-label="Stock">
      <div class="stock-control">
        <button class="btn--icon" type="button" data-action="disminuir" data-id="${producto.id}" aria-label="Disminuir stock">−</button>
        <span class="stock-control__value">${producto.stock}</span>
        <button class="btn--icon" type="button" data-action="aumentar" data-id="${producto.id}" aria-label="Aumentar stock">+</button>
      </div>
    </td>
    <td data-label="Categoría"><span class="badge">${escaparHtml(producto.categoria)}</span></td>
    <td data-label="Acciones">
      <div class="row-actions">
        <button class="btn--icon" type="button" data-action="editar" data-id="${producto.id}" aria-label="Editar producto">✎</button>
        <button class="btn--icon btn--icon--danger" type="button" data-action="eliminar" data-id="${producto.id}" aria-label="Eliminar producto">✕</button>
      </div>
    </td>
  `;

  return fila;
}

function escaparHtml(texto) {
  const div = document.createElement("div");
  div.textContent = texto;
  return div.innerHTML;
}

function formatearPrecio(valor) {
  return new Intl.NumberFormat("es", {
    style: "currency",
    currency: "USD",
  }).format(valor);
}

/* =========================================================
   DASHBOARD (TARJETAS RESUMEN)
========================================================= */

function actualizarDashboard() {
  const totalProductos = productos.length;
  const stockTotal = productos.reduce((suma, p) => suma + p.stock, 0);
  const stockBajo = productos.filter((p) => p.stock < STOCK_BAJO_LIMITE).length;
  const valorInventario = productos.reduce((suma, p) => suma + (p.precio * p.stock), 0);

  cardTotalProductos.textContent = totalProductos;
  cardStockTotal.textContent = stockTotal;
  cardStockBajo.textContent = stockBajo;
  cardValorInventario.textContent = formatearPrecio(valorInventario);
}

/* =========================================================
   MENSAJES DE FEEDBACK
========================================================= */

function mostrarMensaje(texto, tipo = "success") {
  const item = document.createElement("div");
  item.className = `feedback__item feedback__item--${tipo}`;
  item.textContent = texto;
  feedbackContainer.innerHTML = "";
  feedbackContainer.appendChild(item);

  setTimeout(() => {
    if (item.parentNode === feedbackContainer) {
      feedbackContainer.removeChild(item);
    }
  }, 4000);
}

function mostrarError(texto) {
  mostrarMensaje(texto, "error");
}

/* =========================================================
   MODAL: CREAR / EDITAR PRODUCTO
========================================================= */

function abrirModalCrear() {
  idEnEdicion = null;
  formModo.value = "crear";
  modalTitle.textContent = "Nuevo producto";

  productoForm.reset();
  limpiarErroresFormulario();
  formId.disabled = false;

  abrirModal(modalOverlay);
  formId.focus();
}

function abrirModalEditar(producto) {
  idEnEdicion = producto.id;
  formModo.value = "editar";
  modalTitle.textContent = `Editar producto #${producto.id}`;

  formId.value = producto.id;
  formNombre.value = producto.nombre;
  formPrecio.value = producto.precio;
  formStock.value = producto.stock;
  formCategoria.value = producto.categoria;

  // El backend (ProductoUpdate) no permite modificar ID ni stock por esta vía.
  formId.disabled = true;
  formStock.disabled = true;

  limpiarErroresFormulario();
  abrirModal(modalOverlay);
  formNombre.focus();
}

function cerrarModalProducto() {
  cerrarModal(modalOverlay);
  productoForm.reset();
  formId.disabled = false;
  formStock.disabled = false;
  limpiarErroresFormulario();
  idEnEdicion = null;
}

function abrirModal(overlay) {
  overlay.hidden = false;
}

function cerrarModal(overlay) {
  overlay.hidden = true;
}

/* =========================================================
   VALIDACIÓN DEL FORMULARIO (mejora de UX; el backend es la autoridad)
========================================================= */

function limpiarErroresFormulario() {
  ["Id", "Nombre", "Precio", "Stock", "Categoria"].forEach((campo) => {
    document.getElementById(`error${campo}`).textContent = "";
    document.getElementById(`form${campo}`).classList.remove("is-invalid");
  });
}

function marcarCampoInvalido(campo, mensaje) {
  document.getElementById(`error${campo}`).textContent = mensaje;
  document.getElementById(`form${campo}`).classList.add("is-invalid");
}

function validarFormulario(esCreacion) {
  limpiarErroresFormulario();
  let esValido = true;

  if (esCreacion) {
    const idValor = Number(formId.value);
    if (!Number.isInteger(idValor) || idValor <= 0) {
      marcarCampoInvalido("Id", "El ID debe ser un entero positivo.");
      esValido = false;
    }
  }

  if (!formNombre.value.trim()) {
    marcarCampoInvalido("Nombre", "El nombre es obligatorio.");
    esValido = false;
  }

  const precioValor = Number(formPrecio.value);
  if (!(precioValor > 0)) {
    marcarCampoInvalido("Precio", "El precio debe ser mayor que 0.");
    esValido = false;
  }

  if (esCreacion) {
    const stockValor = Number(formStock.value);
    if (!Number.isInteger(stockValor) || stockValor < 0) {
      marcarCampoInvalido("Stock", "El stock no puede ser negativo.");
      esValido = false;
    }
  }

  if (!formCategoria.value.trim()) {
    marcarCampoInvalido("Categoria", "La categoría es obligatoria.");
    esValido = false;
  }

  return esValido;
}

/* =========================================================
   OPERACIONES CONTRA LA API: CREAR / EDITAR / ELIMINAR / STOCK
========================================================= */

async function manejarSubmitFormulario(evento) {
  evento.preventDefault();

  const esCreacion = formModo.value === "crear";
  if (!validarFormulario(esCreacion)) return;

  establecerCargaBoton(btnGuardarForm, true);

  try {
    if (esCreacion) {
      await crearProducto();
      mostrarMensaje("Producto agregado correctamente.");
    } else {
      await editarProducto(idEnEdicion);
      mostrarMensaje("Producto actualizado correctamente.");
    }

    cerrarModalProducto();
    await cargarProductos();
  } catch (error) {
    mostrarError(error.message);
  } finally {
    establecerCargaBoton(btnGuardarForm, false);
  }
}

async function crearProducto() {
  const payload = {
    id: Number(formId.value),
    nombre: formNombre.value.trim(),
    precio: Number(formPrecio.value),
    stock: Number(formStock.value),
    categoria: formCategoria.value.trim(),
  };

  return apiFetch("/productos", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

async function editarProducto(id) {
  // ProductoUpdate solo acepta nombre, precio y categoria.
  const payload = {
    nombre: formNombre.value.trim(),
    precio: Number(formPrecio.value),
    categoria: formCategoria.value.trim(),
  };

  return apiFetch(`/productos/${id}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

function solicitarEliminarProducto(id) {
  idPendienteDeEliminar = id;
  const producto = productos.find((p) => p.id === id);
  confirmMessage.textContent = producto
    ? `¿Eliminar el producto "${producto.nombre}" (ID ${id})? Esta acción no se puede deshacer.`
    : `¿Eliminar el producto con ID ${id}?`;
  abrirModal(confirmOverlay);
}

async function eliminarProducto() {
  if (idPendienteDeEliminar === null) return;

  establecerCargaBoton(btnConfirmarEliminar, true);

  try {
    await apiFetch(`/productos/${idPendienteDeEliminar}`, { method: "DELETE" });
    mostrarMensaje("Producto eliminado correctamente.");
    cerrarModal(confirmOverlay);
    idPendienteDeEliminar = null;
    await cargarProductos();
  } catch (error) {
    mostrarError(error.message);
  } finally {
    establecerCargaBoton(btnConfirmarEliminar, false);
  }
}

async function aumentarStock(id, boton) {
  establecerCargaBoton(boton, true);
  try {
    await apiFetch(`/productos/${id}/stock/aumentar`, {
      method: "PATCH",
      body: JSON.stringify({ cantidad: 1 }),
    });
    await cargarProductos();
  } catch (error) {
    mostrarError(error.message);
  } finally {
    establecerCargaBoton(boton, false);
  }
}

async function disminuirStock(id, boton) {
  establecerCargaBoton(boton, true);
  try {
    await apiFetch(`/productos/${id}/stock/disminuir`, {
      method: "PATCH",
      body: JSON.stringify({ cantidad: 1 }),
    });
    await cargarProductos();
  } catch (error) {
    mostrarError(error.message);
  } finally {
    establecerCargaBoton(boton, false);
  }
}

function establecerCargaBoton(boton, estaCargando) {
  boton.disabled = estaCargando;
}

/* =========================================================
   MANEJO DE EVENTOS (DELEGACIÓN EN LA TABLA)
========================================================= */

function manejarClicEnTabla(evento) {
  const boton = evento.target.closest("button[data-action]");
  if (!boton) return;

  const id = Number(boton.dataset.id);
  const accion = boton.dataset.action;

  switch (accion) {
    case "aumentar":
      aumentarStock(id, boton);
      break;
    case "disminuir":
      disminuirStock(id, boton);
      break;
    case "editar": {
      const producto = productos.find((p) => p.id === id);
      if (producto) abrirModalEditar(producto);
      break;
    }
    case "eliminar":
      solicitarEliminarProducto(id);
      break;
  }
}

/* =========================================================
   INICIALIZACIÓN
========================================================= */

function inicializarEventos() {
  btnNuevoProducto.addEventListener("click", abrirModalCrear);
  btnCerrarModal.addEventListener("click", cerrarModalProducto);
  btnCancelarForm.addEventListener("click", cerrarModalProducto);
  productoForm.addEventListener("submit", manejarSubmitFormulario);

  modalOverlay.addEventListener("click", (evento) => {
    if (evento.target === modalOverlay) cerrarModalProducto();
  });

  btnCancelarConfirm.addEventListener("click", () => {
    idPendienteDeEliminar = null;
    cerrarModal(confirmOverlay);
  });
  btnConfirmarEliminar.addEventListener("click", eliminarProducto);
  confirmOverlay.addEventListener("click", (evento) => {
    if (evento.target === confirmOverlay) {
      idPendienteDeEliminar = null;
      cerrarModal(confirmOverlay);
    }
  });

  tableBody.addEventListener("click", manejarClicEnTabla);
  searchInput.addEventListener("input", renderizarProductos);

  document.addEventListener("keydown", (evento) => {
    if (evento.key !== "Escape") return;
    if (!modalOverlay.hidden) cerrarModalProducto();
    if (!confirmOverlay.hidden) {
      idPendienteDeEliminar = null;
      cerrarModal(confirmOverlay);
    }
  });
}

function inicializar() {
  inicializarEventos();
  verificarEstadoApi();
  cargarProductos();
}

document.addEventListener("DOMContentLoaded", inicializar);