# PantryPilot

### Autonomous Household Shopping Agent

**AI Agents – Final Project**  
**Ayla Livney** — aylalivney@gmail.com  
**Chana Gutenmacher** — chana4@gmail.com  
**August 2026**

PantryPilot is an autonomous household shopping agent that manages recurring shopping decisions over time. It observes household needs, compares purchasing options, and decides what to buy, when to order, and when to wait while considering budget, expiry, upcoming events, and delivery constraints.

## Core Agent Tools

PantryPilot exposes three deterministic tools to the LLM. The LLM decides which tools to use, when to use them, and what action to take based on their results.

### `get_household_state`

This tool is PantryPilot’s view into the household. It checks what is currently in the fridge and pantry, what is running low or expiring, and what else may affect today’s shopping decisions. It returns:

- inventory and quantities
- expiry dates and estimated time until items run out
- target stock levels
- household profile and preferences
- upcoming events
- remaining budget
- pending orders

In the MVP, this information is represented by simulated data. In a real system, it could come from household sensors or cameras, user-provided profile information, calendar integrations, and consumption patterns learned over time.

Household data stays outside the initial prompt and is retrieved through the tool only when needed, helping keep the prompt short.

### `find_purchase_options`

The agent sends the items and quantities it is considering. The tool checks available supermarkets and other suppliers and returns prices, availability, delivery time, delivery fees, and minimum-order constraints. The LLM combines this with the household state to decide based on urgency, timing, cost, and upcoming needs — so the cheapest option is not always the best one.

### `place_order`

Executes the purchasing decision selected by the agent inside the PantryPilot environment. The tool validates the order, checks the remaining budget, calculates the final cost, records the order, and updates the run state so later days can see pending orders and the remaining budget.

- In the MVP, `place_order` does not perform a real financial transaction or send the order to a supermarket.
- In production, the user would approve the order before purchase, keeping a human in the loop.

## Simulation Across Days

The simulation includes seven daily household snapshots with changing inventory, events, consumption, and supplier conditions, giving the agent enough variation to make meaningful decisions over time.

In our runs, the agent:

- chose a faster supplier when timing mattered more than price: *“you have guests today… so I chose the store that could deliver immediately.”*
- consolidated several urgent household and hosting needs into one same-day order, including milk, bread, chicken, produce, eggs, and cat food
- recognized an upcoming birthday need but did not invent unavailable items: *“I did not order a birthday cake or extra party snacks — please arrange cake/snacks separately if needed.”*
- balanced urgency against cost, explaining that an additional immediate order was possible but that *“it’s more economical to buy it from the discount supermarket available in a couple of days.”*

The same agent, prompt, and tools produce different decisions as the observed state changes.

## Simulation Design

Daily inventory snapshots are fixed and are not changed when PantryPilot places an order. Instead, placed orders are tracked separately as pending orders, so the agent can consider what is already on the way before ordering again.

- Pending orders are shown only until their delivery day; once fulfilled, they are no longer listed, even though the fixed inventory snapshots are not updated to reflect the delivery.
- Tool results are the source of truth; the LLM does not invent inventory changes, prices, availability, or delivery information.

## Scheduler

PantryPilot runs once per day, rather than every time something changes in the household. This lets the agent keep working over time while avoiding unnecessary LLM calls — for example, it does not need to run every time someone opens the refrigerator.

- In the MVP, this is implemented as a loop across the selected simulation days.
- Budget and order information carry across the run, so each day can take earlier decisions into account.

## Autonomy and ReAct

- The LLM controls the decision process. It decides what information it needs, which tools to call, whether more information is required, and whether to place an order.
- PantryPilot implements ReAct by feeding each tool result back to the LLM as a new observation. The agent can then continue reasoning, call another tool, act, or stop.
- The tools handle deterministic logic such as prices, availability, budget checks, and order validation. The LLM handles the decisions and trade-offs.

## MVP and Real-World Integration

The MVP simulates the external systems a production version could connect to:

- inventory snapshots → fridge/pantry sensors or computer vision
- household and event data → user profile and calendar integrations
- supplier data → live supermarket catalogs and delivery APIs
- `place_order` → real checkout/order integration
- temporary run state → persistent order and budget history

Our MVP focuses on the decision-making layer: observing the household, reasoning over constraints, choosing tools, and making decisions over time.

## GUI and Project Interface

The GUI allows the user to:

- enter a free-form household-management goal
- choose a simulation range (`From day` / `To day`)
- run PantryPilot
- view the final response
- inspect the full execution trace

Simulation-specific controls:

- `From day` / `To day` lets us choose which part of the seven-day simulation to run and evaluate; this would not be part of the intended real-world UX.
- Each run is limited to three consecutive days because of Vercel’s 300-second API limit.

The project exposes the required API endpoints for execution, agent info, team info, and the architecture diagram.