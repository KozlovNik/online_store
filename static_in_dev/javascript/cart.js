$(function () {
    let deliveryChoiceMenu = $('#id_buying_type'),
        address = $('#id_address'),
        addressLabel = $('label[for="id_address"]');

    deliveryChoiceMenu.on('click', function () {
        if (deliveryChoiceMenu.val() !== 'Самовывоз') {
            address.show();
            addressLabel.show();
        } else {
            address.hide();
            addressLabel.hide();
        }
    });
});