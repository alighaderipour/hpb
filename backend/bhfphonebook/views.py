# backend/bhfphonebook/views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Prefetch
from django.utils import timezone

from .models import (
    Department, SectionType, PhoneType, Section, SectionPhone,
    Staff, StaffPhone, StaffAssignment, TransferHistory
)
from .serializers import (
    DepartmentListSerializer, DepartmentDetailSerializer,
    SectionTypeSerializer, PhoneTypeSerializer,
    SectionListSerializer, SectionDetailSerializer, SectionPhoneSerializer,
    StaffListSerializer, StaffDetailSerializer, StaffPhoneSerializer,
    StaffAssignmentSerializer, TransferHistorySerializer
)

# ================== PhoneType ViewSet ==================

class PhoneTypeViewSet(viewsets.ModelViewSet):
    """API برای مدیریت انواع تلفن"""
    queryset = PhoneType.objects.all()
    serializer_class = PhoneTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_mobile', 'is_active']
    search_fields = ['name', 'code']
    ordering_fields = ['display_order', 'name', 'created_at']
    ordering = ['display_order', 'name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


# ================== SectionType ViewSet ==================

class SectionTypeViewSet(viewsets.ModelViewSet):
    """API برای مدیریت انواع بخش"""
    queryset = SectionType.objects.all()
    serializer_class = SectionTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['display_order', 'name', 'created_at']
    ordering = ['display_order', 'name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


# ================== Department ViewSet ==================


class DepartmentViewSet(viewsets.ModelViewSet):
    """API برای مدیریت دپارتمان‌ها"""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DepartmentDetailSerializer
        return DepartmentListSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """
        ✅ مسیر صحیح: sections__assignments (نه staffassignment)
        """
        return Department.objects.annotate(
            total_sections=Count('sections', distinct=True),
            total_staff=Count(
                'sections__assignments',  # ✅ این صحیح است
                distinct=True,
                filter=Q(sections__assignments__is_current=True)
            )
        ).order_by('name')
# ================== Section ViewSet ==================

class SectionViewSet(viewsets.ModelViewSet):
    """API برای مدیریت بخش‌ها"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'section_type', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['department__name', 'name']

    def get_queryset(self):
        return Section.objects.select_related(
            'department',
            'section_type'
        ).prefetch_related(
            Prefetch(
                'phones',
                queryset=SectionPhone.objects.filter(is_active=True).select_related('phone_type')
            )
        ).all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SectionDetailSerializer
        return SectionListSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


# ================== SectionPhone ViewSet ==================

class SectionPhoneViewSet(viewsets.ModelViewSet):
    """API برای مدیریت تلفن‌های بخش (فقط ادمین)"""
    queryset = SectionPhone.objects.select_related('section', 'phone_type').all()
    serializer_class = SectionPhoneSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['section', 'phone_type', 'is_primary', 'is_active']
    ordering_fields = ['section', 'is_primary', 'created_at']
    ordering = ['section', '-is_primary']


# ================== Staff ViewSet ==================

class StaffViewSet(viewsets.ModelViewSet):
    """API برای مدیریت پرسنل"""
    serializer_class = StaffListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['first_name', 'last_name', 'personnel_code', 'phones__phone_number']
    ordering_fields = ['first_name', 'last_name', 'personnel_code', 'created_at']
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        return Staff.objects.prefetch_related(
            Prefetch(
                'assignments',
                queryset=StaffAssignment.objects.filter(is_current=True).select_related(
                    'section',
                    'section__department'
                ),
                to_attr='current_assignments'
            ),
            Prefetch(
                'phones',
                queryset=StaffPhone.objects.filter(is_active=True).select_related('phone_type'),
                to_attr='active_phones'
            )
        ).all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StaffDetailSerializer
        return StaffListSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', '')
        print(f"📋 Staff List Request - Search: '{search_query}'")
        
        try:
            queryset = self.filter_queryset(self.get_queryset())
            
            if search_query:
                queryset = queryset.filter(
                    Q(first_name__icontains=search_query) |
                    Q(last_name__icontains=search_query) |
                    Q(personnel_code__icontains=search_query) |
                    Q(phones__phone_number__icontains=search_query)
                ).distinct()
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            print(f"✅ Returned {len(serializer.data)} staff members")
            return Response(serializer.data)
            
        except Exception as e:
            print(f"❌ Staff list error: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def active(self, request):
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def phones(self, request, pk=None):
        staff = self.get_object()
        phones = StaffPhone.objects.filter(
            staff=staff, 
            is_active=True
        ).select_related('phone_type')
        serializer = StaffPhoneSerializer(phones, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_phone(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {"error": "فقط ادمین می‌تواند شماره تلفن اضافه کند"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        staff = self.get_object()
        data = request.data.copy()
        data['staff'] = staff.id
        
        serializer = StaffPhoneSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================== StaffPhone ViewSet ==================

class StaffPhoneViewSet(viewsets.ModelViewSet):
    """API برای مدیریت تلفن‌های پرسنل (فقط ادمین)"""
    queryset = StaffPhone.objects.select_related('staff', 'phone_type').all()
    serializer_class = StaffPhoneSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['staff', 'phone_type', 'is_primary', 'is_public', 'is_active']
    ordering_fields = ['staff', 'is_primary', 'created_at']
    ordering = ['staff', '-is_primary']


# ================== StaffAssignment ViewSet ==================

class StaffAssignmentViewSet(viewsets.ModelViewSet):
    """API برای مدیریت انتساب پرسنل به بخش‌ها"""
    queryset = StaffAssignment.objects.select_related('staff', 'section').all()
    serializer_class = StaffAssignmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['staff', 'section', 'is_current']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    ordering = ['-is_current', '-start_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def current(self, request):
        assignments = self.queryset.filter(is_current=True)
        serializer = self.get_serializer(assignments, many=True)
        return Response(serializer.data)


# ================== TransferHistory ViewSet ==================

class TransferHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API برای مشاهده تاریخچه جابجایی‌ها"""
    queryset = TransferHistory.objects.select_related(
        'staff', 'from_section', 'to_section'
    ).all()
    serializer_class = TransferHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['staff', 'from_section', 'to_section']
    ordering_fields = ['transfer_date', 'created_at']
    ordering = ['-transfer_date', '-created_at']


# ================== PhonebookSearch ViewSet ==================

class PhonebookSearchViewSet(viewsets.ViewSet):
    """API برای جستجو در دفترچه تلفن"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '').strip()
        
        if not query or len(query) < 2:
            return Response({
                'staff': [],
                'sections': [],
                'departments': []
            })
        
        # جستجو در پرسنل
        staff = Staff.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(personnel_code__icontains=query)
        ).prefetch_related('phones')[:20]
        
        # جستجو در بخش‌ها
        sections = Section.objects.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query)
        ).select_related('department')[:20]
        
        # جستجو در دپارتمان‌ها
        departments = Department.objects.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query)
        )[:20]
        
        return Response({
            'staff': StaffListSerializer(staff, many=True).data,
            'sections': SectionListSerializer(sections, many=True).data,
            'departments': DepartmentListSerializer(departments, many=True).data
        })


# ================== Statistics ViewSet ==================

class StatisticsViewSet(viewsets.ViewSet):
    """API برای آمار و گزارشات"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        stats = {
            'total_departments': Department.objects.filter(is_active=True).count(),
            'total_sections': Section.objects.filter(is_active=True).count(),
            'total_staff': Staff.objects.filter(is_active=True).count(),
            'total_active_assignments': StaffAssignment.objects.filter(is_current=True).count(),
            'total_transfers': TransferHistory.objects.count(),
        }

        departments = Department.objects.filter(is_active=True).annotate(
            section_count=Count('sections', filter=Q(sections__is_active=True)),
            staff_count=Count(
                'sections__assignments',
                filter=Q(sections__assignments__is_current=True),
                distinct=True
            )
        ).values('id', 'name', 'section_count', 'staff_count')

        stats['departments'] = list(departments)
        return Response(stats)

    @action(detail=False, methods=['get'])
    def recent_transfers(self, request):
        days = int(request.query_params.get('days', 30))
        from_date = timezone.now().date() - timezone.timedelta(days=days)

        transfers = TransferHistory.objects.filter(
            transfer_date__gte=from_date
        ).select_related('staff', 'from_section', 'to_section')[:50]

        serializer = TransferHistorySerializer(transfers, many=True)
        return Response(serializer.data)
