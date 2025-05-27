// static/js/theme-switcher.js

document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;

    // Function to apply theme based on preference
    const applyTheme = (theme) => {
        if (theme === 'dark') {
            body.classList.add('dark-mode');
        } else {
            body.classList.remove('dark-mode');
        }
    };

    // Check local storage for theme preference on page load
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        applyTheme(currentTheme);
    }

    // Event listener for the toggle button
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            let theme = 'light';
            if (body.classList.contains('dark-mode')) {
                theme = 'dark';
            }
            localStorage.setItem('theme', theme);
        });
    }
});
