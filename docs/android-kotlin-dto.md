# Android Kotlin DTO

Dung voi Retrofit + kotlinx.serialization hoac Moshi/Gson. Ten field giu snake_case de khop API.

```kotlin
data class WorkoutPlanRequestDto(
    val basic_profile: BasicProfileDto,
    val body_composition: BodyCompositionDto,
    val segmental_muscle_mass: SegmentalMuscleMassDto,
    val training_goal: String,
    val equipment: List<EquipmentSelectionDto>,
    val preferences: WorkoutPreferencesDto = WorkoutPreferencesDto()
)

data class BasicProfileDto(
    val name: String,
    val age: Int,
    val height_cm: Double,
    val weight_kg: Double
)

data class BodyCompositionDto(
    val body_fat_percentage: Double? = null,
    val skeletal_muscle_mass_kg: Double? = null,
    val body_water_percentage: Double? = null,
    val visceral_fat_level: Double? = null,
    val bmr_kcal: Double? = null,
    val waist_to_hip_ratio: Double? = null
)

data class SegmentalMuscleMassDto(
    val left_arm_muscle_kg: Double? = null,
    val right_arm_muscle_kg: Double? = null,
    val trunk_muscle_kg: Double? = null,
    val left_leg_muscle_kg: Double? = null,
    val right_leg_muscle_kg: Double? = null
)

data class EquipmentSelectionDto(
    val name: String,
    val status: String
)

data class WorkoutPreferencesDto(
    val days_per_week: Int? = null,
    val session_duration_minutes: Int? = null,
    val experience_level: String? = null,
    val injuries_or_limitations: String? = null,
    val preferred_language: String = "vi"
)

interface WorkoutApi {
    @POST("api/v1/workout-plans")
    suspend fun createWorkoutPlan(
        @Body body: WorkoutPlanRequestDto
    ): WorkoutPlanResponseDto

    @GET("api/v1/equipment")
    suspend fun getEquipment(): EquipmentOptionsDto

    @GET("api/v1/training-goals")
    suspend fun getTrainingGoals(): TrainingGoalOptionsDto
}
```

Enum string dung cho app:

```text
training_goal:
build_muscle, lose_fat, gain_strength, improve_endurance, maintain_fitness

equipment.name:
dumbbells, barbell, kettlebell, treadmill, cable_machine, pull_up_bar, bench,
leg_press_machine, smith_machine, resistance_bands, medicine_ball, rowing_machine

equipment.status:
available, unavailable

experience_level:
beginner, intermediate, advanced
```
## Workout progress analysis DTO

```kotlin
data class WorkoutProgressDayAnalysisRequestDto(
    val performed_at: Long,
    val day: Int,
    val day_title: String,
    val entries: List<WorkoutProgressEntryDto>
)

data class WorkoutProgressEntryDto(
    val exercise_name: String,
    val weight_kg: Double? = null,
    val sets: Int? = null,
    val reps: Int? = null,
    val notes: String? = null
)

data class WorkoutProgressDayAnalysisResponseDto(
    val analysis_summary: String,
    val advice: String,
    val recommendations: List<String>,
    val next_steps: List<String>,
    val safety_notes: List<String>,
    val next_week_day: WorkoutDayDto,
    val model: String
)

data class WorkoutDayDto(
    val day: Int,
    val title: String,
    val focus: String,
    val warmup: List<String>,
    val exercises: List<ExerciseDto>,
    val cooldown: List<String>
)

data class ExerciseDto(
    val name: String,
    val sets: Int? = null,
    val reps: String? = null,
    val duration_minutes: Int? = null,
    val rest_seconds: Int? = null,
    val intensity: String,
    val equipment: List<String>,
    val notes: String
)
```

Them vao Retrofit interface:

```kotlin
@POST("api/v1/workout-progress/analyze-day")
suspend fun analyzeWorkoutProgressDay(
    @Body body: WorkoutProgressDayAnalysisRequestDto
): WorkoutProgressDayAnalysisResponseDto
```
