function filtrarEjerciciosGlobal() {
  let input = document.getElementById("buscador").value.toLowerCase();
  let items = document.getElementById("lista-ejercicios").getElementsByClassName("ejercicio-item");
  for (let i = 0; i < items.length; i++) {
    let texto = items[i].innerText.toLowerCase();
    items[i].style.display = texto.includes(input) ? "" : "none";
  }
}

function toggleEdit(rutinaId) {
  const card = document.getElementById("card-" + rutinaId);
  const form = document.getElementById("edit-" + rutinaId);

  if (form && card) {
    const isActive = form.classList.contains("active");
    document.querySelectorAll(".rutina-card").forEach(c => c.classList.remove("expanded"));
    document.querySelectorAll(".edit-form").forEach(f => f.classList.remove("active"));

    if (!isActive) {
      card.classList.add("expanded");
      form.classList.add("active");
    }
  }
}

function filtrarEjerciciosRutina(rutinaId) {
  let input = document.getElementById("buscador-" + rutinaId).value.toLowerCase();
  let items = document.getElementById("lista-" + rutinaId).getElementsByClassName("ejercicio-item");
  for (let i = 0; i < items.length; i++) {
    let texto = items[i].innerText.toLowerCase();
    items[i].style.display = texto.includes(input) ? "" : "none";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const buscador = document.getElementById("buscador");
  if (buscador) {
    buscador.addEventListener("keyup", filtrarEjerciciosGlobal);
  }
});




