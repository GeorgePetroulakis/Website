from django import forms
from .models import Topic, Entry, Profile


from django.contrib.auth.forms import UserCreationForm
class TopicForm(forms.ModelForm):
    class Meta:
        model=Topic
        fields=['text']
        labels={'text':''}

class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['text']
        labels={'text':''}
        widgets={'text':forms.Textarea(attrs={'cols':80})}



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'email', 'vsco_url', 'insta_url', 'snapchat_url', 'First_Name', 'Last_Name']




    
