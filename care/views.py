from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from animals.models import Animal, Category
from .models import Care
from .forms import CareForm


def all_animals_care(request):
    """
    A view to show all animal care guides
    """
    animals = Animal.objects.all()
    care = Care.objects.all()
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            animals = animals.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
    #  Pagination from Django docs.
    paginator = Paginator(animals, 6)  # Show 6 results per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'animals': animals,
        'current_categories': categories,
        'care': care,
        'page_obj': page_obj,

    }

    return render(request, 'care/care.html', context)


def animal_care(request, animal_id):
    """
    View for Animal Care.
    """
    animal = get_object_or_404(Animal, pk=animal_id)
    try:
        care = Care.objects.get(animal=animal)
    except Care.DoesNotExist:
        care = Care.objects.all()
        messages.error(request, 'Sorry, this animal has no care guide yet.')
    context = {
        'animal': animal,
        'care': care,
    }
    return render(request, 'care/care_details.html', context)


@login_required
def add_care(request, animal_id):
    """ Add an care guide to animal """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only administrators can do that.')
        return redirect(reverse('home'))

    animal = get_object_or_404(Animal, pk=animal_id)
    if request.method == 'POST':
        form = CareForm(request.POST, request.FILES)
        if form.is_valid():
            if Care.objects.filter(animal=animal).exists():
                messages.error(request, 'Animal already exists')
            else:
                form = form.save()
                messages.success(request, 'Successfully added Care guide!')
                return redirect(reverse('all_animals_care'))
        else:
            messages.error(request,
                           'Failed to add care guide. Please ensure the form is \
                           valid.')
    else:
        form = CareForm()

    template = 'care/add_care.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_care(request, animal_id):
    """ Edit an care guide """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store admins can do that.')
        return redirect(reverse('home'))

    animal = get_object_or_404(Animal, pk=animal_id)
    try:
        care = Care.objects.get(animal=animal)
    except Care.DoesNotExist:
        care = Care.objects.all()
        messages.error(request, 'Sorry, this animal has no care guide yet.')
    if request.method == 'POST':
        form = CareForm(request.POST, request.FILES, instance=care)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated care guide!')
            return redirect(reverse('all_animals_care'))
        else:
            messages.error(request, 'Failed to update care guide. Please ensure \
                           the form is valid.')
    else:
        form = CareForm(instance=care)
        messages.info(request, f'You are editing {care.name}')

    template = 'care/edit_care.html'
    context = {
        'form': form,
        'animal': animal,
        'care': care,
    }

    return render(request, template, context)


@login_required
def delete_care(request, animal_id):
    """ Delete an animal """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store admins can do that.')
        return redirect(reverse('home'))
    animal = get_object_or_404(Animal, pk=animal_id)
    care = Care.objects.get(animal=animal)
    care.delete()
    messages.success(request, 'Care guide deleted!')
    return redirect(reverse('all_animals_care'))
