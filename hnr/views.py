from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.http import urlencode

def about(request):
    return render(request, 'about.html')