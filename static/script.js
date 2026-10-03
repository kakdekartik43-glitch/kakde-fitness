
// MOBILE NAVIGATION
const menuToggle = document.getElementById("menu-toggle");
const navMenu = document.getElementById("nav-menu");

if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", function () {
        navMenu.classList.toggle("open");
    });

    navMenu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            navMenu.classList.remove("open");
        });
    });
}

// CHATBOT ELEMENTS
const chatPanel = document.getElementById("chat-panel");
const chatLauncher = document.getElementById("chat-launcher");
const chatLabel = document.getElementById("chat-label");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const messages = document.getElementById("messages");

// OPEN CHAT
function openChat() {
    chatPanel.classList.remove("hidden");
    chatLauncher.style.display = "none";
    chatLabel.style.display = "none";
    userInput.focus();
}

// MINIMIZE CHAT
function minimizeChat() {
    chatPanel.classList.add("hidden");
    chatLauncher.style.display = "flex";
    chatLabel.style.display = "block";
}

// CLOSE CHAT
function closeChat() {
    minimizeChat();
}

// ADD A USER MESSAGE
function addUserMessage(text) {
    const message = document.createElement("div");
    message.className = "user-message";
    message.textContent = text;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
}

// ADD AN AI MESSAGE
function addBotMessage(text) {
    const wrapper = document.createElement("div");
    wrapper.className = "bot-message";

    const logo = document.createElement("div");
    logo.className = "message-logo";
    logo.textContent = "✦";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.textContent = text;

    wrapper.appendChild(logo);
    wrapper.appendChild(bubble);
    messages.appendChild(wrapper);

    messages.scrollTop = messages.scrollHeight;
    return bubble;
}

// SEND MESSAGE TO FLASK / OLLAMA
async function sendMessage(text) {
    const messageText = (text || userInput.value).trim();

    if (!messageText) return;

    addUserMessage(messageText);
    userInput.value = "";

    const replyBubble = addBotMessage("Typing...");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: messageText
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.reply || "Server error");
        }

        replyBubble.textContent = data.reply || "Sorry, I could not prepare a reply.";

    } catch (error) {
        console.error("Chatbot error:", error);
        replyBubble.textContent =
            "Sorry, I could not connect to the AI. Please try again.";
    }

    messages.scrollTop = messages.scrollHeight;
}

// FORM SUBMISSION
if (chatForm) {
    chatForm.addEventListener("submit", function (event) {
        event.preventDefault();
        sendMessage();
    });
}

// QUICK QUESTIONS
function askQuickQuestion(question) {
    sendMessage(question);
}
