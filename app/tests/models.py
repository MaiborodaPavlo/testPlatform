from django.db import models
from django.urls import reverse


class Test(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)
    n_passed = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='tests',
        related_query_name='test',
    )
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tests:detail', kwargs={'pk': self.pk})


class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    right_answers = models.PositiveIntegerField()

    class Meta:
        unique_together = ['test', 'user']


class Question(models.Model):
    text = models.CharField(max_length=255)
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        related_query_name='question',
    )


class Answer(models.Model):
    text = models.CharField(max_length=255)
    is_right = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        related_query_name='answer',
    )

    def __str__(self):
        return self.text
