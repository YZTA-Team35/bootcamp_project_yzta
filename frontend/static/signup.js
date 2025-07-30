document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signupForm');
    const messageDiv = document.getElementById('signupMessage');
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        messageDiv.textContent = '';
        const name = document.getElementById('name').value;
        const surname = document.getElementById('surname').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        try {
            const response = await fetch(`${CONFIG.BASE_URL}/auth/signup`, {

                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, surname, email, password })
            });
            const data = await response.json();
            if (response.ok) {
                messageDiv.style.color = 'lightgreen';
                messageDiv.textContent = 'Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz...';
                setTimeout(() => { window.location.href = '/signin'; }, 1200);
            } else {
                messageDiv.style.color = 'salmon';
                messageDiv.textContent = data.detail || 'Kayıt başarısız!';
            }
        } catch (err) {
            messageDiv.style.color = 'salmon';
            messageDiv.textContent = 'Sunucuya ulaşılamıyor!';
        }
    });
}); 