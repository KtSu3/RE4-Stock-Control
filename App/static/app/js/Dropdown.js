document.addEventListener('DOMContentLoaded', () => {
    const dropdown = document.querySelector('.dropbtn');
    const dropdownContent = document.querySelector('.dropdown-content');

    dropdown.addEventListener('click', () => {
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    });

    window.addEventListener('click', (event) => {
        if (!event.target.matches('.dropbtn')) {
            if (dropdownContent.style.display === 'block') {
                dropdownContent.style.display = 'none';
            }
        }
    });
});