from .models import Category


def show_categories(request):
    cats = Category.objects.all()
    return {
        'cats': cats,
    }
