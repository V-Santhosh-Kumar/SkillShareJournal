fetch("/note/getAll")
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            let notes = data.data;

            document.querySelector(".cardcontainer").innerHTML = "";

            notes.forEach(note => {
                let imgs = "";
                note.image.forEach(image => {
                    imgs += `<img src="${image}" class="img-thumbnail w-25">`;
                });

                let bookmarkIcon = note.isSaved
                    ? `<i class="bi bi-bookmark-fill text-dark fs-4"></i>`
                    : `<i class="bi bi-bookmark fs-4"></i>`;

                let likeIcon = note.isLiked
                    ? `<i class="bi bi-heart-fill text-danger fs-4"></i> <span style="margin-top: -8px;font-size: 11px;"> ${note.likeCount} </span>`
                    : `<i class="bi bi-heart fs-4"></i> <span style="margin-top: -8px;font-size: 11px;"> ${note.likeCount} </span>`;

                // ✅ Build comments section
                let commentsHtml = "";
                if (note.comments && note.comments.length > 0) {
                    note.comments.forEach(c => {
                        commentsHtml += `
                            <div class="card w-100 p-2 mb-2">
                                <span><i class="bi bi-person-circle"></i> ${c.user || "Anonymous"}</span>
                                <p class="text-wrap text-break">${c.comment}</p>
                            </div>
                        `;
                    });
                } else {
                    commentsHtml = `<p class="text-muted">No comments yet</p>`;
                }

                let card = `
                <div class="container mt-5" style="flex:1 0 35%; height: 50vh !important; width: 25% !important;">
                    <div class="d-flex justify-content-between rounded-3"
                        style=" color: black; background-color: #fbdfc1 ;">
                        <div class="col-md-2 w-75 p-3" style="overflow-y: auto; scrollbar-width: none;">
                            <div class="row d-flex justify-content-center align-items-center">
                                <div class="col">2hr ago</div>
                                <span class="badge w-25 vh-25  px-1" style="background-color: #DD7D5B ;">${note.tag}</span>
                            </div>
                            <div class="d-flex column-gap-2 my-3" style="width: 100%;overflow-x: auto;">  
                                ${imgs}
                            </div>
                            <div class="row" style="border-bottom: 1px solid white;">
                                <h5>${note.title}</h5>
                                <p class="text-wrap text-break">${note.description}</p>
                            </div>

                            <!-- ✅ Comments Section -->
                            <div class="comments-section mt-2">
                                <h6>Comments</h6>
                                <div class="d-flex gap-2 justify-content-between">
                                ${commentsHtml}
                                </div>
                            </div>
                        </div>

                        <!-- Right Side Icons -->
                        <div class="col-md-2 p-2 rounded-3 d-flex flex-column justify-content-between align-items-center"
                            style="background-color: #DD7D5B;">
                            <div class="d-flex flex-column align-items-center row-gap-2">
                                <a class="nav-link" style="border: 2px solid black; border-radius: 100px; width: 30px; height: 30px; 
                                    display: flex; align-items: center; justify-content: center; scale: 0.9;">
                                    <i class="bi bi-person fs-5"></i>
                                </a>
                                <a class="nav-link like-btn d-flex flex-column align-items-center" data-noteid="${note.id}"> ${likeIcon}</a>

                                <a class="nav-link commentBtn" data-noteid="${note.id}" data-bs-toggle="modal" data-bs-target="#commentModal">
                                    <i class="bi bi-chat-left-text fs-4"></i>
                                </a>

                                <a class="nav-link shareBtn" data-noteid="${note.id}" data-bs-toggle="modal" data-bs-target="#shareModal">
                                    <i class="bi bi-send fs-4"></i>
                                </a>

                                <a class="nav-link bookmark-btn" data-noteid="${note.id}">
                                    ${bookmarkIcon}
                                </a>
                            </div>
                            <div>
                                <a class="nav-link"><i class="bi bi-three-dots-vertical fs-4"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
                `;

                document.querySelector(".cardcontainer").innerHTML += card;
            });


            // Attach click events to all bookmark buttons
            document.querySelectorAll(".bookmark-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    const notesId = btn.getAttribute("data-noteid");
                    const userId = "YOUR_USER_ID_HERE"; // Replace this with logged-in userId


                    const icon = btn.querySelector("i");


                    fetch("/savedNotes/toggle", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ userId, notesId })
                    })
                        .then(res => res.json())
                        .then(resp => {
                            if (resp.status === "success") {
                                if (resp.action === "saved") {
                                    icon.classList.remove("bi-bookmark");
                                    icon.classList.add("bi-bookmark-fill", "text-dark");
                                } else if (resp.action === "unsaved") {
                                    icon.classList.remove("bi-bookmark-fill", "text-dark");
                                    icon.classList.add("bi-bookmark");
                                }
                            } else {
                                alert("Error: " + resp.message);
                            }
                        })
                        .catch(err => console.error(err));
                });
            });

            // Attach click events to all like buttons
            document.querySelectorAll(".like-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    const notesId = btn.getAttribute("data-noteid");
                    const icon = btn.querySelector("i");

                    fetch("/like/toggle", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ notesId })
                    })
                        .then(res => res.json())
                        .then(resp => {
                            if (resp.status === "success") {
                                if (resp.action === "liked") {
                                    icon.classList.remove("bi-heart");
                                    icon.classList.add("bi-heart-fill", "text-danger");
                                } else if (resp.action === "unliked") {
                                    icon.classList.remove("bi-heart-fill", "text-danger");
                                    icon.classList.add("bi-heart");
                                }
                            } else {
                                alert("Error: " + resp.message);
                            }
                        })
                        .catch(err => console.error(err));
                });
            });

            document.querySelectorAll(".commentBtn").forEach(commentBtn => {
                commentBtn.addEventListener("click", () => {
                    document.getElementById("notesId").value = commentBtn.getAttribute("data-noteid")
                })
            })
        }
    });


document.getElementById("copyBtn").addEventListener("click", () => {
    const input = document.getElementById("shareLink");

    input.select();
    input.setSelectionRange(0, 99999); // for mobile devices

    navigator.clipboard.writeText(input.value)
        .then(() => {
            // Optional: give user feedback
            alert("Copied: " + input.value);
        })
        .catch(err => {
            console.error("Failed to copy: ", err);
        });
});

document.addEventListener("click", (event) => {
    if (event.target.closest(".shareBtn")) {
        const btn = event.target.closest(".shareBtn");
        const notesId = btn.getAttribute("data-noteid");

        const shareURL = `http://localhost:5000/note/getSpecific?id=${notesId}`;
        console.log("Generated share URL:", shareURL);

        const shareLinkInput = document.getElementById("shareLink");
        if (shareLinkInput) {
            shareLinkInput.value = shareURL;
        } else {
            console.error('Share Link input not found!');
        }
    }
});
    