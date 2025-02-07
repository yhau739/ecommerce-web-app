const addLinks = document.querySelectorAll('a.index-add-link');
// Loop through the selected elements and attach a click event listener
addLinks.forEach(link => {
    link.addEventListener('click', function (event) {
        // Prevent the default behavior of the link (e.g., navigating to a new page)
        event.preventDefault();

        // quantity preset to 1
        var quantity = 1;
        var productId = $(this).data('product-id');

        var endpoint = '/products/' + productId + '/add_to_cart/' + quantity + '/';

        // Send the AJAX POST request to the "add_to_cart" endpoint
        $.ajax({
            url: endpoint,
            type: 'POST',
            dataType: 'json', // Change the data type as needed
            success: function (response) {
                if (response.success) {
                    setTimeout(function() {
                        location.reload();
                    }, 500);
                    // Handle the success response from the server
                    toastr.success(response.message, 'Success', {
                        closeButton: true,
                        positionClass: 'toast-top-center',
                        progressBar: true,
                        newestOnTop: true
                    });
                    // refresh
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

const removeBtn = document.querySelectorAll('button.remove_btn');
// Loop through the selected elements and attach a click event listener
removeBtn.forEach(link => {
    link.addEventListener('click', function (event) {
        // quantity preset to 1
        var quantity = 1;
        var productId = $(this).data('product-id');

        var endpoint = '/products/' + productId + '/add_to_cart/' + quantity + '/';

        // Send the AJAX POST request to the "add_to_cart" endpoint
        $.ajax({
            url: endpoint,
            type: 'POST',
            dataType: 'json', // Change the data type as needed
            success: function (response) {
                if (response.success) {
                    setTimeout(function() {
                        location.reload();
                    }, 1000);
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