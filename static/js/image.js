fetch("/note/getAll")
  .then(res => res.json())
  .then(data => {
    if (data.status == "success") {
      let notes = data.data;

      document.querySelector(".cardcontainer").innerHTML = "";

      notes.forEach((note, index) => {

        let carouselInner = ""
        note.image.forEach((image, index) => {
            carouselInner += `
              <div class="carousel-item ${index == 0? "active": ""}">
                <img src="${image}" class="img-thumbnail w-100">
              </div>
            `
        })

        let card = `
          <div class="card w-25" style="background-color: #fbdfc1;">
              <!-- Dynamic Image -->
              <div id="carouselExample${index}" class="carousel slide">
                <div class="carousel-inner">
                  ${carouselInner}
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample${index}" data-bs-slide="prev">
                  <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                  <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#carouselExample${index}" data-bs-slide="next">
                  <span class="carousel-control-next-icon" aria-hidden="true"></span>
                  <span class="visually-hidden">Next</span>
                </button>
              </div>
              
              <!-- Footer Section -->
              <div class="card px-3" style="background-color: #DD7D5B;">
                  <div class="d-flex justify-content-between align-items-center">
                      <div class="d-flex column-gap-2 align-items-center">
                          <a class="nav-link" aria-disabled="true">
                            <i class="bi bi-person-circle fs-4"></i>
                          </a>
                          <!-- Dynamic Title -->
                          <h5>${note.title}</h5>
                      </div>
                      <!-- Dynamic Link -->
                      <a href="${note.link}" target="_blank" class="nav-link" aria-disabled="true">
                          <i class="bi bi-link-45deg fs-4"></i>
                      </a>
                  </div>
              </div>
          </div>
        `;

        document.querySelector(".cardcontainer").innerHTML += card;
      });
    }
  });

