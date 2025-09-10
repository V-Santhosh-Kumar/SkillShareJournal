const form = document.getElementById("roleForm")

form.addEventListener('submit', (e)=>{
    e.preventDefault()

    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    fetch('/role/new', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(resposne => resposne.json())
    .then(data =>{
        console.log(data)
    })
})