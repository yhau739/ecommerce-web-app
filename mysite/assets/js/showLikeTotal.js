$(document).ready(function () {
    // Function to update the Like badge
    function updateLikeBadge(totalItems) {
        console.log("Updating Like badge");
        $('#Like_badge').text(totalItems); // Update the badge text
    }

    // Make an AJAX request to fetch the total number of order items
    $.ajax({
        url: '/api/get_like_total/', //Write endpoint at view
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log("Received raw data:", data);
            // Update the UI with the total number of order items
            updateLikeBadge(data.no_distinct_items);
        },
        error: function () {
            // Handle errors if the AJAX request fails
            console.error('Error fetching Like total');
        }
    });
});
