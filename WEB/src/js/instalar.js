document.addEventListener('DOMContentLoaded', () => {
    let deferredPrompt;

    // Registrar el evento beforeinstallprompt
    window.addEventListener('beforeinstallprompt', (event) => {
        // Guardar la referencia al evento
        event.preventDefault();
        deferredPrompt = event;
        // Mostrar un mensaje o botón para invitar al usuario a instalar la aplicación
        // Por ejemplo, aquí se puede mostrar un botón "Instalar aplicación"
        if(isMobileDevice() == true){
            const installButton = document.getElementById('installButton');
            installButton.style.display = 'block';
        }
    });

    // Escuchar clics en el botón de instalación
    const installButton = document.getElementById('installButton');
    installButton.addEventListener('click', () => {
        // Mostrar el prompt de instalación si está disponible
        if (deferredPrompt) {
            deferredPrompt.prompt();

            // Esperar a que el usuario interactúe con el prompt
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('El usuario ha aceptado instalar la aplicación');
                } else {
                    console.log('El usuario ha rechazado instalar la aplicación');
                }

                // Limpiar la referencia al prompt
                deferredPrompt = null;
            });
        }
    });
});

function isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}
