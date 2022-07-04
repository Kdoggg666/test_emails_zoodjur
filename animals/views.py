from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Avg
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Animal, Category, Rating
from care.models import Care
from .forms import AnimalForm, ReviewForm


def all_animals(request):
    """
    A view to show all animals, including sorting and search queries as
    well as average rating and user reviews
    """
    animals = Animal.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                animals = animals.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            animals = animals.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            animals = animals.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter \
                               any search criteria!")
                return redirect(reverse('animals'))

            queries = Q(
                        name__icontains=query) | Q(
                                                   description__icontains=query
                                                   )
            animals = animals.filter(queries)

    current_sorting = f'{sort}_{direction}'
    #  Pagination from Django docs.
    paginator = Paginator(animals, 6)  # Show 6 results per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'animals': animals,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'page_obj': page_obj,
    }

    return render(request, 'animals/animals.html', context)


def animal_details(request, animal_id):
    """
    View for Animal Details with ratings.
    """
    avg_stars = Rating.objects.all().aggregate(Avg('rating_out_of_five'))
    # for key, value in avg_stars.items():
    #     intstar = int(value)

    animal = get_object_or_404(Animal, pk=animal_id)
    try:
        care = Care.objects.get(animal=animal)
    except Care.DoesNotExist:
        care = Care.objects.all()
    ratings = Rating.objects.all()

    context = {
        'animal': animal,
        'ratings': ratings,
        'care': care,
        'avg_stars': avg_stars,
        # 'intstar': intstar,

    }
    return render(request, 'animals/animal_details.html', context)


@login_required
def add_animal(request):
    """ Add an animal to GbgZoo """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only administrators can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save()
            messages.success(request, 'Successfully added animal!')
            print('Validated')
            return redirect(reverse('animal_details', args=[animal.id]))
        else:
            messages.error(request,
                           'Failed to add animal. Please ensure the form is \
                           valid.')
            print('not Validated')
    else:
        form = AnimalForm()
        print('else')

    template = 'animals/add_animal.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_animal(request, animal_id):
    """ Edit an animal """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store admins can do that.')
        return redirect(reverse('home'))

    animal = get_object_or_404(Animal, pk=animal_id)
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated animal!')
            return redirect(reverse('animal_details', args=[animal.id]))
        else:
            messages.error(request, 'Failed to update animal. Please ensure \
                           the form is valid.')
    else:
        form = AnimalForm(instance=animal)
        messages.info(request, f'You are editing {animal.name}')

    template = 'animals/edit_animal.html'
    context = {
        'form': form,
        'animal': animal,
    }

    return render(request, template, context)


@login_required
def delete_animal(request, animal_id):
    """ Delete an animal """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store admins can do that.')
        return redirect(reverse('home'))

    animal = get_object_or_404(Animal, pk=animal_id)
    animal.delete()
    messages.success(request, 'Animal deleted!')
    return redirect(reverse('animals'))


@login_required
def add_review(request, animal_id):
    """ Add a review to an animal """
    animal = get_object_or_404(Animal, pk=animal_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Successfully added reveiw!')
            return redirect(reverse('animal_details', args=[animal.id]))
        else:
            messages.error(request,
                           'Failed to add reveiw. Please ensure the form is \
                           valid.')
    else:
        form = ReviewForm()

    template = 'animals/add_review.html'
    context = {
        'form': form,
        'animal': animal,
    }

    return render(request, template, context)


@login_required
def edit_review(request, animal_id, review_id):
    """ Edit a review """
    animal = get_object_or_404(Animal, pk=animal_id)
    review = get_object_or_404(Rating, pk=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated review!')
            return redirect(reverse('animal_details', args=[animal.id]))
        else:
            messages.error(request, 'Failed to update review. Please ensure \
                           the form is valid.')
    else:
        form = ReviewForm(instance=review)
        messages.info(request, f'You are editing the review for {animal.name}')

    template = 'animals/edit_review.html'
    context = {
        'form': form,
        'animal': animal,
    }

    return render(request, template, context)


@login_required
def delete_review(request, animal_id, review_id):
    """ Delete a review """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store admins can do that.')
        return redirect(reverse('home'))

    review = get_object_or_404(Rating, pk=review_id)
    review.delete()
    messages.success(request, 'Review deleted!')
    return redirect(reverse('animals'))
