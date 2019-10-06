$(function(){
    $('.add-to-cart').on('click', function (e) {
        if ($(this).attr('class') === 'add-to-cart--added'){
            return
        }
        e.preventDefault();
        let product_slug = $(this).attr('data-slug');
        let data = {
            product_slug: product_slug
        };
        $.ajax({
            type: "GET",
            url: "/add_to_cart/",
            data: data,
            success: function (data) {
                $('#cart_count').html(data.cart_total);
                let product_id = $('#' + product_slug);
                product_id.html('Перейти в корзину');
                product_id.removeClass('add-to-cart');
                product_id.addClass('add-to-cart--added');
            },
        })
    });
});

$(function(){
    $('.remove-from-cart').on('click', function (e) {
        e.preventDefault();
        let product_slug = $(this).attr('data-slug');
        let data = {
            product_slug: product_slug
        };
        $.ajax({
            type: "GET",
            url: "/remove_from_cart/",
            data: data,
            success: function (data) {
                $('#cart_count').html(data.cart_total);
                $('#cart-total-price').html(data.cart_total_price);
                $('#'+product_slug).remove();
                if (data.cart_total === 0){
                    $('.cart__table').css('display', 'none');
                }
            },
        })
    });
});

$(function(){
    $('.cart-item-quantity').on('click', function (e) {
        let quantity = $(this).val();
        let item_id = $(this).attr('data-id');
        let data = {
            quantity: quantity,
            item_id: item_id
        };
        $.ajax({
            type: 'GET',
            url: '/change_item_quantity/',
            data: data,
            success: function (data) {
                $('#cart-item-total-' + item_id).html(data.item_total + ' руб.');
                $('#cart-total-price').html(data.cart_total_price + 'руб.');
            }
        })
    })
});

// Функция отключает верхнее всплывающее окно
let closeButton = document.getElementsByClassName('upper-popup-window__close-button')[0],
    upperPopUpWindow = document.getElementsByClassName('upper-popup-window')[0],
    upperPopUpWindowHidden = document.getElementsByClassName('upper-popup-window-hidden')[0];
closeButton.addEventListener('click', function () {
   upperPopUpWindow.style.display = 'none';
   upperPopUpWindowHidden.style.display = 'block';
});