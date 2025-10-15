from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Room, Hostel
from .forms import RoomForm, HostelForm


def is_admin(user):
    """Check if user is admin"""
    if user.is_superuser:
        return True
    try:
        return user.profile.role == 'admin'
    except:
        return False


@login_required
def room_list(request):
    """List all rooms"""
    rooms = Room.objects.all()
    
    # Calculate statistics
    total_rooms = rooms.count()
    # Count occupied rooms (rooms with allocations)
    from students.models import Allocation
    occupied_room_ids = Allocation.objects.values_list('room_id', flat=True).distinct()
    occupied_rooms = len(occupied_room_ids)
    available_rooms = total_rooms - occupied_rooms
    
    context = {
        'rooms': rooms,
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'available_rooms': available_rooms,
    }
    return render(request, 'rooms/room_list.html', context)


@login_required
@user_passes_test(is_admin)
def room_add(request):
    """Add new room"""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            messages.success(request, f'Room {room.room_number} added successfully!')
            return redirect('room_list')
    else:
        form = RoomForm()
    
    context = {
        'form': form,
        'title': 'Add Room',
    }
    return render(request, 'rooms/room_form.html', context)


@login_required
@user_passes_test(is_admin)
def room_edit(request, pk):
    """Edit room"""
    room = get_object_or_404(Room, pk=pk)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, f'Room {room.room_number} updated successfully!')
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    
    context = {
        'form': form,
        'title': 'Edit Room',
        'room': room,
    }
    return render(request, 'rooms/room_form.html', context)


@login_required
@user_passes_test(is_admin)
def room_delete(request, pk):
    """Delete room"""
    room = get_object_or_404(Room, pk=pk)
    
    if request.method == 'POST':
        room_number = room.room_number
        room.delete()
        messages.success(request, f'Room {room_number} deleted successfully!')
        return redirect('room_list')
    
    context = {
        'room': room,
    }
    return render(request, 'rooms/room_confirm_delete.html', context)


@login_required
def room_detail(request, pk):
    """View room details"""
    room = get_object_or_404(Room, pk=pk)
    from students.models import Allocation
    allocations = Allocation.objects.filter(room=room)
    
    context = {
        'room': room,
        'allocations': allocations,
    }
    return render(request, 'rooms/room_detail.html', context)


# Hostel Views
@login_required
def hostel_list(request):
    """List all hostels"""
    hostels = Hostel.objects.all()
    context = {
        'hostels': hostels,
    }
    return render(request, 'rooms/hostel_list.html', context)


@login_required
@user_passes_test(is_admin)
def hostel_add(request):
    """Add new hostel"""
    if request.method == 'POST':
        form = HostelForm(request.POST)
        if form.is_valid():
            hostel = form.save()
            messages.success(request, f'Hostel {hostel.name} added successfully!')
            return redirect('hostel_list')
    else:
        form = HostelForm()
    
    context = {
        'form': form,
        'title': 'Add Hostel',
    }
    return render(request, 'rooms/hostel_form.html', context)


@login_required
@user_passes_test(is_admin)
def hostel_edit(request, pk):
    """Edit hostel"""
    hostel = get_object_or_404(Hostel, pk=pk)
    
    if request.method == 'POST':
        form = HostelForm(request.POST, instance=hostel)
        if form.is_valid():
            form.save()
            messages.success(request, f'Hostel {hostel.name} updated successfully!')
            return redirect('hostel_list')
    else:
        form = HostelForm(instance=hostel)
    
    context = {
        'form': form,
        'title': 'Edit Hostel',
        'hostel': hostel,
    }
    return render(request, 'rooms/hostel_form.html', context)


@login_required
@user_passes_test(is_admin)
def hostel_delete(request, pk):
    """Delete hostel"""
    hostel = get_object_or_404(Hostel, pk=pk)
    
    if request.method == 'POST':
        hostel_name = hostel.name
        hostel.delete()
        messages.success(request, f'Hostel {hostel_name} deleted successfully!')
        return redirect('hostel_list')
    
    context = {
        'hostel': hostel,
    }
    return render(request, 'rooms/hostel_confirm_delete.html', context)


@login_required
def hostel_detail(request, pk):
    """View hostel details"""
    hostel = get_object_or_404(Hostel, pk=pk)
    rooms = hostel.rooms.all()
    
    context = {
        'hostel': hostel,
        'rooms': rooms,
    }
    return render(request, 'rooms/hostel_detail.html', context)
