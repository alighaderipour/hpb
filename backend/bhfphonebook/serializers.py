from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from .models import (
    Department, SectionType, PhoneType, Section, SectionPhone,
    Staff, StaffPhone, StaffAssignment, TransferHistory,
    transfer_staff
)


# ================== Phone Type Serializers ==================

class PhoneTypeSerializer(serializers.ModelSerializer):
    """سریالایزر نوع تلفن"""
    
    class Meta:
        model = PhoneType
        fields = [
            'id', 'name', 'code', 'is_mobile', 'is_active',
            'display_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ================== Section Type Serializers ==================

class SectionTypeSerializer(serializers.ModelSerializer):
    """سریالایزر نوع سکشن"""
    total_sections = serializers.SerializerMethodField()
    
    class Meta:
        model = SectionType
        fields = [
            'id', 'name', 'code', 'description', 'is_active',
            'display_order', 'total_sections', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_total_sections(self, obj):
        return obj.sections.filter(is_active=True).count()


# ================== Department Serializers ==================

class DepartmentListSerializer(serializers.ModelSerializer):
    """سریالایزر لیست دپارتمان‌ها"""
    
    total_sections = serializers.IntegerField(read_only=True)  # ✅ حذف source
    total_staff = serializers.IntegerField(read_only=True)  # ✅ حذف source
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'description', 'is_active',
            'total_sections', 'total_staff', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class DepartmentDetailSerializer(serializers.ModelSerializer):
    """سریالایزر جزئیات دپارتمان"""
    total_sections = serializers.IntegerField(source='total_sections', read_only=True)
    total_staff = serializers.IntegerField(source='total_staff', read_only=True)
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'description', 'is_active',
            'total_sections', 'total_staff', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ================== Section Phone Serializers ==================

class SectionPhoneSerializer(serializers.ModelSerializer):
    """سریالایزر تلفن بخش"""
    phone_type_name = serializers.CharField(source='phone_type.name', read_only=True)
    phone_type_code = serializers.CharField(source='phone_type.code', read_only=True)
    
    class Meta:
        model = SectionPhone
        fields = [
            'id', 'section', 'phone_type', 'phone_type_name', 'phone_type_code',
            'phone_number', 'is_primary', 'is_active', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        """اعتبارسنجی سریالایزر"""
        # بررسی تنها بودن primary برای هر نوع
        if data.get('is_primary', False):
            instance = self.instance
            section = data.get('section', instance.section if instance else None)
            phone_type = data.get('phone_type', instance.phone_type if instance else None)
            
            if section and phone_type:
                existing = SectionPhone.objects.filter(
                    section=section,
                    phone_type=phone_type,
                    is_primary=True,
                    is_active=True
                )
                if instance:
                    existing = existing.exclude(pk=instance.pk)
                
                if existing.exists():
                    raise serializers.ValidationError(
                        f'این بخش قبلاً یک شماره {phone_type.name} اصلی دارد'
                    )
        
        return data


# ================== Section Serializers ==================

class SectionListSerializer(serializers.ModelSerializer):
    """سریالایزر لیست سکشن‌ها"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    section_type_name = serializers.CharField(source='section_type.name', read_only=True)
    primary_phone = serializers.CharField(read_only=True)
    current_staff_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Section
        fields = [
            'id', 'department', 'department_name', 'section_type',
            'section_type_name', 'name', 'code', 'description',
            'primary_phone', 'current_staff_count', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SectionDetailSerializer(serializers.ModelSerializer):
    """سریالایزر جزئیات سکشن"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    section_type_name = serializers.CharField(source='section_type.name', read_only=True)
    phones = SectionPhoneSerializer(many=True, read_only=True)
    primary_phone = serializers.CharField(read_only=True)
    phone_list = serializers.CharField(read_only=True)
    current_staff_count = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Section
        fields = [
            'id', 'department', 'department_name', 'section_type',
            'section_type_name', 'name', 'code', 'description',
            'phones', 'primary_phone', 'phone_list', 'full_name',
            'current_staff_count', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ================== Staff Phone Serializers ==================

class StaffPhoneSerializer(serializers.ModelSerializer):
    """سریالایزر تلفن پرسنل"""
    phone_type_name = serializers.CharField(source='phone_type.name', read_only=True)
    phone_type_code = serializers.CharField(source='phone_type.code', read_only=True)
    is_mobile = serializers.BooleanField(source='phone_type.is_mobile', read_only=True)
    
    class Meta:
        model = StaffPhone
        fields = [
            'id', 'staff', 'phone_type', 'phone_type_name', 'phone_type_code',
            'is_mobile', 'phone_number', 'is_primary', 'is_active',
            'is_public', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        """اعتبارسنجی"""
        if data.get('is_primary', False):
            instance = self.instance
            staff = data.get('staff', instance.staff if instance else None)
            phone_type = data.get('phone_type', instance.phone_type if instance else None)
            
            if staff and phone_type:
                existing = StaffPhone.objects.filter(
                    staff=staff,
                    phone_type=phone_type,
                    is_primary=True,
                    is_active=True
                )
                if instance:
                    existing = existing.exclude(pk=instance.pk)
                
                if existing.exists():
                    raise serializers.ValidationError(
                        f'این پرسنل قبلاً یک شماره {phone_type.name} اصلی دارد'
                    )
        
        return data

class StaffPhonePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPhone
        fields = [
            'phone_number',
            'phone_type'
        ]


# ================== Staff Assignment Serializers ==================

class StaffAssignmentSerializer(serializers.ModelSerializer):
    """سریالایزر انتساب پرسنل"""
    staff_name = serializers.CharField(source='staff.full_name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    section_phone = serializers.CharField(source='section.primary_phone', read_only=True)
    duration_days = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = StaffAssignment
        fields = [
            'id', 'staff', 'staff_name', 'section', 'section_name',
            'section_phone', 'start_date', 'end_date', 'is_current',
            'position', 'notes', 'duration_days', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        """اعتبارسنجی"""
        # بررسی تاریخ
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError({
                    'end_date': 'تاریخ پایان نمی‌تواند قبل از تاریخ شروع باشد'
                })
        
        # بررسی is_current
        if data.get('is_current', False):
            if data.get('end_date'):
                raise serializers.ValidationError({
                    'end_date': 'انتساب فعلی نمی‌تواند تاریخ پایان داشته باشد'
                })
            
            # چک کردن انتساب فعلی دیگر
            instance = self.instance
            staff = data.get('staff', instance.staff if instance else None)
            
            if staff:
                existing = StaffAssignment.objects.filter(
                    staff=staff,
                    is_current=True
                )
                if instance:
                    existing = existing.exclude(pk=instance.pk)
                
                if existing.exists():
                    raise serializers.ValidationError(
                        'این پرسنل در حال حاضر یک انتساب فعال دارد'
                    )
        
        return data


# ================== Staff Serializers ==================

class StaffListSerializer(serializers.ModelSerializer):
    """سریالایزر لیست پرسنل"""
    full_name = serializers.CharField(read_only=True)
    current_section_name = serializers.SerializerMethodField()
    current_section_phone = serializers.CharField(source='current_phone', read_only=True)
    primary_mobile = serializers.SerializerMethodField()
    
    class Meta:
        model = Staff
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'personnel_code',
            'national_code', 'email', 'current_section_name',
            'current_section_phone', 'primary_mobile', 'is_active',
            'hire_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_current_section_name(self, obj):
        section = obj.current_section
        return section.full_name if section else None
    
    def get_primary_mobile(self, obj):
        """فقط اگر عمومی باشد یا کاربر ادمین باشد"""
        request = self.context.get('request')
        if request and request.user.is_staff:
            return obj.primary_mobile
        
        # برای کاربران عادی فقط موبایل عمومی
        public_mobile = obj.phones.filter(
            phone_type__is_mobile=True,
            is_public=True,
            is_active=True
        ).first()
        return public_mobile.phone_number if public_mobile else None


class StaffDetailSerializer(serializers.ModelSerializer):
    """سریالایزر جزئیات پرسنل"""
    full_name = serializers.CharField(read_only=True)
    phones = serializers.SerializerMethodField()
    current_section = serializers.SerializerMethodField()
    current_phone = serializers.CharField(read_only=True)
    assignments = StaffAssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Staff
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'personnel_code',
            'national_code', 'email', 'phones', 'current_section',
            'current_phone', 'assignments', 'is_active', 'hire_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_phones(self, obj):
        """برگرداندن تلفن‌ها بر اساس سطح دسترسی"""
        request = self.context.get('request')
        
        if request and request.user.is_staff:
            # ادمین همه شماره‌ها را می‌بیند
            phones = obj.phones.filter(is_active=True)
            return StaffPhoneSerializer(phones, many=True).data
        else:
            # کاربران عادی فقط شماره‌های عمومی
            phones = obj.phones.filter(is_public=True, is_active=True)
            return StaffPhonePublicSerializer(phones, many=True).data
    
    def get_current_section(self, obj):
        section = obj.current_section
        if section:
            return {
                'id': section.id,
                'name': section.name,
                'full_name': section.full_name,
                'primary_phone': section.primary_phone
            }
        return None


# ================== Transfer History Serializers ==================

class TransferHistorySerializer(serializers.ModelSerializer):
    """سریالایزر تاریخچه جابجایی"""
    staff_name = serializers.CharField(source='staff.full_name', read_only=True)
    from_section_name = serializers.SerializerMethodField()
    to_section_name = serializers.SerializerMethodField()
    
    class Meta:
        model = TransferHistory
        fields = [
            'id', 'staff', 'staff_name', 'from_section', 'from_section_name',
            'to_section', 'to_section_name', 'transfer_date', 'reason',
            'approved_by', 'notes', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_from_section_name(self, obj):
        return obj.from_section.full_name if obj.from_section else 'بدون بخش'
    
    def get_to_section_name(self, obj):
        return obj.to_section.full_name if obj.to_section else 'بدون بخش'


class StaffTransferSerializer(serializers.Serializer):
    """سریالایزر برای جابجایی پرسنل"""
    staff_id = serializers.IntegerField()
    new_section_id = serializers.IntegerField()
    transfer_date = serializers.DateField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    approved_by = serializers.CharField(required=False, allow_blank=True)
    position = serializers.CharField(required=False, allow_blank=True)
    
    def validate_staff_id(self, value):
        """بررسی وجود پرسنل"""
        if not Staff.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError('پرسنل یافت نشد یا غیرفعال است')
        return value
    
    def validate_new_section_id(self, value):
        """بررسی وجود بخش"""
        if not Section.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError('بخش یافت نشد یا غیرفعال است')
        return value
    
    def validate(self, data):
        """اعتبارسنجی کلی"""
        staff = Staff.objects.get(id=data['staff_id'])
        new_section = Section.objects.get(id=data['new_section_id'])
        
        # بررسی اینکه آیا در حال حاضر در همین بخش است
        current = staff.current_section
        if current and current.id == new_section.id:
            raise serializers.ValidationError(
                'پرسنل در حال حاضر در این بخش مشغول است'
            )
        
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        """انجام جابجایی"""
        staff = Staff.objects.get(id=validated_data['staff_id'])
        new_section = Section.objects.get(id=validated_data['new_section_id'])
        
        transfer_date = validated_data.get('transfer_date', timezone.now().date())
        reason = validated_data.get('reason')
        approved_by = validated_data.get('approved_by')
        position = validated_data.get('position')
        
        assignment, transfer = transfer_staff(
            staff=staff,
            new_section=new_section,
            transfer_date=transfer_date,
            reason=reason,
            approved_by=approved_by
        )
        
        # اضافه کردن position اگر وجود داشت
        if position:
            assignment.position = position
            assignment.save()
        
        return transfer


# ================== Search & Report Serializers ==================

class PhonebookSearchSerializer(serializers.Serializer):
    """سریالایزر جستجو در دفترچه تلفن"""
    query = serializers.CharField(required=False, allow_blank=True)
    department_id = serializers.IntegerField(required=False)
    section_id = serializers.IntegerField(required=False)
    section_type_id = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False, default=True)
