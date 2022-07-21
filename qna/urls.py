from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "qna"
urlpatterns = [
    path("question", views.question_index, name="question.index"),
    path("question/create", views.question_create, name="question.create"),
    path("question/search", views.question_search, name="question.search"),
    path("question/<int:id>/edit", views.question_edit, name="question.edit"),
    path("question/<int:id>/delete", views.question_delete, name="question.delete"),
    path("question/<slug:slug>", views.question_show, name="question.show"),
    path("answer", views.answer_index, name="answer.index"),
    path("answer/create", views.answer_create, name="answer.create"),
    path("answer/<int:id>/edit", views.answer_edit, name="answer.edit"),
    path("answer/<int:id>/delete", views.answer_delete, name="answer.delete"),
]
