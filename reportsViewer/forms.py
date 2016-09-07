from django import forms
from reportsViewer.models import RequestReport, Category
from django.contrib.auth.models import User

class RequestReportForm(forms.ModelForm):
    
    #title = forms.CharField(max_length=500, help_text="Please enter report title")
    #description = forms.Textarea()
    #attachment = forms.FileField()
    #frequency = forms.ChoiceField()
    #url = forms.URLField()
    
#    def __init__(self, *args, **kwargs):
#        self.user = kwargs.pop('user')
#        super(RequestReportForm, self).__init__(*args, **kwargs)
#
#    def getUserId(self):
#        return self.user
#    print(getUserId())

    class Meta:
        model = RequestReport
        #widgets = {'user': forms.HiddenInput(), 'status': forms.HiddenInput()}
        fields = ['title', 'description', 'attachment', 'frequency', 'url']

class PublishReportForm(forms.Form):
    types = (('P', 'Already Generated Report'), ('R', 'Real Time Manually Generated Report'))
    attachment = forms.FileField()
    type = forms.ChoiceField(choices=types, initial='P', widget=forms.Select(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    title = forms.CharField(max_length=1500, help_text="Please enter report title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all())
