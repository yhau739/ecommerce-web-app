$(document).ready(function() {
    $("#checkoutBtn").click(function() {
        // Show the loader for 3 seconds
        $(".loader-con").addClass("active-loader-con");

        // Set a timer to remove the loader-active class after 3 seconds
        // setTimeout(function() {
        //     $(".loader-con").removeClass("active-loader-con");
        // }, 3000); // 3000 milliseconds = 3 seconds

    });
});