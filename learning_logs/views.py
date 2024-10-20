
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Topic, Entry, Profile
from .forms import TopicForm, EntryForm, ProfileForm
from django.contrib import messages


def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required    
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required    
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def profile_search(request):
    query = request.GET.get('q', '')  # Get the search query
    results = []
    
    if query:
        # Filter users whose username contains the search query (case-insensitive)
        results = User.objects.filter(username__icontains=query)
    
    context = {'results': results, 'query': query}
    return render(request, 'learning_logs/profile_search_results.html', context)

@login_required
def select_topic_to_remove(request):
    """View to list topics for removal."""
    topics = Topic.objects.filter(owner=request.user)  # Filter by user ownership if needed
    context = {'topics': topics}
    return render(request, 'learning_logs/select_topic_to_remove.html', context)

@login_required
def remove_topic(request, topic_id):
    """Remove a specific topic."""
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        raise Http404

    # Ensure the topic belongs to the logged-in user (if required)
    if topic.owner != request.user:
        return redirect('learning_logs:topics')

    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:select_topic_to_remove')

    context = {'topic': topic}
    return render(request, 'learning_logs/confirm_delete_topic.html', context)

@login_required
def user_profile(request, user_id):
    # Get the user by their ID or return 404 if not found
    user = get_object_or_404(User, id=user_id)
    profile=user.profile

    # Pass only the user object to the context (no additional profile functionality)
    context = {'user': user,
               'email':user.email,
               'profile':profile,}
    
    return render(request, 'learning_logs/user_profile.html', context)

@login_required
def edit_user_profile(request, user_id):
    """Edit an existing user profile."""
    user = get_object_or_404(User, id=user_id)

    # Check if the user trying to edit is the logged-in user
    if user != request.user:
        return redirect('learning_logs:user_profile', user_id=request.user.id)

    profile = get_object_or_404(Profile, user=user)  # Get the user's profile

    if request.method != 'POST':
        # Initial request; pre-fill form with the current user information.
        form = ProfileForm(instance=profile)  # Use ProfileForm to edit Profile
    else:
        # POST data submitted; process data.
        form = ProfileForm(instance=profile, data=request.POST, files=request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('learning_logs:user_profile', user_id=user.id)

    context = {'form': form, 'user': user}
    return render(request, 'learning_logs/edit_user_profile.html', context)



@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile_to_follow = user_to_follow.profile

    # Add the user to the followers
    if request.user not in profile_to_follow.followers.all():
        profile_to_follow.followers.add(request.user)
       
    return redirect('learning_logs:user_profile', user_id=user_to_follow.id)

@login_required
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    profile_to_unfollow = user_to_unfollow.profile

    # Remove the user from the followers
    if request.user in profile_to_unfollow.followers.all():
        profile_to_unfollow.followers.remove(request.user)
        

    return redirect('learning_logs:user_profile', user_id=user_to_unfollow.id)
