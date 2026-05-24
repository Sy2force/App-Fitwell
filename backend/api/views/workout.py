from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from api.models import WorkoutSession, ExerciseSet, Exercise
from api.serializers import (WorkoutSessionSerializer, WorkoutSessionCreateSerializer, 
                            ExerciseSetSerializer, ExerciseSetCreateSerializer, ExerciseSerializer)

class WorkoutSessionViewSet(viewsets.ModelViewSet):
    """
    API to manage workout sessions.
    - POST: Start a new session
    - GET: Retrieve session history
    - PATCH: Update a session (notes)
    - DELETE: Delete a session
    - Custom actions: complete_session, add_set
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return WorkoutSessionCreateSerializer
        return WorkoutSessionSerializer
    
    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user).prefetch_related('sets__exercise').order_by('-started_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Mark a session as completed.
        Automatically calculates duration, total volume and awards XP.
        """
        session = self.get_object()
        
        if session.status == 'completed':
            return Response({'error': 'Session already completed'}, status=status.HTTP_400_BAD_REQUEST)
        
        session.complete_session()
        
        serializer = self.get_serializer(session)
        return Response({
            'message': 'Session completed successfully',
            'xp_earned': 50 + (session.duration_minutes // 10) * 10,
            'session': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def add_set(self, request, pk=None):
        """
        Add a set to an active session.
        """
        session = self.get_object()
        
        if session.status != 'active':
            return Response({'error': 'Session is not active'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ExerciseSetCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(session=session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Retrieve user's active session (if any).
        """
        active_session = WorkoutSession.objects.filter(
            user=request.user, 
            status='active'
        ).prefetch_related('sets__exercise').first()
        
        if active_session:
            serializer = self.get_serializer(active_session)
            return Response(serializer.data)
        return Response({'message': 'No active session'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Global statistics of user's workouts.
        """
        sessions = WorkoutSession.objects.filter(user=request.user, status='completed')
        
        total_sessions = sessions.count()
        total_volume = sum(s.total_volume for s in sessions)
        total_duration = sum(s.duration_minutes for s in sessions)
        
        return Response({
            'total_sessions': total_sessions,
            'total_volume_kg': round(total_volume, 2),
            'total_duration_minutes': total_duration,
            'average_duration': round(total_duration / total_sessions, 2) if total_sessions > 0 else 0,
            'average_volume': round(total_volume / total_sessions, 2) if total_sessions > 0 else 0,
        })

class ExerciseSetViewSet(viewsets.ModelViewSet):
    """
    API to manage individual sets.
    Mainly read only, creation is done via WorkoutSession.add_set
    """
    serializer_class = ExerciseSetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ExerciseSet.objects.filter(session__user=self.request.user).select_related('exercise', 'session')

class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for exercise library (read only for users).
    """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['muscle_group', 'difficulty']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'difficulty']
