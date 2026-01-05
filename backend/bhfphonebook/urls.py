from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    PhoneTypeViewSet, SectionTypeViewSet, DepartmentViewSet,
    SectionViewSet, SectionPhoneViewSet,
    StaffViewSet, StaffPhoneViewSet, StaffAssignmentViewSet,
    TransferHistoryViewSet, PhonebookSearchViewSet, StatisticsViewSet
)

# ایجاد روتر اصلی
router = DefaultRouter()

# ثبت ViewSet‌ها
router.register(r'phone-types', PhoneTypeViewSet, basename='phonetype')
router.register(r'section-types', SectionTypeViewSet, basename='sectiontype')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'section-phones', SectionPhoneViewSet, basename='sectionphone')
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'staff-phones', StaffPhoneViewSet, basename='staffphone')
router.register(r'assignments', StaffAssignmentViewSet, basename='assignment')
router.register(r'transfer-history', TransferHistoryViewSet, basename='transferhistory')
router.register(r'phonebook', PhonebookSearchViewSet, basename='phonebook')
router.register(r'statistics', StatisticsViewSet, basename='statistics')

app_name = 'bhfphonebook'

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Routes
    path('', include(router.urls)),
]
