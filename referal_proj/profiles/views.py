from cProfile import Profile
from django.shortcuts import render
from .models import Profile

# Create your views here.
def my_recommendations_view(request):
    profile = Profile.objects.get(user=request.user)
    my_recs = profile.get_recommended_profile()   
    points = profile.points
    context = {'my_recs':my_recs, "your_points":points}
    return render(request, 'profiles/main.html', context)