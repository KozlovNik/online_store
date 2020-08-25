window.addEventListener('DOMContentLoaded', () => {
    // Ajax запрос на добавление товара в корзину
    let addToCartItems = document.getElementsByClassName('add-to-cart');
    Array.from(addToCartItems).forEach(function (element) {
        element.addEventListener('click', function (event) {
            if (this.getAttribute('class') === 'add-to-cart--added') {
                return;
            }
            event.preventDefault();
            let product_slug = this.getAttribute('data-slug'),
                link = `/add_to_cart/?product_slug=${product_slug}`,
                xhr = new XMLHttpRequest();
            xhr.onload = function () {
                if (xhr.status === 200) {
                    let data = JSON.parse(xhr.response),
                        productId = document.getElementById(product_slug),
                        totalSum = document.getElementById('cart-total-sum'),
                        cartCount = document.getElementById('cart_count');
                    productId.innerText = 'Перейти в корзину';
                    productId.classList.remove('add-to-cart');
                    productId.classList.add('add-to-cart--added');
                    totalSum.innerText = parseFloat(data.cart_total_sum).toFixed(2);
                    cartCount.innerText = data.cart_total;
                }
            };
            xhr.open('GET', link, true);
            xhr.send();
        });
    });


    // Ajax запрос на удаление товара из корзины
    let removeFromCartItems = document.getElementsByClassName('remove-from-cart');
    Array.from(removeFromCartItems).forEach(function (element) {
        element.addEventListener('click', function (event) {
                event.preventDefault();
                console.log(this);
                let product_slug = this.getAttribute('data-slug'),
                    link = `/remove_from_cart/?product_slug=${product_slug}`,
                    xhr = new XMLHttpRequest();
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        let data = JSON.parse(xhr.response),
                            cartCount = document.getElementById('cart_count'),
                            totalPrice = document.getElementById('cart-total-price'),
                            totalSum = document.getElementById('cart-total-sum'),
                            productId = document.getElementById(product_slug);
                        console.log(totalPrice);
                        cartCount.innerHTML = data.cart_total;
                        totalPrice.innerHTML = data.cart_total_price;
                        totalSum.innerHTML = parseFloat(data.cart_total_price).toFixed(2);
                        productId.remove();
                        if (data.cart_total === 0) {
                            let cartTable = document.getElementById("content-wrapper"),
                                para = document.createElement('p');
                            cartTable.style.display = 'none';
                            para.innerHTML = 'Ваша корзина пуста';
                            document.getElementById('page-main').appendChild(para);
                            para.classList.add('cart__heading', 'cart__heading--empty-cart');
                        }
                    }
                };
                xhr.open('GET', link, true);
                xhr.send();
            }
        );
    });

    // Ajax запрос на изменение количества определенного товара в корзине
    let cartItemQuantity = document.getElementsByClassName('cart-item-quantity');
    Array.from(cartItemQuantity).forEach(function (element) {
        element.addEventListener('click', function (event) {
            let quantity = this.value,
                item_id = this.getAttribute('data-id'),
                link = `/change_item_quantity/?quantity=${quantity}&item_id=${item_id}`,
                xhr = new XMLHttpRequest();
            console.log(link);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    let data = JSON.parse(xhr.response),
                        cartItemTotal = document.getElementById(`cart-item-total-${item_id}`),
                        cartTotalPrice = document.getElementById('cart-total-price'),
                        cartCount = document.getElementById('cart_count'),
                        cartTotalSum = document.getElementById('cart-total-sum');
                    cartItemTotal.innerHTML = data.item_total;
                    cartTotalPrice.innerHTML = data.cart_total_price;
                    cartCount.innerHTML = data.cart_total_quantity;
                    cartTotalSum.innerHTML = parseFloat(data.cart_total_price).toFixed(2);
                }
            };
            xhr.open('GET', link, true);
            xhr.send();
        });
    });
});
