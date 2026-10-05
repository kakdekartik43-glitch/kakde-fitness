// =====================================================
// MOBILE NAVIGATION
// =====================================================

const menuToggle = document.getElementById("menu-toggle");
const navMenu = document.getElementById("nav-menu");

if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", function () {
        navMenu.classList.toggle("open");
        navMenu.classList.toggle("active");
    });

    navMenu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            navMenu.classList.remove("open");
            navMenu.classList.remove("active");
        });
    });
}


// =====================================================
// AI CHATBOT
// =====================================================

const chatPanel = document.getElementById("chat-panel");
const chatLauncher = document.getElementById("chat-launcher");
const chatLabel = document.getElementById("chat-label");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const messages = document.getElementById("messages");


// OPEN CHAT
function openChat() {

    if (!chatPanel) return;

    chatPanel.classList.remove("hidden");

    if (chatLauncher) {
        chatLauncher.style.display = "none";
    }

    if (chatLabel) {
        chatLabel.style.display = "none";
    }

    if (userInput) {
        userInput.focus();
    }
}


// MINIMIZE CHAT
function minimizeChat() {

    if (!chatPanel) return;

    chatPanel.classList.add("hidden");

    if (chatLauncher) {
        chatLauncher.style.display = "flex";
    }

    if (chatLabel) {
        chatLabel.style.display = "block";
    }
}


// CLOSE CHAT
function closeChat() {
    minimizeChat();
}


// ADD USER MESSAGE
function addUserMessage(text) {

    if (!messages) return;

    const message = document.createElement("div");

    message.className = "user-message";

    message.textContent = text;

    messages.appendChild(message);

    messages.scrollTop = messages.scrollHeight;
}


// ADD AI MESSAGE
function addBotMessage(text) {

    if (!messages) return null;

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


// SEND MESSAGE TO FLASK
async function sendMessage(text) {

    if (!userInput) return;

    const messageText =
        (text || userInput.value).trim();


    if (!messageText) return;


    addUserMessage(messageText);

    userInput.value = "";


    const replyBubble =
        addBotMessage("Typing...");


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

            throw new Error(
                data.reply || "Server error"
            );

        }


        if (replyBubble) {

            replyBubble.textContent =
                data.reply ||
                "Sorry, I could not prepare a reply.";

        }


    } catch (error) {

        console.error(
            "Chatbot error:",
            error
        );


        if (replyBubble) {

            replyBubble.textContent =
                "Sorry, I could not connect to the AI. Please try again.";

        }

    }


    if (messages) {

        messages.scrollTop =
            messages.scrollHeight;

    }

}


// CHAT FORM
if (chatForm) {

    chatForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            sendMessage();

        }
    );

}


// QUICK QUESTIONS
function askQuickQuestion(question) {

    openChat();

    sendMessage(question);

}


// =====================================================
// NIGHT / LIGHT MODE
// =====================================================

const themeButton =
    document.getElementById("theme-toggle");

const themeMenu =
    document.getElementById("theme-menu");

const nightModeButton =
    document.getElementById("night-mode");

const lightModeButton =
    document.getElementById("light-mode");


// OPEN THEME OPTIONS
if (themeButton && themeMenu) {

    themeButton.addEventListener(
        "click",
        function (event) {

            event.stopPropagation();

            themeMenu.classList.toggle("show");

        }
    );

}


// NIGHT MODE
if (nightModeButton) {

    nightModeButton.addEventListener(
        "click",
        function () {

            document.body.classList.remove(
                "light-mode"
            );

            localStorage.setItem(
                "theme",
                "dark"
            );


            if (themeMenu) {
                themeMenu.classList.remove("show");
            }

        }
    );

}


// LIGHT MODE
if (lightModeButton) {

    lightModeButton.addEventListener(
        "click",
        function () {

            document.body.classList.add(
                "light-mode"
            );

            localStorage.setItem(
                "theme",
                "light"
            );


            if (themeMenu) {
                themeMenu.classList.remove("show");
            }

        }
    );

}


// CLOSE THEME MENU WHEN CLICKING OUTSIDE
document.addEventListener(
    "click",
    function (event) {

        if (
            themeMenu &&
            themeButton &&
            !themeMenu.contains(event.target) &&
            !themeButton.contains(event.target)
        ) {

            themeMenu.classList.remove("show");

        }

    }
);


// LOAD SAVED THEME
const savedTheme =
    localStorage.getItem("theme");


if (savedTheme === "light") {

    document.body.classList.add(
        "light-mode"
    );

} else {

    document.body.classList.remove(
        "light-mode"
    );

}


// =====================================================
// BMI CALCULATOR
// =====================================================

function calculateBMI() {

    const heightInput =
        document.getElementById("height");

    const weightInput =
        document.getElementById("weight");

    const result =
        document.getElementById("bmi-result");


    if (
        !heightInput ||
        !weightInput ||
        !result
    ) {

        return;

    }


    const height =
        parseFloat(heightInput.value);

    const weight =
        parseFloat(weightInput.value);


    if (
        !height ||
        !weight ||
        height <= 0 ||
        weight <= 0
    ) {

        result.innerHTML =
            "<p>Please enter valid height and weight.</p>";

        return;

    }


    const heightInMeters =
        height / 100;


    const bmi =
        weight /
        (heightInMeters * heightInMeters);


    result.innerHTML = `
        <h2>Your BMI: ${bmi.toFixed(1)}</h2>
        <p>
            BMI is a general screening measure
            and is not a medical diagnosis.
        </p>
    `;

}


// =====================================================
// AUTO HIDE FLASH MESSAGES
// =====================================================

setTimeout(function () {

    const flashMessages =
        document.querySelectorAll(".flash");


    flashMessages.forEach(
        function (message) {

            message.style.opacity = "0";


            setTimeout(
                function () {

                    message.remove();

                },
                500
            );

        }
    );

}, 4000);
