from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Member

def admin_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("dashboard")  # Redirect to dashboard
        else:
            messages.error(request, "Invalid credentials or not a superuser")
    
    return render(request, "login.html")

def admin_logout(request):
    logout(request)
    return redirect("admin-login")


@login_required
def dashboard(request):
    events = Event.objects.all()
    
    # Count total events & members
    event_count = events.count()
    member_count = Member.objects.count()
    
    # Add member count to each event
    for event in events:
        event.members_count = Member.objects.filter(event=event).count()

    return render(request, "dashboard.html", {
        "events": events,
        "event_count": event_count,
        "member_count": member_count
    })


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event-list')  # Redirect to event list after saving
    else:
        form = EventForm()
    
    return render(request, 'add_event.html', {'form': form})

def event_list(request):
    events = Event.objects.all() 
    return render(request, 'event_list.html', {'events': events})


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event-list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")  # Success message
            return redirect('event-list')  # Redirect back to event list
    
    else:
        form = EventForm(instance=event)
    
    return render(request, 'event_form.html', {'form': form, 'event': event})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':  # Confirm before deleting
        event.delete()
        messages.success(request, "Event deleted successfully!")  # Success message
        return redirect('event-list')

    return render(request, 'event_confirm_delete.html', {'event': event})


def member_list(request):
    events = Event.objects.all()
    members = Member.objects.all()
    
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, id=event_id)

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        Member.objects.create(event=event, name=name, email=email, phone=phone)
        return redirect('member-list')

    return render(request, 'member_list.html', {'events': events, 'members': members})

from django.shortcuts import render
from .models import Event, Member
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse

def event_members_page(request):
    """Display a page to select an event and show members."""
    events = Event.objects.all()  # Fetch all events
    members = None  # Default to None if no event selected yet

    if request.method == 'POST':  # If the form is submitted
        event_id = request.POST.get('event_id')  # Get selected event ID from form
        if event_id:
            event = Event.objects.get(id=event_id)  # Get the event by ID
            members = Member.objects.filter(event=event)  # Get members of the selected event

            # Generate the PDF when the form is submitted
            return generate_event_pdf(event, members)

    return render(request, 'event_members.html', {'events': events, 'members': members})


def generate_event_pdf(event, members):
    """Generate a PDF for the selected event and members."""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{event.name}_members.pdf"'

    # Create the PDF
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Create a stylesheet for the event name title
    styles = getSampleStyleSheet()
    title_style = styles['Title']

    # Prepare the data for the table
    data = [
        ['Name', 'Email', 'Phone'],  # Table headers
    ]

    # Add member data to the table
    for member in members:
        data.append([member.name, member.email, member.phone])

    # Create the table
    table = Table(data)

    # Add table style (border, background color, etc.)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Add the event name as a title at the top of the page
    event_title = Paragraph(f"<strong>{event.name}</strong>", title_style)

    # Build the PDF with the event title and table
    doc.build([event_title, table])

    return response
