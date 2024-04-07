$(document).ready(() => {
    $("#addForm").on("submit", (event) => {
        if($("#searchTextbox").val().trim() == "") {
            event.preventDefault();
            const selectedElement = $("#element").val()
            $("#element").val('1')

            const quantity = $("#quantity").val()
            $("#quantity").val("")

            const lab = $("#lab").val()
            $("#lab").val("")

            const notes = $("#notes").val()
            $("#notes").val("None")

            fetch("/add", {method: "POST", body: JSON.stringify({element: selectedElement, quantity: quantity, lab: lab, notes: notes}), headers: {'Content-Type': 'application/json'}}).then((res) => {
                res.json().then((data) => {
                    if(data.error) {
                        const errorElement = document.getElementById("error-msg")
                        errorElement.style.opacity = 1
                        errorElement.style.display = 'block'
                        errorElement.innerHTML = data.error
                        setTimeout(() => {
                            errorElement.style.opacity = 0
                            setTimeout(() => {
                                errorElement.style.display = 'None'
                            }, 500)
                        }, 1500)
                    }
                    else if(data.id) {
                        const successElement = document.getElementById("success-msg")
                        successElement.style.display = 'block'
                        document.getElementById("viewer").setAttribute("href", `/view?id=${data.id}`)
                    }
                })
            })
        }
    })
});