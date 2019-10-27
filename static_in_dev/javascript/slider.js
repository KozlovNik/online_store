window.addEventListener('DOMContentLoaded', () => {
    let inner = document.getElementsByClassName('inner')[0];
    let width = 1000;
    let bubbles = document.getElementsByClassName('bubble');

    function switchImg(index) {
        inner.style.left = -width * index + 'px';
    }

    let nextSlide = function () {
        let current = document.querySelector('.bubble__active');
        current.classList.remove('bubble__active');
        if (current.nextElementSibling) {
            current.nextElementSibling.classList.add('bubble__active');
            let elIndex = Array.from(bubbles).indexOf(current.nextElementSibling);
            switchImg(elIndex)
        } else {
            bubbles[0].classList.add('bubble__active');
            switchImg(0)
        }
    };

    let autoSlider = setInterval(nextSlide, 5000);

    for (let i = 0; i < bubbles.length; i++) {
        bubbles[i].addEventListener('click', function () {
            clearInterval(autoSlider);
            for (let y = 0; y < bubbles.length; y++) {
                bubbles[y].classList.remove('bubble__active');
            }
            bubbles[i].classList.add('bubble__active');
            let elIndex = Array.from(bubbles).indexOf(bubbles[i]);
            switchImg(elIndex);
            autoSlider = setInterval(nextSlide, 5000);
        });
    }
});
