document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const messageDiv = document.getElementById('loginMessage');
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        messageDiv.textContent = '';
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        try {
            const response = await fetch(`${CONFIG.BASE_URL}/auth/login`, {

                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await response.json();
            if (response.ok && data.access_token) {
                localStorage.setItem('access_token', data.access_token);
                messageDiv.style.color = 'lightgreen';
                messageDiv.textContent = 'Başarıyla giriş yapıldı, yönlendiriliyorsunuz...';
                // Başarılı giriş sonrası kullanıcıyı sohbet sayfasına (statik .html) yönlendir
                setTimeout(() => { window.location.href = 'chat.html'; }, 1000);
            } else {
                messageDiv.style.color = 'salmon';
                messageDiv.textContent = data.detail || 'Giriş başarısız!';
            }
        } catch (err) {
            messageDiv.style.color = 'salmon';
            messageDiv.textContent = 'Sunucuya ulaşılamıyor!';
        }
    });
}); 