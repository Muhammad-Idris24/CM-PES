document.addEventListener("change", (event) => {
  if (event.target.name === "contract" && location.pathname.includes("/evaluations/new/")) {
    const params = new URLSearchParams(location.search);
    if (params.get("contract") !== event.target.value) {
      location.href = `${location.pathname}?contract=${event.target.value}`;
    }
  }
});

const menuToggle = document.querySelector("[data-menu-toggle]");
const navWrap = document.querySelector("[data-nav-wrap]");
if (menuToggle && navWrap) {
  menuToggle.addEventListener("click", () => {
    const isOpen = navWrap.classList.toggle("is-open");
    menuToggle.setAttribute("aria-expanded", String(isOpen));
  });
}
