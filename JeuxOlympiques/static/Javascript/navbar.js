const navbarElementsToToggle = document.querySelectorAll(".toggle-menu");
const iconToggle = document.querySelector(".icon-toggle");

const toggleMenu = () => navbarElementsToToggle.forEach(el => el.classList.toggle("hidden"));

iconToggle.addEventListener("click", toggleMenu);