/*
==========================================
Agrited Gallery
==========================================
*/

document.addEventListener("DOMContentLoaded", () => {

    const lightbox = GLightbox({

        selector: ".glightbox",

        touchNavigation: true,

        loop: true,

        zoomable: true,

        draggable: true,

        autoplayVideos: true,

        openEffect: "zoom",

        closeEffect: "fade",

        slideEffect: "slide",

        moreLength: 60,

        plyr: {

            css: "",

            js: ""

        }

    });

});

document.querySelectorAll(".farm-gallery").forEach(gallery => {

    const images = gallery.querySelectorAll("a.glightbox");

    const counter = gallery.querySelector(".gallery-count");

    if(counter){

        counter.textContent = `${images.length} Photos`;

    }

});

document.querySelectorAll("img").forEach(img=>{

    img.loading="lazy";

});

document.querySelectorAll("img").forEach(image=>{

    image.addEventListener("load",()=>{

        image.classList.add("loaded");

    });

});

