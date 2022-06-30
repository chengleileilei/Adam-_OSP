from django.urls import path
from . import views

app_name = "face"
urlpatterns = [
    path('getMenuAdmin', views.MenuAdminView.as_view()),
    path('imageUpload', views.ImageUploadView.as_view()),
    path('generateImage', views.GenerateImageView.as_view()),
    path('generatePatch', views.GeneratePatchView.as_view()),
    path('evaluateModel', views.EvaluateModelView.as_view()),
]
