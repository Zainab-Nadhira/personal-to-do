document.addEventListener("DOMContentLoaded", function() {
    const toggle = document.getElementById("toggle-theme");
    const modeLabel = document.getElementById("mode-label");

    // Load saved mode from localStorage
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
        toggle.checked = true;
        modeLabel.textContent = "Dark Mode";
    }

    toggle.addEventListener("change", function() {
        document.body.classList.toggle("dark-mode");
        if (document.body.classList.contains("dark-mode")) {
            modeLabel.textContent = "Dark Mode";
            localStorage.setItem('darkMode','true');
        } else {
            modeLabel.textContent = "Light Mode";
            localStorage.setItem('darkMode','false');
        }
    });
});
