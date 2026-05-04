import json

from fastapi import HTTPException, status
from openai import OpenAI, OpenAIError

from app.core.config import settings
from app.schemas.workout import WorkoutPlan, WorkoutPlanRequest


SYSTEM_PROMPT = """
You are a certified fitness planning assistant for a gym app.
Create practical, safe workout plans from user profile, InBody data,
segmental muscle mass, training goal, and available equipment.

Rules:
- Return only data that matches the provided schema.
- Write in the user's preferred language.
- Ask for missing information in follow_up_questions, but still produce a useful plan using clear assumptions.
- Do not diagnose medical conditions.
- If injuries, pain, abnormal body composition, or health risks are mentioned, advise consulting a qualified professional.
- Use only equipment marked as available. If equipment is unavailable, provide substitutions.
- Include warmup, cooldown, rest, intensity, weekly progression, recovery, and nutrition guidance.
"""


class OpenAIWorkoutService:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            self.client: OpenAI | None = None
            return
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate_plan(self, request: WorkoutPlanRequest) -> WorkoutPlan:
        if self.client is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY is not configured. Add it to .env.",
            )

        payload = request.model_dump(mode="json")
        user_prompt = (
            "Generate a personalized gym workout plan for this JSON input:\n"
            f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
        )

        try:
            response = self.client.responses.parse(
                model=settings.openai_model,
                instructions=SYSTEM_PROMPT,
                input=[{"role": "user", "content": user_prompt}],
                text_format=WorkoutPlan,
            )
        except OpenAIError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"OpenAI request failed: {exc}",
            ) from exc

        if response.output_parsed is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="OpenAI returned an empty workout plan.",
            )

        return response.output_parsed
