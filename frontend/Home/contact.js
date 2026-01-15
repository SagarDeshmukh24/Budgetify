// contact.js - Contact Form Handler for Budgetwala

/**
 * CSRF helper function for Django
 * Retrieves the CSRF token from cookies
 */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/**
 * Initialize contact form when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('contactForm');

  if (!form) {
    console.error('Contact form not found');
    return;
  }

  form.addEventListener('submit', async function(e) {
    e.preventDefault();

    // Collect form data
    const formData = {
      name: form.name.value,
      email: form.email.value,
      message: form.message.value
    };

    // Basic validation
    if (!formData.name || !formData.email || !formData.message) {
      alert('Please fill in all fields');
      return;
    }

    try {
      // Send POST request to Django backend
      const response = await fetch("http://127.0.0.1:8000/contact/", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
      });

      const result = await response.json();

      if (response.ok) {
        alert('Message sent successfully!');
        form.reset();
      } else {
        alert('Error: ' + (result.error || 'Something went wrong'));
      }
    } catch (err) {
      console.error('Server error:', err);
      alert('Server error: ' + err.message);
    }
  });
});