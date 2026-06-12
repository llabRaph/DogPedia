document.addEventListener("DOMContentLoaded", () => {
    
    // 1. Gestion du bandeau déroulant pour lister les informations des races
    const raceTitles = document.querySelectorAll(".race-title");
    
    raceTitles.forEach(title => {
        title.addEventListener("click", () => {
            const detailsBlock = title.nextElementSibling;
            
            if (detailsBlock.style.display === "none" || detailsBlock.style.display === "") {
                detailsBlock.style.display = "flex";
                title.style.backgroundColor = "#eef5fc";
            } else {
                detailsBlock.style.display = "none";
                title.style.backgroundColor = "#fff";
            }
        });
    });

});

// 2. Sélecteur de photo Adulte / Chiot
function showPhoto(btn, src) {
    // Changer la source de l'image
    const img = btn.closest('.photo-selector').querySelector('.zoomable-img');
    img.src = src;

    // Mettre à jour le bouton actif
    btn.closest('.photo-buttons').querySelectorAll('.photo-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}