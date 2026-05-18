from rest_framework import serializers
from api.models.program import Program, ProgramDay, ProgramExercise, UserProgramProgress


class ProgramExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)
    exercise_muscle_group = serializers.CharField(source='exercise.muscle_group', read_only=True)

    class Meta:
        model = ProgramExercise
        fields = [
            'id', 'exercise', 'exercise_name', 'exercise_muscle_group',
            'order', 'sets', 'reps', 'rest_seconds', 'weight_note', 'notes'
        ]


class ProgramDaySerializer(serializers.ModelSerializer):
    exercises = ProgramExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = ProgramDay
        fields = [
            'id', 'day_number', 'name', 'description', 'is_rest_day',
            'estimated_duration_minutes', 'exercises'
        ]


class ProgramSerializer(serializers.ModelSerializer):
    days = ProgramDaySerializer(many=True, read_only=True)

    class Meta:
        model = Program
        fields = [
            'id', 'name', 'slug', 'goal', 'level', 'duration',
            'description_short', 'description_long', 'image',
            'total_sessions', 'duration_weeks', 'nutrition_tips', 'equipment_needed',
            'created_at', 'updated_at', 'days'
        ]


class UserProgramProgressSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    progress_percentage = serializers.ReadOnlyField()

    class Meta:
        model = UserProgramProgress
        fields = [
            'id', 'user', 'program', 'program_name', 'status',
            'current_day', 'days_completed', 'progress_percentage',
            'started_at', 'completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user']
