from django.conf.urls import url

from trust.views import AllowInstructions, DecisionLongCSVExport

views_to_add = [
    AllowInstructions,
    DecisionLongCSVExport

]
urlpatterns = [url(i.url_pattern, i.as_view(), name=i.url_name) for i in views_to_add]
