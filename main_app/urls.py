from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'), #about
    path('races/', views.races_index, name='index'),#all races route
    path('races/<int:race_id>/', views.races_detail, name='detail'), #race detail
    path('races/create/', views.RaceCreate.as_view(), name='races_create'), #create reace
    path('races/<int:pk>/update/', views.RaceUpdate.as_view(), name= 'races_update'), #update race
    path('races/<int:pk>/delete/', views.RaceDelete.as_view(), name='races_delete'), #delete race
    
    path('races/<int:race_id>/add_training/', views.add_training, name='add_training'), # create training
    
    path('races/<int:race_id>/assoc_goal/<int:goal_id>/', views.assoc_goal, name='assoc_goal'), # assign goal 
    path('goals/', views.GoalList.as_view(), name='goals_index'), # all goals route
    path('goals/<int:pk>/', views.GoalDetail.as_view(), name='goals_detail'), # goal detail route
    path('goals/create/', views.GoalCreate.as_view(), name='goals_create'), # create goal route
    path('goals/<int:pk>/update/', views.GoalUpdate.as_view(), name='goals_update'), # update goal route
    path('goals/<int:pk>/delete/', views.GoalDelete.as_view(), name='goals_delete'), # delete Goal route
    
    path('races/<int:race_id>/assoc_goal/<int:goal_id>', views.assoc_goal, name='assoc_goal'), #associate training with race
    path('races/<int:race_id>/add_photo/', views.add_photo, name='add_photo'), #add photo to race route
    
    path('accounts/signup/', views.signup, name='signup'), # signup route
    ]

