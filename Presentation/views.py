
# from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect

from .models import Texte
from .filters import TexteFilter
from .forms import AuteurForm


def index(request):
    textes = Texte.objects.order_by("id")
    myFilter = TexteFilter(request.GET, queryset=textes)
    textes = myFilter.qs
    context = {
        'textes' : textes,
        'myFilter' : myFilter
        }
    return render(request, 'Presentation/index.html', context)


def texte(request, key):
    # gérer les erreurs
    texte = get_object_or_404(Texte, url=key)
    context = {
        'texte' : texte,
        'mouvements' : texte.mouvement_set.all()
        }
    return render(request, 'Presentation/texte.html', context)


def add(request):
    texte = get_object_or_404(Texte, title="Vénus Anadyomène")
    return render(request, 'Presentation/add.html')



def add_author(request):

    form = AuteurForm()

    if request.method == 'POST':
        form = AuteurForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('Presentation:index')

    context = {'form' : form}

    return render(request, 'Presentation/add_author.html', context)


"""
postgres://wbkyadcsvbxuxo:c0bc16d253c36491e54421aced963b00f47a953be77985bf31b8b4904334ba6f@ec2-34-201-95-176.compute-1.amazonaws.com:5432/d1vr5hrp4stq7p
postgres://wbkyadcsvbxuxo:c0bc16d253c36491e54421aced963b00f47a953be77985bf31b8b4904334ba6f@ec2-34-201-95-176.compute-1.amazonaws.com:5432/d1vr5hrp4stq7p

"""
