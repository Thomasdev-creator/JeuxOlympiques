function filterOffers() {
    var maxPrice = document.getElementById('priceFilter').value;
    var tickets = document.getElementsByClassName('ticket');
    for (var i = 0; i < tickets.length; i++) {
        var price = parseFloat(tickets[i].getAttribute('data-price'));
        if (maxPrice !== '0' && price > maxPrice) {
            tickets[i].style.display = 'none';
        } else {
            tickets[i].style.display = 'block';
        }
    }
}

