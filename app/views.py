from django.shortcuts import render
from django.template import RequestContext

from .forms import CountryForm


# Create your views here.
def countries_view(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            countries = form.cleaned_data.get('countries')
            # do something with your results
    else:
        form = CountryForm

    return render(
        request,
        'render_country.html',
        {'form': form}
    )
