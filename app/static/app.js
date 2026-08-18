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

    runButton.textContent = "PantryPilot is running...";
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
                result.error ||
                "Something went wrong while running PantryPilot.";

            stepsBox.textContent =
                "No execution steps available.";

            return;
        }

        responseBox.textContent = result.response;
        stepsBox.innerHTML = "";

        result.steps.forEach(function (step, index) {
            const stepElement = document.createElement("div");
            stepElement.className = "step-card";

            const stepTitle = document.createElement("strong");
            stepTitle.textContent = `Step ${index + 1}`;

            let actionText = "Final decision and recommendations";

            const responseMessages =
                step.response && step.response.messages
                    ? step.response.messages
                    : [];

            for (const message of responseMessages) {
                if (message.tool_calls && message.tool_calls.length > 0) {
                    const toolName = message.tool_calls[0].name;

                    if (toolName === "get_household_state") {
                        actionText = "Checked household state";
                    } else if (toolName === "find_purchase_options") {
                        actionText = "Compared purchase options";
                    } else if (toolName === "place_order") {
                        actionText = "Placed mock order";
                    } else {
                        actionText = `Used tool: ${toolName}`;
                    }

                    break;
                }
            }

            const action = document.createElement("p");
            action.className = "step-summary";
            action.textContent = actionText;

            const details = document.createElement("details");

            const summary = document.createElement("summary");
            summary.textContent = "Show technical details";

            const detailsContent = document.createElement("pre");
            detailsContent.textContent =
                JSON.stringify(
                    {
                        module: step.module,
                        prompt: step.prompt,
                        response: step.response
                    },
                    null,
                    2
                );

            details.appendChild(summary);
            details.appendChild(detailsContent);

            stepElement.appendChild(stepTitle);
            stepElement.appendChild(action);
            stepElement.appendChild(details);

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