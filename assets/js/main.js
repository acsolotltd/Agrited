/*
==========================================
Scroll Progress
==========================================
*/

const progressBar = document.getElementById("progressBar");

window.addEventListener("scroll", () => {

    const totalHeight =
        document.documentElement.scrollHeight -
        window.innerHeight;

    const progress =
        (window.scrollY / totalHeight) * 100;

    progressBar.style.width = progress + "%";

});

const header=document.querySelector(".header");

window.addEventListener("scroll",()=>{

    if(window.scrollY>50){

        header.classList.add("scrolled");

    }

    else{

        header.classList.remove("scrolled");

    }

});