const form = document.getElementById("roleForm")

form.addEventListener('submit', (e)=>{
    e.preventDefault()

    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    let id = document.getElementById("roleId")?.value

    if (id) {
        fetch(`/role/update?id=${id}`, {
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
                    alert("This role already exists.")    
                }
                else{
                    alert(data.message)
                }
            }
        })
    }
    else{
        fetch('/role/new', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(resposne => resposne.json())
        .then(data =>{
            if (data.status == "success") {
                form.reset()
            }
            else{
                
                if (data.message.includes("duplicate")) {
                    alert("This role already exists.")    
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
    let table = $('#roleTable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/role/getAll",
            "type": "GET",
            "dataSrc": function (json) {
                return json.data;
            },
        },
        "columns": [
            { "data": "name", "defaultContent": "N/A" },
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

    $('#roleTable tbody').on('click', '.delete-btn', function () {
        let id = $(this).data('id');
        if(confirm('Are you sure you want to delete this inquiry?')){
            $.ajax({
                url: `/role/delete?id=${id}`,
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

        fetch(`/role/getSpecific?id=${id}`)
        .then(resposne => resposne.json())
        .then(data =>{
            if (data.status == "success") {
                document.getElementById("editRole").value = data.data.name
                document.getElementById("roleId").value = data.data.id

                let modal = new bootstrap.Modal(document.getElementById("addUserModal"))
                modal.show()
            }
            else{
                alert(data.message)
            }
        })
    }
})