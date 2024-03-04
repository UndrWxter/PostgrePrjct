document.addEventListener('DOMContentLoaded', function () {
    const showMoreFiltersBtn = document.getElementById('showMoreFiltersBtn');
    const closeFiltersBtn = document.getElementById('closeFiltersBtn');
    const additionalFiltersContainer = document.getElementById('additionalFiltersContainer');
    const overlay = document.getElementById('additionalFiltersOverlay');

    showMoreFiltersBtn.addEventListener('click', function (event) {
        event.preventDefault();
        additionalFiltersContainer.classList.add('show');
        overlay.style.display = 'block';
    });

    closeFiltersBtn.addEventListener('click', function (event) {
        event.preventDefault();
        additionalFiltersContainer.classList.remove('show');
        overlay.style.display = 'none';
    });

    overlay.addEventListener('click', function (event) {
        if (event.target === overlay) {
            additionalFiltersContainer.classList.remove('show');
            overlay.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    var modal = document.getElementById("myModal");
    var btn = document.getElementById("myBtn");
    var span = document.getElementsByClassName("close")[0];

    btn.onclick = function() {
      modal.style.display = "block";
    }

    span.onclick = function() {
      modal.style.display = "none";
    }

    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
});



