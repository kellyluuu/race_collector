
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Race, Goal, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import boto3
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TrainingForm

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'mycatcollector'

# ----------------------------------- home ----------------------------------- #
def home(request):
    # return render(request, 'home.html')
    races = Race.objects.all()
    return render(request, 'home.html', {'races': races})

# ----------------------------------- about ---------------------------------- #
def about(request):
    return render(request, 'about.html')


# -------------------------------- SIGNUP view ------------------------------- #

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # standard signup setup with django
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


# ---------------------------------------------------------------------------- #
#                                  RACE VIEWS                                  #
# ---------------------------------------------------------------------------- #
# ------------------------------ RACE INDEX VIEW ----------------------------- #

def races_index(request):
    races = request.user.race_set.all()
    return render(request, 'races/index.html', {'races': races})

# ----------------------------- RACE DETAIL VIEW ----------------------------- #
def races_detail(request, race_id):
    race = Race.objects.get(id=race_id)
    goals_race_doesnt_have = Goal.objects.exclude(id__in = race.goals.all().values_list('id'))
    training_form = TrainingForm()
    return render(request, 'races/detail.html', {'race': race, 'training_form': training_form, 'goals': goals_race_doesnt_have })

# -------------------------------- create race ------------------------------- #
class RaceCreate(LoginRequiredMixin, CreateView):
    model = Race
    fields = ['race_name', 'race_type', 'year', 'distance', 'link']
    success_url= '/races/'
    # This inherited method is called when a
    # valid cat form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        return super().form_valid(form)
    


class RaceUpdate (LoginRequiredMixin, UpdateView):
    model = Race
    fields = ['race_name', 'race_type', 'year', 'distance', 'link']


class RaceDelete(LoginRequiredMixin, DeleteView):
    model = Race
    success_url="/races/"


# ---------------------------------------------------------------------------- #
#                                 TRAINING VIEW                                #
# ---------------------------------------------------------------------------- #

def add_training(request, race_id):
    form = TrainingForm(request.POST)
    if form.is_valid():
        new_training = form.save(commit=False)
        new_training.race_id = race_id
        new_training.save()
    return redirect('detail', race_id=race_id)





# ---------------------------------------------------------------------------- #
#                                  GOAL VIEWS                                  #
# ---------------------------------------------------------------------------- #
def assoc_goal(request, race_id, goal_id):
    Race.objects.get(id=race_id).goals.add(goal_id)
    return redirect ('detail', race_id=race_id)


class GoalList(LoginRequiredMixin, ListView):
    model = Goal
    

class GoalDetail(LoginRequiredMixin, DetailView):
    model = Goal

  
class GoalCreate(LoginRequiredMixin, CreateView):
    model = Goal
    fields = '__all__'

  
class GoalUpdate(LoginRequiredMixin, UpdateView):
    model = Goal
    fields = ['goal_race']

   
class GoalDelete(LoginRequiredMixin, DeleteView):
    model: Goal
    success_url = '/goals/'
    
    

    
    
# ---------------------------------------------------------------------------- #
#                                     PHOTO                                    #
# ---------------------------------------------------------------------------- #
def add_photo(request, race_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, race_id=race_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', race_id=race_id)
    








