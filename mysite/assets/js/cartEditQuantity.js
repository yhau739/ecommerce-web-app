// Delegate Events for dynamically generated elements
$(document).ready(function () {
    $('#cart_item_con').on('click', '#addQuantityBtn', function () {
        // Perform actions based on each child addbtn element inside cart_item_con
        // Find the parent element
        var productElement = $(this).closest('.parent_con');
        // Get Quantity & data element
        var quantityInput = productElement.find('#quantityInput');
        // Extract Values
        var quantity = quantityInput.val();
        quantity = parseInt(quantity, 10) + 1;
        var productId = quantityInput.data('product-id');
        console.log("Quantity:" + quantity);
        console.log("ProductID:" + productId);
        toastr.info('Adding More!', 'Success', {
            closeButton: true,
            positionClass: 'toast-top-center',
            progressBar: true,
            newestOnTop: true,
            timeOut: 1000,
            onShown: function (toast) {
                updateQuantityOnServer(quantity, productId, true);
            },
        });
    });

    $('#cart_item_con').on('click', '#minusQuantityBtn', function () {
        // Perform actions based on each child addbtn element inside cart_item_con
        // Find the parent element
        var productElement = $(this).closest('.parent_con');
        // Get Quantity & data element
        var quantityInput = productElement.find('#quantityInput');
        // Extract Values
        var quantity = quantityInput.val();
        quantity = parseInt(quantity, 10);
        quantity = quantity == 1 ? 1 : quantity - 1;
        var productId = quantityInput.data('product-id');
        console.log("Quantity:" + quantity);
        console.log("ProductID:" + productId);
        toastr.info('Reducing Some!', 'Success', {
            closeButton: true,
            positionClass: 'toast-top-center',
            progressBar: true,
            newestOnTop: true,
            timeOut: 1000,
            onShown: function (toast) {
                updateQuantityOnServer(quantity, productId, false);
            },
        });
    });

    // Function to update quantity on the server
    function updateQuantityOnServer(quantity, productId, add) {
        // Because UI is update at the end, and value is extracted from UI
        var quantity = quantity;
        var productId = productId;

        // This is for the update UI id, its dynamically generated
        var item_total_html = '#order_item_total_' + productId;
        var endpoint = '/products/' + productId + '/edit_cart/' + quantity + '/';
        console.log(endpoint);

        // Send the AJAX POST request to update the quantity on the server
        $.ajax({
            url: endpoint,
            type: 'POST',
            dataType: 'json', // Change the data type as needed
            success: function (response) {
                if (response.success) {
                    // Handle the success response from the server
                    console.log("Successfully update")

                    // Update UI
                    // update Dynamically
                    $(item_total_html).text('$ ' + response.item_total);
                    var order_total = '$ ' + parseFloat(response.order_total).toFixed(2);
                    var order_final = '$ ' + (parseFloat(response.order_total) + 10).toFixed(2);
                    // Static updates
                    $('#order_total_before').text(order_total);
                    $('#order_total_after').text(order_final);
                    // Number Update
                    if (add) {
                        updateQuantityNumber(productId, true);
                    } else {
                        updateQuantityNumber(productId, false);
                    }
                } else {
                    toastr.error(response.items, 'Error', {
                        closeButton: true,
                        positionClass: 'toast-top-center',
                        progressBar: true,
                        newestOnTop: true
                    });
                    if (!add){
                        updateQuantityNumber(productId, false);
                    }
                }
            },
            error: function (xhr, status, error) {
                // Handle errors here
                toastr.error('Error updating quantity:', error, {
                    closeButton: true,
                    positionClass: 'toast-top-center',
                    progressBar: true,
                    newestOnTop: true
                });
            }
        });
    }

    function updateQuantityNumber(productId, isAdd) {
        // Find the input element with the matching data-product-id
        var inputField = $('input[data-product-id="' + productId + '"]');

        // Retrieve the current value of the input
        var oldValue = parseFloat(inputField.val());

        // Calculate the new value based on the increment or decrement direction
        var newVal = isAdd ? oldValue + 1 : (oldValue > 1 ? oldValue - 1 : 1);

        // Update the input field's value with the new value
        inputField.val(newVal);
    }

});
