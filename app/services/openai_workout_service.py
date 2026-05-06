import json

from fastapi import HTTPException, status
from openai import OpenAI, OpenAIError

from app.core.config import settings
from app.schemas.workout import (
    WorkoutAdvice,
    WorkoutAdviceRequest,
    WorkoutPlan,
    WorkoutPlanRequest,
    WorkoutProgressDayAnalysis,
    WorkoutProgressDayAnalysisRequest,
)


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


PROGRESS_ANALYSIS_SYSTEM_PROMPT = """
You are a certified fitness progress analysis assistant for a gym app.
Analyze one completed workout day and recommend the next progression.

Rules:
- Return only data that matches the provided schema.
- Write in Vietnamese.
- Base recommendations on the performed entries, planned details inside notes, user notes, and safety.
- Keep advice practical and conservative. Do not over-progress if form, pain, fatigue, or missing data create uncertainty.
- If sets are missing, infer cautiously from the planned details in notes when available, and mention tracking gaps in next_steps.
- Preserve the same day number for next_week_day.
- Build next_week_day as a progressed version of the performed day with warmup, exercises, cooldown, rest, intensity, equipment, and notes.
- Do not diagnose medical conditions.
- If pain, injury, dizziness, severe discomfort, or abnormal symptoms are mentioned, advise consulting a qualified professional.
"""


ADVICE_SYSTEM_PROMPT = """
You are a certified fitness advice assistant for a gym app.
Answer the user's latest question using their profile, available equipment,
current plan, today's workout, recent session states, workout logs, and chat history.

Rules:
- Return only data that matches the provided schema.
- Write in the user's preferred language from context.profile.preferred_language.
- Keep advice practical, conservative, and specific to today's context.
- Do not diagnose medical conditions or claim to replace a clinician.
- If pain, injury, dizziness, numbness, weakness, chest pain, severe discomfort, or abnormal symptoms are mentioned, include safety guidance and set needs_medical_attention true when red flags or persistent symptoms are present.
- For pain questions, avoid recommending exercises that directly provoke pain and suggest lower-risk alternatives, recovery, or rest.
- Use suggested_actions for app-level next steps such as modify_today_workout, recovery, deload, rest_day, nutrition, hydration, or ask_follow_up.
- Set plan_adjustment to null unless a concrete replacement workout day is clearly useful and can be built safely from the available data.
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

    def analyze_progress_day(
        self, request: WorkoutProgressDayAnalysisRequest
    ) -> WorkoutProgressDayAnalysis:
        if self.client is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY is not configured. Add it to .env.",
            )

        payload = request.model_dump(mode="json")
        user_prompt = (
            "Analyze this completed workout day and recommend next week's day JSON:\n"
            f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
        )

        try:
            response = self.client.responses.parse(
                model=settings.openai_model,
                instructions=PROGRESS_ANALYSIS_SYSTEM_PROMPT,
                input=[{"role": "user", "content": user_prompt}],
                text_format=WorkoutProgressDayAnalysis,
            )
        except OpenAIError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"OpenAI request failed: {exc}",
            ) from exc

        if response.output_parsed is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="OpenAI returned an empty workout progress analysis.",
            )

        return response.output_parsed

    def advise(self, request: WorkoutAdviceRequest) -> WorkoutAdvice:
        if self.client is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY is not configured. Add it to .env.",
            )

        payload = request.model_dump(mode="json")
        user_prompt = (
            "Answer this fitness advice conversation JSON using the latest message:\n"
            f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
        )

        try:
            response = self.client.responses.parse(
                model=settings.openai_model,
                instructions=ADVICE_SYSTEM_PROMPT,
                input=[{"role": "user", "content": user_prompt}],
                text_format=WorkoutAdvice,
            )
        except OpenAIError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"OpenAI request failed: {exc}",
            ) from exc

        if response.output_parsed is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="OpenAI returned an empty workout advice response.",
            )

        return response.output_parsed



