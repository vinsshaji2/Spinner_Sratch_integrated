const canvas = document.getElementById("wheelCanvas");
const ctx = canvas.getContext("2d");

let offers = [];
const center = 275;
const radius = 240;

let angle = 0;
let spinning = false;

let basePrice = 0;
let selectedModule = "";
let userEmail = "";
let lastWinText = "";

// 🎨 Draw the wheel
function drawWheel() {
    if (!offers.length) return;

    const slice = 2 * Math.PI / offers.length;

    ctx.clearRect(0, 0, 550, 550);

    for (let i = 0; i < offers.length; i++) {
        const start = angle + i * slice;
        const end = start + slice;

        ctx.beginPath();
        ctx.moveTo(center, center);
        ctx.arc(center, center, radius, start, end);
        ctx.fillStyle = `hsl(${i * 360 / offers.length}, 70%, 50%)`;
        ctx.fill();
        ctx.strokeStyle = "white";
        ctx.lineWidth = 3;
        ctx.stroke();

        // Draw text
        ctx.save();
        ctx.translate(center, center);
        ctx.rotate(start + slice / 2);
        ctx.textAlign = "right";
        ctx.fillStyle = "white";
        ctx.font = "bold 16px Arial";
        ctx.shadowColor = "rgba(0,0,0,0.5)";
        ctx.shadowBlur = 3;
        wrapText(ctx, offers[i], radius - 20, -10, 110, 20);
        ctx.restore();
    }

    // Draw center circle
    ctx.beginPath();
    ctx.arc(center, center, 30, 0, 2 * Math.PI);
    ctx.fillStyle = "white";
    ctx.fill();
    ctx.strokeStyle = "#333";
    ctx.lineWidth = 3;
    ctx.stroke();
}

// 🎯 Perfect spin logic
function spinTo(index) {
    if (spinning) return;
    spinning = true;

    const spinBtn = document.getElementById("spinBtn");
    spinBtn.disabled = true;
    spinBtn.textContent = "SPINNING...";

    const slice = 2 * Math.PI / offers.length;
    const fullRotations = 7;
    const pointerAngle = -Math.PI / 2;

    // Normalize current angle
    angle = angle % (2 * Math.PI);

    const targetAngle =
        fullRotations * 2 * Math.PI +
        pointerAngle -
        (index * slice + slice / 2);

    const startAngle = angle;
    const delta = targetAngle - startAngle;
    const duration = 4500;
    const startTime = performance.now();

    function animate(now) {
        const progress = Math.min((now - startTime) / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 4);
        angle = startAngle + delta * ease;

        drawWheel();

        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            angle = angle % (2 * Math.PI);
            spinning = false;
            showWinPopup(offers[index]);
        }
    }

    requestAnimationFrame(animate);
}

function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
    const words = text.split(" ");
    let line = "";
    let lines = [];

    for (let i = 0; i < words.length; i++) {
        const testLine = line + words[i] + " ";
        const metrics = ctx.measureText(testLine);
        if (metrics.width > maxWidth && i > 0) {
            lines.push(line);
            line = words[i] + " ";
        } else {
            line = testLine;
        }
    }
    lines.push(line);

    for (let i = 0; i < lines.length; i++) {
        ctx.fillText(lines[i].trim(), x, y + i * lineHeight);
    }
}

// 🖱️ Button click
document.getElementById("spinBtn").onclick = async () => {
    if (spinning) return;

    const res = await fetch("/spin");
    const data = await res.json();

    offers = data.offers;
    basePrice = data.base_price;
    selectedModule = data.module;
    userEmail = data.email || "";

    spinTo(data.index);
};

// 🚀 Initial load
let loaded = false;

function loadWheel() {
    if (loaded) return;
    loaded = true;

    // Check if already spun in this session
    if (sessionStorage.getItem("hasSpun")) {
        lastWinText = sessionStorage.getItem("winText");
        selectedModule = sessionStorage.getItem("module");
        basePrice = parseInt(sessionStorage.getItem("basePrice"));
        userEmail = sessionStorage.getItem("email") || "";

        const spinBtn = document.getElementById("spinBtn");
        spinBtn.disabled = true;
        spinBtn.textContent = "ALREADY SPUN";

        alert("You already spun the wheel! Click OK to send your offer to WhatsApp.");

        setTimeout(() => {
            closePopup();
        }, 500);

        return;
    }

    fetch("/spin")
        .then(res => res.json())
        .then(data => {
            offers = data.offers;
            basePrice = data.base_price;
            selectedModule = data.module;
            userEmail = data.email || "";
            drawWheel();
        });
}

loadWheel();

// 🎉 Popup
function showWinPopup(text) {
    lastWinText = text;

    // Save win in browser session
    sessionStorage.setItem("hasSpun", "true");
    sessionStorage.setItem("winText", text);
    sessionStorage.setItem("module", selectedModule);
    sessionStorage.setItem("basePrice", basePrice);
    sessionStorage.setItem("email", userEmail);

    document.getElementById("popupText").innerText = "🎉 You Won!";

    const detailsText = `${text} for ${selectedModule.toUpperCase()}`;
    document.getElementById("popupDetails").innerText = detailsText;

    document.getElementById("popup").classList.remove("hidden");

    // Confetti effect
    createConfetti();
}

function closePopup() {
    lastWinText = lastWinText || sessionStorage.getItem("winText");
    selectedModule = selectedModule || sessionStorage.getItem("module");
    basePrice = basePrice || parseInt(sessionStorage.getItem("basePrice"));
    userEmail = userEmail || sessionStorage.getItem("email") || "";

    let msg = "";
    const percentMatch = lastWinText.match(/^(\d+)% Discount$/);

    if (percentMatch) {
        const percent = parseInt(percentMatch[1]);
        const finalAmount = basePrice - (basePrice * percent / 100);

        msg =
            `🎉 Spin & Win Result!\n\n` +
            `Module: ${selectedModule}\n` +
            `Offer: ${lastWinText}\n` +
            `Base Price: ₹${basePrice}\n` +
            `Final Amount: ₹${finalAmount}\n` +
            `(Saved ₹${basePrice - finalAmount}!)\n\n` +
            `Email: ${userEmail}\n\n` +
            `I'd like to book this offer!`;
    } else {
        msg =
            `🎉 Spin & Win Result!\n\n` +
            `Module: ${selectedModule}\n` +
            `Offer: ${lastWinText}\n` +
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