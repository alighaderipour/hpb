from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Q
from .models import (
    Department, SectionType, PhoneType, Section, SectionPhone,
    Staff, StaffPhone, StaffAssignment, TransferHistory
)


# ================== Inline Admin Classes ==================

class SectionPhoneInline(admin.TabularInline):
    """نمایش شماره تلفن‌های بخش در صفحه بخش"""
    model = SectionPhone
    extra = 1
    fields = ['phone_type', 'phone_number', 'is_primary', 'is_active', 'description']
    autocomplete_fields = ['phone_type']


class StaffPhoneInline(admin.TabularInline):
    """نمایش شماره تلفن‌های پرسنل در صفحه پرسنل"""
    model = StaffPhone
    extra = 1
    fields = ['phone_type', 'phone_number', 'is_primary', 'is_public', 'is_active', 'description']
    autocomplete_fields = ['phone_type']


class StaffAssignmentInline(admin.TabularInline):
    """نمایش انتساب‌های پرسنل"""
    model = StaffAssignment
    extra = 0
    fields = ['section', 'start_date', 'end_date', 'is_current', 'position']
    readonly_fields = ['is_current']
    autocomplete_fields = ['section']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('section', 'section__department')


# ================== PhoneType Admin ==================

@admin.register(PhoneType)
class PhoneTypeAdmin(admin.ModelAdmin):
    """مدیریت انواع تلفن"""
    list_display = ['name', 'code', 'is_mobile_badge', 'is_active_badge', 'display_order', 'created_at']
    list_filter = ['is_mobile', 'is_active', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['display_order', 'name']
    list_editable = ['display_order']
    
    fieldsets = [
        ('اطلاعات پایه', {
            'fields': ['name', 'code', 'is_mobile', 'is_active']
        }),
        ('تنظیمات نمایش', {
            'fields': ['display_order'],
            'classes': ['collapse']
        }),
        ('اطلاعات سیستمی', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def is_mobile_badge(self, obj):
        if obj.is_mobile:
            return format_html('<span style="color: green;">✓ موبایل</span>')
        return format_html('<span style="color: gray;">✗ ثابت</span>')
    is_mobile_badge.short_description = 'نوع'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">●</span> فعال')
        return format_html('<span style="color: red;">●</span> غیرفعال')
    is_active_badge.short_description = 'وضعیت'


# ================== SectionType Admin ==================

@admin.register(SectionType)
class SectionTypeAdmin(admin.ModelAdmin):
    """مدیریت انواع سکشن"""
    list_display = ['name', 'code', 'total_sections', 'is_active_badge', 'display_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['display_order', 'name']
    list_editable = ['display_order']
    
    fieldsets = [
        ('اطلاعات پایه', {
            'fields': ['name', 'code', 'description', 'is_active']
        }),
        ('تنظیمات نمایش', {
            'fields': ['display_order'],
            'classes': ['collapse']
        }),
        ('اطلاعات سیستمی', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def total_sections(self, obj):
        count = obj.sections.filter(is_active=True).count()
        if count > 0:
            url = reverse('admin:bhfphonebook_section_changelist') + f'?section_type__id__exact={obj.id}'
            return format_html('<a href="{}">{} بخش</a>', url, count)
        return '0 بخش'
    total_sections.short_description = 'تعداد بخش‌ها'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">●</span> فعال')
        return format_html('<span style="color: red;">●</span> غیرفعال')
    is_active_badge.short_description = 'وضعیت'


# ================== Department Admin ==================

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """مدیریت دپارتمان‌ها"""
    list_display = ['name', 'code', 'total_sections_count', 'total_staff_count', 'is_active_badge', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['name']
    
    fieldsets = [
        ('اطلاعات پایه', {
            'fields': ['name', 'code', 'description', 'is_active']
        }),
        ('آمار', {
            'fields': ['total_sections_count', 'total_staff_count'],
            'classes': ['collapse']
        }),
        ('اطلاعات سیستمی', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]
    readonly_fields = ['total_sections_count', 'total_staff_count', 'created_at', 'updated_at']
    
    def total_sections_count(self, obj):
        count = obj.total_sections()
        if count > 0:
            url = reverse('admin:bhfphonebook_section_changelist') + f'?department__id__exact={obj.id}'
            return format_html('<a href="{}">{} بخش</a>', url, count)
        return '0 بخش'
    total_sections_count.short_description = 'تعداد بخش‌ها'
    
    def total_staff_count(self, obj):
        count = obj.total_staff()
        if count > 0:
            return format_html('<strong>{}</strong> نفر', count)
        return '0 نفر'
    total_staff_count.short_description = 'تعداد پرسنل'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">●</span> فعال')
        return format_html('<span style="color: red;">●</span> غیرفعال')
    is_active_badge.short_description = 'وضعیت'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            section_count=Count('sections', filter=Q(sections__is_active=True))
        )


# ================== Section Admin ==================

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """مدیریت بخش‌ها"""
    list_display = ['name', 'code', 'department_link', 'section_type', 'primary_phone_display', 
                    'current_staff_count_display', 'is_active_badge']
    list_filter = ['is_active', 'department', 'section_type', 'created_at']
    search_fields = ['name', 'code', 'description', 'department__name']
    ordering = ['department__name', 'name']
    autocomplete_fields = ['department', 'section_type']
    inlines = [SectionPhoneInline]
    
    fieldsets = [
        ('اطلاعات پایه', {
            'fields': ['department', 'section_type', 'name', 'code', 'description', 'is_active']
        }),
        ('شماره تلفن', {
            'fields': ['primary_phone_display', 'phone_list_display'],
            'classes': ['collapse']
        }),
        ('پرسنل', {
            'fields': ['current_staff_count_display'],
            'classes': ['collapse']
        }),
        ('اطلاعات سیستمی', {
            'fields': ['full_name_display', 'created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]
    readonly_fields = ['primary_phone_display', 'phone_list_display', 'current_staff_count_display', 
                       'full_name_display', 'created_at', 'updated_at']
    
    def department_link(self, obj):
        url = reverse('admin:bhfphonebook_department_change', args=[obj.department.id])
        return format_html('<a href="{}">{}</a>', url, obj.department.name)
    department_link.short_description = 'دپارتمان'
    
    def primary_phone_display(self, obj):
        phone = obj.primary_phone
        if phone:
            return format_html('<strong>{}</strong>', phone)
        return format_html('<span style="color: red;">بدون شماره</span>')
    primary_phone_display.short_description = 'شماره اصلی'
    
    def phone_list_display(self, obj):
        phones = obj.phone_list
        return phones if phones else 'بدون شماره'
    phone_list_display.short_description = 'لیست شماره‌ها'
    
    def current_staff_count_display(self, obj):
        count = obj.current_staff_count
        if count > 0:
            return format_html('<strong>{}</strong> نفر', count)
        return '0 نفر'
    current_staff_count_display.short_description = 'پرسنل فعلی'
    
    def full_name_display(self, obj):
        return obj.full_name
    full_name_display.short_description = 'نام کامل'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">●</span> فعال')
        return format_html('<span style="color: red;">●</span> غیرفعال')
    is_active_badge.short_description = 'وضعیت'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('department', 'section_type').prefetch_related('phones')


# ================== SectionPhone Admin ==================

@admin.register(SectionPhone)
class SectionPhoneAdmin(admin.ModelAdmin):
    """مدیریت شماره تلفن‌های بخش"""
    list_display = ['section', 'phone_type', 'phone_number', 'is_primary_badge', 'is_active_badge', 'created_at']
    list_filter = ['is_primary', 'is_active', 'phone_type', 'created_at']
    search_fields = ['phone_number', 'section__name', 'description']
    ordering = ['section', '-is_primary', 'phone_type']
    autocomplete_fields = ['section', 'phone_type']
    
    fieldsets = [
        ('اطلاعات پایه', {
            'fields': ['section', 'phone_type', 'phone_number']
        }),
        ('تنظیمات', {
            'fields': ['is_primary', 'is_active', 'description']
        }),
        ('اطلاعات سیستمی', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def is_primary_badge(self, obj):
        if obj.is_primary:
            return format_html('<span style="color: green;">★</span> اصلی')
        return format_html('<span style="color: gray;">☆</span> فرعی')
    is_primary_badge.short_description = 'نوع'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">●</span> فعال')
        return format_html('<span style="color: red;">●</span> غیرفعال')
    is_active_badge.short_description = 'وضعیت'


# ================== Staff Admin ==================

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """مدیریت پرسنل"""
    list_display = ['full_name', 'personnel_code', 'current_section_display', 'current_phone_display',
                    'primary_mobile_display', 'is_active_badge', 'hire_date']
    list_filter = ['is_active', 'hire_date', 'created_at']
    search_fields = ['first_name', 'last_name', 'personnel_code', 'national_code', 'email']
    ordering = ['last_name', 'first_name']
    inlines = [StaffPhoneInline, StaffAssignmentInline]
    date_hierarchy = 'hire_date'
    
    fieldsets = [
        ('اطلاعات شخصی', {
            'fields': ['first_name', 'last_name', 'personnel_code', 'national_code', 'email']
        }),
        ('اطلاعات شغلی', {
            'fields': ['hire_date', 'is_active']
        }),
        ('بخش فعلی', {
            'fields': ['current_section_display', 'current_phone_display'],
            'classes': ['collapse']
        }),
        ('شماره تماس', {
            'fields': ['primary_mobile_display', 'primary_landline_display'],
            'classes': ['collapse']
        }),
        ('اطلاعات سیستمی', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]
    readonly_fields = ['current_section_display', 'current_phone_display', 
                       'primary_mobile_display', 'primary_landline_display',
                       'created_at', 'updated_at']
    
    def current_section_display(self, obj):
        section = obj.current_section
        if section:
            url = reverse('admin:bhfphonebook_section_change', args=[section.id])
            return format_html('<a href="{}">{}</a>', url, section.full_name)
        return format_html('<span style="color: red;">بدون انتساب</span>')
    current_section_display.short_description = 'بخش فعلی'
    
    def current_phone_display(self, obj):
        phone = obj.current_phone
        if phone:
            return format_html('<strong>{}</strong>', phone)
        return 'بدون شماره'
    current_phone_display.short_description = 'شماره بخش فعلی'
    
    def primary_mobile_display(self, obj):
        mobile = obj.primary_mobile
        if mobile:
            return format_html('<strong>{}</strong>', mobile)
        return 'بدون موبایل'
    primary_mobile_display.short_description = 'موبایل اصلی'
    
    def primary_landline_display(self, obj):
        landline = obj.primary_landline
        if landline:
            return landline
        return 'بدون تلفن ثابت'
    primary_landline_display.short_description = 'تلفن ثابت اصلی'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">●</span> فعال')
        return format_html('<span style="color: red;">●</span> غیرفعال')
    is_active_badge.short_description = 'وضعیت'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('phones', 'assignments')


# ================== StaffPhone Admin ==================

@admin.register(StaffPhone)
class StaffPhoneAdmin(admin.ModelAdmin):
    """مدیریت شماره تلفن‌های پرسنل"""
    list_display = ['staff', 'phone_type', 'phone_number', 'is_primary_badge', 
                    'is_public_badge', 'is_active_badge', 'created_at']
    list_filter = ['is_primary', 'is_public', 'is_active', 'phone_type', 'created_at']
    search_fields = ['phone_number', 'staff__first_name', 'staff__last_name', 'description']
    ordering = ['staff', '-is_primary', 'phone_type']
    autocomplete_fields = ['staff', 'phone_type']
    
    fieldsets = [
        ('اطلاعات پایه', {
            'fields': ['staff', 'phone_type', 'phone_number']
        }),
        ('تنظیمات', {
            'fields': ['is_primary', 'is_public', 'is_active', 'description']
        }),
        ('اطلاعات سیستمی', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def is_primary_badge(self, obj):
        if obj.is_primary:
            return format_html('<span style="color: green;">★</span> اصلی')
        return format_html('<span style="color: gray;">☆</span> فرعی')
    is_primary_badge.short_description = 'نوع'
    
    def is_public_badge(self, obj):
        if obj.is_public:
            return format_html('<span style="color: blue;">👁</span> عمومی')
        return format_html('<span style="color: orange;">🔒</span> خصوصی')
    is_public_badge.short_description = 'دسترسی'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">●</span> فعال')
        return format_html('<span style="color: red;">●</span> غیرفعال')
    is_active_badge.short_description = 'وضعیت'


# ================== StaffAssignment Admin ==================

@admin.register(StaffAssignment)
class StaffAssignmentAdmin(admin.ModelAdmin):
    """مدیریت انتساب پرسنل به بخش‌ها"""
    list_display = ['staff', 'section', 'start_date', 'end_date', 'is_current_badge', 
                    'duration_days_display', 'created_at']
    list_filter = ['is_current', 'start_date', 'created_at']
    search_fields = ['staff__first_name', 'staff__last_name', 'section__name', 'position', 'notes']
    ordering = ['-is_current', '-start_date']
    autocomplete_fields = ['staff', 'section']
    date_hierarchy = 'start_date'
    
    fieldsets = [
        ('اطلاعات پایه', {
            'fields': ['staff', 'section', 'position']
        }),
        ('تاریخ', {
            'fields': ['start_date', 'end_date', 'is_current', 'duration_days_display']
        }),
        ('یادداشت', {
            'fields': ['notes'],
            'classes': ['collapse']
        }),
        ('اطلاعات سیستمی', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]
    readonly_fields = ['is_current', 'duration_days_display', 'created_at', 'updated_at']
    
    def is_current_badge(self, obj):
        if obj.is_current:
            return format_html('<span style="color: green; font-weight: bold;">✓ فعلی</span>')
        return format_html('<span style="color: gray;">✗ گذشته</span>')
    is_current_badge.short_description = 'وضعیت'
    
    def duration_days_display(self, obj):
        days = obj.duration_days
        if days is not None:
            if days < 30:
                return f'{days} روز'
            elif days < 365:
                months = days // 30
                return f'{months} ماه'
            else:
                years = days // 365
                return f'{years} سال'
        return 'در حال انجام'
    duration_days_display.short_description = 'مدت زمان'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('staff', 'section', 'section__department')


# ================== TransferHistory Admin ==================

@admin.register(TransferHistory)
class TransferHistoryAdmin(admin.ModelAdmin):
    """مشاهده تاریخچه جابجایی‌ها (فقط خواندنی)"""
    list_display = ['staff', 'from_section_display', 'to_section_display', 
                    'transfer_date', 'approved_by', 'created_at']
    list_filter = ['transfer_date', 'created_at']
    search_fields = ['staff__first_name', 'staff__last_name', 'reason', 'approved_by', 'notes']
    ordering = ['-transfer_date', '-created_at']
    autocomplete_fields = ['staff', 'from_section', 'to_section']
    date_hierarchy = 'transfer_date'
    
    # فقط مشاهده، بدون امکان ویرایش یا حذف
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = [
        ('اطلاعات جابجایی', {
            'fields': ['staff', 'from_section', 'to_section', 'transfer_date']
        }),
        ('جزئیات', {
            'fields': ['reason', 'approved_by', 'notes']
        }),
        ('اطلاعات سیستمی', {
            'fields': ['created_at'],
        }),
    ]
    readonly_fields = ['staff', 'from_section', 'to_section', 'transfer_date', 
                       'reason', 'approved_by', 'notes', 'created_at']
    
    def from_section_display(self, obj):
        if obj.from_section:
            url = reverse('admin:bhfphonebook_section_change', args=[obj.from_section.id])
            return format_html('<a href="{}">{}</a>', url, obj.from_section.full_name)
        return format_html('<span style="color: gray;">بدون بخش</span>')
    from_section_display.short_description = 'از بخش'
    
    def to_section_display(self, obj):
        if obj.to_section:
            url = reverse('admin:bhfphonebook_section_change', args=[obj.to_section.id])
            return format_html('<a href="{}">{}</a>', url, obj.to_section.full_name)
        return format_html('<span style="color: gray;">بدون بخش</span>')
    to_section_display.short_description = 'به بخش'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('staff', 'from_section', 'to_section')


# ================== Admin Site Customization ==================

# تنظیمات پنل ادمین
admin.site.site_header = 'پنل مدیریت دفترچه تلفن بیمارستان'
admin.site.site_title = 'دفترچه تلفن'
admin.site.index_title = 'مدیریت اطلاعات'

# فعال کردن autocomplete برای مدل‌های مورد نیاز
admin.site.enable_nav_sidebar = True
