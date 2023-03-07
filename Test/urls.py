from django.urls import path, include

from .views import PersonViewSet, TryingViewSet, AnswerViewSet, TestViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'person', PersonViewSet)
router.register(r'trying', TryingViewSet)
router.register(r'answer', AnswerViewSet)
router.register(r'test', TestViewSet)


urlpatterns = [
    path('person/<slug:person_login>/', include(router.urls)),
    path('test/<slug:testing_slug>/', include(router.urls)),
    path('trying/<int:trying_id>/', include(router.urls)),
    path('', include(router.urls))

]
