// -----------------------------
// GLOBAL STATE
// -----------------------------
let selectedEmailText = "";
let currentEmailStatus = "";
let lastThreadId = "";
let analyzing = false;


// -----------------------------
// START
// -----------------------------
window.addEventListener("load", () => {
    console.log("Sentinel Started");

    addFloatingButton();
    detectOpenedEmail();
});


// -----------------------------
// FLOATING BUTTON
// -----------------------------
function addFloatingButton() {
    if (document.getElementById("ai-float-btn")) {
        return;
    }

    let btn = document.createElement("button");

    btn.id = "ai-float-btn";
    btn.innerHTML = "✨";

    btn.style = `
        position:fixed;
        bottom:25px;
        right:25px;
        width:65px;
        height:65px;
        border-radius:50%;
        border:none;
        background:linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );
        color:white;
        font-size:28px;
        cursor:pointer;
        z-index:999999;
    `;

    btn.onclick = togglePanel;

    document.body.appendChild(btn);
}


// -----------------------------
// PANEL TOGGLE
// -----------------------------
function togglePanel() {
    let panel = document.getElementById(
        "sentinel-panel"
    );

    if (panel) {
        panel.remove();
    } else {
        createPanel();
    }
}


// -----------------------------
// CLEAN EMAIL TEXT
// -----------------------------
function cleanEmailText(text) {
    return text
        .replace(/unsubscribe/gi, "")
        .replace(/read more/gi, "")
        .replace(/comments?/gi, "")
        .replace(/upvotes?/gi, "")
        .replace(/hide.*$/gim, "")
        .trim();
}


// -----------------------------
// SINGLE SOURCE OF TRUTH
// Extract exact visible email
// -----------------------------
function extractCurrentEmail() {
    const emailBodies = document.querySelectorAll(
        "div.a3s.aiL, div.a3s"
    );

    if (!emailBodies.length) {
        return "";
    }

    let fullText = "";

    emailBodies.forEach((body) => {
        fullText +=
            body.innerText.trim() +
            "\n\n";
    });

    fullText = cleanEmailText(fullText);

    console.log(
        "Fresh Extracted Email:",
        fullText
    );

    return fullText.trim();
}


// -----------------------------
// DETECT OPENED EMAIL
// -----------------------------
function detectOpenedEmail() {
    setInterval(() => {

        const currentThreadId =
            window.location.href;

        const text =
            extractCurrentEmail();

        if (!text) {
            return;
        }

        if (text.length < 20) {
            return;
        }

        if (
            currentThreadId ===
            lastThreadId &&
            text === selectedEmailText
        ) {
            return;
        }

        if (analyzing) {
            return;
        }

        const emailBodies =
            document.querySelectorAll(
                "div.a3s.aiL, div.a3s"
            );

        analyzing = true;

        lastThreadId =
            currentThreadId;

        console.log(
            "New Email Opened"
        );

        setTimeout(() => {
            analyzeEmail(
                text,
                emailBodies[
                    emailBodies.length - 1
                ]
            );
        }, 1200);

    }, 1500);
}


// -----------------------------
// ANALYZE EMAIL
// -----------------------------
function analyzeEmail(
    text,
    emailBody
) {
    console.log(
        "Sending for analysis:",
        text
    );

    fetch(
        "https://sentinel-core-q5qw.onrender.com/analyze",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        }
    )
    .then(res => res.json())
    .then(data => {

        console.log(
            "Detection:",
            data
        );

        analyzing = false;

        removeSafePopup();

        if (
            data.status ===
            "BLOCKED"
        ) {
            currentEmailStatus =
                "BLOCKED";

            selectedEmailText =
                text;

            blockEmail(
                emailBody,
                data
            );

            return;
        }

        currentEmailStatus =
            data.status;

        selectedEmailText =
            text;

        showSafePopup(
            data.status
        );
    })
    .catch(err => {
        analyzing = false;

        console.log(
            "Analyze Error:",
            err
        );
    });
}


// -----------------------------
// BLOCK EMAIL
// -----------------------------
function blockEmail(
    emailBody,
    data
) {
    let container =
        emailBody.closest(
            "div[role='main']"
        );

    if (!container) {
        container = emailBody;
    }

    container.innerHTML = `
        <div style="
            display:flex;
            align-items:center;
            justify-content:center;
            height:80vh;
        ">
            <div style="
                background:#1f2937;
                color:white;
                padding:25px;
                border-radius:12px;
                width:500px;
                text-align:center;
            ">
                <h2 style="color:red;">
                    🚫 Malicious Email Blocked
                </h2>

                <p>
                    <b>Detected Type:</b>
                    ${
                        data.types &&
                        data.types.length
                        ? data.types.join(", ")
                        : "Unknown Threat"
                    }
                </p>
            </div>
        </div>
    `;
}


// -----------------------------
// SAFE POPUP
// -----------------------------
function showSafePopup(status) {
    removeSafePopup();

    let popup =
        document.createElement("div");

    popup.id = "safe-popup";

    popup.style = `
        position:fixed;
        bottom:90px;
        right:20px;
        background:
        ${
            status === "FLAGGED"
            ? "#f59e0b"
            : "#22c55e"
        };
        color:white;
        padding:10px 15px;
        border-radius:8px;
        z-index:9999;
        font-weight:bold;
    `;

    popup.innerText =
        status === "FLAGGED"
        ? "⚠ Suspicious Email"
        : "✅ Safe Email";

    document.body.appendChild(
        popup
    );

    setTimeout(() => {
        popup.remove();
    }, 3000);
}


// -----------------------------
// REMOVE SAFE POPUP
// -----------------------------
function removeSafePopup() {
    let popup =
        document.getElementById(
            "safe-popup"
        );

    if (popup) {
        popup.remove();
    }
}


// -----------------------------
// CREATE PANEL
// -----------------------------
function createPanel() {
    let panel =
        document.createElement("div");

    panel.id = "sentinel-panel";

    panel.style = `
        position: fixed;
        top: 70px;
        right: 24px;
        width: 390px;
        height: 570px;
        background: white;
        border-radius: 20px;
        z-index: 999999;
        padding:20px;
    `;

    panel.innerHTML = `
        <input id="cmd"
        placeholder="summarize / reply"
        />

        <button id="runBtn">
            Execute
        </button>

        <div id="statusText">
            Ready
        </div>

        <div id="result">
            No output yet.
        </div>
    `;

    document.body.appendChild(panel);

    document.getElementById(
        "runBtn"
    ).onclick = runTask;
}


// -----------------------------
// RUN TASK
// Sends exact console content
// -----------------------------
function runTask() {

    let cmd =
        document
        .getElementById("cmd")
        .value
        .trim();

    let output =
        document.getElementById(
            "result"
        );

    let statusText =
        document.getElementById(
            "statusText"
        );

    const freshEmailText =
        extractCurrentEmail();

    if (!freshEmailText) {
        output.innerText =
            "Open an email first.";

        statusText.innerText =
            "No email selected";

        return;
    }

    if (
        currentEmailStatus ===
        "BLOCKED"
    ) {
        output.innerText =
            "Blocked mail cannot be processed.";

        statusText.innerText =
            "Blocked";

        return;
    }

    console.log(
        "Sending to backend:",
        freshEmailText
    );

    output.innerText =
        "Processing request...";

    statusText.innerText =
        "Processing...";

    fetch(
        "https://sentinel-core-q5qw.onrender.com/task",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                command: cmd,
                email: freshEmailText
            })
        }
    )
    .then(res => res.json())
    .then(data => {
        output.innerText =
            data.result ||
            data.error;

        statusText.innerText =
            "Completed";
    })
    .catch(err => {
        console.log(
            "Task Error:",
            err
        );

        output.innerText =
            "Task failed.";

        statusText.innerText =
            "Failed";
    });
}