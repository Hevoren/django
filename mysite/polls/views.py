from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from .models import Question, Choice, User, Vote
from django.urls import reverse
from django.views import generic
from .forms import RegisterUserForm
from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import ChangeUserInfoForm
from django.db import IntegrityError


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


@login_required
def vote(request, question_id):
    question_vote = get_object_or_404(Question, pk=question_id)
    vote, created = Vote.objects.get_or_create(voter=request.user, question_vote=question_vote)
    if not created:
        return render(request, 'polls/detail.html', {
            'question': question_vote,
            'error_message': 'Голосовать можно только один раз'
        })
    try:
        selected_choice = question_vote.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question_vote,
            'error_message': 'Вы не сделали выбор'
        })

    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_vote.id,)))


class StudioLoginView(LoginView):
    template_name = 'registrations/login.html'


class StudioLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registrations/login.html'


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('polls:index')


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'registration/delete_user.html'
    success_url = reverse_lazy('polls:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin,
                         UpdateView):
    model = User
    template_name = 'registration/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('polls:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class QuestionListView(LoginRequiredMixin, generic.ListView):
    model = Question
    template_name = 'polls/question_list.html'


class QuestionCreate(CreateView):
    model = Question
    fields = ['question_text', 'description_question', 'description_choice', 'img']

    def form_valid(self, form):
        form.instance.voter = self.request.user
        form.instance.pub_date = datetime.date.today()
        return super().form_valid(form)


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('my-question')
