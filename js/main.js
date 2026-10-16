document.addEventListener('DOMContentLoaded', function () {
  var yearEl = document.getElementById('year');
  if (yearEl) { yearEl.textContent = new Date().getFullYear(); }

  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      links.classList.toggle('open');
      var expanded = links.classList.contains('open');
      toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { links.classList.remove('open'); });
    });
  }
});

// ---- guide downloads (Netlify Forms) ----
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('form.guide-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var pdf = f.getAttribute('data-pdf');
      var btn = f.querySelector('button'); if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(f)).toString() })
      .catch(function () {})
      .then(function () {
        var done = f.querySelector('.lead-done'); if (done) done.hidden = false;
        if (btn) btn.textContent = 'Sent';
        window.open(pdf, '_blank');
      });
    });
  });

  // ---- DSCR calculator ----
  var rent = document.getElementById('rent'), piti = document.getElementById('piti');
  if (rent && piti) {
    var out = document.getElementById('ratio'), v = document.getElementById('verdict');
    var upd = function () {
      var x = (parseFloat(rent.value) || 0) / Math.max(parseFloat(piti.value) || 1, 1);
      out.textContent = x.toFixed(2);
      v.textContent = x >= 1.25 ? 'Strong: most DSCR lenders are comfortable here'
        : x >= 1 ? 'Borderline: some lenders accept 1.0 to 1.24' : "Below 1.0: rent doesn't cover the payment";
    };
    rent.addEventListener('input', upd); piti.addEventListener('input', upd); upd();
  }
});
