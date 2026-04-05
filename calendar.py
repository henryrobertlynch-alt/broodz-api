"""
features/calendar.py — Family calendar coordination.
"""

from family import FamilyProfile
from features.claude_client import ask_claude


async def coordinate_calendar(profile: FamilyProfile, request: str) -> str:
    """Handle a calendar coordination request — scheduling, conflicts, reminders."""

    system = f"""You are Brood, an organised AI assistant for busy families.
You know this family well:
{profile.build_context()}

Help coordinate the family's schedule. Be specific about times, who's involved,
and flag any likely conflicts. When suggesting calendar events, format them clearly
so they're easy to add to Google or Apple Calendar.

For each event suggest:
- Title
- Day & time
- Duration
- Who's involved
- Any prep notes"""

    user = f"""Calendar request: {request}

Help me coordinate this. If there are multiple events or people involved,
list each one clearly. Flag anything that might clash with a typical family schedule."""

    return await ask_claude(system, user, max_tokens=1000)
