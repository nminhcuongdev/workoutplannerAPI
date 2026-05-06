from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class TrainingGoal(str, Enum):
    build_muscle = "build_muscle"
    lose_fat = "lose_fat"
    gain_strength = "gain_strength"
    improve_endurance = "improve_endurance"
    maintain_fitness = "maintain_fitness"


class EquipmentName(str, Enum):
    dumbbells = "dumbbells"
    barbell = "barbell"
    kettlebell = "kettlebell"
    treadmill = "treadmill"
    cable_machine = "cable_machine"
    pull_up_bar = "pull_up_bar"
    bench = "bench"
    leg_press_machine = "leg_press_machine"
    smith_machine = "smith_machine"
    resistance_bands = "resistance_bands"
    medicine_ball = "medicine_ball"
    rowing_machine = "rowing_machine"


class EquipmentStatus(str, Enum):
    available = "available"
    unavailable = "unavailable"


class ExperienceLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class BasicProfile(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=13, le=90)
    height_cm: float = Field(gt=80, le=250)
    weight_kg: float = Field(gt=25, le=350)


class BodyComposition(BaseModel):
    body_fat_percentage: float | None = Field(default=None, ge=1, le=70)
    skeletal_muscle_mass_kg: float | None = Field(default=None, gt=0, le=100)
    body_water_percentage: float | None = Field(default=None, ge=20, le=80)
    visceral_fat_level: float | None = Field(default=None, ge=1, le=30)
    bmr_kcal: float | None = Field(default=None, ge=500, le=5000)
    waist_to_hip_ratio: float | None = Field(default=None, ge=0.4, le=1.5)


class SegmentalMuscleMass(BaseModel):
    left_arm_muscle_kg: float | None = Field(default=None, gt=0, le=20)
    right_arm_muscle_kg: float | None = Field(default=None, gt=0, le=20)
    trunk_muscle_kg: float | None = Field(default=None, gt=0, le=80)
    left_leg_muscle_kg: float | None = Field(default=None, gt=0, le=40)
    right_leg_muscle_kg: float | None = Field(default=None, gt=0, le=40)


class EquipmentSelection(BaseModel):
    name: EquipmentName
    status: EquipmentStatus


class WorkoutPreferences(BaseModel):
    days_per_week: int | None = Field(default=None, ge=1, le=7)
    session_duration_minutes: int | None = Field(default=None, ge=20, le=180)
    experience_level: ExperienceLevel | None = None
    injuries_or_limitations: str | None = Field(default=None, max_length=1000)
    preferred_language: str = Field(default="vi", min_length=2, max_length=10)


class WorkoutPlanRequest(BaseModel):
    basic_profile: BasicProfile
    body_composition: BodyComposition
    segmental_muscle_mass: SegmentalMuscleMass
    training_goal: TrainingGoal
    equipment: list[EquipmentSelection] = Field(min_length=1)
    preferences: WorkoutPreferences = Field(default_factory=WorkoutPreferences)

    @field_validator("equipment")
    @classmethod
    def equipment_names_must_be_unique(
        cls, equipment: list[EquipmentSelection]
    ) -> list[EquipmentSelection]:
        names = [item.name for item in equipment]
        if len(names) != len(set(names)):
            raise ValueError("Equipment names must be unique.")
        return equipment


class Exercise(BaseModel):
    name: str
    sets: int | None = None
    reps: str | None = None
    duration_minutes: int | None = None
    rest_seconds: int | None = None
    intensity: str
    equipment: list[str]
    notes: str


class WorkoutDay(BaseModel):
    day: int
    title: str
    focus: str
    warmup: list[str]
    exercises: list[Exercise]
    cooldown: list[str]


class ProgressionPlan(BaseModel):
    week: int
    instructions: str


class NutritionGuidance(BaseModel):
    calorie_guidance: str
    protein_guidance: str
    hydration_guidance: str


class WorkoutPlan(BaseModel):
    analysis_summary: str
    follow_up_questions: list[str]
    assumptions: list[str]
    weekly_schedule: list[WorkoutDay]
    progression_plan: list[ProgressionPlan]
    nutrition_guidance: NutritionGuidance
    recovery_guidance: list[str]
    safety_notes: list[str]


class WorkoutPlanResponse(BaseModel):
    plan: WorkoutPlan
    model: str


class WorkoutProgressEntry(BaseModel):
    exercise_name: str = Field(min_length=1, max_length=200)
    weight_kg: float | None = Field(default=None, gt=0, le=1000)
    sets: int | None = Field(default=None, ge=1, le=100)
    reps: int | None = Field(default=None, ge=0, le=1000)
    notes: str | None = Field(default=None, max_length=3000)


class WorkoutProgressDayAnalysisRequest(BaseModel):
    performed_at: int = Field(gt=0)
    day: int = Field(ge=1, le=365)
    day_title: str = Field(min_length=1, max_length=200)
    entries: list[WorkoutProgressEntry] = Field(min_length=1)


class WorkoutProgressDayAnalysis(BaseModel):
    analysis_summary: str
    advice: str
    recommendations: list[str]
    next_steps: list[str]
    safety_notes: list[str]
    next_week_day: WorkoutDay


class WorkoutProgressDayAnalysisResponse(WorkoutProgressDayAnalysis):
    model: str


class AdviceConversationMessage(BaseModel):
    role: str = Field(pattern="^(assistant|user)$")
    content: str = Field(min_length=1, max_length=5000)
    created_at: int = Field(gt=0)


class AdviceProfile(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    age: int | None = Field(default=None, ge=13, le=90)
    height_cm: float | None = Field(default=None, gt=80, le=250)
    weight_kg: float | None = Field(default=None, gt=25, le=350)
    body_fat_percentage: float | None = Field(default=None, ge=1, le=70)
    skeletal_muscle_mass_kg: float | None = Field(default=None, gt=0, le=100)
    body_water_liters: float | None = Field(default=None, gt=0, le=200)
    visceral_fat_level: float | None = Field(default=None, ge=1, le=30)
    bmr_kcal: float | None = Field(default=None, ge=500, le=5000)
    waist_to_hip_ratio: float | None = Field(default=None, ge=0.4, le=1.5)
    left_arm_muscle_kg: float | None = Field(default=None, gt=0, le=20)
    right_arm_muscle_kg: float | None = Field(default=None, gt=0, le=20)
    trunk_muscle_kg: float | None = Field(default=None, gt=0, le=80)
    left_leg_muscle_kg: float | None = Field(default=None, gt=0, le=40)
    right_leg_muscle_kg: float | None = Field(default=None, gt=0, le=40)
    training_goal: str | None = Field(default=None, max_length=100)
    days_per_week: int | None = Field(default=None, ge=1, le=7)
    session_duration_minutes: int | None = Field(default=None, ge=20, le=180)
    experience_level: str | None = Field(default=None, max_length=50)
    injuries_or_limitations: str | None = Field(default=None, max_length=1000)
    preferred_language: str = Field(default="vi", min_length=2, max_length=10)


class AdviceEquipment(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    status: str = Field(min_length=1, max_length=50)


class AdviceCurrentPlan(BaseModel):
    weekly_schedule: list[WorkoutDay] = Field(default_factory=list)


class AdviceSessionState(BaseModel):
    date: str = Field(min_length=1, max_length=50)
    day: int | None = Field(default=None, ge=1, le=365)
    status: str = Field(min_length=1, max_length=50)
    updated_at: int = Field(gt=0)


class AdviceContext(BaseModel):
    profile: AdviceProfile
    equipment: list[AdviceEquipment] = Field(default_factory=list)
    current_plan: AdviceCurrentPlan | None = None
    today_workout: WorkoutDay | None = None
    recent_session_states: list[AdviceSessionState] = Field(default_factory=list)
    recent_workout_logs: list[dict[str, Any]] = Field(default_factory=list)
    data_notes: list[str] = Field(default_factory=list)


class WorkoutAdviceRequest(BaseModel):
    sent_at: int = Field(gt=0)
    message: str = Field(min_length=1, max_length=5000)
    conversation_history: list[AdviceConversationMessage] = Field(
        default_factory=list,
        max_length=50,
    )
    context: AdviceContext


class WorkoutAdviceAction(BaseModel):
    type: str = Field(min_length=1, max_length=100)
    label: str = Field(min_length=1, max_length=200)
    details: str = Field(min_length=1, max_length=1000)


class WorkoutAdvice(BaseModel):
    reply: str
    recommendations: list[str]
    safety_notes: list[str]
    suggested_actions: list[WorkoutAdviceAction]
    needs_medical_attention: bool
    plan_adjustment: WorkoutDay | None = None


class WorkoutAdviceResponse(WorkoutAdvice):
    model: str

