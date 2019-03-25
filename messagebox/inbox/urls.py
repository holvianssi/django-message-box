from django.conf.urls import url

from messagebox.inbox.views import ReceiveMessageView

urlpatterns = [
    url(r'^inbox/$', ReceiveMessageView.as_view(), name='inbox:inbox'),
]
