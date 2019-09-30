let cartBtns = document.getElementsByClassName('add-to-cart');


for (i = 0; i < cartBtns.length; i++) {
    cartBtns[i].addEventListener('click', function (event) {
        let target = event.target;
        event.preventDefault();
        target.style.backgroundColor = 'yellow';
        console.log(target.getAttribute('data-slug'))
    });
}


