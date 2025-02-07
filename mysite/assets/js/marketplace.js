const exclusiveCheckboxes = document.querySelectorAll('.exclusive-checkbox-price');
const applyBtn = document.getElementById('applyBtn');
const resetBtn = document.getElementById('resetBtn');
var resetEndpoint = "/api/reset_filtered_products/";

// Collect Criteria for filtering
var priceFilter = 'price-0';
var endpoint = "/api/get_filtered_products/";

exclusiveCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        // When a checkbox is checked, disable the other checkboxes
        if (this.checked) {
            // Update filter
            priceFilter = checkbox.id;
            // Uncheck other checkbox
            exclusiveCheckboxes.forEach(otherCheckbox => {
                if (otherCheckbox !== this) {
                    otherCheckbox.checked = false;
                    // otherCheckbox.disabled = true;
                }
            });
        } else {
            // When a checkbox is unchecked, re-enable all checkboxes
            priceFilter = 'price-0';
            exclusiveCheckboxes.forEach(otherCheckbox => {
                otherCheckbox.disabled = false;
            });
        }
    });
});

applyBtn.addEventListener('click', function () {
    console.log('submitted: ' + priceFilter);
    // Search Query
    var searchInput = document.getElementById("searchValue");
    var inputValue = searchInput.value;
    $.ajax({
        url: endpoint + priceFilter + '?search_keyword=' + inputValue,
        type: 'GET',
        dataType: 'json', // Change the data type as needed
        success: function (response) {
            // Update the UI to reflect fetched data
            $('#update-con').html(response.updated_product_html);
            $('#update-pagination').html(response.updated_pagination_html);


            toastr.success("Filters applied", 'Success', {
                closeButton: true,
                positionClass: 'toast-top-center',
                progressBar: true,
                timeOut: '1000',
                newestOnTop: true
            });
        },
        error: function (xhr, status, error) {
            // Handle errors here
            toastr.error('Error Filtering:', error, {
                closeButton: true,
                positionClass: 'toast-top-center',
                progressBar: true,
                timeOut: '1000',
                newestOnTop: true
            });
        }
    });
});
console.log('initial:' + priceFilter);

// Ajax call
resetBtn.addEventListener('click', function () {
    // Uncheck all existing checkbox
    exclusiveCheckboxes.forEach(otherCheckbox => {
        otherCheckbox.checked = false;
    });

    // Reset Values
    priceFilter = 'price-0';
    $("#searchValue").val("");

    // Make an AJAX request to the reset endpoint
    $.ajax({
        url: resetEndpoint,
        method: 'GET', // You can change the HTTP method as needed
        success: function (response) {
            // Update the UI with the template returned from the server
            $('#update-con').html(response.updated_product_html);
            $('#update-pagination').html(response.updated_pagination_html);
            console.log(response.updated_pagination_html);

            toastr.success("Filters reset!", 'Success', {
                closeButton: true,
                positionClass: 'toast-top-center',
                progressBar: true,
                timeOut: '1000',
                newestOnTop: true
            });
            const allPriceCheckbox = document.getElementById("price-0");
            allPriceCheckbox.checked = true;
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
});