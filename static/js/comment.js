const form = document.getElementById("commentForm")

form.addEventListener('submit', (e) => {
    e.preventDefault()

    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    fetch('/comment/new', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(resposne => resposne.json())
        .then(data => {
            if (data.status == "success") {
                alert(data.message)
                form.reset()


                const modalBody = document.querySelector(
                    "#commentModal .comments-container"
                );
                let newComment = `

                    <div class="card p-2">
                        <span><i class="bi bi-person-circle"></i> ${data.data.username}</span>
                        <p class="text-wrap text-break">${data.data.comment}</p>
                    </div>  
                `;
                modalBody.insertAdjacentHTML("beforeend", newComment);
            } else {
                alert(data.message);
            }
        })
        .catch((err) => console.error(err));
})

document.querySelector("#commentModal").addEventListener("shown.bs.modal", (event) => {
    event.stopPropagation()
    const noteId = document.getElementById("notesId").value;

    const modalBody = document.querySelector(
        "#commentModal .comments-container"
    );
    modalBody.innerHTML = "<p>Loading comments...</p>";

    if (noteId) {
        // Fetch comments for this note
        fetch(`/comment/getByNoteId/${noteId}`)
            .then((res) => res.json())
            .then((data) => {
                if (data.status === "success") {
                    modalBody.innerHTML = "";

                    if (data.data.length === 0) {
                        modalBody.innerHTML =
                            "<p class='text-muted'>No comments yet. Be the first to comment!</p>";
                    } else {
                        data.data.forEach((comment) => {
                            let commentCard = `
                                <div class="card p-2">
                                    <span><i class="bi bi-person-circle"></i> ${comment.username}</span>
                                    <p class="text-wrap text-break">${comment.comment}</p>
                                </div>
                            `;
                            modalBody.innerHTML += commentCard;
                        });
                    }
                } else {
                    modalBody.innerHTML =
                        "<p class='text-danger'>Failed to load comments.</p>";
                }
            })
            .catch((err) => {
                console.error(err);
                modalBody.innerHTML =
                    "<p class='text-danger'>Error loading comments.</p>";
            });
    }
})