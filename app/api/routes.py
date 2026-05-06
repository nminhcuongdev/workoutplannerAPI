from fastapi import APIRouter

from app.core.config import settings
from app.schemas.workout import (
    EquipmentName,
    TrainingGoal,
    WorkoutAdviceRequest,
    WorkoutAdviceResponse,
    WorkoutPlanRequest,
    WorkoutPlanResponse,
    WorkoutProgressDayAnalysisRequest,
    WorkoutProgressDayAnalysisResponse,
)
from app.services.openai_workout_service import OpenAIWorkoutService


router = APIRouter()
workout_service = OpenAIWorkoutService()


@router.get("/training-goals", tags=["Metadata"])
def get_training_goals() -> dict[str, list[str]]:
    return {"training_goals": [goal.value for goal in TrainingGoal]}


@router.get("/equipment", tags=["Metadata"])
def get_equipment() -> dict[str, list[str]]:
    return {"equipment": [equipment.value for equipment in EquipmentName]}


@router.post(
    "/workout-plans",
    response_model=WorkoutPlanResponse,
    tags=["Workout Plans"],
)
def create_workout_plan(request: WorkoutPlanRequest) -> WorkoutPlanResponse:
    plan = workout_service.generate_plan(request)
    return WorkoutPlanResponse(plan=plan, model=settings.openai_model)


@router.post(
    "/workout-progress/analyze-day",
    response_model=WorkoutProgressDayAnalysisResponse,
    tags=["Workout Progress"],
)
def analyze_workout_progress_day(
    request: WorkoutProgressDayAnalysisRequest,
) -> WorkoutProgressDayAnalysisResponse:
    analysis = workout_service.analyze_progress_day(request)
    return WorkoutProgressDayAnalysisResponse(
        **analysis.model_dump(mode="json"),
        model=settings.openai_model,
    )


@router.post(
    "/workout-advice",
    response_model=WorkoutAdviceResponse,
    tags=["Workout Advice"],
)
def create_workout_advice(request: WorkoutAdviceRequest) -> WorkoutAdviceResponse:
    advice = workout_service.advise(request)
    return WorkoutAdviceResponse(
        **advice.model_dump(mode="json"),
        model=settings.openai_model,
    )


