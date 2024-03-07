# from django.shortcuts import render, HttpResponse
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import get_object_or_404
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView
# from django.views.generic.list import ListView
# from django.views.generic import TemplateView
# from django.views.generic.edit import FormView
# from core.decorators import login_required_view
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import AddAccount
# from .models import Account
# from django.urls import reverse_lazy
# # Create your views here.


# # class AccountHome(TemplateView):
# #     template_name = 'account/home.html'   
# class AccountHome(ListView):
#     model = Account
#     template_name = 'account/home.html' 
#     context_object_name = 'accounts'
#     # ordering=['acount_name']
#     def get_queryset(self):
#         # Filter the accounts based on the currently logged-in user
#         return Account.objects.filter(user=self.request.user)

# class AddAccountView(CreateView):
#     template_name = 'account/account-add.html'
#     form_class = AddAccount
#     model = Account
#     success_url = reverse_lazy('account-home')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

#     def get_initial(self):
#         return {'account_name': 'Punjab National Bank',
#                 'account_number': 1798001500005703,
#                 'balance': 77777}
# # class AddAccountView(TemplateView):
# #     template_name = 'account/account-add.html'
    
# #     def get(self, request, *args, **kwargs):
# #         form = AddAccount()
# #         return render(request, self.template_name, {'form': form})
    
    
# #     def post(self, request, *args, **kwargs):
# #         form = AddAccount(request.POST)
# #         if form.is_valid():
# #             new = form.save(commit=False)
# #             new.user = request.user
# #             new.save()
# #             return render(request, self.template_name, {'form': form})
    
    
# #     def get(self, request):
# #         form = AddAccount()
# #         return render(request, self.template_name, {'form': form})
    
# class AccountDetailView(LoginRequiredMixin, DetailView):
#     model = Account
#     template_name = 'account/account-detail.html'
#     context_object_name = 'account'
#     pk_url_kwarg = 'pk'

#     def get_queryset(self):
#         # Ensure that the query only includes accounts of the currently logged-in user
#         return Account.objects.filter(user=self.request.user)

#     def get_object(self, queryset=None):
#         # Override get_object to ensure it works with the filtered queryset
#         queryset = self.get_queryset()
#         return get_object_or_404(queryset, pk=self.kwargs.get(self.pk_url_kwarg))

    
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context["allaccount"] = self.model.objects.all().order_by['acount_name']
#     #     return context
        
        
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .forms import AddAccount
from .models import Account
from core.decorators import login_required_view

class AccountHome(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'account/home.html' 
    context_object_name = 'accounts'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class AddAccountView(LoginRequiredMixin, CreateView):
    template_name = 'account/account-add.html'
    form_class = AddAccount
    model = Account
    success_url = reverse_lazy('account-home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        return {
            'account_name': 'Punjab National Bank',
            'account_number': '1798001500005703',
            'balance': 77777
        }

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'account/account-detail.html'
    context_object_name = 'account'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs.get(self.pk_url_kwarg))
