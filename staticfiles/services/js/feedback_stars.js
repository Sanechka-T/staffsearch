const stars = document.querySelectorAll('.star');
     stars.forEach(star => {
     star.addEventListener('click', function() {
     stars.forEach(s => s.classList.remove('selected'));
     for (let i = 0; i <= [...stars].indexOf(this); i++) {
     stars[i].classList.add('selected');
     }
  });
});