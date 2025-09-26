fetch("/note/getAll")
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            function timeAgo(dateString) {
                let now = new Date();
                let noteDate = new Date(dateString);
                let diff = Math.floor((now - noteDate) / 1000); // in seconds

                if (diff < 60) return `${diff} sec ago`;
                if (diff < 3600) return `${Math.floor(diff / 60)} min ago`;
                if (diff < 86400) return `${Math.floor(diff / 3600)} hr ago`;
                if (diff < 2592000) return `${Math.floor(diff / 86400)} days ago`;
                return noteDate.toLocaleDateString(); // fallback full date
            }

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
                    <div class="note-card card shadow-sm">
                        <div class="d-flex h-100">
                            
                            <!-- Left Content -->
                            <div class="flex-grow-1 p-3 overflow-auto">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <small class="text-muted">${timeAgo(note.addedTime)}</small>
                                    <span class="badge px-2 py-1" style="background-color: #DD7D5B;">${note.tag}</span>
                                </div>


                                <div class="d-flex gap-2 mb-2 overflow-auto">
                                    ${imgs}
                                </div>

                                <h5 class="fw-bold">${note.title}</h5>
                                <p class="text-wrap text-break">${note.description}</p>

                                <!-- Comments Section -->
                                <div class="comments-section mt-3">
                                    <h6 class="fw-semibold">Comments</h6>
                                    <div class="comments-container">
                                        ${commentsHtml}
                                    </div>
                                </div>
                            </div>

                            <!-- Right Side Icons -->
                            <div class="icon-bar d-flex flex-column justify-content-between align-items-center p-2">
                                <div class="d-flex flex-column align-items-center gap-3">
                                    <a class="nav-link user-icon">
                                        <i class="bi bi-person fs-5"></i>
                                    </a>
                                    <a class="nav-link like-btn d-flex flex-column align-items-center" data-noteid="${note.id}">
                                        ${likeIcon}
                                    </a>
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
                                <a class="nav-link"><i class="bi bi-three-dots-vertical fs-4"></i></a>
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
    if (event.target.closest(".shareBtn")){ 
        const btn = event.target.closest(".shareBtn"); 
        const notesId = btn.getAttribute("data-noteid"); 
        const shareURL = `http://localhost:5000/note/${notesId}`; 
        console.log("Generated share URL:", shareURL); 
        const shareLinkInput = document.getElementById("shareLink"); 
        if (shareLinkInput) { shareLinkInput.value = shareURL; } 
        else { console.error('Share Link input not found!'); } 
    } 
});