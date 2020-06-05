from django.shortcuts import render, redirect
from .models import Challenge, KnitNight, Ads
from django.contrib import messages
from .forms import CreateChallenge, CreateKnit, CreateYarn
from accounts.models import CustomUser
from django.db.models import F


def my_page(request):
    mychallenges = Challenge.objects.filter(
        participants=request.user)  # Get all the challenges which have the logged in user as a participant
    myknit = KnitNight.objects.filter(
        participants=request.user)  # Get all the knit night which have the logged in user as a participant
    myads = Ads.objects.filter(
        created_by=request.user)  # Get all the ads which have the logged in user as a participant

    context = {
        'mychallenges': mychallenges,
        'myknit': myknit,
        'myads': myads,
    }
    return render(request, "my_page.html", context)


# Show a table of challenges
def challengeView(request):
    challenges = Challenge.objects.all()  # Get all the challenges in the database

    context = {
        'challenges': challenges,
    }
    return render(request, 'challenge/challenge.html', context)


# Shows a detailed view of the challenge
def challenge_detail(request, pk):
    challenges = Challenge.objects.get(pk=pk) # Using the primary key/ID to get the requested challenge
    count = Challenge.objects.values('participants').filter(pk=pk).exclude(
        participants__isnull=True).count()  # Counts the participants for a challenge
    current_user = request.user

    if request.method == "POST":
        challenges.save()
        challenges.participants.add(current_user)  # Add the current logged in user to participants
        messages.success(request, 'Du er påmeldt!')

    context = {
        'challenges': challenges,
        'count': count
    }
    return render(request, 'challenge/challenge_detail.html', context)


# Create challenge
def create_challenge(request):
    current_user = request.user  # Get the currently logged in user
    if request.method == "POST":
        form = CreateChallenge(request.POST)
        if form.is_valid():
            b = current_user
            a = form.cleaned_data["challenge_name"]
            t = form.cleaned_data["description"]
            d = form.cleaned_data["rec_user_level"]
            f = Challenge(created_by=b, challenge_name=a, description=t, rec_user_level=d)
            f.save()

            return redirect('chall')
        else:
            messages.error(request, 'Vennligst fyll ut alle feltene')

    else:
        form = CreateChallenge()

    return render(request, "challenge/create_challenge.html", {"form": form})


def deregister_challenge(request, pk):
    # Deregister from a challenge
    challenges = Challenge.objects.get(pk=pk)
    challenges.save()
    challenges.participants.remove(request.user)  # Add the current logged in user to participants

    return redirect("my_page")


# When user click on complete challenge
def complete_challenge(request):
    us = request.user
    challenges = CustomUser.objects.values('completed_challenges').filter(
        username=us)  # Get the value of completed challenges based on username
    challenges.update(completed_challenges=F('completed_challenges') + 1)  # Increment the completed challenges by 1

    # for challenge in challenges:
    #     val = challenge['completed_challenges']
    #     chall = CustomUser.objects.values('completed_challenges').filter(username=us)

    messages.success(request, 'Gratulerer, du har fullført utfordringen!')
    return redirect("my_page")


def knitView(request):
    knit = KnitNight.objects.all()  # Get all the knit nights in the database

    context = {
        'knit': knit,
    }
    return render(request, 'knit/knit.html', context)


# Shows a detailed view of the knit night
def knit_detail(request, pk):
    knit = KnitNight.objects.get(pk=pk)  # Using the primary key/ID to get the requested knit night
    count = KnitNight.objects.values('participants').filter(pk=pk).exclude(
        participants__isnull=True).count()  # Counts the participants for a knit night
    current_user = request.user

    if request.method == "POST":
        knit.save()
        knit.participants.add(current_user)  # Add the current logged in user to participants
        messages.success(request, 'Du er påmeldt!')

    context = {
        'knit': knit,
        'count': count
    }
    return render(request, 'knit/knit_detail.html', context)


def deregister_knit(request, pk):
    # Deregister from a knit night
    challenges = KnitNight.objects.get(pk=pk)
    challenges.save()
    challenges.participants.remove(request.user)  # Add the current logged in user to participants

    return redirect("my_page")


# Create knit night
def create_knit(request):
    current_user = request.user  # Get the currently logged in user
    if request.method == "POST":
        form = CreateKnit(request.POST)
        if form.is_valid():
            b = current_user
            a = form.cleaned_data["knit_name"]
            t = form.cleaned_data["description"]
            d = form.cleaned_data["time_start"]
            e = form.cleaned_data["time"]
            f = KnitNight(created_by=b, knit_name=a, description=t, time=e, time_start=d)
            f.save()

            return redirect('knit')
        else:
            messages.error(request, 'Vennligst fyll ut alle feltene')

    else:
        form = CreateKnit()

    return render(request, "knit/create_knit.html", {"form": form})


def yarnView(request):
    yarn = Ads.objects.all()  # Get all the yarn ads in the database

    context = {
        'yarn': yarn,
    }
    return render(request, 'ads/yarn.html', context)


def create_yarn(request):
    current_user = request.user  # Get the currently logged in user
    if request.method == "POST":
        form = CreateYarn(request.POST)
        if form.is_valid():
            b = current_user
            a = form.cleaned_data["yarn_name"]
            t = form.cleaned_data["description"]
            e = form.cleaned_data["url"]
            f = Ads(created_by=b, yarn_name=a, description=t, url=e)
            f.save()

            return redirect('yarn')
        else:
            messages.error(request, 'Vennligst fyll ut alle feltene')

    else:
        form = CreateYarn()

    return render(request, "ads/create_yarn.html", {"form": form})
