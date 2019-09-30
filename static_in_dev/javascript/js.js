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
    $('.remove_from_cart').on('click', function (e) {
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
                $('#'+product_slug).remove();
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
                $('#cart-item-total-' + item_id).html(data.item_total + ' руб.')
            }
        })
    })
});