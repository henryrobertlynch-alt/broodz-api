"""
family.py — Family profile and context engine.
This is the memory that makes Brood feel like it knows your family.
"""

from typing import Optional, List


class FamilyProfile:
    def __init__(
        self,
        family_id: str,
        adults: List[str],
        kids: List[dict],
        dietary_notes: Optional[str] = None,
        weekly_budget: Optional[float] = None,
        location: Optional[str] = None,
    ):
        self.family_id     = family_id
        self.adults        = adults        # e.g. ["Sarah", "Mike"]
        self.kids          = kids          # e.g. [{"name": "Maya", "age": 7, "notes": "lactose intolerant"}]
        self.dietary_notes = dietary_notes # e.g. "No gluten for Leo"
        self.weekly_budget = weekly_budget # e.g. 150.0
        self.location      = location      # e.g. "Denver, CO"

    def build_context(self) -> str:
        """
        Builds a plain-English family context string that gets injected
        into every Claude prompt so responses are always personalised.
        """
        kids_str = ", ".join(
            f"{k['name']} (age {k['age']}{', ' + k['notes'] if k.get('notes') else ''})"
            for k in self.kids
        ) if self.kids else "no children listed"

        adults_str = " and ".join(self.adults) if self.adults else "the parents"

        lines = [
            f"Family: {adults_str}",
            f"Children: {kids_str}",
        ]
        if self.dietary_notes:
            lines.append(f"Dietary needs: {self.dietary_notes}")
        if self.weekly_budget:
            lines.append(f"Weekly grocery budget: ${self.weekly_budget:.0f}")
        if self.location:
            lines.append(f"Location: {self.location}")

        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "family_id":     self.family_id,
            "adults":        self.adults,
            "kids":          self.kids,
            "dietary_notes": self.dietary_notes,
            "weekly_budget": self.weekly_budget,
            "location":      self.location,
        }
