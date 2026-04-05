"""
features/claude_client.py
Shared Anthropic client used by all feature modules.
"""

import os
import anthropic

def get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable not set.")
    return anthropic.Anthropic(api_key=api_key)

async def ask_claude(system_prompt: str, user_message: str, max_tokens: int = 1024) -> str:
    """Single-turn Claude call. Returns the response text."""
    client = get_client()
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    return message.content[0].text

async def ask_claude_with_history(
    system_prompt: str,
    conversation_history: list,
    max_tokens: int = 1024
) -> str:
    """Multi-turn Claude call with conversation history."""
    client = get_client()
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=conversation_history
    )
    return message.content[0].text
