# PantryPilot simulated data

This folder contains the small, controlled household world used by the PantryPilot MVP.

The CSV files are deliberately limited to 12 products. The goal is not to reproduce an entire supermarket. The goal is to provide enough variety for the agent to demonstrate meaningful reasoning about shortages, expiry, routine restocking, supplier minimums, urgency, and order consolidation.

## Important design principle

`products.csv` is the canonical product catalogue.

Every other CSV refers to products using the exact `item_id` values defined in `products.csv`. When a new product is introduced, add it to `products.csv` first and then reference the same ID everywhere else.

The inventory files currently repeat `item_name` and `unit` because the existing Python service expects those columns. `products.csv` is still the authoritative source for those values.

## File descriptions

### products.csv

Defines every product that exists in the simulated PantryPilot world.

Used by both the household-state side and the supplier-options side.

Fields:

- `item_id`: stable machine-readable product code used in every CSV and tool input.
- `item_name`: human-readable display name.
- `category`: broad product group.
- `unit`: unit in which household quantity and supplier quantity are measured.
- `perishable`: whether expiry is normally relevant.

This file does not describe how much is currently at home or where the product can be bought.

### stock_targets.csv

Defines Maya's normal household baseline: which products she generally wants to keep at home and how much.

This is what allows PantryPilot to distinguish between:

- an item that is intentionally not stocked;
- a regular household item that is completely missing;
- an item that is present but below its preferred minimum.

Fields:

- `item_id`: reference to `products.csv`.
- `is_regular_item`: whether this product is normally kept in the home.
- `minimum_quantity`: level below which replenishment should be considered.
- `target_quantity`: desired quantity after restocking.
- `priority`: importance of avoiding a shortage, currently `essential` or `normal`.

This file describes desired stock, not current stock.

### consumption_patterns.csv

Contains mocked learned estimates of how quickly the household consumes each product.

The current project does not yet implement the learning process. This file represents the result that a future learning component might derive from purchase history, inventory changes, or user feedback.

Fields:

- `item_id`: reference to `products.csv`.
- `estimated_units_per_day`: estimated average daily consumption in the product's canonical unit.
- `confidence`: confidence in the estimate.
- `source`: mocked origin of the estimate.

The inventory service uses this data to calculate estimated days until depletion.

### inventory_day_1.csv

A complete snapshot of the household inventory on simulated Day 1.

Day 1 is designed to show a relatively well-stocked home with a few meaningful issues:

- milk is becoming low;
- yogurt is plentiful but close to expiry;
- rice is a regular item but completely missing;
- most other essentials are still adequately stocked.

This supports reasoning such as using an expiring substitute or delaying a small delivery.

### inventory_day_2.csv

A complete snapshot of the household inventory on simulated Day 2.

Day 2 is designed to show several products approaching their reorder levels:

- milk is almost gone;
- bread, produce, coffee, and cat food are declining;
- yogurt expires today;
- rice remains missing;
- chicken is nearing expiry.

This supports a decision about whether to make a medium-sized order now or wait briefly and consolidate.

### inventory_day_3.csv

A complete snapshot of the household inventory on simulated Day 3.

Day 3 is designed to create a substantial restocking need:

- milk, bread, and rice are absent;
- eggs, pasta, produce, chicken, coffee, olive oil, and cat food are below their preferred minimums;
- yogurt is nearly depleted.

A basket that restores products toward their target quantities should be large enough for supermarket minimum-order rules to become relevant.

### suppliers.csv

Contains mocked offers for every product from three suppliers.

The values are fictional and exist only for the course simulation. They should not be treated as current real-world prices.

The three supplier profiles intentionally create trade-offs:

- `Shufersal`: moderate prices, direct delivery, ₪150 minimum, one-day delay.
- `AM:PM`: higher prices, Wolt delivery, no minimum, same-day availability.
- `Osher Ad`: lower prices, ₪250 minimum, two-day delay.

Fields:

- `supplier_id`: stable supplier code.
- `supplier_name`: display name.
- `supplier_type`: broad supplier category.
- `item_id`: product being offered.
- `unit_price`: price for one canonical product unit.
- `available`: whether the offer can currently be purchased.
- `delivery_channel`: how the order is delivered.
- `delivery_fee`: fixed delivery charge for the supplier basket.
- `minimum_order`: required merchandise subtotal before delivery.
- `earliest_available_day`: relative delivery delay used by the current code:
  - `0` means same day;
  - `1` means the next day;
  - `2` means two days later.

## How the files work together

Example for rice:

1. `products.csv` says that `rice` exists and is measured by package.
2. `stock_targets.csv` says rice is a regular item with a preferred target of two packages.
3. `inventory_day_2.csv` says the current quantity is zero.
4. `consumption_patterns.csv` provides the estimated usage rate.
5. `suppliers.csv` provides purchase possibilities.

The household-state tool should explain the need.

The purchase-options tool should calculate realistic supplier baskets.

The Smart LLM should connect those results and decide whether to wait, substitute, consolidate, order, or take no action.

## Data limitations

This is intentionally controlled mock data.

It does not yet include:

- household profile;
- monthly budget;
- upcoming events;
- learned substitution preferences;
- order history;
- automatic inventory changes after an order;
- real supplier APIs.

Those can be introduced later without changing the canonical product IDs in this folder.

## Target Quantity

target_quantity is the preferred quantity after a replenishment decision has already been made. Being below the target does not by itself mean the item should be purchased.
