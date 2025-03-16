from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Notice
from .forms import NoticeForm
from accounts.models import User

@login_required
def notice_list(request):
    """View all notices - accessible by all logged in users"""
    notices = Notice.objects.all()  # Ordered by -created_at due to Meta
    return render(request, 'notices/notice_list.html', {'notices': notices})

@login_required
def create_notice(request):
    """Create a new notice - only for teachers"""
    if not request.user.is_teacher() and not request.user.is_admin():
        return HttpResponseForbidden("Only teachers can create notices.")
    
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            return redirect('notice_list')
    else:
        form = NoticeForm()
    
    return render(request, 'notices/notice_form.html', {'form': form})

@login_required
def delete_notice(request, pk):
    """Delete a notice - teachers can delete their own, admins can delete any"""
    notice = get_object_or_404(Notice, pk=pk)
    
    # Teachers can only delete their own notices
    if request.user.is_teacher() and request.user != notice.author:
        return HttpResponseForbidden("You can only delete your own notices.")
    
    # Only admins and the teacher who created the notice can delete
    if not (request.user.is_admin() or request.user == notice.author):
        return HttpResponseForbidden("You don't have permission to delete this notice.")
    
    if request.method == 'POST':
        notice.delete()
        messages.success(request, "Notice deleted successfully.")
        return redirect('notice_list')
    
    return render(request, 'notices/notice_confirm_delete.html', {'notice': notice})

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