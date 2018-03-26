# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Question, Choice

#Classe que retorna a pagina inicial do site
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	def get_queryset(self):
		"""Retorna as 5 ultimas perguntas publicadas."""
		return Question.objects.order_by('-pub_date')[:5]

#Classe que retorna a pagina de detalhes de cada questão passa pelo id
class DetailView(generic.DetailView):
	model = Question
	template_name='polls/detail.html'

#Classe que retorna resultados de cada questão
class ResultsView(generic.DetailView):
	model = Question
	template_name='polls/results.html'

#Função para calcular votos das questões
def vote(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
