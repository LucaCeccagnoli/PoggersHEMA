from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.template import Context, Template

from articles.models import Article

# Create your views here.