// JavaScript source code

// CAREER COMPASS - JAVASCRIPT

// Confirm before deleting a career plan
function confirmDelete() {
    return confirm(
        "Are you sure you want to delete this career plan?"
    );
}

// Display a welcome message
function showWelcome() {
    alert("Welcome to Career Compass!");
}

// Validate form inputs
function validateForm(form) {
    if (!form.checkValidity()) {
        form.reportValidity();
        return false;
    }

    return true;
}

// Show or hide password
function togglePassword(inputId) {
    const passwordField = document.getElementById(inputId);

    if (!passwordField) {
        return;
    }

    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}
