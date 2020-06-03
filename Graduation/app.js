document.querySelectorAll('.drag-area').forEach(element => {
    element.addEventListener('click', () => {
        element.parentNode.classList.toggle('closed');
    });
});