function showErrorToast(message) {
    toastr.error(message, 'Error', {
        closeButton: true,
        positionClass: 'toast-top-center',
        progressBar: true,
        timeOut: '1000',
        newestOnTop: true
    });
}

function showSuccessToast(message) {
    toastr.success(message, 'Success', {
        closeButton: true,
        positionClass: 'toast-top-center',
        progressBar: true,
        timeOut: '1000',
        newestOnTop: true
    });
}
