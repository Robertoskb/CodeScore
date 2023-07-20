const navBar = document.querySelector("nav"),
       menuBtns = document.querySelectorAll(".menu-icon"),
       overlay = document.querySelector(".overlay");
     menuBtns.forEach((menuBtn) => {
       menuBtn.addEventListener("click", () => {
         navBar.classList.toggle("open");
       });
     });
     overlay.addEventListener("click", () => {
       navBar.classList.remove("open");
     });

     document.addEventListener('DOMContentLoaded', function() {
      var menuToggle = document.getElementsByClassName('menu-toggle');
      
      Array.from(menuToggle).forEach(function(element) {
        element.addEventListener('click', function() {
          this.classList.toggle('active');
        });
      });
    });

(() => {
  const forms = document.querySelectorAll('.delete-form');

  for (const form of forms){
    if (form) {
      form.addEventListener('submit', function(event) {
        event.preventDefault();

        const confirmed = confirm('Você tem certeza?');

        if (confirmed) {
          form.submit();
        }
      });
    }
  }

})();