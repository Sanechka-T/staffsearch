let navigations = document.querySelectorAll('.navigation');

navigations.forEach(function(navigation) {
    navigation.onclick = function() {
        navigation.classList.toggle('active');
    }
});