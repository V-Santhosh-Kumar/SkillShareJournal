
fetch("/note/getAll")
.then(res => res.json())
.then(data =>{
    if (data.status === "success") {
        let notes = data.data

        document.querySelector(".cardcontainer").innerHTML = ""

        notes.forEach(note => {
            let imgs = ""
            note.image.forEach(image => {
                imgs += `<img src="${image}" class="img-thumbnail w-25">`
            })

            let card = `
                <div class="container mt-5" style="flex:1 0 35%; height: 50vh !important; width: 25% !important;">
                    <div class="d-flex justify-content-between rounded-3"
                        style=" color: black; background-color: #fbdfc1 ;">
                        <div class="col-md-2 w-75 p-3" style="overflow-y: auto; scrollbar-width: none;">
                            <div class="row d-flex  justify-content-center align-items-center">
                                <div class="col">
                                    2hr ago
                                </div>
                                <span class="badge w-25 vh-25  px-1" style="background-color: #DD7D5B ;">Python/var</span>
                            </div>
                            <div class="d-flex column-gap-2 my-3" style="width: 100%;overflow-x: auto;">  
                                ${imgs}
                            </div>
                            <div class="row" style="border-bottom: 1px solid white;">
                                <h5>${note.title}</h5>
                                <p class="text-wrap text-break">${note.description}</p>
                            </div>
                            <div class="d-flex justify-content-between p-2 column-gap-1 vh-25">
                                <div class="card w-50 p-2">
                                    <span><i class="bi bi-person-circle"></i> Username</span>
                                    <p class="text-wrap text-break">xrtcfgvybhujnkdxcfygvhubj</p>

                                </div>
                                <div class="card w-50 p-2">
                                    <span><i class="bi bi-person-circle"></i> Username</span>
                                    <p class="text-wrap text-break">xrtcfgvybhujnkdxcfygvhubj</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-2 p-2 rounded-3" style="display: flex;
                        flex-direction: column;
                        height: -webkit-fill-available;
                        justify-content: space-between;
                        align-items: center; background-color: #DD7D5B ;">
                            <div style="    display: flex;
                        flex-direction: column;
                        height: -webkit-fill-available;
                        row-gap: 10px;
                        align-items: center;">
                                <a class="nav-link"
                                    style="border: 2px solid black; border-radius: 100px; width: 30px; height: 30px; text-align: center; display: flex; align-items: center; justify-content: center; scale: 0.9;"
                                    aria-disabled="true"><i class="bi bi-person fs-5"></i></a>
                                <a class="nav-link" aria-disabled="true"><i class="bi bi-heart fs-4"></i>
                                    <a class="nav-link" aria-disabled="true"><i class="bi bi-chat-left-text fs-4"></i></a>
                                    <a class="nav-link" aria-disabled="true"><i class="bi bi-send fs-4"></i></a>
                                    <a class="nav-link" aria-disabled="true"><i class="bi bi-bookmark fs-4"></i></a>
                            </div>
                            <div>
                                <a class="nav-link" aria-disabled="true"><i class="bi bi-three-dots-vertical fs-4"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
            `


            document.querySelector(".cardcontainer").innerHTML += card
        });
    }
})  