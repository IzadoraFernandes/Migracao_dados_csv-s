from django import forms
from .models import Rating, Tag, Movie, Link, GenomeScore, GenomeTag, FileUpload


class CSVUploadForm(forms.Form):
    file = forms.FileField()

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['userId', 'movieId', 'rating', 'timestamp']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['userId', 'movieId', 'tag', 'timestamp']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['movieId', 'title', 'genres']

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['movieId', 'imdbId', 'tmdbId']

class GenomeScoreForm(forms.ModelForm):
    class Meta:
        model = GenomeScore
        fields = ['movieId', 'tagId', 'relevance']

class GenomeTagForm(forms.ModelForm):
    class Meta:
        model = GenomeTag
        fields = ['tagId', 'tag']

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file_name', 'upload_date', 'processing_time', 'records_inserted', 'records_failed', 'task_id']
