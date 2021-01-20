from django import forms
from django.forms import inlineformset_factory
from nested_formset import nestedformset_factory, BaseNestedModelForm

from .models import Question, Answer, Test


class TestForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    class Meta:
        model = Test
        fields = ['name', 'description']


class QuestionForm(BaseNestedModelForm):

    text = forms.CharField(
        label='Text',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )


class AnswerForm(forms.ModelForm):

    text = forms.CharField(
        label='Text',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    is_right = forms.BooleanField(
        label='Is right',
        widget=forms.CheckboxInput(),
        required=False
    )

    class Meta:
        model = Answer
        fields = ['text', 'is_right']


QuestionAnswersFormset = nestedformset_factory(
    Test,
    Question,
    form=QuestionForm,
    nested_formset=inlineformset_factory(
        Question,
        Answer,
        form=AnswerForm,
        max_num=4,
        min_num=4,
        validate_min=True,
        extra=0,
    ),
    extra=0,
    min_num=5,
    validate_min=True,
)


class AnswerProcessForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('initial'):
            choices = kwargs['initial']['choices']
            self.fields['answers'] = forms.ChoiceField(
                choices=choices,
                label='',
                widget=forms.RadioSelect()
            )
