const runButton = document.getElementById("run-button");
const responseBox = document.getElementById("response");
const stepsBox = document.getElementById("steps");
const promptBox = document.getElementById("prompt");

runButton.addEventListener("click", function () {
    const userPrompt = promptBox.value.trim();

    if (!userPrompt) {
        responseBox.textContent = "Please enter a request first.";
        return;
    }

    runButton.textContent = "PantryPilot is thinking...";
    runButton.disabled = true;

    // Temporary mock response.
    // Later this will come from POST /api/execute.
    const mockResult = {
        response:
            "I recommend ordering the urgent household items today and choosing the supplier with same-day delivery.",

        steps: [
            {
                module: "pantrypilot_agent",
                prompt: "Check the household state for day 3.",
                response: "Found several items that are depleted or running low."
            },
            {
                module: "pantrypilot_agent",
                prompt: "Compare purchase options.",
                response: "Compared available suppliers, prices and delivery times."
            },
            {
                module: "pantrypilot_agent",
                prompt: "Choose the most practical option.",
                response: "Selected the supplier that can handle the urgent needs today."
            }
        ]
    };

    responseBox.textContent = mockResult.response;

    stepsBox.innerHTML = "";

    mockResult.steps.forEach(function (step, index) {
        const stepElement = document.createElement("div");

        stepElement.innerHTML = `
            <strong>Step ${index + 1} — ${step.module}</strong>
            <p><strong>Prompt:</strong> ${step.prompt}</p>
            <p><strong>Response:</strong> ${step.response}</p>
        `;

        stepsBox.appendChild(stepElement);
    });

    runButton.textContent = "Run Agent →";
    runButton.disabled = false;
});