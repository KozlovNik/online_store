let loginCloseButton = document.getElementById('flag'),
    loginWindow = document.getElementById('popup-login-window'),
    loginButton = document.getElementById('login-button'),
    backgroundWindow = document.getElementById('modal-login'),
    loginFormErrors = document.getElementById('login-form__errors');

if (loginButton) {
    loginButton.addEventListener('click', function (event) {
        loginFormErrors.innerText = '';
        event.preventDefault();
        if (loginWindow.style.display !== 'block') {
            loginWindow.style.display = 'block';
            backgroundWindow.style.display = 'block'
        }
    });
}

hideLoginFormOnClick = function(){
    backgroundWindow.style.display = 'none';
    loginWindow.style.display = 'none';
};

backgroundWindow.addEventListener('click', hideLoginFormOnClick);
loginCloseButton.addEventListener('click', hideLoginFormOnClick);


$(function () {
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
                if (data.response) {
                    myForm.unbind('submit').submit();
                } else {
                    errors.html('Неверный логин или пароль')
                }
            },
            error: function (ThrowError) {
            },
        });
    })
});


$(function () {
    $('#add-to-favorites').on('click', function () {
        let addToFavoritesButton = $(this),
            slug = $(this).attr('data-slug-fav'),
            favoritesQuantity = $('#favorites-quantity'),
            data = {
                slug: slug,
            };

        $.ajax({
            type: 'GET',
            url: '/add_to_favorites/',
            data: data,
            success: function (data) {
                if (data.user_authenticated) {
                    if (!addToFavoritesButton.hasClass('add-to-favorites--active')) {
                        addToFavoritesButton.addClass('add-to-favorites--active');
                    } else {
                        addToFavoritesButton.removeClass('add-to-favorites--active')
                    }
                    favoritesQuantity.html(data.quantity_of_favorites)
                } else {
                    $('#modal-login').css('display', 'block');
                    $('#popup-login-window').css('display', 'block');
                    $('#login-form__errors').html('Чтобы добавлять товары в закладки, необходимо авторизироваться')
                }
            }
        })
    })
});

$(function () {
    $('.bookmarked').on('click', function (event) {
        event.preventDefault();
        let bookmarked = $(this),
            slug = $(this).attr('data-slug'),
            favoritesQuantity = $('#favorites-quantity'),
            data = {
                slug: slug,
            };

        $.ajax({
            type: 'GET',
            url: '/add_to_favorites/',
            data: data,
            success: function (data) {
                console.log(data.response);
                if (data.user_authenticated === true) {
                    favoritesQuantity.html(data.quantity_of_favorites);
                    if (data.response === true) {
                        bookmarked.html('Товар в закладках');
                    } else if (data.response === false) {
                        bookmarked.html('Добавить в закладки');
                    }
                } else {
                    $('#modal-login').css('display', 'block');
                    $('#popup-login-window').css('display', 'block');
                    $('#login-form__errors').html('Чтобы добавлять товары в закладки, необходимо авторизироваться')
                }
            }
        })
    })
});

$(function () {
    $('#my-favorites').on('click', function (event) {
        let href = $(this).attr('href');
        event.preventDefault();
        $.ajax({
            type: 'GET',
            url: '/is_authenticated/',
            success: function (data) {
                if (data.is_authenticated) {
                    window.location = href
                } else {
                    $('#modal-login').css('display', 'block');
                    $('#popup-login-window').css('display', 'block');
                    $('#login-form__errors').html('Чтобы просматривать товары в закладках, необходимо авторизироваться')
                }
            }
        })
    })
});

// Заполнители окна регистрации
let emailPlaceHolder = document.getElementById('id_username').placeholder = 'Введите электронную почту',
    passPlaceHolder = document.getElementById('id_password').placeholder = 'Введите пароль';
