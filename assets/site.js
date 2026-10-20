
(function () {
  var root = document.documentElement;
  var lang = root.getAttribute("data-lang") || "en";

  function setLang(l) {
    lang = l;
    root.setAttribute("data-lang", l);
    root.lang = l;
    convert();
  }
  document.querySelectorAll(".lang button").forEach(function (b) {
    b.addEventListener("click", function () { setLang(b.getAttribute("data-set")); });
  });

  // in-page navigation that works inside the viewer frame
  document.querySelectorAll("[data-go]").forEach(function (a) {
    a.addEventListener("click", function (ev) {
      var t = document.getElementById(a.getAttribute("data-go"));
      if (!t) return;
      ev.preventDefault();
      if (a.getAttribute("data-go") === "top") window.scrollTo({ top: 0 });
      else t.scrollIntoView({ block: "start" });
    });
  });

  // ruler numbers (one label per 96px "inch")
  var ruler = document.getElementById("ruler");
  function drawRuler() {
    ruler.innerHTML = "";
    var n = Math.ceil(ruler.clientWidth / 96);
    for (var i = 1; i <= n; i++) {
      var s = document.createElement("span"); s.textContent = i; s.style.left = (i * 96 + 4) + "px"; ruler.appendChild(s);
    }
  }
  drawRuler(); window.addEventListener("resize", drawRuler);

  // scale converter
  var val = document.getElementById("c-val"), unit = document.getElementById("c-unit");
  var out = document.getElementById("c-out"), sub = document.getElementById("c-sub");
  var scale = 12;
  function gcd(a, b) { return b ? gcd(b, a % b) : a; }
  function frac(x) {
    var whole = Math.floor(x), sixteenths = Math.round((x - whole) * 16);
    if (sixteenths === 16) { whole += 1; sixteenths = 0; }
    if (sixteenths === 0) return String(whole);
    var g = gcd(sixteenths, 16), num = sixteenths / g, den = 16 / g;
    return (whole ? whole + " " : "") + num + "/" + den;
  }
  function trim(n, d) { return Number(n.toFixed(d)).toString(); }
  function convert() {
    if (!val) return;
    var v = parseFloat(val.value);
    if (!isFinite(v) || v < 0) {
      out.textContent = "—";
      sub.textContent = lang === "es" ? "Escribe un número mayor que cero." : "Type a number above zero.";
      return;
    }
    var inches = unit.value === "ft" ? v * 12 : unit.value === "cm" ? v / 2.54 : v;
    var mini = inches / scale, mm = mini * 25.4;
    var inLabel = lang === "es" ? "pulg" : "in";
    out.textContent = trim(mini, 2) + " " + inLabel;
    sub.textContent = "≈ " + frac(mini) + " " + inLabel + " · " + trim(mm, mm < 10 ? 1 : 0) + " mm";
  }
  if (val) {
  val.addEventListener("input", convert);
  unit.addEventListener("change", convert);
  document.querySelectorAll(".scales button").forEach(function (b) {
    b.addEventListener("click", function () {
      scale = Number(b.getAttribute("data-scale"));
      document.querySelectorAll(".scales button").forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
      convert();
    });
  });
  document.querySelectorAll(".presets button").forEach(function (b) {
    b.addEventListener("click", function () { val.value = b.getAttribute("data-v"); unit.value = b.getAttribute("data-u"); convert(); });
  });
  document.getElementById("conv").addEventListener("submit", function (e) { e.preventDefault(); });
  }

  setLang(lang);
})();

// ---- hero room box: drawn in perspective with the living-room wallpaper ----
(function () {
  var cv = document.getElementById("roombox"); if (!cv || !cv.getContext) return;
  var wall = new Image(); wall.src = "/assets/img/a6be88383367.jpg";
  var W = 600, H = 450;
  var O = { l: 46, t: 40, r: 554, b: 398 };          // front opening (11.8 : 8.3)
  var V = { x: 300, y: 214 }, k = 0.6;                // vanishing point, back-wall scale
  function P(x, y, f) { return { x: V.x + f * (x - V.x), y: V.y + f * (y - V.y) }; }
  var B = { l: P(O.l, 0, k).x, r: P(O.r, 0, k).x, t: P(0, O.t, k).y, b: P(0, O.b, k).y };
  function fAt(d) { return 1 / (1 + d * (1 / k - 1)); } // scale at depth d (0 front, 1 back)
  function dAt(t) { var f = 1 - t * (1 - k); return (1 / f - 1) / (1 / k - 1); }
  function poly(c, pts, fill) { c.beginPath(); c.moveTo(pts[0].x, pts[0].y); for (var i = 1; i < pts.length; i++) c.lineTo(pts[i].x, pts[i].y); c.closePath(); if (fill) { c.fillStyle = fill; c.fill(); } }
  function draw() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2), cssW = cv.clientWidth || W;
    cv.width = Math.round(cssW * dpr); cv.height = Math.round(cssW * dpr * H / W);
    var c = cv.getContext("2d"), s = cv.width / W; c.setTransform(s, 0, 0, s, 0, 0);
    c.clearRect(0, 0, W, H);
    // wooden box
    var g = c.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#9a673f"); g.addColorStop(1, "#6f4527");
    c.fillStyle = g; c.fillRect(18, 14, W - 36, H - 34);
    c.fillStyle = "rgba(255,255,255,.08)"; c.fillRect(18, 14, W - 36, 4);
    // ceiling
    poly(c, [{x:O.l,y:O.t},{x:O.r,y:O.t},{x:B.r,y:B.t},{x:B.l,y:B.t}], "#efe9df");
    g = c.createLinearGradient(0, O.t, 0, B.t); g.addColorStop(0, "rgba(60,40,20,.28)"); g.addColorStop(1, "rgba(60,40,20,.04)");
    poly(c, [{x:O.l,y:O.t},{x:O.r,y:O.t},{x:B.r,y:B.t},{x:B.l,y:B.t}], g);
    // floor: planks running front to back
    var fl = [{x:O.l,y:O.b},{x:B.l,y:B.b},{x:B.r,y:B.b},{x:O.r,y:O.b}];
    poly(c, fl, "#b07a4b");
    c.save(); poly(c, fl); c.clip();
    var n = 15;
    for (var i = 0; i <= n; i++) {
      var u = i / n, xf = O.l + u * (O.r - O.l), xb = B.l + u * (B.r - B.l);
      if (i < n) { // alternate plank tone
        poly(c, [{x:xf,y:O.b},{x:xb,y:B.b},{x:B.l + (i+1)/n*(B.r-B.l),y:B.b},{x:O.l + (i+1)/n*(O.r-O.l),y:O.b}], i % 3 === 0 ? "rgba(255,240,220,.07)" : i % 3 === 1 ? "rgba(60,30,10,.06)" : "rgba(0,0,0,0)");
      }
      c.strokeStyle = "rgba(70,40,18,.45)"; c.lineWidth = .8; c.beginPath(); c.moveTo(xf, O.b); c.lineTo(xb, B.b); c.stroke();
    }
    for (var j = 0; j < n; j++) { // staggered board ends
      var dd = ((j * 37) % 10) / 10 * .8 + .1, f = fAt(dd);
      var x0 = V.x + f * (O.l + j / n * (O.r - O.l) - V.x), x1 = V.x + f * (O.l + (j + 1) / n * (O.r - O.l) - V.x), y = V.y + f * (O.b - V.y);
      c.beginPath(); c.moveTo(x0, y); c.lineTo(x1, y); c.stroke();
    }
    g = c.createLinearGradient(0, B.b, 0, O.b); g.addColorStop(0, "rgba(40,20,5,.30)"); g.addColorStop(1, "rgba(40,20,5,0)");
    c.fillStyle = g; c.fillRect(O.l, B.b, O.r - O.l, O.b - B.b);
    // rug
    function fp(u, d) { var f = fAt(d); return { x: V.x + f * (O.l + u * (O.r - O.l) - V.x), y: V.y + f * (O.b - V.y) }; }
    poly(c, [fp(.27,.32), fp(.73,.32), fp(.73,.86), fp(.27,.86)], "#c25a6c");
    poly(c, [fp(.30,.38), fp(.70,.38), fp(.70,.82), fp(.30,.82)], "#e9c9a8");
    poly(c, [fp(.33,.44), fp(.67,.44), fp(.67,.77), fp(.33,.77)], "#b84d61");
    c.restore();
    // walls (wallpaper runs left wall -> back wall -> right wall as one strip)
    var iw = wall.naturalWidth, ih = wall.naturalHeight, ok = iw > 0;
    var depthSrc = ih * 8.7 / 8.3, backSrc = ih * 11.8 / 8.3;
    function col(sx, x, y0, y1, w) {
      if (ok) c.drawImage(wall, Math.floor(((sx % iw) + iw) % iw), 0, 1, ih, x, y0, w, y1 - y0);
      else { c.fillStyle = "#e9d7bf"; c.fillRect(x, y0, w, y1 - y0); }
    }
    var step = 1 / s;
    for (var x = O.l; x < B.l; x += step) { // left wall
      var t = (x - O.l) / (B.l - O.l), yT = O.t + t * (B.t - O.t), yB = O.b + t * (B.b - O.b);
      col(dAt(t) * depthSrc, x, yT, yB, step + .4);
    }
    for (x = B.l; x < B.r; x += step) col(depthSrc + (x - B.l) / (B.r - B.l) * backSrc, x, B.t, B.b, step + .4);
    for (x = B.r; x < O.r; x += step) {
      t = (O.r - x) / (O.r - B.r); yT = O.t + t * (B.t - O.t); yB = O.b + t * (B.b - O.b);
      col(depthSrc + backSrc + (1 - dAt(t)) * depthSrc, x, yT, yB, step + .4);
    }
    // wall shading
    g = c.createLinearGradient(O.l, 0, B.l, 0); g.addColorStop(0, "rgba(30,15,5,.30)"); g.addColorStop(1, "rgba(30,15,5,.10)");
    poly(c, [{x:O.l,y:O.t},{x:B.l,y:B.t},{x:B.l,y:B.b},{x:O.l,y:O.b}], g);
    g = c.createLinearGradient(O.r, 0, B.r, 0); g.addColorStop(0, "rgba(30,15,5,.22)"); g.addColorStop(1, "rgba(30,15,5,.06)");
    poly(c, [{x:O.r,y:O.t},{x:B.r,y:B.t},{x:B.r,y:B.b},{x:O.r,y:O.b}], g);
    // corner lines
    c.strokeStyle = "rgba(60,35,15,.35)"; c.lineWidth = 1;
    [[B.l,B.t,B.l,B.b],[B.r,B.t,B.r,B.b],[O.l,O.t,B.l,B.t],[O.r,O.t,B.r,B.t],[O.l,O.b,B.l,B.b],[O.r,O.b,B.r,B.b]].forEach(function (L) { c.beginPath(); c.moveTo(L[0], L[1]); c.lineTo(L[2], L[3]); c.stroke(); });
    // framed picture on the back wall
    var bw = B.r - B.l, bh = B.b - B.t, px = V.x - bw * .13, py = B.t + bh * .14, pw = bw * .26, ph = bh * .26;
    c.fillStyle = "rgba(30,15,5,.25)"; c.fillRect(px + 3, py + 4, pw, ph);
    c.fillStyle = "#c9a24a"; c.fillRect(px, py, pw, ph);
    c.fillStyle = "#f4efe6"; c.fillRect(px + 5, py + 5, pw - 10, ph - 10);
    g = c.createLinearGradient(0, py + 9, 0, py + ph - 9); g.addColorStop(0, "#a9c6d6"); g.addColorStop(.55, "#dfe8de"); g.addColorStop(.56, "#7f9e6e"); g.addColorStop(1, "#5d7d52");
    c.fillStyle = g; c.fillRect(px + 9, py + 9, pw - 18, ph - 18);
    c.fillStyle = "#4e6b45"; c.beginPath(); c.moveTo(px + 9, py + ph * .62); c.quadraticCurveTo(px + pw * .4, py + ph * .38, px + pw - 9, py + ph * .66); c.lineTo(px + pw - 9, py + ph - 9); c.lineTo(px + 9, py + ph - 9); c.closePath(); c.fill();
    // hanging lamp + warm glow
    var lx = V.x, cy0 = (O.t + B.t) / 2 + 4, ly = B.t + bh * .02;
    c.strokeStyle = "#3b2a1c"; c.lineWidth = 1.2; c.beginPath(); c.moveTo(lx, cy0); c.lineTo(lx, ly); c.stroke();
    var rg = c.createRadialGradient(lx, ly + 14, 2, lx, ly + 40, 230);
    rg.addColorStop(0, "rgba(255,214,140,.55)"); rg.addColorStop(.35, "rgba(255,200,120,.16)"); rg.addColorStop(1, "rgba(255,200,120,0)");
    c.save(); c.globalCompositeOperation = "screen"; poly(c, [{x:O.l,y:O.t},{x:O.r,y:O.t},{x:O.r,y:O.b},{x:O.l,y:O.b}], rg); c.restore();
    c.fillStyle = "#7a2840"; c.beginPath(); c.moveTo(lx - 7, ly); c.lineTo(lx + 7, ly); c.lineTo(lx + 22, ly + 18); c.lineTo(lx - 22, ly + 18); c.closePath(); c.fill();
    c.fillStyle = "#ffe2a6"; c.beginPath(); c.ellipse(lx, ly + 19, 13, 3.2, 0, 0, Math.PI * 2); c.fill();
    // inner edge of the box opening
    c.strokeStyle = "rgba(40,22,8,.6)"; c.lineWidth = 2; c.strokeRect(O.l, O.t, O.r - O.l, O.b - O.t);
  }
  if (wall.complete) draw(); else { wall.onload = draw; draw(); }
  var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(draw, 120); });
})();
// ---- Puerto Rican guide: zinc corrugation, balusters, paint chips ----
(function () {
  var NS = "http://www.w3.org/2000/svg";
  var corr = document.getElementById("corr");
  if (corr) for (var x = 30; x < 330; x += 5.5) {
    var r = document.createElementNS(NS, "rect");
    r.setAttribute("x", x); r.setAttribute("y", 38); r.setAttribute("width", 2.2); r.setAttribute("height", 66); r.setAttribute("fill", "rgba(70,80,86,.32)");
    corr.appendChild(r);
  }
  var bal = document.getElementById("balusters");
  if (bal) [[52, 154], [206, 310]].forEach(function (seg) {
    for (var x = seg[0]; x < seg[1]; x += 9) {
      var r = document.createElementNS(NS, "rect");
      r.setAttribute("x", x); r.setAttribute("y", 148); r.setAttribute("width", 3); r.setAttribute("height", 20); bal.appendChild(r);
    }
  });
  var houses = document.getElementById("pr-houses");
  document.querySelectorAll(".pr-paint .chip").forEach(function (b) {
    b.addEventListener("click", function () {
      houses.style.setProperty("--house", b.getAttribute("data-c"));
      document.querySelectorAll(".pr-paint .chip").forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
    });
  });
})();
// ---- wallpaper planner ----
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var form = $("pl-form"); if (!form) return;
  var unit = "in", ALLOW = 0.125, MARGIN = 0.25, WRAP = 0.25, method = "strip";
  var PAPER = { letter: [8.5, 11], a4: [8.27, 11.69], legal: [8.5, 14] };
  var T = {
    en: { sheets: "sheets", sheet: "sheet", of: "Print on", portrait: "portrait", landscape: "landscape", cut: "Cut each sheet to", tall: "tall", run: "wall run",
      left: "left wall", back: "back wall", right: "right wall", wrapL: "wrap onto left wall", wrapR: "wrap onto right wall", piece: "Piece", covers: "covers", trimLast: "trim off the extra", plusSpare: "Print one spare in case of a mistake.",
      tooTall: function (h, m) { return "The wall is too tall for this paper: each strip needs " + h + ", and the paper fits " + m + " at most. Choose Legal paper, or plan a horizontal seam hidden under a chair rail."; },
      corner: function (d, c) { return "A seam lands " + d + " from the " + c + " corner, which is fiddly to glue. Let sheet 1 hang " + fmt(0.5) + " past the front edge and trim it after; that moves every seam over."; },
      bad: "Enter a size above zero for each wall.", none: "Pick at least one wall to cover.", backLeft: "back-left", backRight: "back-right", separate: "Without the back wall, each side is its own piece." },
    es: { sheets: "hojas", sheet: "hoja", of: "Imprime en", portrait: "vertical", landscape: "horizontal", cut: "Corta cada hoja a", tall: "de alto", run: "recorrido",
      left: "pared izquierda", back: "pared del fondo", right: "pared derecha", wrapL: "doblez sobre la pared izquierda", wrapR: "doblez sobre la pared derecha", piece: "Pieza", covers: "cubre", trimLast: "recorta lo que sobre", plusSpare: "Imprime una de repuesto por si acaso.",
      tooTall: function (h, m) { return "La pared es muy alta para este papel: cada tira necesita " + h + " y el papel da para " + m + " como máximo. Usa papel Legal o planifica una unión horizontal escondida bajo la moldura de media pared."; },
      corner: function (d, c) { return "Una unión cae a " + d + " de la esquina " + c + ", y ahí es difícil pegar. Deja que la hoja 1 sobresalga " + fmt(0.5) + " del borde del frente y recórtala después; así se mueven todas las uniones."; },
      bad: "Escribe una medida mayor que cero para cada pared.", none: "Elige al menos una pared.", backLeft: "del fondo izquierda", backRight: "del fondo derecha", separate: "Sin la pared del fondo, cada lado es una pieza aparte." }
  };
  var PNAME = { en: { letter: "Letter", a4: "A4", legal: "Legal" }, es: { letter: "papel carta", a4: "A4", legal: "papel legal" } };
  var POPT = { en: { letter: "Letter 8.5 × 11 in", a4: "A4 210 × 297 mm", legal: "Legal 8.5 × 14 in" }, es: { letter: "Carta 8.5 × 11 pulg", a4: "A4 210 × 297 mm", legal: "Legal 8.5 × 14 pulg" } };
  function L() { return document.documentElement.getAttribute("data-lang") === "es" ? "es" : "en"; }
  function gcd(a, b) { return b ? gcd(b, a % b) : a; }
  function fmt(inches) {
    if (unit === "cm") return (Math.round(inches * 2.54 * 10) / 10).toString() + " cm";
    var w = Math.floor(inches + 1e-9), n = Math.round((inches - w) * 16);
    if (n === 16) { w++; n = 0; }
    var t = n ? ((w ? w + " " : "") + (n / gcd(n, 16)) + "/" + (16 / gcd(n, 16))) : String(w);
    return t + (L() === "es" ? " pulg" : " in");
  }
  var exact = { "pl-w": 11.8, "pl-d": 8.7, "pl-h": 8.3 };  // inches, unrounded, so switching units never drifts
  ["pl-w", "pl-d", "pl-h"].forEach(function (id) {
    $(id).addEventListener("input", function () { var v = parseFloat($(id).value); exact[id] = isFinite(v) ? (unit === "cm" ? v / 2.54 : v) : NaN; });
  });
  function num(id) { var v = parseFloat($(id).value); return isFinite(v) && v > 0 ? (unit === "cm" ? v / 2.54 : v) : NaN; }

  function setUnit(u) {
    if (u === unit) return;
    ["pl-w", "pl-d", "pl-h"].forEach(function (id) {
      var v = exact[id]; if (!isFinite(v)) return;
      $(id).value = u === "cm" ? (Math.round(v * 2.54 * 10) / 10) : (Math.round(v * 100) / 100);
    });
    unit = u;
    $("pl-u-in").setAttribute("aria-pressed", String(u === "in")); $("pl-u-cm").setAttribute("aria-pressed", String(u === "cm"));
    run();
  }

  function run() {
    [].forEach.call($("pl-paper").options, function (o) { o.textContent = POPT[L()][o.value]; });
    var t = T[L()], W = num("pl-w"), Dp = num("pl-d"), H = num("pl-h");
    var walls = [["L", $("pl-L").checked, Dp, t.left], ["B", $("pl-B").checked, W, t.back], ["R", $("pl-R").checked, Dp, t.right]];
    var warn = [], list = $("pl-list"), svgBox = $("pl-svg");
    list.innerHTML = ""; svgBox.innerHTML = "";
    function fail(msg) { $("pl-big").textContent = "—"; $("pl-big-lab").textContent = ""; $("pl-sub").textContent = ""; $("pl-warn").hidden = false; $("pl-warn").textContent = msg; }
    if (!(W && Dp && H)) return fail(t.bad);
    if (!walls.some(function (w) { return w[1]; })) return fail(t.none);

    // paper orientation: strip height must fit; prefer the wider usable width
    var p = PAPER[$("pl-paper").value], stripH = H + 2 * ALLOW, best = null;
    [[p[0], p[1], "portrait"], [p[1], p[0], "landscape"]].forEach(function (o) {
      var uw = o[0] - 2 * MARGIN, uh = o[1] - 2 * MARGIN;
      if (uh + 1e-9 >= stripH && (!best || uw > best.uw)) best = { uw: uw, uh: uh, name: o[2] };
    });
    if (!best) return fail(t.tooTall(fmt(stripH), fmt(Math.max(p[0], p[1]) - 2 * MARGIN)));
    var ov = parseFloat($("pl-ov").value), step = best.uw - ov;

    // contiguous groups in order left -> back -> right
    var groups = [], cur = null;
    if (method === "back") {
      // back wall first (with a small wrap onto each covered side), then each side wall on its own
      if (walls[1][1]) {
        var bg = [];
        if (walls[0][1]) bg.push(["wL", true, WRAP, t.wrapL]);
        bg.push(walls[1]);
        if (walls[2][1]) bg.push(["wR", true, WRAP, t.wrapR]);
        groups.push(bg);
      }
      if (walls[0][1]) groups.push([walls[0]]);
      if (walls[2][1]) groups.push([walls[2]]);
    } else {
      walls.forEach(function (w) { if (w[1]) { if (!cur) { cur = []; groups.push(cur); } cur.push(w); } else cur = null; });
      if (!$("pl-B").checked && groups.length > 1) warn.push(t.separate);
    }

    var total = 0, pieces = [];
    groups.forEach(function (g) {
      var len = g.reduce(function (a, w) { return a + w[2]; }, 0);
      var n = len <= best.uw + 1e-9 ? 1 : 1 + Math.ceil((len - best.uw) / step - 1e-9);
      var corners = [], acc = 0;
      g.forEach(function (w, k) { acc += w[2]; if (k < g.length - 1) corners.push([acc, w[0] + g[k + 1][0]]); });
      var sheets = [];
      for (var k = 0; k < n; k++) {
        var a = k * step, b = Math.min(a + best.uw, len);
        var on = [], x = 0;
        g.forEach(function (w) { var s0 = x, s1 = x + w[2]; if (b > s0 + 0.05 && a < s1 - 0.05) on.push(w[3]); x = s1; });
        sheets.push({ a: a, b: b, on: on, last: k === n - 1 && n > 1, leftover: k === n - 1 ? best.uw - (b - a) : 0 });
        if (k > 0 && method === "strip") corners.forEach(function (c) {
          var d = Math.abs(a - c[0]);
          if (d < 0.25) warn.push(t.corner(fmt(d), c[1] === "LB" ? t.backLeft : t.backRight));
        });
      }
      total += n; pieces.push({ g: g, len: len, sheets: sheets, corners: corners });
    });

    $("pl-big").textContent = total;
    $("pl-big-lab").textContent = (total === 1 ? t.sheet : t.sheets) + " · " + t.of + " " + PNAME[L()][$("pl-paper").value] + ", " + t[best.name];
    $("pl-sub").textContent = t.cut + " " + fmt(stripH) + " " + t.tall + ". " + t.plusSpare;

    var no = 0;
    pieces.forEach(function (pc, pi) {
      pc.sheets.forEach(function (sh) {
        no++;
        var li = document.createElement("li");
        li.innerHTML = (pieces.length > 1 ? t.piece + " " + (pi + 1) + " · " : "") + t.covers + " <b>" + fmt(sh.a) + " – " + fmt(sh.b) + "</b> · " + sh.on.join(" + ") +
          (sh.last && sh.leftover > 0.05 ? " · " + t.trimLast + " (" + fmt(sh.leftover) + ")" : "");
        list.appendChild(li);
      });
    });

    // to-scale diagram of the unfolded walls
    var S = 22, padX = 6, gap = 18, labH = 18, h = stripH * S;
    var totalLen = pieces.reduce(function (a, pc) { return a + pc.len; }, 0);
    var vw = totalLen * S + padX * 2 + gap * (pieces.length - 1), vh = h + labH * 2 + 6;
    var out = ['<svg viewBox="0 0 ' + vw.toFixed(1) + ' ' + vh.toFixed(1) + '" role="img" aria-label="Wallpaper sheets laid over the unfolded walls">'];
    var ox = padX, y0 = labH;
    no = 0;
    pieces.forEach(function (pc) {
      var x = ox;
      pc.g.forEach(function (w) {
        out.push('<rect class="wall" x="' + x.toFixed(1) + '" y="' + (y0 + ALLOW * S).toFixed(1) + '" width="' + (w[2] * S).toFixed(1) + '" height="' + (H * S).toFixed(1) + '"/>');
        if (w[2] >= 1) out.push('<text class="muted" x="' + (x + w[2] * S / 2).toFixed(1) + '" y="' + (y0 + h + 14).toFixed(1) + '" text-anchor="middle">' + w[3] + " · " + fmt(w[2]) + '</text>');
        x += w[2] * S;
      });
      pc.sheets.forEach(function (sh, k) {
        no++;
        var sx = ox + sh.a * S, sw = (sh.b - sh.a) * S;
        out.push('<rect class="' + (k % 2 ? "sheet-b" : "sheet-a") + '" x="' + sx.toFixed(1) + '" y="' + y0 + '" width="' + sw.toFixed(1) + '" height="' + h.toFixed(1) + '"/>');
        out.push('<circle class="numbg" cx="' + (sx + 11).toFixed(1) + '" cy="' + (y0 + 13) + '" r="8"/><text class="num" x="' + (sx + 11).toFixed(1) + '" y="' + (y0 + 16.5) + '" text-anchor="middle">' + no + '</text>');
        if (k > 0) out.push('<line class="seam" x1="' + sx.toFixed(1) + '" y1="' + (y0 - 4) + '" x2="' + sx.toFixed(1) + '" y2="' + (y0 + h + 4).toFixed(1) + '"/>');
      });
      pc.corners.forEach(function (c) { var cx = ox + c[0] * S; out.push('<line class="corner" x1="' + cx.toFixed(1) + '" y1="' + (y0 + ALLOW * S).toFixed(1) + '" x2="' + cx.toFixed(1) + '" y2="' + (y0 + h - ALLOW * S).toFixed(1) + '"/>'); });
      [ALLOW * S, h - ALLOW * S].forEach(function (yy) { out.push('<line class="allow" x1="' + ox + '" y1="' + (y0 + yy).toFixed(1) + '" x2="' + (ox + pc.len * S).toFixed(1) + '" y2="' + (y0 + yy).toFixed(1) + '"/>'); });
      out.push('<text x="' + ox + '" y="12">' + t.run + " " + fmt(pc.len) + '</text>');
      ox += pc.len * S + gap;
    });
    out.push("</svg>");
    svgBox.innerHTML = out.join("");
    $("pl-warn").hidden = !warn.length; $("pl-warn").innerHTML = warn.map(function (m) { return "<span>" + m + "</span>"; }).join("");
  }

  form.addEventListener("input", run); form.addEventListener("change", run);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  function setMethod(m) { method = m; $("pl-m-strip").setAttribute("aria-pressed", String(m === "strip")); $("pl-m-back").setAttribute("aria-pressed", String(m === "back")); run(); }
  $("pl-m-strip").addEventListener("click", function () { setMethod("strip"); });
  $("pl-m-back").addEventListener("click", function () { setMethod("back"); });
  $("pl-u-in").addEventListener("click", function () { setUnit("in"); });
  $("pl-u-cm").addEventListener("click", function () { setUnit("cm"); });
  document.querySelectorAll(".lang button").forEach(function (b) { b.addEventListener("click", function () { setTimeout(run, 0); }); });
  run();
})();
// ---- start-here checklist (saved per viewer) ----
(function () {
  var boxes = document.querySelectorAll("[data-sup]"); if (!boxes.length) return;
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem("mns-starter") || "{}") || {}; } catch (e) { saved = {}; }
  function count() {
    var have = 0, must = 0, mustHave = 0;
    boxes.forEach(function (b) {
      var isMust = b.closest("label").querySelector(".tag.must");
      if (b.checked) have++;
      if (isMust) { must++; if (b.checked) mustHave++; }
    });
    var es = document.documentElement.getAttribute("data-lang") === "es";
    document.getElementById("sup-count").textContent = es
      ? have + " de " + boxes.length + " listos · " + mustHave + " de " + must + " esenciales"
      : have + " of " + boxes.length + " ready · " + mustHave + " of " + must + " must-haves";
  }
  boxes.forEach(function (b) {
    b.checked = !!saved[b.getAttribute("data-sup")];
    b.addEventListener("change", function () {
      saved[b.getAttribute("data-sup")] = b.checked;
      try { localStorage.setItem("mns-starter", JSON.stringify(saved)); } catch (e) {}
      count();
    });
  });
  document.querySelectorAll(".lang button").forEach(function (b) { b.addEventListener("click", function () { setTimeout(count, 0); }); });
  count();
})();
