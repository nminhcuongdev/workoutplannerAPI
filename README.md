# Workout Planner API

FastAPI backend tao lich tap gym bang OpenAI LLM. API duoc thiet ke de Android Kotlin MVVM Jetpack Compose goi bang JSON.

## Cai dat

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Nhap `OPENAI_API_KEY` vao file `.env`.

## Chay server

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Mo Swagger:

```text
http://localhost:8000/docs
```

## Endpoint chinh

`POST /api/v1/workout-plans`

Body mau:

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

Android DTO/Retrofit mau nam trong `docs/android-kotlin-dto.md`.

## Thong tin nen thu them tu user

API da ho tro cac field optional trong `preferences`, nhung app nen hoi them:

- So buoi tap moi tuan
- Thoi luong moi buoi
- Trinh do tap
- Chan thuong/han che van dong
- Gioi tinh, muc do hoat dong hien tai, lich sinh hoat, mon bai tap khong thich neu can ca nhan hoa sau hon
"# workoutplannerAPI"
## Phan tich tien do mot ngay tap

`POST /api/v1/workout-progress/analyze-day`

Body mau:

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

API tra ve phan tich, loi khuyen, recommendations, next_steps, safety_notes va `next_week_day` de app co the hien thi lich tap goi y cho tuan tiep theo.
