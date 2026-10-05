
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
// =====================================================
// MOBILE MENU
// =====================================================

const menuToggle = document.getElementById("menu-toggle");
const navMenu = document.getElementById("nav-menu");

if (menuToggle && navMenu) {

    menuToggle.addEventListener("click", function () {

        navMenu.classList.toggle("active");

    });

}


// =====================================================
// DARK / LIGHT MODE
// =====================================================

const themeButton =
    document.getElementById("theme-toggle");

if (themeButton) {

    themeButton.addEventListener(
        "click",
        function () {

            document.body.classList.toggle(
                "light-mode"
            );

            if (
                document.body.classList.contains(
                    "light-mode"
                )
            ) {

                themeButton.textContent = "☀️";

                localStorage.setItem(
                    "theme",
                    "light"
                );

            } else {

                themeButton.textContent = "🌙";

                localStorage.setItem(
                    "theme",
                    "dark"
                );
            }

        }
    );

}


// Load saved theme

if (
    localStorage.getItem("theme") === "light"
) {

    document.body.classList.add(
        "light-mode"
    );

    if (themeButton) {

        themeButton.textContent = "☀️";

    }

}


// =====================================================
// BMI CALCULATOR
// =====================================================

function calculateBMI() {

    const height =
        parseFloat(
            document.getElementById("height").value
        );

    const weight =
        parseFloat(
            document.getElementById("weight").value
        );

    const result =
        document.getElementById("bmi-result");


    if (
        !height ||
        !weight ||
        height <= 0 ||
        weight <= 0
    ) {

        result.innerHTML =
            "Please enter valid height and weight.";

        return;

    }


    const heightMeters =
        height / 100;

    const bmi =
        weight /
        (heightMeters * heightMeters);


    result.innerHTML =
        `<h2>Your BMI: ${bmi.toFixed(1)}</h2>`;


    if (bmi < 18.5) {

        result.innerHTML +=
            "<p>General range: Underweight.</p>";

    } else if (bmi < 25) {

        result.innerHTML +=
            "<p>General range: Healthy weight.</p>";

    } else if (bmi < 30) {

        result.innerHTML +=
            "<p>General range: Overweight.</p>";

    } else {

        result.innerHTML +=
            "<p>General range: Obesity range.</p>";

    }

}


// =====================================================
// AUTO HIDE FLASH MESSAGES
// =====================================================

setTimeout(function () {

    const messages =
        document.querySelectorAll(
            ".flash"
        );

    messages.forEach(function (message) {

        message.style.opacity = "0";

        setTimeout(function () {

            message.remove();

        }, 500);

    });

}, 4000);
