/**
 * FemBridge – chatbot.js
 * Floating chatbot UI and message handling
 */

document.addEventListener("DOMContentLoaded", () => {
  const chatBtn    = document.getElementById("chatbot-btn");
  const chatWindow = document.getElementById("chatbot-window");
  const closeBtn   = document.getElementById("chatbot-close");
  const chatInput  = document.getElementById("chat-input");
  const sendBtn    = document.getElementById("chat-send");
  const messages   = document.getElementById("chatbot-messages");

  if (!chatBtn) return;  // Chatbot not on this page

  // Toggle open/close
  chatBtn.addEventListener("click", () => {
    chatWindow.classList.toggle("open");
    if (chatWindow.classList.contains("open") && messages.children.length === 0) {
      appendMsg("bot", "👋 Hi! I'm FemBot, your career assistant. How can I help you today?");
    }
    if (chatWindow.classList.contains("open")) chatInput?.focus();
  });

  closeBtn?.addEventListener("click", () => chatWindow.classList.remove("open"));

  // Send message
  async function sendMessage() {
    const msg = chatInput.value.trim();
    if (!msg) return;

    appendMsg("user", msg);
    chatInput.value = "";

    // Typing indicator
    const typingId = appendMsg("bot", "...", true);

    const data = await apiFetch("/chat", {
      method: "POST",
      body: JSON.stringify({ message: msg }),
    });

    // Remove typing indicator
    document.getElementById(typingId)?.remove();

    appendMsg("bot", data.response || "Sorry, I couldn't understand that. Try again!");
  }

  sendBtn?.addEventListener("click", sendMessage);
  chatInput?.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  });

  function appendMsg(role, text, isTyping = false) {
    const id  = "msg-" + Date.now();
    const div = document.createElement("div");
    div.id        = id;
    div.className = role === "bot" ? "msg-bot" : "msg-user";
    div.textContent = text;
    if (isTyping) div.style.opacity = "0.6";
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return id;
  }
});