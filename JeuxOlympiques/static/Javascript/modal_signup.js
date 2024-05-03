// JavaScript pour afficher la popup et gérer les événements de clic

// Lorsque l'utilisateur clique sur le lien, afficher la popup
document.getElementById('policyLink').addEventListener('click', function (event) {
    event.preventDefault(); // Empêche le lien de suivre son URL
    document.getElementById('policyPopup').classList.remove('hidden');
});

// Lorsque l'utilisateur clique sur le bouton de fermeture de la popup, la cacher
document.getElementById('closePopupButton').addEventListener('click', function () {
    document.getElementById('policyPopup').classList.add('hidden');
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('registrationForm').addEventListener('submit', function (event) {
        if (!document.getElementById('policyCheckbox').checked) {
            event.preventDefault(); // Empêche la soumission du formulaire si la case n'est pas cochée
            alert('Veuillez accepter la politique de sécurité pour continuer.');
        }
    });
});