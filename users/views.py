from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

# Create your views here.

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username = new_user.username, password = request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)

def edit_profile(request):
    print("--- [VIEW EDIT_PROFILE FOI CHAMADA] ---")
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        print("--- [MODO POST ATIVADO] ---")
        u_form = UserUpdateForm(request.POST ,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        is_u_valid = u_form.is_valid()
        is_p_valid = p_form.is_valid()
        
        print(f"Formulário de User é válido? {is_u_valid}")
        print(f"Formulário de Profile é válido? {is_p_valid}")

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            print(">>> SUCESSO: Dados salvos no banco.")
            return redirect('edit_profile')
        
        else:
            print(">>> FALHA: Formulários inválidos.")
            print("Erros do User Form:", u_form.errors.as_json())
            print("Erros do Profile Form:", p_form.errors.as_json())
            print("---------------------------------")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/edit_profile.html', context)