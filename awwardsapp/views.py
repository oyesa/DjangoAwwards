from django.shortcuts import render, redirect
import datetime as dt
from django.contrib.auth.decorators import login_required









# Create your views here.
@login_required(login_url='/accounts/login')
def home(request):
  title='Crowne Awards'
  date=dt.date.today()


  return render(request, 'home.html', {'title':title, 'date':date, })
