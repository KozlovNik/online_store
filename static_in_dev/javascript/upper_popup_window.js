window.addEventListener('DOMContentLoaded', () => {
    let closeButton = document.getElementsByClassName('upper-popup-window__close-button')[0],
        upperPopUpWindow = document.getElementsByClassName('upper-popup-window')[0],
        upperPopUpWindowHidden = document.getElementsByClassName('upper-popup-window-hidden')[0];
    closeButton.addEventListener('click', function () {
        upperPopUpWindow.style.display = 'none';
        upperPopUpWindowHidden.style.display = 'block';
    });
});

