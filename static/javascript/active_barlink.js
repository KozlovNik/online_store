document.addEventListener('DOMContentLoaded', function () {
    let linkPaths = document.getElementsByClassName('navbar__link'),
        documentPath = document.location.pathname;
    [].forEach.call(linkPaths,function (element) {
        if (documentPath.includes(element.getAttribute('href'))){
            element.classList.add('navbar__link--active');
        }
    });
});