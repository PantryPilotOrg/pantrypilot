from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from app.agent.model import llm
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tracing import trace_model_call
from app.tools.find_purchase_options import find_purchase_options
from app.tools.household_tool import get_household_state
from app.tools.place_order import place_order


class PurchaseItem(BaseModel):
    item_id: str = Field(
        description="Unique ID of the household item to purchase."
    )
    quantity: float = Field(
        gt=0,
        description="Quantity of the item to purchase. Must be greater than zero."
    )


class FindPurchaseOptionsInput(BaseModel):
    items: list[PurchaseItem] = Field(
        description="List of household items and required quantities to purchase."
    )


class PlaceOrderInput(BaseModel):
    supplier_id: str = Field(
        description="ID of the supplier selected for the order."
    )
    items: list[PurchaseItem] = Field(
        description="List of household items and quantities to order."
    )


def find_purchase_options_tool(
    items: list[PurchaseItem],
) -> dict:
    """
    Convert validated purchase items to dictionaries
    for the existing purchase-options tool.
    """
    return find_purchase_options(
        [item.model_dump() for item in items]
    )


def place_order_tool(
    supplier_id: str,
    items: list[PurchaseItem],
) -> dict:
    """
    Convert validated order items to dictionaries
    for the existing place-order tool.
    """
    return place_order(
        supplier_id=supplier_id,
        items=[item.model_dump() for item in items],
    )


household_tool = StructuredTool.from_function(
    func=get_household_state,
    name="get_household_state",
    description=(
        "Get the household state for a specific simulation day. "
        "Use this tool when you need to understand the household's current needs "
        "before making shopping decisions. It returns the household profile, budget, "
        "inventory levels, depletion and expiry risks, stock targets, and upcoming events."
    ),
)


purchase_tool = StructuredTool.from_function(
    func=find_purchase_options_tool,
    name="find_purchase_options",
    args_schema=FindPurchaseOptionsInput,
    description=(
        "Find and compare purchase options for a list of household items and quantities. "
        "Use this tool when items need to be purchased and you need to determine which "
        "supplier can fulfill the request. It returns supplier prices, item availability, "
        "delivery details, minimum-order requirements, total cost, missing items, "
        "and whether each supplier option can currently be ordered."
    ),
)


order_tool = StructuredTool.from_function(
    func=place_order_tool,
    name="place_order",
    args_schema=PlaceOrderInput,
    description=(
        "Validate and simulate placing an order with a selected supplier. "
        "Use this tool only after a supplier and the requested item quantities "
        "have been selected based on available purchase options. "
        "The tool validates whether the order can be placed and returns the "
        "result of the simulated order attempt."
    ),
)


agent = create_agent(
    model=llm,
    tools=[
        household_tool,
        purchase_tool,
        order_tool,
    ],
    system_prompt=SYSTEM_PROMPT,
    middleware=[trace_model_call],
)