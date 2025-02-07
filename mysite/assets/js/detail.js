// JavaScript
$(document).ready(function () {
    // Attach a click event listener to the "Add To Cart" button
    $('#addToCartBtn').on('click', function () {
        // Get the value from the quantity input field
        var quantity = $('#quantityInput').val();
        var productId = $(this).data('product-id');

        var endpoint ='/products/' + productId + '/add_to_cart/' + quantity + '/';
        console.log(endpoint)

        // Send the AJAX POST request to the "add_to_cart" endpoint
        $.ajax({
            url: endpoint,
            type: 'POST',
            dataType: 'json', // Change the data type as needed
            success: function (response) {
                if (response.success) {
                    // Handle the success response from the server
                    toastr.success(response.message, 'Success', {
                        closeButton: true,
                        positionClass: 'toast-top-center',
                        progressBar: true,
                        newestOnTop: true
                    });
                    // can update the UI
                } else {
                    toastr.error(response.items, 'Error', {
                        closeButton: true,
                        positionClass: 'toast-top-center',
                        progressBar: true,
                        newestOnTop: true
                    });
                }
            },
            error: function (xhr, status, error) {
                // Handle errors here
                toastr.error("There is something wrong with the server! Please contact the admin", 'Error', {
                    closeButton: true,
                    positionClass: 'toast-top-center',
                    progressBar: true,
                    newestOnTop: true
                });
            }
        });
    });
});
