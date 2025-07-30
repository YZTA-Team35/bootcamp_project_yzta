// AI yanıt
const aiResponses = [
  "Bu mesaj örnek olarak atılıyor"]; // API buraya gelmeli

// variables
let messageInput, messagesContainer, sendButton, welcomeSection;

// sayfa yüklendiğinde çalışanlar
window.addEventListener('load', function() {
  console.log('Page loaded, initializing...');
  
  // html js entegrasyonu
  messageInput = document.getElementById("messageInput");
  messagesContainer = document.getElementById("messagesContainer");
  sendButton = document.getElementById("sendButton");
  welcomeSection = document.getElementById("welcomeSection");
  
  // hata check
  if (!messageInput || !messagesContainer || !sendButton || !welcomeSection) {
    console.error('Required elements not found!');
    return;}
  
  console.log('Elements found, setting up events...');
  
  // send button state
  sendButton.disabled = true;
  
  // Enter ile mesaj gönder shift+enter ile satır atla
  messageInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage(); } });

  // Input girilmezse çalışmaz
  messageInput.addEventListener("input", function() {
    sendButton.disabled = messageInput.value.trim() === ""; });
  
  // LOGIN KONTROLÜ
  const token = localStorage.getItem('access_token');
      if (!token) {
        // Token yoksa kullanıcıyı statik giriş sayfasına yönlendir
        window.location.href = 'signin.html';
        return;
      }

  // LOGOUT
  const logoutButton = document.getElementById('logoutButton');
  if (logoutButton) {
    logoutButton.onclick = function() {
          localStorage.removeItem('access_token');
          // Çıkış sonrası statik giriş sayfasına yönlendir
          window.location.href = 'signin.html';
    };
  }

  // GÖRSEL YÜKLEME & TAHMİN
  const imageForm = document.getElementById('imageUploadForm');
  const imageInput = document.getElementById('imageInput');
  const predictMessage = document.getElementById('predictMessage');
  if (imageForm && imageInput && predictMessage) {
    imageForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      predictMessage.textContent = '';
      if (!imageInput.files || imageInput.files.length === 0) {
        predictMessage.style.color = 'salmon';
        predictMessage.textContent = 'Lütfen bir fotoğraf seçin!';
        return;
      }
      const formData = new FormData();
      formData.append('file', imageInput.files[0]);
      try {
        predictMessage.style.color = '#fff';
        predictMessage.textContent = 'Yükleniyor, lütfen bekleyin...';
        const response = await fetch(`${CONFIG.BASE_URL}/images/predict`, {

          method: 'POST',
          headers: { 'Authorization': 'Bearer ' + token },
          body: formData
        });
        const data = await response.json();
        if (response.ok) {
          predictMessage.style.color = 'lightgreen';
          predictMessage.textContent = 'Tahmin: ' + (data.result || JSON.stringify(data));
        } else {
          predictMessage.style.color = 'salmon';
          predictMessage.textContent = data.detail || 'Tahmin başarısız!';
        }
      } catch (err) {
        predictMessage.style.color = 'salmon';
        predictMessage.textContent = 'Sunucuya ulaşılamıyor!';
      }
    });
  }

  // Mesaj inputuna tıklanınca dosya seçici aç
  if (messageInput) {
    messageInput.addEventListener('click', function(e) {
      // Sadece ilk tıklamada dosya seçici aç
      if (messageInput.type === 'text') {
        e.preventDefault();
        // Geçici bir file input oluştur
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.style.display = 'none';
        document.body.appendChild(fileInput);
        fileInput.click();
        fileInput.addEventListener('change', async function() {
          if (fileInput.files && fileInput.files.length > 0) {
            const file = fileInput.files[0];
            await sendImageToModel(file);
          }
          document.body.removeChild(fileInput);
        });
      }
    });
  }

  // Görseli modele gönder
  async function sendImageToModel(file) {
    const predictMessage = document.getElementById('predictMessage');
    const token = localStorage.getItem('access_token');
        if (!token) {
          // Token yoksa kullanıcıyı statik giriş sayfasına yönlendir
          window.location.href = 'signin.html';
          return;
        }
    const formData = new FormData();
    formData.append('file', file);
    try {
      predictMessage.style.color = '#fff';
      predictMessage.textContent = 'Yükleniyor, lütfen bekleyin...';
      // Kullanıcı görsel yüklediğinde user mesajı olarak ekle
      addMessage('Bir görsel gönderdiniz.', 'user');
      showTyping();
      const response = await fetch(`${CONFIG.BASE_URL}/images/predict`, {

        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token },
        body: formData
      });
      const data = await response.json();
      hideTyping();
      predictMessage.textContent = '';
      if (response.ok) {
        // Modelden dönen json'u düzgün Türkçe metne çevir
        let botMsg = '';
        if (data.prediction && typeof data.prediction === 'object') {
          const pred = data.prediction;
          if (pred.class) {
            botMsg += `Hastalık: ${pred.class}\n`;
          }
          if (pred.confidence !== undefined) {
            botMsg += `Olasılık: %${Number(pred.confidence).toFixed(2)}\n`;
          }
          if (pred.explanation) {
            botMsg += `Açıklama: ${pred.explanation}\n`;
          }
          // Diğer alanlar
          Object.entries(pred).forEach(([k, v]) => {
            if (!["class","confidence","explanation"].includes(k)) {
              botMsg += `${k}: ${v}\n`;
            }
          });
          botMsg = botMsg.trim();
          if (!botMsg) botMsg = 'Modelden anlamlı bir sonuç alınamadı.';
        } else if (data.result) {
          botMsg = 'Tahmin: ' + data.result;
        } else if (typeof data === 'object') {
          // Sık karşılaşılan anahtarlar için özel metin
          if (data.disease_name || data.disease || data.label) {
            botMsg += `Hastalık: ${data.disease_name || data.disease || data.label}\n`;
          }
          if (data.probability || data.confidence) {
            botMsg += `Olasılık: %${((data.probability || data.confidence) * 100).toFixed(1)}\n`;
          }
          if (data.explanation) {
            botMsg += `Açıklama: ${data.explanation}\n`;
          }
          // Diğer alanları ekle
          Object.entries(data).forEach(([k, v]) => {
            if (!["result","disease_name","disease","label","probability","confidence","explanation"].includes(k)) {
              botMsg += `${k}: ${v}\n`;
            }
          });
          botMsg = botMsg.trim();
          if (!botMsg) botMsg = 'Modelden anlamlı bir sonuç alınamadı.';
        } else {
          botMsg = JSON.stringify(data);
        }
        addMessage(botMsg, 'bot');
      } else {
        addMessage(data.detail || 'Tahmin başarısız!', 'bot');
      }
    } catch (err) {
      hideTyping();
      addMessage('Sunucuya ulaşılamıyor!', 'bot');
    }
  }

  console.log('Initialization complete!');});

function sendMessage() { // mesaj gönderme
  console.log('Send message called');
  
  if (!messageInput || !messagesContainer || !sendButton || !welcomeSection) {
    console.error('Elements not initialized');
    return;}
  
  const text = messageInput.value.trim(); // girdi var mı 
  if (!text) return;

  console.log('Sending message:', text);

  // ilk mesajdan sonra giriş kısmını gizle
  welcomeSection.classList.add("hidden");

  // kullanıcı mesajını ekle
  addMessage(text, "user");
  messageInput.value = "";
  sendButton.disabled = true;

  // yazıyor anımasynu 
  showTyping();

  // bekletme ve cevap
  setTimeout(() => {
    hideTyping();
    const randomResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)];
    addMessage(randomResponse, "bot");}, 1500 + Math.random() * 1000);}

function addMessage(text, sender) { // mesaj ekleme
  if (!messagesContainer) return;
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;
  messageDiv.textContent = text;
  messagesContainer.appendChild(messageDiv);
  scrollToBottom();}

function showTyping() { // yazıyor animasyonu
  if (!messagesContainer) return;
  
  const typingDiv = document.createElement("div"); 
  typingDiv.className = "message typing";
  typingDiv.id = "typingIndicator";
  typingDiv.innerHTML = `
    <div class="typing-dots">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>`;
  messagesContainer.appendChild(typingDiv);
  scrollToBottom();}

function hideTyping() {
  const typingIndicator = document.getElementById("typingIndicator");
  if (typingIndicator) {
    typingIndicator.remove(); }}

function scrollToBottom() { // otomatık alta kayma
  if (messagesContainer) {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;}}

function selectOption(message) { // kutulara tıklandığında mesaj yazma
  console.log('Option selected:', message);
  if (messageInput) {
    messageInput.value = message;
    sendMessage();}}