document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form");
  forms.forEach(form => {
    form.addEventListener("submit", e => {
      const inputs = form.querySelectorAll("input[required]");
      let valido = true;
      inputs.forEach(input => {
        if (!input.value.trim()) {
          valido = false;
          input.style.border = "2px solid red";
        } else {
          input.style.border = "2px solid green";
        }
      });
      if (!valido) {
        alert("Por favor completa todos los campos.");
        e.preventDefault();
      }
    });
  });
});


let descansoActivo = false; // controla si hay un descanso en curso

function finalizarSerie(element, descanso) {
  if (element.classList.contains("completed")) return;
  if (descansoActivo) return; // evita iniciar otro descanso si ya hay uno

  element.classList.add("completed");
  descansoActivo = true; // marca que hay un descanso activo

  const bar = element.querySelector(".descanso-bar");
  const text = element.querySelector(".descanso-text");
  let tiempo = parseInt(descanso);
  let progreso = 0;
  bar.style.width = "0%";
  text.textContent = `Descanso: ${tiempo}s`;

  const intervalo = setInterval(() => {
    progreso += 100 / parseInt(descanso);
    bar.style.width = progreso + "%";
    tiempo--;
    text.textContent = `Descanso: ${tiempo}s`;
    if (tiempo <= 0) {
      clearInterval(intervalo);
      bar.style.width = "100%";
      text.textContent = "¡Descanso terminado!";
      descansoActivo = false; // libera para permitir otro descanso
    }
  }, 1000);
}

function finalizarEjercicio() {
  alert("¡Rutina finalizada!");
}
