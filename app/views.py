# views.py

from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View, FormView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from .forms import *
from .models import RealEstate, LeaseContract, Notifications, Photo, Mailling
from django.http import HttpResponseRedirect
from django.db.models import Avg
from django.utils.timezone import make_aware


from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime

class SearchPage(ListView):
    model = RealEstate
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context


class SearchResults(ListView):
    model = RealEstate
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 3
    

    def get_queryset(self):
        queryset = RealEstate.objects.all()

        title = self.request.GET.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)

        property_type = self.request.GET.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type__icontains=property_type)

        area_from = self.request.GET.get('area_from')
        if area_from:
            queryset = queryset.filter(area__gte=area_from)

        area_to = self.request.GET.get('area_to')
        if area_to:
            queryset = queryset.filter(area__lte=area_to)

        num_rooms_from = self.request.GET.get('num_rooms_from')
        if num_rooms_from:
            queryset = queryset.filter(num_rooms__gte=num_rooms_from)
        
        num_rooms = self.request.GET.get('num_rooms')
        if num_rooms:
            queryset = queryset.filter(num_rooms=num_rooms)

        num_rooms_to = self.request.GET.get('num_rooms_to')
        if num_rooms_to:
            queryset = queryset.filter(num_rooms__lte=num_rooms_to)

        bath_rooms_from = self.request.GET.get('bath_rooms_from')
        if bath_rooms_from:
            queryset = queryset.filter(bath_rooms__gte=bath_rooms_from)

        bath_rooms_to = self.request.GET.get('bath_rooms_to')
        if bath_rooms_to:
            queryset = queryset.filter(bath_rooms__lte=bath_rooms_to)

        bed_rooms_from = self.request.GET.get('bed_rooms_from')
        if bed_rooms_from:
            queryset = queryset.filter(bed_rooms__gte=bed_rooms_from)

        bed_rooms_to = self.request.GET.get('bed_rooms_to')
        if bed_rooms_to:
            queryset = queryset.filter(bed_rooms__lte=bed_rooms_to)

        address = self.request.GET.get('address')
        if address:
            queryset = queryset.filter(address__icontains=address)

        district_location = self.request.GET.get('district_location')
        if district_location:
            queryset = queryset.filter(district_location__icontains=district_location)

        rent_cost_from = self.request.GET.get('rent_cost_from')
        if rent_cost_from:
            queryset = queryset.filter(rent_cost__gte=rent_cost_from)

        rent_cost_to = self.request.GET.get('rent_cost_to')
        if rent_cost_to:
            queryset = queryset.filter(rent_cost__lte=rent_cost_to)

        rent_type = self.request.GET.get('rent_type')
        if rent_type:
            queryset = queryset.filter(rent_type=rent_type)

        order = self.request.GET.get('order')
        if order:
            if order=="new":
                queryset = queryset.order_by("-update_date")
            elif order=="old":
                queryset = queryset.order_by("update_date")
            elif order=="cheep":
                queryset = queryset.order_by("rent_cost")
            elif order=="expen":
                queryset = queryset.order_by("-rent_cost")

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        # Преобразование строки в объект datetime

        if start_date or end_date:
            if end_date:
                end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
            if start_date:
                start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
            ids = []
            for i in queryset:
                ok = True
                for j in i.lease_contracts.all():
                    if start_date and start_date >= j.start_date and start_date <= j.end_date:
                        ok = False
                        break
                    elif end_date and end_date >= j.start_date and end_date <= j.end_date:
                        ok = False
                        break
                if ok:
                    ids.append(i.pk)
            queryset = queryset.filter(pk__in=ids)

        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['liked'] = list(Favorites.objects.filter(user=self.request.user).values_list('property', flat=True))
        context['q'] = self.request.GET.get('q')
        context['current_url'] = self.request.build_absolute_uri()
        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context
    
    def post(self, request, *args, **kwargs):
        obj = RealEstate.objects.get(pk=request.POST.get('prop_id'))
        if request.POST.get('form_submit') == 'like':
            favotite = Favorites(user=self.request.user, property=obj)
            favotite.save()
            obj.liked += 1
            obj.save()
        elif request.POST.get('form_submit') == 'unlike':
            Favorites.objects.get(user=self.request.user, property=obj).delete()
            obj.liked -= 1
            obj.save()

        return redirect(self.request.POST.get('current_url', SearchResults.as_view()))

class property_detail(DetailView):
    model = RealEstate
    template_name = "property_detail.html"
    pk_url_kwarg = "property_id"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['liked'] = Favorites.objects.filter(user=self.request.user).exists()
            context['applied'] = LeaseContract.objects.filter(tenant=self.request.user, applied=True, property=self.object).exists()
        context['avg_rating'] = self.object.reviews.aggregate(avg_rating=Avg('rate'))['avg_rating']

        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context

    def post(self, request, *args, **kwargs):
        obj = super().get_object(queryset=None)
        if request.POST.get('form_submit') == 'like':
            favotite = Favorites(user=self.request.user, property=obj)
            favotite.save()
            obj.liked += 1
            obj.save()
        elif request.POST.get('form_submit') == 'unlike':
            Favorites.objects.get(user=self.request.user).delete()
            obj.liked -= 1
            obj.save()
        elif request.POST.get('form_submit') == 'review':
            rate = request.POST.get('rate')
            review = Reviews(user=self.request.user, property=obj, rate=rate)
            comment = request.POST.get('comment')
            if comment:
                review.comment = comment
            review.save()

        elif request.POST.get('form_submit') == 'book':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            property = self.get_object()
            owner = self.get_object().owner
            tenant = request.user

            lease_contract = LeaseContract(
                start_date=start_date,
                end_date=end_date,
                property=property,
                owner=owner,
                tenant=tenant
            )
            lease_contract.save()
            notification = Notifications(user=owner, type=1)
            notification.save()
            if Mailling.objects.filter(user=owner).exists():
                send_email("New application\nGo check it", "Notification", Mailling.objects.get(user=owner).email)
        return redirect('property_detail', property_id=self.kwargs.get('property_id'))

class property_reviews(ListView):
    model = Reviews
    template_name = "reviews.html"
    context_object_name = 'reviews'
    paginate_by = 3

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        property = get_object_or_404(RealEstate, pk=property_id)
        return Reviews.objects.filter(property=property)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        property_id = self.kwargs.get('property_id')
        context['post'] = get_object_or_404(RealEstate, pk=property_id)
        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "signup.html"
    success_url = reverse_lazy("search")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")

class LoginUser(LoginView):
    authentication_form = LoginUserForm
    template_name = "login.html"
    def get_success_url(self) -> str:
        return reverse_lazy("home")

def logout_user(request):
    logout(request)
    return redirect("home")

class landlord_add_property(LoginRequiredMixin, View):
    template_name = 'landlord_add_property.html'
    login_url =  reverse_lazy('login')

    def get(self, request):
        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False
        return render(request, self.template_name, {'notifications_num': notifications_num, 'email_passed': email_passed})

    def post(self, request):
        # Получение данных из формы
        title = request.POST.get('title')
        property_type = request.POST.get('property_type')
        area = request.POST.get('area')
        num_rooms = request.POST.get('num_rooms')
        bath_rooms = request.POST.get('bath_rooms')
        bed_rooms = request.POST.get('bed_rooms')
        address = request.POST.get('address')
        district_location = request.POST.get('district_location')
        rent_cost = request.POST.get('rent_cost')
        rent_type = request.POST.get('rent_type')
        description = request.POST.get('description')
        owner_number = request.POST.get('owner_number')
        whatsapp = request.POST.get('whatsapp', False)
        telegram = request.POST.get('telegram')

        # Создание объекта RealEstate
        real_estate = RealEstate.objects.create(
            title=title,
            property_type=property_type,
            area=area,
            address=address,
            district_location=district_location,
            rent_cost=rent_cost,
            rent_type=rent_type,
            description=description,
            owner = request.user,
            owner_number=owner_number,
            whatsapp=whatsapp,
            telegram=telegram,
        )
        if owner_number:
            real_estate.owner_number = owner_number
        if whatsapp is not None:
            real_estate.whatsapp = whatsapp
        if telegram:
            real_estate.telegram = telegram
        if num_rooms:
            real_estate.num_rooms = num_rooms
        if bath_rooms:
            real_estate.bath_rooms = bath_rooms
        if bed_rooms:
            real_estate.bed_rooms = bed_rooms

        order = 0
        for image in request.FILES.getlist('photos'):
            order += 1
            photo = Photo.objects.create(image=image, order=order)
            real_estate.photos.add(photo)
        real_estate.save()
        # Перенаправление после успешного сохранения
        return redirect('landlord_add_property')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context
    
def about(request):
    notifications_num = 0
    email_passed = True
    if request.user.is_authenticated:
        notifications_num = Notifications.objects.filter(user=request.user).count()
        if Mailling.objects.filter(user=request.user).exists():
            email_passed = True
        else:
            email_passed = False
    return render(request, 'about.html', {'notifications_num': notifications_num, 'email_passed': email_passed})


class ContactView(FormView):
    form_class = ContactForm
    template_name = "contact.html"
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        # Обработка успешного ввода данных формы
        instance = form.save()
        # Дополнительный код, если это необходимо
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context

def home(request):
    if request.method == 'POST':
        notifications_num = 0
        if request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=request.user).count()
        mailling = Mailling(user=request.user, email=request.POST.get('email'))
        mailling.save()
        return render(request, 'index.html', {'notifications_num': notifications_num, 'email_passed': True})
    else:
        notifications_num = 0
        email_passed = True
        if request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=request.user).count()
            if Mailling.objects.filter(user=request.user).exists():
                email_passed = True
            else:
                email_passed = False
        return render(request, 'index.html', {'notifications_num': notifications_num, 'email_passed': email_passed})

def user_account(request, user_id):
    get_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        get_user.username = request.POST['username']
        get_user.first_name = request.POST['first_name']
        get_user.last_name = request.POST['last_name']
        get_user.email = request.POST['email']
        get_user.save()

        notifications_num = 0
        email_passed = True
        if request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=request.user).count()
            if Mailling.objects.filter(user=request.user).exists():
                email_passed = True
            else:
                email_passed = False

        return redirect('user_account', user_id=get_user.pk)
    notifications_num = 0
    email_passed = True
    if request.user.is_authenticated:
        notifications_num = Notifications.objects.filter(user=request.user).count()
        if Mailling.objects.filter(user=request.user).exists():
            email_passed = True
        else:
            email_passed = False
    return render(request, "user_account.html", {"get_user": get_user, 'notifications_num': notifications_num, 'email_passed': email_passed})

class user_account_properties(LoginRequiredMixin, ListView):
    model = RealEstate
    login_url =  reverse_lazy('login')
    template_name = "user_account_properties.html"
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        return RealEstate.objects.filter(owner=user)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == "delete":
            real_estate = get_object_or_404(RealEstate, pk=request.POST.get('pk'))
            Photo.objects.filter(real_estate=real_estate).delete()
            real_estate.delete()
        elif request.POST.get('action') == "update":
            obj = get_object_or_404(RealEstate, pk=request.POST.get('pk'))

            title = request.POST.get('title')
            property_type = request.POST.get('property_type')
            area = request.POST.get('area')
            num_rooms = request.POST.get('num_rooms')
            bath_rooms = request.POST.get('bath_rooms')
            bed_rooms = request.POST.get('bed_rooms')
            address = request.POST.get('address')
            district_location = request.POST.get('district_location')
            rent_cost = request.POST.get('rent_cost')
            rent_type = request.POST.get('rent_type')
            description = request.POST.get('description')
            owner_number = request.POST.get('owner_number')
            whatsapp = request.POST.get('whatsapp', False)
            telegram = request.POST.get('telegram')

            obj.title = title
            obj.property_type = property_type
            obj.area = area
            obj.num_rooms = num_rooms
            obj.bath_rooms = bath_rooms
            obj.bed_rooms = bed_rooms
            obj.address = address
            obj.district_location = district_location
            obj.rent_cost = rent_cost
            obj.rent_type = rent_type
            obj.description = description
            obj.owner_number = owner_number
            obj.whatsapp = whatsapp
            obj.telegram = telegram

            # Сохранение изменений в базе данных
            obj.save()
        return HttpResponseRedirect(reverse('user_account_properties', kwargs={'user_id': self.kwargs['user_id']}))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context
    
class user_account_applications(LoginRequiredMixin, ListView):
    model = LeaseContract
    login_url = reverse_lazy('login')
    template_name = "user_account_applications.html"
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        get_user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        return LeaseContract.objects.filter(applied=False).filter(owner=get_user)
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'confirm':
            pk = request.POST.get('pk')
            lease_contract = get_object_or_404(LeaseContract, pk=pk)
            lease_contract.applied = True
            lease_contract.save()
            notification = Notifications(user=lease_contract.tenant, type=2)
            notification.save()
            if Mailling.objects.filter(user=lease_contract.tenant).exists():
                send_email("Your application is confirmed!", "Notification", Mailling.objects.get(user=lease_contract.tenant).email)
        elif request.POST.get('action') == 'deny':
            pk = request.POST.get('pk')
            lease_contract = get_object_or_404(LeaseContract, pk=pk)
            lease_contract.delete()
            notification = Notifications(user=lease_contract.tenant, type=3)
            notification.save()
            if Mailling.objects.filter(user=lease_contract.tenant).exists():
                send_email("Your application is denied", "Notification", Mailling.objects.get(user=lease_contract.tenant).email)
        elif request.POST.get('action') == 'notification':
            pk = request.POST.get('pk')
            Notifications.objects.get(pk=pk).delete()
        return redirect('user_account_applications', user_id=self.kwargs.get('user_id'))
    
class user_account_contracts(LoginRequiredMixin, ListView):
    model = LeaseContract
    login_url = reverse_lazy('login')
    template_name = "user_account_contracts.html"
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        get_user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        return LeaseContract.objects.filter(applied=True).filter(owner=get_user)
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'deny':
            pk = request.POST.get('pk')
            lease_contract = get_object_or_404(LeaseContract, pk=pk)
            lease_contract.delete()
            notification = Notifications(user=lease_contract.tenant, type=4)
            notification.save()
            if Mailling.objects.filter(user=lease_contract.tenant).exists():
                send_email("Your rent is denied", "Notification", Mailling.objects.get(user=lease_contract.tenant).email)
        return redirect('user_account_contracts', user_id=self.kwargs.get('user_id'))
    
class user_account_rents(LoginRequiredMixin, ListView):
    model = LeaseContract
    login_url = reverse_lazy('login')
    template_name = "user_account_rents.html"
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        get_user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        return LeaseContract.objects.filter(applied=True).filter(tenant=get_user)
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'deny':
            pk = request.POST.get('pk')
            lease_contract = get_object_or_404(LeaseContract, pk=pk)
            lease_contract.delete()
            notification = Notifications(user=lease_contract.tenant, type=4)
            notification.save()
            if Mailling.objects.filter(user=lease_contract.tenant).exists():
                send_email("Your rent is denied", "Notification", Mailling.objects.get(user=lease_contract.tenant).email)
        return redirect('user_account_contracts', user_id=self.kwargs.get('user_id'))
    
class landlord_update_property(DetailView):
    model = RealEstate
    template_name = "landlord_update_property.html"
    pk_url_kwarg = "property_id"
    context_object_name = "post"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context
        
    
class NotificationsView(LoginRequiredMixin, ListView):
    model = Notifications
    login_url =  reverse_lazy('login')
    template_name = "notifications.html"
    context_object_name = "notifications"
    paginate_by = 3

    def get_queryset(self):
        return Notifications.objects.filter(user=self.request.user)  
    
    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk')
        Notifications.objects.get(pk=pk).delete()
        return redirect(reverse('notifications'))
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False

        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context

def send_email(text, title, *emails):
    email_sender = "project.django@mail.ru"
    email_getters = emails

    smtp_server = SMTP("smtp.mail.ru", 587)
    smtp_server.starttls()

    smtp_server.login(email_sender, 'uZLLDURsAGB7ns3b5ADt')

    subject = title
    body = text
    message = MIMEMultipart()
    message["From"] = email_sender
    message["To"] = ', '.join(email_getters)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    smtp_server.sendmail(email_sender, email_getters, message.as_string())

class FavoritesView(LoginRequiredMixin, ListView):
    model = Favorites
    login_url =  reverse_lazy('login')
    template_name = "favorites.html"
    context_object_name = "favorites"
    paginate_by = 3

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user)  
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        notifications_num = 0
        email_passed = True
        if self.request.user.is_authenticated:
            notifications_num = Notifications.objects.filter(user=self.request.user).count()
            if Mailling.objects.filter(user=self.request.user).exists():
                email_passed = True
            else:
                email_passed = False
        if self.request.user.is_authenticated:
            context['liked'] = list(Favorites.objects.filter(user=self.request.user).values_list('property', flat=True))
        context['notifications_num'] = notifications_num
        context['email_passed'] = email_passed
        return context
    
    def post(self, request, *args, **kwargs):
        obj = RealEstate.objects.get(pk=request.POST.get('prop_id'))
        if request.POST.get('form_submit') == 'like':
            favotite = Favorites(user=self.request.user, property=obj)
            favotite.save()
            obj.liked += 1
            obj.save()
        elif request.POST.get('form_submit') == 'unlike':
            Favorites.objects.get(user=self.request.user, property=obj).delete()
            obj.liked -= 1
            obj.save()
        return redirect('favorites')

def landlord_update_photos(request, property_id):
    post = get_object_or_404(RealEstate, pk=property_id)
    if request.method == 'POST':
        if 'add_photo' in request.POST:
            new_photo_image = request.FILES.get('new_photo_image')
            photo_id = request.POST.get('add_photo')
            photo = get_object_or_404(Photo, id=photo_id)
            order = photo.order + 1
            post.photos.filter(order__gte=order).update(order=models.F('order') + 1)
            new_photo = Photo.objects.create(image=new_photo_image, order=order)
            post.photos.add(new_photo)
            post.save()

            notifications_num = 0
            email_passed = True
            if request.user.is_authenticated:
                notifications_num = Notifications.objects.filter(user=request.user).count()
            if Mailling.objects.filter(user=request.user).exists():
                email_passed = True
            else:
                email_passed = False
            return redirect(reverse('landlord_update_photos', kwargs={'property_id': property_id}))
        
        elif 'add_first_photo' in request.POST:
            new_photo_image = request.FILES.get('new_photo_image')
            order = 1
            post.photos.all().update(order=models.F('order') + 1)
            new_photo = Photo.objects.create(image=new_photo_image, order=order)
            post.photos.add(new_photo)
            post.save()

            notifications_num = 0
            email_passed = True
            if request.user.is_authenticated:
                notifications_num = Notifications.objects.filter(user=request.user).count()
            if Mailling.objects.filter(user=request.user).exists():
                email_passed = True
            else:
                email_passed = False
            return redirect(reverse('landlord_update_photos', kwargs={'property_id': property_id}))
        
        elif 'remove_photo' in request.POST:
            photo_id = request.POST.get('remove_photo')
            photo = get_object_or_404(Photo, id=photo_id)
            photo_order = photo.order
            photo.delete()

            # Обновление order для фотографий после удаленной
            post.photos.filter(order__gt=photo_order).update(order=models.F('order') - 1)
            post.save()

            notifications_num = 0
            email_passed = True
            if request.user.is_authenticated:
                notifications_num = Notifications.objects.filter(user=request.user).count()
            if Mailling.objects.filter(user=request.user).exists():
                email_passed = True
            else:
                email_passed = False
            return redirect(reverse('landlord_update_photos', kwargs={'property_id': property_id}))
    notifications_num = 0
    email_passed = True
    if request.user.is_authenticated:
        notifications_num = Notifications.objects.filter(user=request.user).count()
    if Mailling.objects.filter(user=request.user).exists():
        email_passed = True
    else:
        email_passed = False
    return render(request, 'landlord_update_photos.html', {'post': post, 'notifications_num': notifications_num, 'email_passed': email_passed, 'property_id' : property_id})

def edit_account(request, user_id):
    notifications_num = 0
    email_passed = True
    if request.user.is_authenticated:
        notifications_num = Notifications.objects.filter(user=request.user).count()
    if Mailling.objects.filter(user=request.user).exists():
        email_passed = True
    else:
        email_passed = False
    return render(request, 'edit_account.html', {'notifications_num': notifications_num, 'email_passed': email_passed})

def page_not_found(request, exception):
    notifications_num = 0
    email_passed = True
    if request.user.is_authenticated:
        notifications_num = Notifications.objects.filter(user=request.user).count()
    if Mailling.objects.filter(user=request.user).exists():
        email_passed = True
    else:
        email_passed = False
    return render(request, '404.html', {'notifications_num': notifications_num, 'email_passed': email_passed})

def base_for_test(request):
    notifications_num = 0
    email_passed = True
    if request.user.is_authenticated:
        notifications_num = Notifications.objects.filter(user=request.user).count()
    if Mailling.objects.filter(user=request.user).exists():
        email_passed = True
    else:
        email_passed = False
    return render(request, 'base.html', {'notifications_num': notifications_num, 'email_passed': email_passed})