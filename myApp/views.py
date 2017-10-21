from django.shortcuts import render

# Create your views here.

# Topic List to be populated in the Dropdown menu
topic = ['Donald Trump', 'Justin Bieber', 'Apple', 'Taylor Swift', 'Virat Kholi', 'Narendra Modi', 'SRK', 'NYU']

# Method loaded for the first time
def index(request):
    return render(request, 'myApp/mymap.html', {'topics':topic})

# Request sent from the form and used for subsequnet calls
def tweetsearch(request):
    if request.method == "POST":
        searchText = request.POST['dropdown-menu']

    return render(request, 'myApp/mymap.html',{'topics':topic})
