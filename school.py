"""
features/school.py — School admin, email drafting, and activity research.
"""

from family import FamilyProfile
from features.claude_client import ask_claude


async def draft_school_email(
    profile: FamilyProfile,
    recipient: str,
    subject: str,
    context: str
) -> str:
    """Draft a polished email to a teacher, coach, or school administrator."""

    system = f"""You are Brood, an AI assistant for busy families.
You know this family well:
{profile.build_context()}

Draft warm, professional emails on behalf of the family.
Match the tone to the recipient — slightly more formal for teachers and principals,
friendly and casual for coaches. Keep emails concise and clear.
Always sign off with the appropriate parent's name."""

    user = f"""Draft an email with the following details:

To: {recipient}
Subject: {subject}
Context: {context}

Write a complete, ready-to-send email. Keep it warm but to the point.
Include a subject line at the top."""

    return await ask_claude(system, user, max_tokens=800)


async def research_activity(
    profile: FamilyProfile,
    activity_type: str,
    age: int,
    location: str
) -> str:
    """Research and summarise local activities for a child."""

    system = f"""You are Brood, a helpful AI assistant for busy families.
You know this family well:
{profile.build_context()}

When researching activities, give practical, actionable information.
Consider cost, schedule fit for busy parents, and age appropriateness.
Be honest about what you know vs. what they should verify locally."""

    user = f"""Research {activity_type} options for a {age}-year-old in {location}.

Include:
- What to look for in a good program
- Typical cost range
- Questions to ask when calling
- Red flags to watch out for
- Best times of year to enroll

Give practical advice a busy parent can act on today."""

    return await ask_claude(system, user, max_tokens=1000)
