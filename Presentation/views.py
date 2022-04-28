
# from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect

from .models import Mouvement, Texte, Ligne
from .filters import TexteFilter
from .forms import *


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

'''
def add(request):
    # ajouter un texte et des mouvements 
    
    if request.method == 'POST': 
        #print(1)
        tform = TexteForm(request.POST)
        mformslist = [(MouvementForm(request.POST),LigneInlineFormSet(request.POST, request.FILES)) for _ in range(6)]
        lformset = LigneInlineFormSet(request.POST, request.FILES)
        #print(2)
        if tform.is_valid():
            new_texte = tform.save()
            #print(3)
            for mf, lformset in mformslist:

                new_mvt = mf.save(commit=False)
                #print(4)
                #print(new_mvt.title)
                if new_mvt.title + new_mvt.range != '':
                    
                    #print(5)
                    new_mvt.texte = new_texte
                    new_mvt.save()
                    if lformset.is_valid():
                        #print(6)
                        for lf in lformset:
                            new_ligne = lf.save(commit=False)
                            #print(7)
                            if new_ligne.citation + new_ligne.outil + new_ligne.analyse !='':
                                #print(8)
                                new_ligne.mouvement = new_mvt
                                new_ligne.save()
            
            new_text = tform.save()
            for mform in mformslist:
                new_mvt = mform.save(commit=False)
                if new_mvt.title + new_mvt.range != '':
                    new_mvt.texte = new_text
                    new_mvt.save()
                
            return redirect('Presentation:texte', key=tform.instance.url)
    
    else: 
        tform = TexteForm()
        mformslist = [(MouvementForm(), LigneInlineFormSet()) for _ in range(6)]
        lformset = LigneInlineFormSet()
    #            modifier la template 
    return render(request, 'Presentation/add.html', {'tform':tform, 'mformslist':mformslist, 'lformset':lformset})
'''



def add_author(request):

    form = AuteurForm()

    if request.method == 'POST':
        form = AuteurForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('Presentation:index')

    context = {'form' : form}

    return render(request, 'Presentation/add_author.html', context)
