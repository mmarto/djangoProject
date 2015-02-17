from django import forms
from reportsViewer.models import RequestReport

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
