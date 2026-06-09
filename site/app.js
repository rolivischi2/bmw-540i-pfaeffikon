/* BMW 540i landing page · interactions */
(function () {
  "use strict";

  /* ---- sticky nav ---- */
  var nav = document.getElementById("nav");
  var onScroll = function () {
    nav.classList.toggle("is-stuck", window.scrollY > 40);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---- scroll reveal ---- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- lightbox ---- */
  var imgs = Array.prototype.slice.call(document.querySelectorAll(".lb"));
  var sources = imgs.map(function (i) { return i.getAttribute("data-full"); });
  var alts = imgs.map(function (i) { return i.getAttribute("alt") || ""; });
  var box = document.getElementById("lightbox");
  var boxImg = box.querySelector(".lightbox__img");
  var current = 0;

  function show(i) {
    current = (i + sources.length) % sources.length;
    boxImg.src = sources[current];
    boxImg.alt = alts[current];
  }
  function open(i) {
    show(i);
    box.classList.add("is-open");
    box.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }
  function close() {
    box.classList.remove("is-open");
    box.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  imgs.forEach(function (img, i) {
    img.addEventListener("click", function () { open(i); });
  });
  box.querySelector(".lightbox__close").addEventListener("click", close);
  box.querySelector(".lightbox__nav--prev").addEventListener("click", function (e) {
    e.stopPropagation(); show(current - 1);
  });
  box.querySelector(".lightbox__nav--next").addEventListener("click", function (e) {
    e.stopPropagation(); show(current + 1);
  });
  box.addEventListener("click", function (e) {
    if (e.target === box) close();
  });
  document.addEventListener("keydown", function (e) {
    if (!box.classList.contains("is-open")) return;
    if (e.key === "Escape") close();
    else if (e.key === "ArrowLeft") show(current - 1);
    else if (e.key === "ArrowRight") show(current + 1);
  });
})();
