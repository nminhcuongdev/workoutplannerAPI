from fastapi import APIRouter

from app.core.config import settings
from app.schemas.workout import (
    EquipmentName,
    TrainingGoal,
    WorkoutPlanRequest,
    WorkoutPlanResponse,
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
