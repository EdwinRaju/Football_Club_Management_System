const form = document.getElementById("Form");
const fnameInput = document.getElementById("fname");
const lnameInput = document.getElementById("lname");
const salaryInput = document.getElementById("salary");
const jerseyNumberInput = document.getElementById("jerseyNumber");
const emailInput = document.getElementById("email");
const emailError = document.getElementById("emailError");
const roleSelect = document.getElementById("role");
const passwordInput = document.getElementById("password");
const passwordError = document.getElementById("passwordError");
const imageInput = document.getElementById("image");
const fileTypeError = document.getElementById("fileTypeError");
const dob = document.getElementById("dob");
const contractStartDateInput = document.getElementById("cdate");

// Function to validate that only alphabets are entered in the first name and last name fields
function validateAlphabetsOnly(inputElement) {
    const inputValue = inputElement.value;
    const regex = /^[a-zA-Z]+$/;
    if (!regex.test(inputValue)) {
        inputElement.classList.add("error");
        inputElement.nextElementSibling.textContent = "Enter valid name";
        return false;
    } else {
        inputElement.classList.remove("error");
        inputElement.nextElementSibling.textContent = ""; // Clear error message
        return true;
    }
}

// Function to validate salary (numeric and between 10000 and 100000)
function validateSalary(inputElement) {
    const inputValue = inputElement.value;
    const regex = /^[0-9]+$/;
    if (!regex.test(inputValue) || inputValue < 10000 || inputValue > 100000) {
        inputElement.classList.add("error");
        inputElement.nextElementSibling.textContent = "Salary must be a number between 10000 and 100000.";
        return false;
    } else {
        inputElement.classList.remove("error");
        inputElement.nextElementSibling.textContent = ""; // Clear error message
        return true;
    }
}

// Function to validate date of birth
function validateDateOfBirth(inputElement) {
    const dobValue = inputElement.value;
    const currentDate = new Date();
    const selectedDate = new Date(dobValue);

    if (isNaN(selectedDate) || selectedDate > currentDate) {
        inputElement.classList.add("error");
        inputElement.nextElementSibling.textContent = "Enter a valid date of birth.";
        return false;
    } else {
        inputElement.classList.remove("error");
        inputElement.nextElementSibling.textContent = ""; // Clear error message
        return true;
    }
}

// Function to validate contract start date
function validateContractStartDate(inputElement) {
    const contractStartDateValue = inputElement.value;
    const currentDate = new Date();
    const selectedDate = new Date(contractStartDateValue);

    if (isNaN(selectedDate) || selectedDate < currentDate) {
        inputElement.classList.add("error");
        inputElement.nextElementSibling.textContent = "Enter a valid contract start date.";
        return false;
    } else {
        inputElement.classList.remove("error");
        inputElement.nextElementSibling.textContent = ""; // Clear error message
        return true;
    }
}

// Function to validate jersey number (between 1 and 99)
function validateJerseyNumber(inputElement) {
    const inputValue = parseInt(inputElement.value, 10);
    if (isNaN(inputValue) || inputValue < 1 || inputValue > 99) {
        inputElement.classList.add("error");
        inputElement.nextElementSibling.textContent = "Jersey number must be between 1 and 99.";
        return false;
    } else {
        inputElement.classList.remove("error");
        inputElement.nextElementSibling.textContent = ""; // Clear error message
        return true;
    }
}

// Function to validate password length
function validatePassword(inputElement) {
    const passwordValue = inputElement.value;

    // Check if the password contains at least 8 characters
    if (passwordValue.length < 8) {
        inputElement.classList.add("error");
        passwordError.textContent = "Password must be at least 8 characters long.";
        return false;
    }

    // Check if the password contains at least one uppercase letter
    if (!/[A-Z]/.test(passwordValue)) {
        inputElement.classList.add("error");
        passwordError.textContent = "Password must include at least one uppercase letter.";
        return false;
    }

    // Check if the password contains at least one lowercase letter
    if (!/[a-z]/.test(passwordValue)) {
        inputElement.classList.add("error");
        passwordError.textContent = "Password must include at least one lowercase letter.";
        return false;
    }

    // Check if the password contains at least one number
    if (!/\d/.test(passwordValue)) {
        inputElement.classList.add("error");
        passwordError.textContent = "Password must include at least one number.";
        return false;
    }

    // Check if the password contains at least one special character
    if (!/[$@$!%*?&]/.test(passwordValue)) {
        inputElement.classList.add("error");
        passwordError.textContent = "Password must include at least one special character ($, @, !, %, *, ?, or &).";
        return false;
    }

    // If all checks pass, remove error class and clear error message
    inputElement.classList.remove("error");
    passwordError.textContent = "";
    return true;
}

// Function to validate email
emailInput.addEventListener("input", () => {
    validateEmail(emailInput);
});

// Add a blur event listener to show the email error message after exiting the input field
emailInput.addEventListener("blur", () => {
    validateEmail(emailInput);
});
function validateEmail(inputElement) {
    const emailValue = inputElement.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailValue)) {
        inputElement.classList.add("error");
        emailError.textContent = "Invalid email format.";
        return false;
    } else {
        inputElement.classList.remove("error");
        emailError.textContent = ""; // Clear error message
        return true;
    }
}

// Function to validate file type
function validateImageFileType(inputElement) {
    const allowedExtensions = ["jpg", "jpeg", "png"];
    const fileName = inputElement.value.toLowerCase();
    const fileExtension = fileName.substring(fileName.lastIndexOf(".") + 1);

    if (!allowedExtensions.includes(fileExtension)) {
        inputElement.classList.add("error");
        fileTypeError.textContent = "Please select a JPG or PNG image.";
        return false;
    } else {
        inputElement.classList.remove("error");
        fileTypeError.textContent = ""; // Clear error message
        return true;
    }
}

// Add input event listeners for real-time validation
fnameInput.addEventListener("input", () => {
    validateAlphabetsOnly(fnameInput);
});

lnameInput.addEventListener("input", () => {
    validateAlphabetsOnly(lnameInput);
});

salaryInput.addEventListener("input", () => {
    validateSalary(salaryInput);
});

jerseyNumberInput.addEventListener("input", () => {
    validateJerseyNumber(jerseyNumberInput);
});

dob.addEventListener("input", () => {
    validateDateOfBirth(dob);
});

contractStartDateInput.addEventListener("input", () => {
    validateContractStartDate(contractStartDateInput);
});

emailInput.addEventListener("input", () => {
    validateEmail(emailInput);
});

passwordInput.addEventListener("input", () => {
    validatePassword(passwordInput);
});

// Add a change event listener to the role select input for jersey number field toggle
roleSelect.addEventListener("change", toggleJerseyNumberField);
function toggleJerseyNumberField() {
    if (roleSelect.value === "player") {
        jerseyNumberField.style.display = "block";
    } else {
        jerseyNumberField.style.display = "none";
    }
}

// Add a change event listener to the image input for file type validation
imageInput.addEventListener("change", () => {
    validateImageFileType(imageInput);
});

// Add a submit event listener to the form
Form.addEventListener("submit", (event) => {
    // Perform validation checks here
    const isFirstNameValid = validateAlphabetsOnly(fnameInput);
    const isLastNameValid = validateAlphabetsOnly(lnameInput);
    const isSalaryValid = validateSalary(salaryInput);
    const isDateOfBirthValid = validateDateOfBirth(dob);
    const isContractStartDateValid = validateContractStartDate(contractStartDateInput);
    const isEmailValid = validateEmail(emailInput);
    const isPasswordValid = validatePassword(passwordInput);

    // Check file type validation
    const isImageFileTypeValid = validateImageFileType(imageInput);
    const isJerseyNumberValid = roleSelect.value === "player" ? validateJerseyNumber(jerseyNumberInput) : true;
    
    // If any validation check fails, prevent form submission
    if (
        !isFirstNameValid ||
        !isLastNameValid ||
        !isSalaryValid ||
        !isDateOfBirthValid ||
        !isContractStartDateValid ||
        !isEmailValid ||
        !isPasswordValid ||
        !isImageFileTypeValid ||
        !isJerseyNumberValid
    ) {
        event.preventDefault();
    }
});