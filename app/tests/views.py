from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.db import transaction
from django.db.models import Prefetch
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.views.generic.detail import DetailView

from django_filters.views import FilterView

from .filters import TestFilter
from .forms import TestForm, QuestionAnswersFormset, AnswerProcessForm
from .models import Test, Result, Answer


@method_decorator(login_required, name='dispatch')
class TestListView(FilterView):
    model = Test
    template_name = 'tests/test_list.html'
    filterset_class = TestFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('owner')


@method_decorator(login_required, name='dispatch')
class TestDetailView(DetailView):
    model = Test
    template_name = 'tests/test_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('owner')\
            .prefetch_related(
                'questions',
                Prefetch('results', queryset=Result.objects.filter(user_id=self.request.user.id))
            )


class IsTestOwnerMixin(AccessMixin):
    """Verify that the current user is test owner."""
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            return self.handle_no_permission()
        return super().get(request, *args, **kwargs)


class BaseTestFormView:
    model = Test
    form_class = TestForm

    def get_success_url(self):
        return reverse('tests:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        context = self.get_context_data()
        questions = context['questions']

        print(questions.is_valid())

        with transaction.atomic():
            form.instance.owner = self.request.user
            self.object = form.save()
            if questions.is_valid():
                questions.instance = self.object
                questions.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TestCreateView(BaseTestFormView, CreateView):

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = QuestionAnswersFormset(self.request.POST)
        else:
            data['questions'] = QuestionAnswersFormset()
        return data


@method_decorator(login_required, name='dispatch')
class TestUpdateView(BaseTestFormView, IsTestOwnerMixin, UpdateView):

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = QuestionAnswersFormset(self.request.POST, instance=self.object)
        else:
            data['questions'] = QuestionAnswersFormset(instance=self.object)
        return data


@login_required
def test_process(request, pk):
    answer_formset = formset_factory(AnswerProcessForm, extra=0)
    test = Test.objects.prefetch_related('questions', 'questions__answers').get(pk=pk)
    
    choices = []
    for question in test.questions.all():
        d = defaultdict(list)
        for answer in question.answers.all():
            d['choices'].append((answer.id, answer.text))
        choices.append(d)

    if request.method == 'POST':
        answer_formset = answer_formset(request.POST, initial=choices)
        if answer_formset.is_valid():
            answers_ids = [
                answer_form.cleaned_data.get('answers') 
                for answer_form in answer_formset 
                if answer_form.is_valid()
            ]
            n_right_answers = Answer.objects.filter(id__in=answers_ids, is_right=True).count()
            test.n_passed += 1
            with transaction.atomic():
                try:
                    results = test.results.get(user=request.user)
                    results.right_answers = n_right_answers
                    results.save()
                except Result.DoesNotExist:
                    test.results.create(test=test, user=request.user, right_answers=n_right_answers)
                test.save()
            return redirect('tests:detail', pk=test.pk)
    else:
        answer_formset = answer_formset(initial=choices)

    combined = zip(test.questions.all(), answer_formset)
    context = {
        'combined': combined,
        'answer_formset': answer_formset,
        'test': test,
    }
    return render(request, 'tests/process.html', context)
