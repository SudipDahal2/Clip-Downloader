from django import forms

class DownloadForm(forms.Form):
    url = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Paste YouTube link(s)... one per line"
        })
    )

    FORMAT_CHOICES = [
        ('mp3', 'MP3 (Audio)'),
        ('mp4', 'MP4 (Video)')
    ]

    MODE_CHOICES = [
        ('single', 'Single'),
        ('bulk', 'Bulk')
    ]

    file_format = forms.ChoiceField(choices=FORMAT_CHOICES)
    mode = forms.ChoiceField(choices=MODE_CHOICES)
    quality = forms.CharField(required=False)