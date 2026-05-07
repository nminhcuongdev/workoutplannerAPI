# Workout Planner API

FastAPI backend for generating gym workout plans and workout advice with OpenAI LLMs. The API is designed for Android Kotlin MVVM Jetpack Compose clients that exchange JSON.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your `OPENAI_API_KEY` to the `.env` file.

## Run the server

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open Swagger:

```text
http://localhost:8000/docs
```

## Core endpoint

`POST /api/v1/workout-plans`

Example body:

```json
{
  "basic_profile": {
    "name": "Minh",
    "age": 28,
    "height_cm": 175,
    "weight_kg": 72
  },
  "body_composition": {
    "body_fat_percentage": 18.5,
    "skeletal_muscle_mass_kg": 34.2,
    "body_water_percentage": 58,
    "visceral_fat_level": 7,
    "bmr_kcal": 1650,
    "waist_to_hip_ratio": 0.86
  },
  "segmental_muscle_mass": {
    "left_arm_muscle_kg": 3.2,
    "right_arm_muscle_kg": 3.3,
    "trunk_muscle_kg": 28,
    "left_leg_muscle_kg": 9.8,
    "right_leg_muscle_kg": 9.9
  },
  "training_goal": "build_muscle",
  "equipment": [
    { "name": "dumbbells", "status": "available" },
    { "name": "barbell", "status": "available" },
    { "name": "treadmill", "status": "unavailable" }
  ],
  "preferences": {
    "days_per_week": 4,
    "session_duration_minutes": 60,
    "experience_level": "intermediate",
    "injuries_or_limitations": "No known injuries",
    "preferred_language": "vi"
  }
}
```

Android DTO and Retrofit examples are in `docs/android-kotlin-dto.md`.

## Optional user inputs

The API supports optional fields in `preferences`, but the app should ask for these when needed:

- Days per week
- Session duration
- Experience level
- Injuries or movement limitations
- Gender, current activity level, daily schedule, and disliked exercises for deeper personalization

## Workout progress analysis

`POST /api/v1/workout-progress/analyze-day`

Example body:

```json
{
  "performed_at": 1777950000000,
  "day": 1,
  "day_title": "Upper Body Strength",
  "entries": [
    {
      "exercise_name": "Dumbbell Bench Press",
      "weight_kg": 22.5,
      "sets": null,
      "reps": 10,
      "notes": "Day 1 - Upper Body Strength | Planned: 4 sets - 8-10 reps - 60s rest - Moderate to High | User note: Form on, rep cuoi hoi nang"
    },
    {
      "exercise_name": "Pull-Ups",
      "weight_kg": null,
      "sets": null,
      "reps": 8,
      "notes": "Day 1 - Upper Body Strength | Planned: 3 sets - 6-8 reps - 60s rest - Moderate to High"
    }
  ]
}
```

The API returns analysis, advice, recommendations, next steps, safety notes, and `next_week_day` so the app can show a suggested plan for the next week.

## Workout advice with LLM

`POST /api/v1/workout-advice`

Example body:

```json
{
  "sent_at": 1778047200000,
  "message": "Today my shoulder hurts. Should I train?",
  "conversation_history": [
    {
      "role": "assistant",
      "content": "Ask me about today's workout, pain, recovery, nutrition, or how to adjust your current plan.",
      "created_at": 1778047100000
    },
    {
      "role": "user",
      "content": "Today my shoulder hurts. Should I train?",
      "created_at": 1778047200000
    }
  ],
  "context": {
    "profile": {
      "name": "Marcus",
      "age": 28,
      "height_cm": 170,
      "weight_kg": 63,
      "training_goal": "muscle_gain",
      "days_per_week": 5,
      "session_duration_minutes": 60,
      "experience_level": "intermediate",
      "preferred_language": "vi"
    },
    "equipment": [
      { "name": "Dumbbells", "status": "Available" },
      { "name": "Bench", "status": "Available" }
    ],
    "current_plan": { "weekly_schedule": [] },
    "today_workout": null,
    "recent_session_states": [],
    "recent_workout_logs": [],
    "data_notes": []
  }
}
```

The API returns `reply`, `recommendations`, `safety_notes`, `suggested_actions`, `needs_medical_attention`, `plan_adjustment`, and `model`. `plan_adjustment` is `null` when the LLM only needs to answer the question, or a `WorkoutDay` when it should suggest an adjusted workout.
