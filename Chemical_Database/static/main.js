$(document).ready(() => {
    $("#searchForm").on("submit", (event) => {
        if($("#searchTextbox").val().trim() == "") {
            event.preventDefault();
            $("#searchTextbox").val("").focus();
        }
    })
});