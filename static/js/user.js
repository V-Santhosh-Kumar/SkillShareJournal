const form = document.getElementById("userForm")

form.addEventListener('submit', (e)=>{
    e.preventDefault()

    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    let id = document.getElementById("userId")?.value

    if (id) {
        fetch(`/user/update?id=${id}`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(resposne => resposne.json())
        .then(data =>{
            if (data.status == "success") {
                alert(data.message)
                location.reload()
            }
            else{
                
                if (data.message.includes("duplicate")) {
                    alert("This user name is already exists.")    
                }
                else{
                    alert(data.message)
                }
            }
        })
    }
    else{
        fetch('/user/new', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(resposne => resposne.json())
        .then(data =>{
            if (data.status == "success") {
                location.reload()
            }
            else{
                if (data.message.includes("duplicate")) {
                    alert("This user name is already exists.")    
                }
                else{
                    alert(data.message)
                }
            }
        })
    }
})


// let roleTable = document.getElementById("roleTable")

// let table = new DataTable(roleTable);


$(document).ready(function () {
    let table = $('#userTable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/user/getAll",
            "type": "GET",
            "dataSrc": function (json) {
                return json.data;
            },
        },
        "columns": [
            { "data": "username", "defaultContent": "N/A" },
            { "data": "role", "defaultContent": "N/A" },
            { "data": "email", "defaultContent": "N/A"},
            { "data": "phone", "defaultContent": "N/A"},
            { "data": "addedTime", "defaultContent": "N/A" },
            { "data": "updatedTime", "defaultContent": "N/A" },
            {
                "data": "id",
                "render": function (data) {
                    return `
                    <div class="d-flex">
                    <a class="dropdown-item edit-btn" href="javascript:void(0);" data-id="${data}">
                        <i class="bi bi-pencil me-1 text-dark"></i>
                    </a>
                    <a class="dropdown-item delete-btn" href="javascript:void(0);" data-id="${data}">
                        <i class="bi bi-trash me-1 text-danger"></i>
                    </a>
                    </div>
                `;
                },
                "orderable": false
            }
        ],
        "order": [[1, "asc"]],
        "paging": true,
        "searching": true,
        "autoWidth": false,
    });

    $('#userTable tbody').on('click', '.delete-btn', function () {
        let id = $(this).data('id');
        if(confirm('Are you sure you want to delete this inquiry?')){
            $.ajax({
                url: `/user/delete?id=${id}`,
                type: 'DELETE',
                success: function (response) {
                    if (response.status == "success") {
                        alert(response.message)
                        table.ajax.reload();
                    }
                    else {
                        throw response.message
                    }
                },
                error: function (error) {
                    showAlert('danger', error)
                }
            });
        }
    });
});


document.querySelector('table tbody').addEventListener("click", (event)=>{
    let edit_btn = event.target.closest('.edit-btn')

    if (edit_btn){
        let id = edit_btn.dataset.id
        console.log(id)

        fetch(`/user/getSpecific?id=${id}`)
        .then(resposne => resposne.json())
        .then(data =>{
            if (data.status == "success") {
                let user = data.data
                document.getElementById("editUser").value = data.data.name
                document.getElementById("editUsername").value = user.username
                document.getElementById("editPhone").value = user.phone
                document.getElementById("editEmail").value = user.email
                document.getElementById("editPassword").value = user.password
                document.getElementById("roleSelect").value = user.roleId
                document.getElementById("userId").value = user.id

                let modal = new bootstrap.Modal(document.getElementById("addUserModal"))
                modal.show()
            }
            else{
                alert(data.message)
            }
        })
    }
})


const addUserModal = document.getElementById('addUserModal')
addUserModal.addEventListener('shown.bs.modal', event => {
    fetch('/role/getAllNames')
    .then(resposne => resposne.json())
    .then(data =>{
        if (data.status == "success") {
            let roleSelect = document.getElementById("roleSelect")

            let roles = data.data

            roles.forEach(role => {
                let option = document.createElement("option")
                option.value = role.id
                option.textContent = role.name

                roleSelect.append(option)
            });
        }
        else{
            if (data.message.includes("duplicate")) {
                alert("This user name is already exists.")    
            }
            else{
                alert(data.message)
            }
        }
    })
})