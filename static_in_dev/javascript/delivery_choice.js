window.addEventListener('DOMContentLoaded', () => {
    let deliveryChoiceMenu = document.getElementById('id_buying_type'),
        addressLabel = document.querySelector('label[for="id_address"]'),
        address = document.getElementById('id_address');

    deliveryChoiceMenu.addEventListener('click', () => {
        if (deliveryChoiceMenu.value !== 'Самовывоз') {
            address.style.display = 'block';
            addressLabel.style.display = 'block';
        } else {
            address.style.display = 'none';
            addressLabel.style.display = 'none';
        }
    });
});