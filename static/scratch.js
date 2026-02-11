const canvas = document.getElementById("scratchCanvas");
const ctx = canvas.getContext("2d");
const rewardText = document.getElementById("rewardText");
const instruction = document.getElementById("instruction");

// Set canvas size
canvas.width = 400;
canvas.height = 250;

let isScratching = false;
let hasRevealed = false;
let scratchedPercentage = 0;

let selectedModule = "";
let basePrice = 0;
let userEmail = "";
let rewardOffer = "";

// Check if already scratched
if (sessionStorage.getItem("hasScratched")) {
    rewardOffer = sessionStorage.getItem("scratchReward");
    selectedModule = sessionStorage.getItem("module");
    basePrice = parseInt(sessionStorage.getItem("basePrice"));
    userEmail = sessionStorage.getItem("email") || "";

    rewardText.textContent = rewardOffer;
    instruction.textContent = "You already scratched! Click below to send to WhatsApp.";

    // Show popup immediately
    setTimeout(() => {
        showPopup();
    }, 500);
} else {
    // Initialize scratch card
    initScratchCard();
}

function initScratchCard() {
    // Draw silver scratch layer
    const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
    gradient.addColorStop(0, "#C0C0C0");
    gradient.addColorStop(0.5, "#E8E8E8");
    gradient.addColorStop(1, "#C0C0C0");

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Add text overlay
    ctx.fillStyle = "#333";
    ctx.font = "bold 30px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("SCRATCH HERE", canvas.width / 2, canvas.height / 2 - 20);

    ctx.font = "bold 40px Arial";
    ctx.fillText("🎁", canvas.width / 2, canvas.height / 2 + 30);

    // Fetch reward from server
    fetch("/scratch-reveal", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            rewardOffer = data.reward;
            selectedModule = data.module;
            basePrice = data.base_price;
            userEmail = data.email || "";

            rewardText.textContent = rewardOffer;
        });
}

// Mouse/Touch event handlers
canvas.addEventListener("mousedown", startScratching);
canvas.addEventListener("mousemove", scratch);
canvas.addEventListener("mouseup", stopScratching);
canvas.addEventListener("mouseleave", stopScratching);

canvas.addEventListener("touchstart", (e) => {
    e.preventDefault();
    startScratching(e);
});
canvas.addEventListener("touchmove", (e) => {
    e.preventDefault();
    scratch(e);
});
canvas.addEventListener("touchend", (e) => {
    e.preventDefault();
    stopScratching(e);
});

function startScratching(e) {
    isScratching = true;
}

function stopScratching(e) {
    isScratching = false;
}

function scratch(e) {
    if (!isScratching) return;

    const rect = canvas.getBoundingClientRect();
    let x, y;

    if (e.type.startsWith("touch")) {
        x = e.touches[0].clientX - rect.left;
        y = e.touches[0].clientY - rect.top;
    } else {
        x = e.clientX - rect.left;
        y = e.clientY - rect.top;
    }

    // Scale coordinates to canvas size
    x = x * (canvas.width / rect.width);
    y = y * (canvas.height / rect.height);

    // Clear circular area
    ctx.globalCompositeOperation = "destination-out";
    ctx.beginPath();
    ctx.arc(x, y, 25, 0, Math.PI * 2);
    ctx.fill();

    // Check scratch percentage
    checkScratchPercentage();
}

function checkScratchPercentage() {
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const pixels = imageData.data;
    let transparent = 0;

    for (let i = 3; i < pixels.length; i += 4) {
        if (pixels[i] === 0) {
            transparent++;
        }
    }

    scratchedPercentage = (transparent / (pixels.length / 4)) * 100;

    // If 50% scratched, reveal completely
    if (scratchedPercentage > 50 && !hasRevealed) {
        revealComplete();
    }
}

function revealComplete() {
    hasRevealed = true;

    // Clear entire canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Hide instruction
    instruction.style.display = "none";

    // Save to session
    sessionStorage.setItem("hasScratched", "true");
    sessionStorage.setItem("scratchReward", rewardOffer);
    sessionStorage.setItem("module", selectedModule);
    sessionStorage.setItem("basePrice", basePrice);
    sessionStorage.setItem("email", userEmail);

    // Show confetti
    createConfetti();

    // Show popup after a short delay
    setTimeout(() => {
        showPopup();
    }, 1000);
}

function showPopup() {
    const popupText = document.getElementById("popupText");
    popupText.textContent = `You won ${rewardOffer} for ${selectedModule}!`;

    document.getElementById("popup").classList.remove("hidden");
}

function sendToWhatsApp() {
    rewardOffer = rewardOffer || sessionStorage.getItem("scratchReward");
    selectedModule = selectedModule || sessionStorage.getItem("module");
    basePrice = basePrice || parseInt(sessionStorage.getItem("basePrice"));
    userEmail = userEmail || sessionStorage.getItem("email") || "";

    let msg = "";
    const percentMatch = rewardOffer.match(/^(\d+)% Discount$/);

    if (percentMatch) {
        const percent = parseInt(percentMatch[1]);
        const finalAmount = basePrice - (basePrice * percent / 100);

        msg =
            `🎉 Scratch & Win Result!\n\n` +
            `Module: ${selectedModule}\n` +
            `Offer: ${rewardOffer}\n` +
            `Base Price: ₹${basePrice}\n` +
            `Final Amount: ₹${finalAmount}\n` +
            `(Saved ₹${basePrice - finalAmount}!)\n\n` +
            `Email: ${userEmail}\n\n` +
            `I'd like to book this offer!`;
    } else {
        msg =
            `🎉 Scratch & Win Result!\n\n` +
            `Module: ${selectedModule}\n` +
            `Offer: ${rewardOffer}\n` +
            `Email: ${userEmail}\n\n` +
            `I'd like to book this offer!`;
    }

    // TODO: Replace with your WhatsApp number
    const academyNumber = "917034942438";
    const url = `https://wa.me/${academyNumber}?text=${encodeURIComponent(msg)}`;

    window.open(url, "_blank");

    document.getElementById("popup").classList.add("hidden");
}

// 🎊 Confetti animation
function createConfetti() {
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffd700'];
    const confettiCount = 50;

    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.style.position = 'fixed';
        confetti.style.width = '10px';
        confetti.style.height = '10px';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.top = '-10px';
        confetti.style.opacity = '1';
        confetti.style.zIndex = '9999';
        confetti.style.borderRadius = '50%';

        document.body.appendChild(confetti);

        const fallDuration = Math.random() * 3 + 2;
        const fallDistance = Math.random() * window.innerHeight + window.innerHeight;

        confetti.animate([
            { transform: 'translateY(0px) rotate(0deg)', opacity: 1 },
            { transform: `translateY(${fallDistance}px) rotate(${Math.random() * 360}deg)`, opacity: 0 }
        ], {
            duration: fallDuration * 1000,
            easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
        });

        setTimeout(() => {
            confetti.remove();
        }, fallDuration * 1000);
    }
}

// Responsive canvas sizing
function resizeCanvas() {
    const container = document.querySelector('.scratch-container');
    const rect = container.getBoundingClientRect();

    if (window.innerWidth <= 600) {
        canvas.width = 300;
        canvas.height = 200;
        initScratchCard();
    }
}

window.addEventListener('resize', resizeCanvas);