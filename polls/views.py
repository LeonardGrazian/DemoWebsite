from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Question


class ResultsView(generic.DetailView):
    template_name = 'polls/result.html'
    model = Question


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # re-serve voting form
        return render(request,
                        'polls/detail.html',
                        { 'question': question,
                            'error_message': 'You did not select a choice'
                        })
    else:
        selected_choice.choice_votes += 1
        selected_choice.save()
        # alwasy return an HttpResponseRedirect after processing POST data
        # this prevents a duplicate post if user hits the back button
        return HttpResponseRedirect(reverse('polls:result', args=(question_id,)))
