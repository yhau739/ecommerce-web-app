$(document).ready(function () {
    // Function to update the cart badge
    function updateCartBadge(totalItems) {
        console.log("Updating cart badge");
        $('#cart_badge').text(totalItems); // Update the badge text
    }

    // Make an AJAX request to fetch the total number of order items
    $.ajax({
        url: '/api/get_cart_total/', //Write endpoint at view
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log("Received raw data:", data);
            // Update the UI with the total number of order items
            updateCartBadge(data.no_distinct_items);
        },
        error: function () {
            // Handle errors if the AJAX request fails
            console.error('Error fetching cart total');
        }
    });
});
