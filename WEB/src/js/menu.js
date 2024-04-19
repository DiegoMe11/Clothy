const menuLinks = document.querySelectorAll('#menu a');
const fondoMenu = document.getElementById('fondo-menu');
const logo_svg = document.getElementById('logo-svg');
const pathElement = logo_svg.querySelector('path');
const logo_text = document.getElementById('nombre');
const separador = document.getElementById('separador');

const menu = document.getElementById('menu');
const fondoOscuro = document.getElementById('fondo-oscuro');
var abierto = false;

fondoMenu.style.minWidth = '0px'
fondoOscuro.style.zIndex = '0';

menuLinks.forEach(link => {
    link.addEventListener('mouseover', () => {
        fondoMenu.style.width = '33%';
        fondoOscuro.style.opacity = '1';
        fondoMenu.style.minWidth = '350px'
        abierto = true;
        // Cambiar el color del texto de todos los enlaces a #333 cuando el menú está desplegado
        menuLinks.forEach(link => {
            link.style.color = '#333';
        });
        logo_text.style.color = '#333';
        pathElement.style.fill = '#333';
        pathElement.style.stroke = '#333';
        pathElement.style.transition = '0.3s';
        separador.style.backgroundColor = "#333"
        fondoOscuro.style.zIndex = '2';
    });
    if (abierto = false){
        link.addEventListener('mouseout', () => {
            fondoMenu.style.width = '0%';
            fondoOscuro.style.opacity = '0';
            fondoMenu.style.minWidth = '0'
            abierto = false;

            menuLinks.forEach(link => {
                link.style.color = '#FAFAFA';
            });
            logo_text.style.color = '#FAFAFA';
            pathElement.style.fill = '#FAFAFA';
            pathElement.style.stroke = '#FAFAFA';
            separador.style.backgroundColor = "#FAFAFA"
            fondoOscuro.style.zIndex = '0';
        });
    }
});

menuLinks.forEach(link => {
    link.addEventListener('mouseover', () => {
        link.style.color = '#ff2d00';
    });
    link.addEventListener('mouseout', () => {
        link.style.color = '#333';
    });
});

fondoMenu.addEventListener('mouseover', () => {
    fondoMenu.style.minWidth = '350px'
    fondoMenu.style.width = '33%';
    fondoOscuro.style.opacity = '1';
    abierto = true;
    fondoOscuro.style.zIndex = '2';

});
fondoMenu.addEventListener('mouseout', () => {
    fondoMenu.style.width = '0%';
    fondoOscuro.style.opacity = '0';
    fondoMenu.style.minWidth = '0'
    abierto = false;

    menuLinks.forEach(link => {
        link.style.color = '#FAFAFA';
    });
    logo_text.style.color = '#FAFAFA';
    pathElement.style.fill = '#FAFAFA';
    pathElement.style.stroke = '#FAFAFA';
    separador.style.backgroundColor = "#FAFAFA"
    fondoOscuro.style.zIndex = '0';
});
