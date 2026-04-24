// JavaScript simple para página de agentes

// Cuando la página se carga
document.addEventListener('DOMContentLoaded', function() {
    
    // Efecto hover en las tarjetas
    const cards = document.querySelectorAll('.agent-card');
    
    // Recorrer todas las tarjetas
    for (let i = 0; i < cards.length; i++) {
        let card = cards[i];
        
        // Al hacer clic en una tarjeta
        card.addEventListener('click', function() {
            // Efecto simple con clases
            this.classList.add('clicked');
            
            // Quitar la clase después de un tiempo
            setTimeout(function() {
                card.classList.remove('clicked');
            }, 200);
        });
    }
    
    // Efecto en los iconos
    const icons = document.querySelectorAll('.info-item i');
    
    // Recorrer todos los iconos
    for (let i = 0; i < icons.length; i++) {
        let icon = icons[i];
        
        icon.addEventListener('mouseenter', function() {
            // Añadir clase para hover
            icon.classList.add('icon-hover');
        });
        
        icon.addEventListener('mouseleave', function() {
            // Quitar clase de hover
            icon.classList.remove('icon-hover');
        });
    }
    
    console.log('Página cargada');
});
