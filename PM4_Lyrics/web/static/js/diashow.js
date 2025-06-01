let slideIndex = 0;
const slides = document.getElementsByClassName("slide");

function showSlides() {
    // Alle Slides vorbereiten
    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active", "previous");
    }

    const previousIndex = slideIndex;
    slideIndex = (slideIndex + 1) % slides.length;

    slides[previousIndex].classList.add("previous");
    slides[slideIndex].classList.add("active");

    setTimeout(showSlides, 8000); // Alle 8 Sekunden wechseln
}

showSlides();

