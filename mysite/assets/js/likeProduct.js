$(document).ready(function() {
    // Attach a click event handler to all elements with the class 'like_product_link'
    $('.like_product_link').each(function() {
        $(this).click(function(e) {
            e.preventDefault(); // Prevent the default behavior of the anchor tag

            // Get the product ID from the data attribute
            var productId = $(this).data('product-id');
            var endpoint = "/products/create_product_like/"+ productId +"/";

            // Send an AJAX request to create a new ProductLike object for the customer
            $.ajax({
                url: endpoint,
                method: 'POST',
                success: function(data) {
                    setTimeout(function() {
                        location.reload();
                    }, 500);
                    toastr.success(data.message, 'Success', {
                        closeButton: true,
                        positionClass: 'toast-top-center',
                        progressBar: true,
                        newestOnTop: true
                    });
                },
                error: function(xhr, status, error) {
                    // Handle any errors here
                    console.error(error);
                }
            });
        });
    });
});
