from django.core.management.base import BaseCommand
from api.models import Badge

class Command(BaseCommand):
    help = 'Seeds badges and achievements'

    def handle(self, *args, **kwargs):
        badges = [
            # WORKOUT BADGES
            {"name": "First Workout", "slug": "first-workout", "description": "Complete your first training session", "category": "workout", "icon": "🎯", "condition_type": "workout_count", "condition_value": 1, "xp_reward": 50},
            {"name": "Warrior", "slug": "warrior-10", "description": "Complete 10 training sessions", "category": "workout", "icon": "⚔️", "condition_type": "workout_count", "condition_value": 10, "xp_reward": 200},
            {"name": "Spartan", "slug": "spartan-25", "description": "Complete 25 training sessions", "category": "workout", "icon": "🛡️", "condition_type": "workout_count", "condition_value": 25, "xp_reward": 500},
            {"name": "Titan", "slug": "titan-50", "description": "Complete 50 training sessions", "category": "workout", "icon": "⚡", "condition_type": "workout_count", "condition_value": 50, "xp_reward": 1000},
            {"name": "Legend", "slug": "legend-100", "description": "Complete 100 training sessions", "category": "workout", "icon": "👑", "condition_type": "workout_count", "condition_value": 100, "xp_reward": 2500},
            
            # VOLUME BADGES
            {"name": "Rising Strength", "slug": "volume-1000", "description": "Lift 1000kg of total volume", "category": "workout", "icon": "💪", "condition_type": "total_volume", "condition_value": 1000, "xp_reward": 300},
            {"name": "Powerlifter", "slug": "volume-5000", "description": "Lift 5000kg of total volume", "category": "workout", "icon": "🏋️", "condition_type": "total_volume", "condition_value": 5000, "xp_reward": 800},
            {"name": "Hercules", "slug": "volume-10000", "description": "Lift 10000kg of total volume", "category": "workout", "icon": "💎", "condition_type": "total_volume", "condition_value": 10000, "xp_reward": 1500},
            
            # STREAK BADGES
            {"name": "Kickstart", "slug": "streak-3", "description": "Maintain a 3-day streak", "category": "streak", "icon": "🔥", "condition_type": "current_streak", "condition_value": 3, "xp_reward": 100},
            {"name": "Consistency", "slug": "streak-7", "description": "Maintain a 7-day streak", "category": "streak", "icon": "🔥🔥", "condition_type": "current_streak", "condition_value": 7, "xp_reward": 250},
            {"name": "Iron Discipline", "slug": "streak-14", "description": "Maintain a 14-day streak", "category": "streak", "icon": "🔥🔥🔥", "condition_type": "current_streak", "condition_value": 14, "xp_reward": 500},
            {"name": "Unstoppable", "slug": "streak-30", "description": "Maintain a 30-day streak", "category": "streak", "icon": "🌟", "condition_type": "current_streak", "condition_value": 30, "xp_reward": 1000},
            {"name": "Invincible", "slug": "streak-100", "description": "Maintain a 100-day streak", "category": "streak", "icon": "👑", "condition_type": "current_streak", "condition_value": 100, "xp_reward": 5000},
            
            # MILESTONE BADGES
            {"name": "Welcome", "slug": "welcome", "description": "Create your FitWell account", "category": "milestone", "icon": "🎉", "condition_type": "account_created", "condition_value": 1, "xp_reward": 25},
            {"name": "Planner", "slug": "first-plan", "description": "Generate your first wellness plan", "category": "milestone", "icon": "🧠", "condition_type": "plan_count", "condition_value": 1, "xp_reward": 100},
            {"name": "Level 10", "slug": "level-10", "description": "Reach level 10", "category": "milestone", "icon": "⭐", "condition_type": "level", "condition_value": 10, "xp_reward": 500},
            {"name": "Level 25", "slug": "level-25", "description": "Reach level 25", "category": "milestone", "icon": "🌟", "condition_type": "level", "condition_value": 25, "xp_reward": 1500},
            {"name": "Level 50", "slug": "level-50", "description": "Reach level 50", "category": "milestone", "icon": "💫", "condition_type": "level", "condition_value": 50, "xp_reward": 5000},
            
            # SOCIAL BADGES
            {"name": "Contributor", "slug": "first-comment", "description": "Post your first comment", "category": "social", "icon": "💬", "condition_type": "comment_count", "condition_value": 1, "xp_reward": 50},
            {"name": "Engaged", "slug": "comments-10", "description": "Post 10 comments", "category": "social", "icon": "📢", "condition_type": "comment_count", "condition_value": 10, "xp_reward": 200},
        ]

        self.stdout.write(self.style.SUCCESS(f"🏆 Seeding {len(badges)} Badges..."))
        created_count = 0
        updated_count = 0
        
        for data in badges:
            badge, created = Badge.objects.update_or_create(
                slug=data["slug"],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"   ✅ {badge.icon} {badge.name}"))
            else:
                updated_count += 1
                self.stdout.write(f"   🔄 {badge.icon} {badge.name}")
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Done! Created: {created_count} | Updated: {updated_count}"))
