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
    window.location.href = '/signin';
    return;
  }

  // LOGOUT
  const logoutButton = document.getElementById('logoutButton');
  if (logoutButton) {
    logoutButton.onclick = function() {
      localStorage.removeItem('access_token');
      window.location.href = '/signin';
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
        const response = await fetch('https://bootcampprojectyzta-production.up.railway.app/images/predict', {
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