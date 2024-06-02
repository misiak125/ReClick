window.onload = function() {
    var headerHeight = document.querySelector('nav').offsetHeight;
    var gamebox = document.getElementById('game-box');
    var windowHeight = window.innerHeight;
    var fullHeight = windowHeight - headerHeight;
    gamebox.style.height = fullHeight + 'px';
}