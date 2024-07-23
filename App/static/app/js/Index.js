document.addEventListener('DOMContentLoaded', function() {
    var cards = document.querySelectorAll('.card1, .card2');
    cards.forEach(function(card) {
        card.addEventListener('mouseover', function() {
            card.classList.add('hover');
        });
  
        card.addEventListener('mouseout', function() {
            card.classList.remove('hover');
        });
    });
  });