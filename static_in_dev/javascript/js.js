let currency = ' руб.',
    quantity_word = ' шт.';


// Функция добавляет товар в корзину и обновляет общее число товаров и сумму
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
                $('#cart_count').html(data.cart_total + quantity_word);
                let product_id = $('#' + product_slug);
                product_id.html('Перейти в корзину');
                product_id.removeClass('add-to-cart');
                product_id.addClass('add-to-cart--added');
                $('#cart-total-sum').html(data.cart_total_sum + currency);
            },
        })
    });
});


// Функция удаляет товар из корзины, а также обновляет общее число товаров и сумму
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
                $('#cart_count').html(data.cart_total + quantity_word);
                $('#cart-total-price').html(data.cart_total_price + currency);
                $('#cart-total-sum').html(data.cart_total_price + currency);
                $('#'+product_slug).remove();
                if (data.cart_total === 0){
                    $('.cart__table').css('display', 'none');
                }
            },
        })
    });
});


// Функция обновляет количество определенного товара и общую сумму данного товара в корзине,
// а также общее количество товаров и общую сумму товаров
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
                $('#cart-item-total-' + item_id).html(data.item_total + currency);
                $('#cart-total-price').html(data.cart_total_price + currency);
                $('#cart_count').html(data.cart_total_quantity + quantity_word);
                $('#cart-total-sum').html(data.cart_total_price + currency);
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


$(document).ready(function(){
        $("#id_username").attr('placeholder', 'Введите электронную почту');
        $("#id_password").attr('placeholder', 'Введите пароль');
    });

let loginCloseButton = document.getElementById('flag'),
    loginWindow = document.getElementById('popup-login-window'),
    loginButton = document.getElementById('login-button'),
    backgroundWindow = document.getElementById('modal-login'),
    loginErrors = document.getElementsByClassName('login-form__errors')[0];


loginButton.addEventListener('click', function (event) {
    event.preventDefault();
    console.log(loginErrors);
    if (loginWindow.style.display !== 'block'){
        loginWindow.style.display = 'block';
        backgroundWindow.style.display = 'block'
   }
});

backgroundWindow.addEventListener('click', function () {
   backgroundWindow.style.display = 'none';
   loginWindow.style.display = 'none';
});

loginCloseButton.addEventListener('click', function () {
   loginWindow.style.display = 'none';
   backgroundWindow.style.display = 'none';
});

$(function() {
    let myForm = $('.login-form'),
        errors = $('.login-form__errors');
    myForm.submit(function (event) {
        event.preventDefault();
        let myData = myForm.serialize();
        $.ajax({
            method: 'POST',
            url: '/authenticate_user/',
            data: myData,
            success: function (data) {
                console.log(data.response);
                if (data.response){
                    myForm.unbind('submit').submit();
                }
                else {
                    errors.html('Неверный логин или пароль')
                }
            },
            error: function (ThrowError) {
                console.log(ThrowError);
            },
        });
    })
});

