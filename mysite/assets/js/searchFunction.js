$(document).ready(function () {
    // Attach a click event handler to the element with id "ajaxClick"
    $("#searchBtn").click(function () {
        // Get the input element by its id
        var searchInput = document.getElementById("searchValue");
        // Get the value of the input element
        var inputValue = searchInput.value;
        var endpoint = '/products/marketplace' + '?search_keyword=' + inputValue

        // Perform your Ajax request here
        $.ajax({
            url: endpoint,
            method: 'POST', // or 'GET' or any other HTTP method
            data: { key: 'value' }, // Send any data you need
            success: function (response) {
                // Handle the Ajax response here
                console.log(response);
            },
            error: function (error) {
                // Handle any errors here
                console.error(error);
            }
        });
    });
});