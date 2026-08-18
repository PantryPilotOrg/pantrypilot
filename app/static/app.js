const runButton = document.getElementById("run-button");
const responseBox = document.getElementById("response");
const stepsBox = document.getElementById("steps");
const promptBox = document.getElementById("prompt");
const startDayBox = document.getElementById("start-day");
const endDayBox = document.getElementById("end-day");

runButton.addEventListener("click", async function () {
    const userPrompt = promptBox.value.trim();
    const startDay = Number(startDayBox.value);
    const endDay = Number(endDayBox.value);

    if (!userPrompt) {
        responseBox.textContent = "Please enter a request first.";
        return;
    }

    if (startDay > endDay) {
        responseBox.textContent =
            "Start day cannot be after end day.";
        return;
    }

    runButton.textContent = "PantryPilot is running...";
    runButton.disabled = true;

    responseBox.textContent = "Running simulation...";
    stepsBox.textContent = "Waiting for execution steps...";

    try {
        const apiResponse = await fetch("/api/simulate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: userPrompt,
                start_day: startDay,
                end_day: endDay
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

        responseBox.innerHTML = "";
        stepsBox.innerHTML = "";

        result.results.forEach(function (dayResult) {

            // -------------------------
            // Agent response
            // -------------------------

            const responseElement = document.createElement("div");
            responseElement.className = "day-result";

            const responseTitle = document.createElement("h3");
            responseTitle.textContent =
                `Simulation Day ${dayResult.simulation_day}`;

            const responseText = document.createElement("pre");
            responseText.textContent = dayResult.response;

            responseElement.appendChild(responseTitle);
            responseElement.appendChild(responseText);

            responseBox.appendChild(responseElement);


            // -------------------------
            // Execution steps
            // -------------------------

            const daySteps = document.createElement("div");
            daySteps.className = "day-steps";

            const stepsTitle = document.createElement("h3");
            stepsTitle.textContent =
                `Day ${dayResult.simulation_day} — Execution Steps`;

            daySteps.appendChild(stepsTitle);


            dayResult.steps.forEach(function (step, index) {

                const stepElement = document.createElement("div");
                stepElement.className = "step-card";

                const stepTitle = document.createElement("strong");
                stepTitle.textContent = `Step ${index + 1}`;

                let actionText = "Final decision and recommendations";

                const responseMessages =
                    step.response &&
                    step.response.messages
                        ? step.response.messages
                        : [];

                // Look for tool calls in this step
                for (const message of responseMessages) {

                    if (
                        message.tool_calls &&
                        message.tool_calls.length > 0
                    ) {
                        const toolName =
                            message.tool_calls[0].name;

                        if (toolName === "get_household_state") {
                            actionText =
                                "Checked household state";

                        } else if (
                            toolName === "find_purchase_options"
                        ) {
                            actionText =
                                "Compared purchase options";

                        } else if (
                            toolName === "place_order"
                        ) {
                            actionText =
                                "Placed mock order";

                        } else {
                            actionText =
                                `Used tool: ${toolName}`;
                        }

                        break;
                    }
                }

                const action =
                    document.createElement("p");

                action.className = "step-summary";
                action.textContent = actionText;


                // -------------------------
                // Optional technical details
                // -------------------------

                const details =
                    document.createElement("details");

                const summary =
                    document.createElement("summary");

                summary.textContent =
                    "Show technical details";

                const detailsContent =
                    document.createElement("pre");

                detailsContent.textContent =
                    JSON.stringify(step, null, 2);

                details.appendChild(summary);
                details.appendChild(detailsContent);


                // Add everything to card

                stepElement.appendChild(stepTitle);
                stepElement.appendChild(action);
                stepElement.appendChild(details);

                daySteps.appendChild(stepElement);
            });

            stepsBox.appendChild(daySteps);
        });

    } catch (error) {

        responseBox.textContent =
            "Could not connect to the PantryPilot API.";

        stepsBox.textContent =
            "No execution steps available.";

        console.error(error);

    } finally {

        runButton.textContent =
            "Run Simulation →";

        runButton.disabled = false;
    }
});