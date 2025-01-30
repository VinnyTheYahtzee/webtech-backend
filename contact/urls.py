# urls.py
from django.urls import path

from contact.views import ContactFormView
from contact.views import AdminMessagesView


urlpatterns = [
    path('contactform/', ContactFormView.as_view(), name='contact-form'),
    path('messages/', AdminMessagesView.as_view(), name='contact-messages'),
]
