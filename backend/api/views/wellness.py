from rest_framework import viewsets, permissions
from api.models import WellnessPlan
from api.serializers import WellnessPlanSerializer
from api.services import generate_wellness_plan

class WellnessPlanViewSet(viewsets.ModelViewSet):
    """
    API for the Planner.
    - POST: Generates a plan based on biometrics.
    - GET: Retrieves plan history.
    """
    serializer_class = WellnessPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WellnessPlan.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # 1. Get input data
        data = serializer.validated_data
        
        # 2. Generate plan via centralized service (Single Source of Truth)
        workout_plan, nutrition_plan, health_score = generate_wellness_plan(
            age=data.get('age'),
            gender=data.get('gender'),
            height=data.get('height'),
            weight=data.get('weight'),
            goal=data.get('goal'),
            activity_level=data.get('activity_level')
        )

        # 3. Save
        serializer.save(
            user=self.request.user, 
            workout_plan=workout_plan, 
            nutrition_plan=nutrition_plan
        )
        
        # 4. Update User stats
        if hasattr(self.request.user, 'stats'):
            stats = self.request.user.stats
            stats.health_score = health_score
            
            # Update sub-scores from analysis
            if 'analysis' in workout_plan and 'breakdown' in workout_plan['analysis']:
                breakdown = workout_plan['analysis']['breakdown']
                stats.fitness_score = breakdown.get('fitness', 0)
                stats.recovery_score = breakdown.get('recovery', 0)
                stats.lifestyle_score = breakdown.get('lifestyle', 0)
                stats.consistency_score = breakdown.get('consistency', 0)
            
            # Gamification: +100 XP
            stats.add_xp(100)

    def get_serializer_class(self):
        return WellnessPlanSerializer
