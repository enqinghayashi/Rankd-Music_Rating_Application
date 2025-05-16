document.addEventListener('DOMContentLoaded', function () {
  // Flash message
  const flashContainer = document.querySelector('.flash-message-container');
  if (flashContainer && flashContainer.innerHTML.trim() !== '') {
    flashContainer.style.display = 'block';
    setTimeout(() => {
      flashContainer.style.display = 'none';
    }, 3000); 
  }
});