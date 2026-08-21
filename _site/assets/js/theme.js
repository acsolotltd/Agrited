/*
=====================================
Theme Switch
=====================================
*/

const html = document.documentElement;

const button = document.getElementById("themeToggle");

button.addEventListener("click", () => {

    html.classList.toggle("dark");

    if (html.classList.contains("dark")) {

        localStorage.setItem("theme", "dark");

    } else {

        localStorage.setItem("theme", "light");

    }

});