from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Movie,Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'trailer_link', 'category']

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('release_date', css_class='form-group col-md-6 mb-0'),
                Column('actors', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'poster',
            'description',
            'actors',
            'trailer_link',
            'category',
            Submit('submit', 'Save')
        )

# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['text', 'rating']
