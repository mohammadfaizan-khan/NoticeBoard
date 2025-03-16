from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import User
from .forms import UserCreationForm

@login_required
def user_list(request):
    """View for listing all users - admin only"""
    if not request.user.is_admin():
        return HttpResponseForbidden("Only administrators can access this page.")
    
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
def create_user(request):
    """View for creating a new user - admin only"""
    if not request.user.is_admin():
        return HttpResponseForbidden("Only administrators can access this page.")
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/user_form.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def delete_user(request, user_id):
    """View for deleting a user - admin only"""
    if not request.user.is_admin():
        return HttpResponseForbidden("Only administrators can delete users.")
    
    # Get the user to delete
    user_to_delete = get_object_or_404(User, id=user_id)
    
    # Prevent admins from deleting themselves
    if user_to_delete == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('user_list')
    
    if request.method == 'POST':
        # Delete the user
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"User '{username}' has been deleted successfully.")
        return redirect('user_list')
    
    return render(request, 'accounts/user_confirm_delete.html', {'user_to_delete': user_to_delete})