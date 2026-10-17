// FitNews — interações do site
(function () {
  "use strict";

  // ---------- Abas do plano ----------
  var abas = document.querySelectorAll(".aba");
  abas.forEach(function (btn) {
    btn.addEventListener("click", function () {
      abas.forEach(function (b) { b.classList.remove("ativa"); });
      document.querySelectorAll(".painel").forEach(function (p) { p.classList.remove("ativo"); });
      btn.classList.add("ativa");
      var painel = document.getElementById("aba-" + btn.dataset.aba);
      if (painel) painel.classList.add("ativo");
      try { sessionStorage.setItem("abaFitnews", btn.dataset.aba); } catch (e) {}
    });
  });
  // restaura aba selecionada
  try {
    var salva = sessionStorage.getItem("abaFitnews");
    if (salva) {
      var alvo = document.querySelector('.aba[data-aba="' + salva + '"]');
      if (alvo) alvo.click();
    }
  } catch (e) {}

  // ---------- IMC ----------
  var peso = document.querySelector('input[name="peso"]');
  var altura = document.querySelector('input[name="altura"]');
  var imc = document.getElementById("imc");
  function calcImc() {
    if (!peso || !altura || !imc) return;
    var p = parseFloat(peso.value), a = parseFloat(altura.value);
    if (p > 0 && a > 0) {
      var v = p / Math.pow(a / 100, 2);
      var cls = v < 18.5 ? "abaixo" : v < 25 ? "normal" : v < 30 ? "sobrepeso" : "obesidade";
      var rot = { abaixo: "abaixo do peso", normal: "normal", sobrepeso: "sobrepeso", obesidade: "obesidade" };
      imc.value = v.toFixed(1) + " — " + rot[cls];
    } else {
      imc.value = "";
    }
  }
  if (peso) peso.addEventListener("input", calcImc);
  if (altura) altura.addEventListener("input", calcImc);
  calcImc();

  // ---------- Idade pela data de nascimento ----------
  var nasc = document.getElementById("nascimento");
  var idadeMostra = document.getElementById("idadeMostra");
  function calcIdade() {
    if (!nasc || !idadeMostra) return;
    if (!nasc.value) { idadeMostra.textContent = ""; return; }
    var d = new Date(nasc.value);
    var hoje = new Date();
    var idade = hoje.getFullYear() - d.getFullYear();
    var m = hoje.getMonth() - d.getMonth();
    if (m < 0 || (m === 0 && hoje.getDate() < d.getDate())) idade--;
    idadeMostra.textContent = idade >= 0 ? idade + " anos" : "";
  }
  if (nasc) nasc.addEventListener("change", calcIdade);
  calcIdade();

  // ---------- Limitacoes: "nenhuma" x demais ----------
  var checksLim = document.querySelectorAll('input[name="limitacoes"]');
  checksLim.forEach(function (c) {
    c.addEventListener("change", function () {
      if (c.value === "nenhuma" && c.checked) {
        checksLim.forEach(function (o) { if (o !== c) o.checked = false; });
      } else if (c.value !== "nenhuma" && c.checked) {
        checksLim.forEach(function (o) { if (o.value === "nenhuma") o.checked = false; });
      }
      if (!document.querySelector('input[name="limitacoes"]:checked')) {
        var nen = document.querySelector('input[name="limitacoes"][value="nenhuma"]');
        if (nen) nen.checked = true;
      }
    });
  });

  // ---------- Validacao: minimo 1 foco ----------
  var form = document.getElementById("formPlano");
  if (form) {
    form.addEventListener("submit", function (ev) {
      var focos = form.querySelectorAll('input[name="focos"]:checked');
      var erro = document.getElementById("erroFoco");
      if (focos.length === 0) {
        ev.preventDefault();
        if (erro) {
          erro.hidden = false;
          erro.scrollIntoView({ behavior: "smooth", block: "center" });
        }
        return;
      }
      if (erro) erro.hidden = true;
      var btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.textContent = "Gerando seu plano...";
        setTimeout(function () { btn.disabled = false; }, 4000);
      }
    });
  }
})();
