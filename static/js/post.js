let uploadedImages = [];

function addImages(event) {
    event.preventDefault(); // stop form reload
    const input = document.getElementById("imageUpload");
    const preview = document.getElementById("imagePreview");

    // Add new files to uploadedImages
    Array.from(input.files).forEach(file => {
        uploadedImages.push(file);

        const reader = new FileReader();
        reader.onload = function (e) {
            const img = document.createElement("img");
            img.name = "images[]"
            img.src = e.target.result;
            img.style.width = "120px";
            img.style.height = "120px";
            img.style.objectFit = "cover";
            img.style.borderRadius = "8px";
            preview.appendChild(img);
        };
        reader.readAsDataURL(file);
    });

    // reset input so same file can be chosen again
    input.value = "";
}

// Handle Form Submission
document.getElementById("postForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const code = document.getElementById("code").value;

    // Prepare form data
    const formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    formData.append("code", code);

    uploadedImages.forEach((file, i) => {
        formData.append("images[]", file);
    });


    const tagId = document.querySelector("#roleTag select").value;
    formData.append("tag", tagId);

    // Example: send to Flask endpoint
    fetch("/note/new", {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            console.log("Success:", data);
            if (data.status == "success") {
                alert("Post submitted!");
                document.getElementById("postForm").reset()
                
            }
        })
        .catch(err => {
            console.error("Error:", err);
        });
});

// your existing post.js code here...

// Populate tags dynamically
document.addEventListener("DOMContentLoaded", function () {
    fetch("/tags/getAll")
        .then(res => res.json())
        .then(data => {
            if (data && data.data) {
                let tagSelect = document.querySelector("#roleTag select");
                tagSelect.innerHTML = '<option value="" disabled selected>Select a tag</option>'; 

                data.data.forEach(tag => {
                    let option = document.createElement("option");
                    option.value = tag.id;   // use id for backend reference
                    option.textContent = tag.name;  // show name
                    tagSelect.appendChild(option);
                });
            }
        })
        .catch(err => console.error("Error fetching tags:", err));
});
