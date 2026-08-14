const runButton = document.getElementById("run-button");
const responseBox = document.getElementById("response");
const stepsBox = document.getElementById("steps");
const promptBox = document.getElementById("prompt");

runButton.addEventListener("click", async function () {
    const userPrompt = promptBox.value.trim();

    if (!userPrompt) {
        responseBox.textContent = "Please enter a request first.";
        return;
    }

    runButton.textContent = "PantryPilot is thinking...";
    runButton.disabled = true;

    responseBox.textContent = "Running agent...";
    stepsBox.textContent = "Waiting for execution steps...";

    try {
        const apiResponse = await fetch("/api/execute", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: userPrompt
            })
        });

        const result = await apiResponse.json();

        if (result.status !== "ok") {
            responseBox.textContent =
                result.error || "Something went wrong while running PantryPilot.";

            stepsBox.textContent = "No execution steps available.";
            return;
        }

        responseBox.textContent = result.response;

        stepsBox.innerHTML = "";

        result.steps.forEach(function (step, index) {
            const stepElement = document.createElement("div");
            stepElement.className = "step-card";

            stepElement.innerHTML = `
                <strong>Step ${index + 1} — ${step.module}</strong>
                <p><strong>Prompt:</strong></p>
                <pre>${JSON.stringify(step.prompt, null, 2)}</pre>

                <p><strong>Response:</strong></p>
                <pre>${JSON.stringify(step.response, null, 2)}</pre>
            `;

            stepsBox.appendChild(stepElement);
        });

    } catch (error) {
        responseBox.textContent =
            "Could not connect to the PantryPilot API.";

        stepsBox.textContent =
            "No execution steps available.";

        console.error(error);

    } finally {
        runButton.textContent = "Run Agent →";
        runButton.disabled = false;
    }
});