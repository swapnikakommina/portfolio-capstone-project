// API Gateway endpoint - will be updated after deployment
const API_ENDPOINT = 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/contact';

document.getElementById('contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const statusMessage = document.getElementById('statusMessage');
    const submitButton = e.target.querySelector('button[type="submit"]');
    
    // Collect form data
    const formData = {
        name: document.getElementById('name').value.trim(),
        email: document.getElementById('email').value.trim(),
        subject: document.getElementById('subject').value.trim(),
        message: document.getElementById('message').value.trim(),
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        source: 'portfolio-contact-form'
    };
    
    // Show loading state
    statusMessage.style.display = 'block';
    statusMessage.className = 'status-message loading';
    statusMessage.textContent = 'Sending message to AWS Lambda...';
    submitButton.disabled = true;
    submitButton.textContent = 'Sending...';
    
    try {
        console.log('Sending to:', API_ENDPOINT);
        console.log('Data:', formData);
        
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        console.log('Response status:', response.status);
        const responseData = await response.json();
        console.log('Response data:', responseData);
        
        if (response.ok) {
            statusMessage.className = 'status-message success';
            statusMessage.innerHTML = `
                <strong>✅ Message sent successfully!</strong><br>
                Stored in DynamoDB with ID: ${responseData.id || 'Generated'}<br>
                Lambda processed your request in real-time.
            `;
            document.getElementById('contactForm').reset();
        } else {
            throw new Error(responseData.error || 'Failed to send message');
        }
        
    } catch (error) {
        console.error('Error:', error);
        statusMessage.className = 'status-message error';
        statusMessage.innerHTML = `
            <strong>❌ Error sending message</strong><br>
            ${error.message}<br>
            Please check console for details or try again.
        `;
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Send Message via Lambda';
    }
});

// Add some visual feedback
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.transform = 'scale(1.02)';
        });
        input.addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
        });
    });
});