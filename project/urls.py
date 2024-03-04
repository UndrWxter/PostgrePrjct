from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('search/', views.SearchPage.as_view(), name='search'),
    path('search/results/', views.SearchResults.as_view(), name='search_results'),
    path('property/<int:property_id>/', views.property_detail.as_view(), name='property_detail'),
    path('property/<int:property_id>/reviews/', views.property_reviews.as_view(), name='property_reviews'),
    path('signup/', views.RegisterUser.as_view(), name='signup'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('landlord/add_property/', views.landlord_add_property.as_view(), name='landlord_add_property'),
    path('landlord/update_property/<int:property_id>', views.landlord_update_property.as_view(), name='landlord_update_property'),
    path('landlord/update_photos/<int:property_id>', views.landlord_update_photos, name='landlord_update_photos'),
    path('about/', views.about, name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('user_account/<int:user_id>', views.user_account, name='user_account'),
    path('user_account/<int:user_id>/properties', views.user_account_properties.as_view(), name='user_account_properties'),
    path('user_account/<int:user_id>/applications', views.user_account_applications.as_view(), name='user_account_applications'),
    path('user_account/<int:user_id>/contracts', views.user_account_contracts.as_view(), name='user_account_contracts'),
    path('user_account/<int:user_id>/rents', views.user_account_rents.as_view(), name='user_account_rents'),
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),
    path('captcha/', include('captcha.urls')),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('landlord/update_photos/<int:pk>/', views.landlord_update_photos, name='landlord_update_photos'),
    path('edit_account/<int:user_id>/', views.edit_account, name='edit_account'),
    path('base/', views.base_for_test, name='base'),
]

handler404 = views.page_not_found
