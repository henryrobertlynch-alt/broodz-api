"""
Brood API — Family AI Assistant
Powered by Claude (Anthropic)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os

from family import FamilyProfile
from features.meal import plan_meals, generate_grocery_list
from features.calendar import coordinate_calendar
from features.school import draft_school_email, research_activity

app = FastAPI(title="Brood API", version="1.0.0")

# Allow your Netlify site to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://broodz.netlify.app",  # ← your Netlify URL
        "http://localhost:3000",        # for local testing
        "*"                             # remove this in production
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
# Request / Response models
# ─────────────────────────────────────────

class FamilyProfileRequest(BaseModel):
    family_id: str
    adults: List[str]
    kids: List[dict]          # [{"name": "Maya", "age": 7, "notes": "lactose intolerant"}]
    dietary_notes: Optional[str] = None
    weekly_budget: Optional[float] = None
    location: Optional[str] = None

class MealPlanRequest(BaseModel):
    family_id: str
    week_notes: Optional[str] = None   # e.g. "soccer Tuesday, date night Friday"
    days: Optional[int] = 7

class GroceryRequest(BaseModel):
    family_id: str
    meal_plan: str

class CalendarRequest(BaseModel):
    family_id: str
    request: str               # e.g. "Add soccer pickup Tuesday 4pm for both parents"

class SchoolEmailRequest(BaseModel):
    family_id: str
    recipient: str             # e.g. "Coach Mike", "Mrs Johnson"
    subject: str
    context: str               # e.g. "Maya will miss practice Thursday — family trip"

class ActivityRequest(BaseModel):
    family_id: str
    activity_type: str         # e.g. "soccer camp", "piano lessons"
    age: int
    location: str

class ChatRequest(BaseModel):
    family_id: str
    message: str
    conversation_history: Optional[List[dict]] = []

# In-memory family store (swap for a database later)
family_store: dict = {}

# ─────────────────────────────────────────
# Routes
# ─────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "Brood API is running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok"}

# — Family Profile —

@app.post("/family/setup")
def setup_family(req: FamilyProfileRequest):
    """Save a family's profile so Brood knows their context."""
    profile = FamilyProfile(
        family_id=req.family_id,
        adults=req.adults,
        kids=req.kids,
        dietary_notes=req.dietary_notes,
        weekly_budget=req.weekly_budget,
        location=req.location
    )
    family_store[req.family_id] = profile
    return {"success": True, "message": f"Family profile saved for {req.family_id}"}

@app.get("/family/{family_id}")
def get_family(family_id: str):
    """Retrieve a family's profile."""
    profile = family_store.get(family_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Family not found")
    return profile.to_dict()

# — Meal Planning —

@app.post("/meals/plan")
async def meal_plan(req: MealPlanRequest):
    """Generate a weekly meal plan tailored to the family."""
    profile = _get_profile(req.family_id)
    result = await plan_meals(profile, req.week_notes, req.days)
    return {"success": True, "meal_plan": result}

@app.post("/meals/grocery-list")
async def grocery_list(req: GroceryRequest):
    """Turn a meal plan into a consolidated grocery list."""
    profile = _get_profile(req.family_id)
    result = await generate_grocery_list(profile, req.meal_plan)
    return {"success": True, "grocery_list": result}

# — Calendar —

@app.post("/calendar/coordinate")
async def calendar(req: CalendarRequest):
    """Handle a calendar coordination request."""
    profile = _get_profile(req.family_id)
    result = await coordinate_calendar(profile, req.request)
    return {"success": True, "response": result}

# — School & Activity Admin —

@app.post("/school/email")
async def school_email(req: SchoolEmailRequest):
    """Draft an email to a teacher, coach, or school admin."""
    profile = _get_profile(req.family_id)
    result = await draft_school_email(profile, req.recipient, req.subject, req.context)
    return {"success": True, "draft": result}

@app.post("/school/research-activity")
async def activity_research(req: ActivityRequest):
    """Research local activities for a child."""
    profile = _get_profile(req.family_id)
    result = await research_activity(profile, req.activity_type, req.age, req.location)
    return {"success": True, "results": result}

# — General Chat —

@app.post("/chat")
async def chat(req: ChatRequest):
    """
    General-purpose family assistant chat.
    Brood figures out what the family needs and routes to the right feature.
    """
    from features.chat import handle_chat
    profile = _get_profile(req.family_id)
    result = await handle_chat(profile, req.message, req.conversation_history)
    return {"success": True, "response": result}

# ─────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────

def _get_profile(family_id: str) -> FamilyProfile:
    profile = family_store.get(family_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"No family profile found for '{family_id}'. Call /family/setup first.")
    return profile
