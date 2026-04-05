"""
features/meal.py — Meal planning and grocery list generation.
"""

from family import FamilyProfile
from features.claude_client import ask_claude


async def plan_meals(profile: FamilyProfile, week_notes: str = None, days: int = 7) -> str:
    """Generate a personalised weekly meal plan for the family."""

    notes_line = f"\nThis week's schedule/notes: {week_notes}" if week_notes else ""

    system = f"""You are Brood, a warm and practical AI assistant for busy families.
You know this family well:
{profile.build_context()}

Your job is to plan meals that fit their real life — dietary needs respected,
budget considered, and schedule accounted for. Be practical and specific.
Format the plan clearly by day. Keep suggestions realistic for busy parents."""

    user = f"""Plan {days} days of dinners for our family.{notes_line}

For each day include:
- Dinner (with a short note if it's quick, kid-friendly, or budget-friendly)
- Rough prep time

At the end, add a short note on why this plan works for us."""

    return await ask_claude(system, user, max_tokens=1500)


async def generate_grocery_list(profile: FamilyProfile, meal_plan: str) -> str:
    """Convert a meal plan into a consolidated, organised grocery list."""

    system = f"""You are Brood, a practical AI assistant for busy families.
You know this family well:
{profile.build_context()}

Generate clear, consolidated grocery lists organised by store section.
Always account for dietary restrictions. Estimate quantities for the family size."""

    user = f"""Based on this meal plan, generate a complete grocery list:

{meal_plan}

Organise by section (Produce, Meat & Fish, Dairy, Pantry, etc.).
Note any items that need checking for dietary restrictions.
Include rough quantities. Flag items likely already in the pantry."""

    return await ask_claude(system, user, max_tokens=1200)
