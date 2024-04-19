const slides = document.querySelectorAll('.slide');
let currentSlide = 0;
let isAnimating = false;
var contador = 0;

function showSlide(index) {
    // Verificar si la animación está en curso
    if (isAnimating) {
        return;
    }

    // Marcar la animación como en curso
    isAnimating = true;

    slides.forEach((slide, i) => {
        if (i === index) {
            slide.classList.add('actual'); // Agregar clase 'actual' al slide activo
            slide.classList.remove('anterior'); // Quitar clase 'anterior' del slide activo
        } else if (index === 0 && i === slides.length - 1) {
            slide.classList.add('anterior'); // Agregar clase 'anterior' al último slide si el primer slide está activo
            slide.classList.remove('actual'); // Quitar clase 'actual' del último slide si el primer slide está activo
        } else if (i === index - 1) {
            slide.classList.add('anterior'); // Agregar clase 'anterior' al slide anterior
            slide.classList.remove('actual'); // Quitar clase 'actual' del slide anterior
        } else {
            slide.classList.remove('actual'); // Quitar clase 'actual' de otros slides
            slide.classList.remove('anterior'); // Quitar clase 'anterior' de otros slides
        }
    });

    // Después de completar la animación, marcarla como finalizada
    setTimeout(() => {
        isAnimating = false;
        contador = 0;
    }, 1000); // Duración de la animación en milisegundos
}

function changeSlide(direction) {
    // Verificar si la animación está en curso
    if (isAnimating) {
        return;
    }
    if (direction === 'down') {
        currentSlide = (currentSlide + 1) % slides.length;
    } else if (direction === 'up') {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    }
    showSlide(currentSlide);
}

/*document.addEventListener('DOMContentLoaded', function() {
    setInterval(() => {
        if (isAnimating) {
            return;
        }
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }, 5000);
});*/
document.addEventListener('DOMContentLoaded', function() {
    setInterval(() => {
        if(contador == 5){
            if (isAnimating) {
                return;
            }
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
            contador = 0;
        }
        else{
            contador++;
        }
    }, 1000);
});

document.addEventListener('wheel', function(e) {
    if (isAnimating) {
        return;
    }
    const delta = e.deltaY || e.detail || e.wheelDelta;

    if (delta > 0) { // Scroll hacia abajo
        changeSlide('down');
    } else { // Scroll hacia arriba
        changeSlide('down');
    }
});
