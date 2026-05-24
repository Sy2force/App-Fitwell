from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.utils.translation import gettext_lazy as _
from api.models import User, WellnessPlan, Comment, CustomEvent, DailyLog, Exercise

class DailyLogForm(forms.ModelForm):
    """
    Form for daily journal.
    Fields: Water, Sleep, Mood, Weight, Notes.
    """
    class Meta:
        model = DailyLog
        fields = ['water_liters', 'sleep_hours', 'mood', 'weight', 'notes']
        widgets = {
            'water_liters': forms.NumberInput(attrs={'step': '0.1', 'placeholder': '2.5'}),
            'sleep_hours': forms.NumberInput(attrs={'step': '0.5', 'placeholder': '7.5'}),
            'mood': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '10', 'class': 'w-full'}),
            'weight': forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'kg'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': _('Notes about your day...')}),
        }
        labels = {
            'water_liters': _('Water (L)'),
            'sleep_hours': _('Sleep (h)'),
            'mood': _('Mood (1-10)'),
            'weight': _('Weight (kg)'),
            'notes': _('Daily journal'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_classes = 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-medium'
        for field_name, field in self.fields.items():
            if field_name != 'mood': # Range input styling is different
                field.widget.attrs.update({'class': common_classes})

class CustomEventForm(forms.ModelForm):
    """
    Form to add a custom event to the calendar.
    """
    class Meta:
        model = CustomEvent
        fields = ['title', 'event_type', 'day_of_week', 'start_time', 'end_time', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Ex: Fitness Session, Morning Routine')}),
            'day_of_week': forms.Select(choices=[
                ('monday', _('Monday')),
                ('tuesday', _('Tuesday')),
                ('wednesday', _('Wednesday')),
                ('thursday', _('Thursday')),
                ('friday', _('Friday')),
                ('saturday', _('Saturday')),
                ('sunday', _('Sunday')),
            ]),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'title': _('Activity title'),
            'event_type': _('Type'),
            'day_of_week': _('Day'),
            'start_time': _('Start'),
            'end_time': _('End'),
            'priority': _('Priority'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_classes = 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-medium'
        for field in self.fields.values():
            field.widget.attrs.update({'class': common_classes})

class CustomUserCreationForm(UserCreationForm):
    """
    Custom registration form.
    Uses email and username.
    """
    class Meta:
        model = User
        fields = ('username', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-medium',
            })
            if field_name == 'username':
                field.widget.attrs['placeholder'] = _("Your name")
            elif field_name == 'email':
                field.widget.attrs['placeholder'] = _("your@email.com")

class CustomAuthenticationForm(AuthenticationForm):
    """
    Styled login form.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-medium',
            })
        self.fields['username'].widget.attrs['placeholder'] = _("Name or Email")
        self.fields['password'].widget.attrs['placeholder'] = _("Your password")

class CustomPasswordResetForm(PasswordResetForm):
    """
    Password reset request form.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-medium',
                'placeholder': _('your@email.com')
            })

class CustomSetPasswordForm(SetPasswordForm):
    """
    New password setting form.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-medium',
            })

class WellnessPlanForm(forms.ModelForm):
    """
    Form to generate a wellness plan (AI).
    Collects biometric data.
    """
    class Meta:
        model = WellnessPlan
        fields = ['age', 'gender', 'height', 'weight', 'goal', 'activity_level']
        labels = {
            'age': _('Age'),
            'gender': _('Gender'),
            'height': _('Height'),
            'weight': _('Weight'),
            'goal': _('Goal'),
            'activity_level': _("Activity level"),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definition of common classes
        common_classes = 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-bold appearance-none'
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': common_classes})
            
        # Specific placeholders
        self.fields['height'].widget.attrs['placeholder'] = 'cm'
        self.fields['weight'].widget.attrs['placeholder'] = 'kg'

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height is not None and height <= 0:
            raise forms.ValidationError(_("Height must be greater than 0."))
        return height

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and weight <= 0:
            raise forms.ValidationError(_("Weight must be greater than 0."))
        return weight
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age <= 0:
            raise forms.ValidationError(_("Age must be greater than 0."))
        return age

class CommentForm(forms.ModelForm):
    """
    Form to add a comment on an article.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full bg-white border border-gray-100 p-6 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-medium',
                'rows': 4,
                'placeholder': _('Share your opinion...')
            })
        }
        labels = {
            'content': _('Your comment')
        }

class UserUpdateForm(forms.ModelForm):
    """
    User profile update form (Email, Bio, Avatar).
    """
    class Meta:
        model = User
        fields = ['email', 'bio', 'avatar']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-medium',
                'placeholder': _('your@email.com')
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-medium',
                'rows': 3,
                'placeholder': _('Tell us about your goals...')
            }),
            'avatar': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-medium',
                'placeholder': _('Your image URL')
            })
        }
        labels = {
            'email': _('Email'),
            'bio': _('Biography'),
            'avatar': _('Avatar (URL)'),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Password change form.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text placeholder-gray-300 focus:border-tse_accent focus:ring-0 transition-all font-medium',
            })

class CustomWorkoutForm(forms.Form):
    """
    Form to configure a training session.
    Allows selecting exercises and work/rest times.
    """
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=_('Choose your movements')
    )
    work_duration = forms.IntegerField(
        initial=45,
        min_value=10,
        max_value=300,
        label=_('Work duration (sec)'),
        widget=forms.NumberInput(attrs={'class': 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text focus:border-tse_accent focus:ring-0 transition-all font-bold'})
    )
    rest_duration = forms.IntegerField(
        initial=15,
        min_value=5,
        max_value=300,
        label=_('Rest duration (sec)'),
        widget=forms.NumberInput(attrs={'class': 'w-full bg-white border border-gray-100 p-4 rounded-2xl text-tse_text focus:border-tse_accent focus:ring-0 transition-all font-bold'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom styling for checkboxes if needed, or handle in template

