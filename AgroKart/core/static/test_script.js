document.addEventListener('DOMContentLoaded', function() {
    // Simulate editing user details
    const editedUserDetails = {
        name: "John Doe",
        phone: "1234567890",
        email: "john.doe@example.com",
        address: "123 Farm Lane"
    };
    localStorage.setItem('agrokart_edited_user_details', JSON.stringify(editedUserDetails));

    // Simulate generating the bill
    const orderId = 1; // Assuming order ID is 1 for testing
    window.open(`/generate-bill/${orderId}/`, '_blank');
});
