"""
AI Barista Agent
-----------------
A simple Retrieval-Augmented Generation (RAG) agent built with Google's
Agent Development Kit (ADK). The agent answers questions about a coffee
shop's menu, grounding its responses in a local menu.json data source and
being careful to flag allergens.
"""

import json
import os
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.genai import types

MENU_PATH = Path(__file__).parent / "menu.json"


def load_menu() -> list[dict]:
    """Load the coffee shop menu from the local JSON data source."""
    with open(MENU_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def search_menu(query: str) -> str:
    """Search the coffee shop menu for items matching a keyword, tag, or category.

    Args:
        query: A word or phrase to search for (e.g. "vegan", "cold", "sweet").

    Returns:
        A formatted string listing matching menu items, including price and
        allergen information, or a message if nothing matches.
    """
    menu = load_menu()
    query_lower = query.lower()
    matches = []

    for item in menu:
        haystack = " ".join(
            [item["name"], item["category"], " ".join(item["tags"])]
        ).lower()
        if query_lower in haystack:
            matches.append(item)

    if not matches:
        return f"No menu items found matching '{query}'."

    lines = []
    for item in matches:
        allergens = ", ".join(item["allergens"]) if item["allergens"] else "none"
        lines.append(
            f"- {item['name']} ({item['category']}) - ${item['price']:.2f} "
            f"| tags: {', '.join(item['tags'])} | allergens: {allergens}"
        )
    return "\n".join(lines)


def list_allergen_free_items(allergen: str) -> str:
    """List menu items that do NOT contain a given allergen.

    Args:
        allergen: The allergen to avoid (e.g. "dairy", "gluten", "nuts").

    Returns:
        A formatted string of safe menu items for that allergen.
    """
    menu = load_menu()
    allergen_lower = allergen.lower()
    safe_items = [
        item for item in menu if allergen_lower not in [a.lower() for a in item["allergens"]]
    ]

    if not safe_items:
        return f"No items found without {allergen}."

    lines = [f"- {item['name']} (${item['price']:.2f})" for item in safe_items]
    return f"Items without {allergen}:\n" + "\n".join(lines)


# The ADK agent itself. It uses Gemini as the reasoning model and has two
# tools it can call to ground its answers in the actual menu data (RAG).
root_agent = LlmAgent(
    model=LiteLlm(model="groq/openai/gpt-oss-120b"),
    name="ai_barista",
    description="A friendly AI barista that recommends coffee shop menu items.",
    instruction=(
        "You are a warm, friendly AI barista working at a coffee shop. "
        "Always use the search_menu or list_allergen_free_items tools to "
        "ground your answers in the real menu — never invent menu items or "
        "prices. Always mention allergens when recommending food or drinks. "
        "Keep responses short, friendly, and conversational."
    ),
    tools=[search_menu, list_allergen_free_items],
)


def get_runner() -> InMemoryRunner:
    """Create an in-memory runner for local/interactive use of the agent."""
    return InMemoryRunner(agent=root_agent, app_name="ai_barista_app")
