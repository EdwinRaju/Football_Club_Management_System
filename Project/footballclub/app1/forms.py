from django import forms
from .models import Opponent
from datetime import timedelta  
from django import forms
from .models import TrainingSession


class OpponentForm(forms.ModelForm):
    class Meta:
        model = Opponent
        fields = ['name', 'place', 'contact_no', 'email']
from django import forms
from .models import Match

from django import forms
from .models import Match

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['date', 'venue', 'opponent']
        widgets = {
                  'date': forms.DateInput(attrs={'type': 'date', 'class': 'au-input au-input--full'}),
                  'venue': forms.TextInput(attrs={'class': 'au-input au-input--full'}),
                  'opponent': forms.Select(attrs={'class': 'form-control'}),
              }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        venue = cleaned_data.get('venue')

        if date and venue:
            if Match.objects.filter(date__in=[date, date + timedelta(days=1)], venue=venue).exists():
                self.add_error('date', 'A match is already scheduled on the selected date or the next date.')
        return cleaned_data


from django import forms
from .models import Match

class MatchResultForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['result']


from django import forms
from .models import TrainingSession
from django.utils import timezone
from django.core.exceptions import ValidationError

from django import forms
from .models import TrainingSession, Match
from django.utils import timezone

class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['date', 'venue']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError("Training date must be in the future.")

        # Check if a training session with the same date already exists
        existing_session = TrainingSession.objects.filter(date=date).first()
        if existing_session:
            raise forms.ValidationError(f"A training session for {date} already exists.")

        # Check if a match is scheduled on the same date
        if Match.objects.filter(date=date).exists():
            raise forms.ValidationError(f"A match is already scheduled for {date}.")

        return date





