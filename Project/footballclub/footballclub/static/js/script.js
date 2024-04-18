document.addEventListener("DOMContentLoaded", function () {
    const role = document.getElementById("role");
    const positionField = document.getElementById("positionField");
    const pos = document.getElementById("pos");

    role.addEventListener("change", function () {
        if (role.value === "player") {
            positionField.style.display = "block";
        } else {
            positionField.style.display = "none";
            pos.value = ""; // Clear the selected value
        }
    });

    // Initial state of the position field
    if (role.value === "player") {
        positionField.style.display = "block";
    } else {
        positionField.style.display = "none";
        pos.value = ""; // Clear the selected value
    }
});
