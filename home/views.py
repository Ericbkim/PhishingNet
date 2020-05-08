from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import *
from .read_img import get_img_text, get_text_comp
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import Profile, Post, ExpertiseTags, SubTags, Comment, Votes
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect

@login_required
def home(request):
    return render(request, 'home/home.html')

@login_required
def assigned(request):
    context = {}
    username = request.user
    userID = Profile.objects.filter(user=username).get()
    posts = Post.objects.filter(assignedUserIds=userID.userId).exclude(userId=userID.userId).order_by('-postId').all()
    context = {'posts' : posts}
    return render(request, 'home/created_Tab.html', context)

def recount_votes(context, votes):
    is_phishing = 0
    total_votes = 0
    for vote in votes:
        if vote.positive:
            is_phishing += 1
        total_votes += 1

    context["is_phishing"] = is_phishing
    context["total_votes"] = total_votes
    context["not_phishing"] = total_votes - is_phishing

@login_required
def post(request, postId):                     
    context = {}
    username = request.user
    userProfile = Profile.objects.filter(user=username).get()
    post = Post.objects.filter(postId = postId).get()
    comments = Comment.objects.filter(postId = postId).all()
    votes = Votes.objects.filter(postId = postId).all()
    context["post"] = post
    context["comments"] = comments
    context["votes"] = votes

    recount_votes(context, votes)

    user_voted = Votes.objects.filter(postId = postId).filter(userId=userProfile.userId).all()

    if request.method == 'POST':
        comment_form = CommentUploadForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)  
            instance.postId = post
            instance.userId = userProfile
            instance.save()
    context["comment_form"] = CommentUploadForm() 

    # If the user is viewing a post they've created
    if post.userId == userProfile:               
        return render(request, 'home/post_created.html', context)
    
    # If the user has voted
    elif user_voted:
        if request.method == 'POST':
            vote_form = VoteUploadForm(request.POST)
            if vote_form.is_valid():
                instance = Votes.objects.filter(postId = postId).filter(userId=userProfile.userId).get()
                is_positive = vote_form.cleaned_data.get('positive')
                instance.positive = is_positive
                print(is_positive)
                print(user_voted[0].positive)

                instance.postId = post
                instance.userId = userProfile
                instance.save()
                recount_votes(context, Votes.objects.filter(postId = postId).all())
        context["vote_form"] = VoteUploadForm()
        return render(request, 'home/post_assigned_voted.html', context)
    
    # If the user has not voted
    else:
        if request.method == 'POST':
            vote_form = VoteUploadForm(request.POST)
            if vote_form.is_valid():
                instance = vote_form.save(commit=False)
                instance.positive = vote_form.cleaned_data.get('positive')
                instance.postId = post
                instance.userId = userProfile
                instance.save()
                recount_votes(context, Votes.objects.filter(postId = postId).all())
            context["vote_form"] = VoteUploadForm()
            return render(request, 'home/post_assigned_voted.html', context)
        context["vote_form"] = VoteUploadForm()
        return render(request, 'home/post_assigned.html', context)

    return render(request, 'home/post.html', context)

@login_required
def created(request):
    context = {}
    username = request.user
    userID = Profile.objects.filter(user=username).get()
    posts = Post.objects.filter(userId=userID).order_by('-postId').all()
    context = {'posts' : posts}
    return render(request, 'home/created_Tab.html', context)


@login_required
def suggested(request):
    if request.method == 'POST':
        form = PostUploadForm(request.POST, 
                              request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            tags = form.cleaned_data.get('tags')
            instance = form.save(commit=False)
            #image = request.FILES[0]
            username = request.user
            imageText = "text"
            userID = Profile.objects.filter(user=username).get()
            post = Post.objects.create(userId=userID,
                                        title=title,
                                        image=image,
                                        imageText=imageText)
            post.assignedUserIds.set(assigned_users)
            post.tags.set(tags)


@login_required
def edit(request):
    if request.method == 'POST':
        p_change = PasswordChangeForm(request.user, request.POST)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid() and p_change.is_valid():
            u_form.save()
            p_form.save()
            p_change.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('phish-edit')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        p_change = PasswordChangeForm(request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'p_change': p_change
    }

    return render(request, 'home/edit.html', context)


@login_required
def upload(request):
    if request.method == 'POST':
        form = PostUploadForm(request.POST, 
                              request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            tags = form.cleaned_data.get('tags')
            instance = form.save(commit=False)
            username = request.user
            imageText = "text"
            userID = Profile.objects.filter(user=username).get()

            expertise_tags = set()
            for tag in tags:
                sub_tags_expertise_tags = tag.expertiseTag.all()
                for expertise_tag in sub_tags_expertise_tags:
                    expertise_tags.add(expertise_tag)

            assigned_users = set()
            for expertise_tag in expertise_tags:
                users_with_tag = Profile.objects.filter(expertiseTags=expertise_tag).exclude(userId=userID.userId).all()
                for user_with_tag in users_with_tag:
                    assigned_users.add(user_with_tag)
            
            instance.userId = userID
            instance.imageText = imageText
            instance.save()
            instance.assignedUserIds.set(assigned_users)
            instance.tags.set(tags)
            instance.save()

            postid = instance.postId

            for assigned_user in assigned_users:
                    send_mail('Your Coworker Needs Your Help', f'Go to localhost:8000/post/{postid}/ to help!', 'phishingnet480@gmail.com', [assigned_user.user.email])

            return redirect('phish-home')
    else:
        form = PostUploadForm()
    return render(request, 'home/upload_Tab.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            messages.success(request, f'Your account has been created! You are now able to log in')
            user = authenticate(username=username, password=raw_password)
            tags = form.cleaned_data.get('expertise_tags')

            profile = Profile.objects.create(user=user)
            for tag in tags:
                profile.expertiseTags.add(tag)
            profile.save()

            login(request, user)
            
            return redirect('phish-login')
    else:
        form = UserRegisterForm()
    return render(request, 'home/register.html', {'form': form})

# For testing purposes
def email(request):
    send_mail('this be title', 'this is message', 'test@test.com', ['hyukahn@umich.edu'])
    return render(request, 'home/base.html')                                                                                                      