from django.urls import path, include

from .views import PersonViewSet, TryingViewSet, AnswerViewSet, TestViewSet, QuestionViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'person', PersonViewSet)
router.register(r'trying', TryingViewSet)
router.register(r'answer', AnswerViewSet)
router.register(r'test', TestViewSet)
router.register(r'question', QuestionViewSet)


urlpatterns = [
    path('<slug:person_username>/', include(router.urls)),
    path('<slug:testing_slug>/', include(router.urls)),
    path('<int:trying_id>/', include(router.urls)),
    path('<int:question_id>/', include(router.urls)),
    path('<int:answer_id>/', include(router.urls)),
    path('', include(router.urls))

]
