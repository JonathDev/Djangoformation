# ~/projects/django-web-app/merchex/listings/views.py

from django.http import HttpResponse
from django.shortcuts import render
from listings.models import Band
from listings.models import Listing
from listings.forms import ContactUsForm
from django.core.mail import send_mail
from django.shortcuts import redirect  # ajoutez cet import
from listings.forms import BandForm, ContactUsForm, ListingForm

def band_list(request):  # renommer la fonction de vue
   bands = Band.objects.all()
   return render(request,
           'listings/band_list.html',  # pointe vers le nouveau nom de modèle
           {'bands': bands})



def about(request):
    return render(request, 'listings/about.html')

def contact(request):
    return render(request, 'listings/contact.html')

def listing_list(request):
    listings = Listing.objects.all()
    return render(request,'listings/listing_list.html', {'listings' : listings} )

def band_detail(request, band_id):
    band = Band.objects.get(id=band_id)
    return render(request, 'listings/band_detail.html', {'band': band})


def listing_detail(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    band = listing.band  # suppose que 'listing' a un champ 'band' qui est une relation vers un modèle Band
    return render(request, 'listings/listing_detail.html', {'listing': listing, 'band': band})


def contact(request):
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    if request.method == 'POST':
    # créer une instance de notre formulaire et le remplir avec les données POST
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@merchex.xyz'],
        )
        # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
        # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).
        return redirect('email-sent')  # ajoutez cette instruction de retour
    else:
    # ceci doit être une requête GET, donc créer un formulaire vide
        form = ContactUsForm()
    return render(request,
          'listings/contact.html',
          {'form': form})  # passe ce formulaire au gabarit

def email_sent(request):
    return render(request, 'listings/email_sent.html')

def band_create(request):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            # Créer une nouvelle instance « Band » et la sauvegarder dans la base de données
            band = form.save()
            # Rediriger vers la page de détail du groupe nouvellement créé
            return redirect('band_detail', band.id)   
    else:
        form = BandForm()

    return render(request, 'listings/band_create.html', {'form': form})

def create_listing(request): 
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save()
            return redirect('listing_detail', listing.id)
    else:
        form = ListingForm()

    return render(request, 'listings/create_listing.html', {'form': form})

def band_update(request, id):
    band = Band.objects.get(id=id)

    if request.method == 'POST':
        form = BandForm(request.POST, instance=band)
        if form.is_valid():
            # mettre à jour le groupe existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du groupe que nous venons de mettre à jour
            return redirect('band_detail', band.id)
    else:
        form = BandForm(instance=band)

    return render(request,
                'listings/band_update.html',
                {'form': form})

def listing_update(request, id): 
    listing = Listing.objects.get(id=id)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_detail', listing.id)
    else: 
        form = ListingForm(instance=listing)
    return render(request, 'listings/listing_update.html', {'form' : form})



def band_delete(request, band_id):
    band = Band.objects.get(id=band_id)  # nécessaire pour GET et pour POST

    if request.method == 'POST':
        # supprimer le groupe de la base de données
        band.delete()
        # rediriger vers la liste des groupes
        return redirect('band_list')

    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement

    return render(request,
                    'listings/band_delete.html',
                    {'band': band})


def listing_delete(request, id):
    lisitng = Listing.objects.get(id=id)  # nécessaire pour GET et pour POST

    if request.method == 'POST':
        # supprimer le groupe de la base de données
        lisitng.delete()
        # rediriger vers la liste des groupes
        return redirect('listing_list')

    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement

    return render(request,
                    'listings/listing_delete.html',
                    {'listing': lisitng})

"""def hello(request):
    bands = Band.objects.all()
    listings = Listing.objects.all()
    return render (request, 'listings/hello.html',{'first_band': bands[0]})
"""