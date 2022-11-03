from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from .forms import RegisterUserForm
from .models import Question, Choice, AdvUser
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class StudioLoginView(LoginView):
    template_name = 'registrations/login.html'


class StudioLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registrations/login.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'registrations/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')
