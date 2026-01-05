from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone


class Department(models.Model):
    """دپارتمان‌های بیمارستان"""
    name = models.CharField(max_length=100, unique=True, verbose_name='نام دپارتمان')
    code = models.CharField(max_length=20, unique=True, verbose_name='کد دپارتمان')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        db_table = 'departments'
        verbose_name = 'دپارتمان'
        verbose_name_plural = 'دپارتمان‌ها'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def total_sections(self):
        """تعداد کل سکشن‌های دپارتمان"""
        return self.sections.filter(is_active=True).count()
    
    @property
    def total_staff(self):
        """تعداد کل پرسنل فعال در دپارتمان"""
        return StaffAssignment.objects.filter(
            section__department=self,
            is_current=True
        ).count()


class SectionType(models.Model):
    """انواع سکشن (ایستگاه، منشی، سرپرست و...)"""
    name = models.CharField(max_length=50, unique=True, verbose_name='نام')
    code = models.CharField(max_length=20, unique=True, verbose_name='کد')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    display_order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        db_table = 'section_types'
        verbose_name = 'نوع سکشن'
        verbose_name_plural = 'انواع سکشن'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name


class PhoneType(models.Model):
    """انواع شماره تلفن (ثابت، موبایل، داخلی، فکس و...)"""
    name = models.CharField(max_length=50, unique=True, verbose_name='نام')
    code = models.CharField(max_length=20, unique=True, verbose_name='کد')
    is_mobile = models.BooleanField(default=False, verbose_name='موبایل است؟')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    display_order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        db_table = 'phone_types'
        verbose_name = 'نوع تلفن'
        verbose_name_plural = 'انواع تلفن'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name


class Section(models.Model):
    """بخش‌ها یا سکشن‌های هر دپارتمان"""
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name='sections',
        verbose_name='دپارتمان'
    )
    section_type = models.ForeignKey(
        SectionType, 
        on_delete=models.PROTECT, 
        related_name='sections',
        verbose_name='نوع سکشن'
    )
    name = models.CharField(max_length=100, verbose_name='نام سکشن')
    code = models.CharField(max_length=20, blank=True, null=True, verbose_name='کد سکشن')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        db_table = 'sections'
        verbose_name = 'سکشن'
        verbose_name_plural = 'سکشن‌ها'
        ordering = ['department__name', 'name']
        indexes = [
            models.Index(fields=['department', 'is_active']),
            models.Index(fields=['section_type']),
            models.Index(fields=['code']),
        ]
        unique_together = [['department', 'name']]
    
    def __str__(self):
        return f"{self.department.name} - {self.name}"
    
    @property
    def primary_phone(self):
        """شماره تلفن اصلی"""
        phone = self.phones.filter(is_primary=True, is_active=True).first()
        return phone.phone_number if phone else None
    
    @property
    def all_phones(self):
        """همه شماره‌های فعال"""
        return self.phones.filter(is_active=True)
    
    @property
    def phone_list(self):
        """لیست شماره‌ها به صورت رشته"""
        phones = self.all_phones.values_list('phone_number', flat=True)
        return ', '.join(phones) if phones else ''
    
    @property
    def current_staff_count(self):
        """تعداد پرسنل فعلی"""
        return self.assignments.filter(is_current=True).count()
    
    @property
    def full_name(self):
        """نام کامل شامل دپارتمان و نوع"""
        return f"{self.department.name} - {self.section_type.name} - {self.name}"


class SectionPhone(models.Model):
    """شماره‌های تلفن بخش"""
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='phones',
        verbose_name='بخش'
    )
    phone_type = models.ForeignKey(
        PhoneType,
        on_delete=models.PROTECT,
        verbose_name='نوع تلفن'
    )
    phone_number = models.CharField(max_length=20, verbose_name='شماره تلفن')
    is_primary = models.BooleanField(default=False, verbose_name='شماره اصلی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    description = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name='توضیحات',
        help_text='مثلاً: منشی صبح، ایستگاه شب و...'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        db_table = 'section_phones'
        verbose_name = 'تلفن بخش'
        verbose_name_plural = 'تلفن‌های بخش'
        ordering = ['section', '-is_primary', 'phone_type__display_order']
        indexes = [
            models.Index(fields=['section', 'is_active']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['is_primary']),
        ]
        unique_together = [['section', 'phone_number']]
    
    def __str__(self):
        primary = " (اصلی)" if self.is_primary else ""
        return f"{self.section.name} - {self.phone_type.name}: {self.phone_number}{primary}"
    
    def clean(self):
        """اعتبارسنجی"""
        # اگر این شماره primary شد، چک کنیم که primary دیگه‌ای با همین نوع تلفن وجود نداشته باشه
        if self.is_primary:
            existing = SectionPhone.objects.filter(
                section=self.section,
                phone_type=self.phone_type,
                is_primary=True,
                is_active=True
            ).exclude(pk=self.pk)
            
            if existing.exists():
                raise ValidationError(
                    f'این بخش در حال حاضر یک شماره {self.phone_type.name} اصلی دارد'
                )
        
        # بررسی فرمت شماره تلفن
        phone = self.phone_number.replace(' ', '').replace('-', '')
        if not phone.isdigit():
            raise ValidationError({
                'phone_number': 'شماره تلفن فقط باید شامل اعداد باشد'
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Staff(models.Model):
    """پرسنل بیمارستان"""
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    personnel_code = models.CharField(max_length=20, unique=True, verbose_name='کد پرسنلی')
    national_code = models.CharField(
        max_length=10, 
        unique=True, 
        blank=True, 
        null=True,
        verbose_name='کد ملی'
    )
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    hire_date = models.DateField(blank=True, null=True, verbose_name='تاریخ استخدام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        db_table = 'staff'
        verbose_name = 'پرسنل'
        verbose_name_plural = 'پرسنل'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['personnel_code']),
            models.Index(fields=['national_code']),
            models.Index(fields=['is_active']),
            models.Index(fields=['last_name', 'first_name']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.personnel_code})"
    
    def clean(self):
        """اعتبارسنجی کد ملی"""
        if self.national_code:
            national_code = self.national_code.replace(' ', '').replace('-', '')
            if len(national_code) != 10 or not national_code.isdigit():
                raise ValidationError({
                    'national_code': 'کد ملی باید 10 رقم باشد'
                })
            self.national_code = national_code
    
    @property
    def full_name(self):
        """نام کامل"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def primary_mobile(self):
        """موبایل اصلی"""
        phone = self.phones.filter(
            phone_type__is_mobile=True,
            is_primary=True,
            is_active=True
        ).first()
        return phone.phone_number if phone else None
    
    @property
    def all_mobiles(self):
        """همه موبایل‌های فعال"""
        return self.phones.filter(
            phone_type__is_mobile=True,
            is_active=True
        )
    
    @property
    def public_phones(self):
        """شماره‌های عمومی که همه می‌توانند ببینند"""
        return self.phones.filter(is_public=True, is_active=True)
    
    @property
    def current_section(self):
        """سکشن فعلی پرسنل"""
        current = self.assignments.filter(is_current=True).select_related('section').first()
        return current.section if current else None
    
    @property
    def current_phone(self):
        """شماره تلفن بخش فعلی"""
        section = self.current_section
        return section.primary_phone if section else None


class StaffPhone(models.Model):
    """شماره‌های تلفن/موبایل پرسنل"""
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='phones',
        verbose_name='پرسنل'
    )
    phone_type = models.ForeignKey(
        PhoneType,
        on_delete=models.PROTECT,
        verbose_name='نوع تلفن'
    )
    phone_number = models.CharField(max_length=20, verbose_name='شماره تلفن')
    is_primary = models.BooleanField(default=False, verbose_name='شماره اصلی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_public = models.BooleanField(
        default=False, 
        verbose_name='عمومی',
        help_text='اگر فعال باشد، همه می‌توانند ببینند. در غیر این صورت فقط ادمین'
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='توضیحات'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        db_table = 'staff_phones'
        verbose_name = 'تلفن پرسنل'
        verbose_name_plural = 'تلفن‌های پرسنل'
        ordering = ['staff', '-is_primary', 'phone_type__display_order']
        indexes = [
            models.Index(fields=['staff', 'is_active']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['is_primary']),
            models.Index(fields=['is_public']),
        ]
        unique_together = [['staff', 'phone_number']]
    
    def __str__(self):
        primary = " (اصلی)" if self.is_primary else ""
        public = " - عمومی" if self.is_public else " - خصوصی"
        return f"{self.staff.full_name} - {self.phone_type.name}: {self.phone_number}{primary}{public}"
    
    def clean(self):
        """اعتبارسنجی"""
        # اعتبارسنجی شماره موبایل ایران
        if self.phone_type and self.phone_type.is_mobile:
            mobile = self.phone_number.replace(' ', '').replace('-', '')
            if not mobile.startswith('09') or len(mobile) != 11 or not mobile.isdigit():
                raise ValidationError({
                    'phone_number': 'شماره موبایل باید با 09 شروع شده و 11 رقم باشد'
                })
            self.phone_number = mobile
        
        # چک کردن primary برای هر نوع تلفن
        if self.is_primary:
            existing = StaffPhone.objects.filter(
                staff=self.staff,
                phone_type=self.phone_type,
                is_primary=True,
                is_active=True
            ).exclude(pk=self.pk)
            
            if existing.exists():
                raise ValidationError(
                    f'این پرسنل در حال حاضر یک شماره {self.phone_type.name} اصلی دارد'
                )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class StaffAssignment(models.Model):
    """انتساب پرسنل به بخش"""
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='پرسنل'
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='بخش'
    )
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(blank=True, null=True, verbose_name='تاریخ پایان')
    is_current = models.BooleanField(default=True, verbose_name='فعلی')
    position = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='سمت',
        help_text='سمت یا نقش پرسنل در این بخش'
    )
    notes = models.TextField(blank=True, null=True, verbose_name='یادداشت‌ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        db_table = 'staff_assignments'
        verbose_name = 'انتساب پرسنل'
        verbose_name_plural = 'انتساب‌های پرسنل'
        ordering = ['-is_current', '-start_date']
        indexes = [
            models.Index(fields=['staff', 'is_current']),
            models.Index(fields=['section', 'is_current']),
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ]
    
    def __str__(self):
        current = " (فعلی)" if self.is_current else ""
        return f"{self.staff.full_name} - {self.section.name}{current}"
    
    def clean(self):
        """اعتبارسنجی"""
        # بررسی تاریخ پایان
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({
                'end_date': 'تاریخ پایان نمی‌تواند قبل از تاریخ شروع باشد'
            })
        
        # اگر is_current=True است، نباید end_date داشته باشد
        if self.is_current and self.end_date:
            raise ValidationError({
                'end_date': 'انتساب فعلی نمی‌تواند تاریخ پایان داشته باشد'
            })
        
        # اگر is_current=False است، باید end_date داشته باشد
        if not self.is_current and not self.end_date:
            raise ValidationError({
                'end_date': 'انتساب غیرفعلی باید تاریخ پایان داشته باشد'
            })
        
        # هر پرسنل فقط یک انتساب فعلی می‌تواند داشته باشد
        if self.is_current:
            existing = StaffAssignment.objects.filter(
                staff=self.staff,
                is_current=True
            ).exclude(pk=self.pk)
            
            if existing.exists():
                raise ValidationError(
                    'این پرسنل در حال حاضر یک انتساب فعال دارد'
                )
    
    def save(self, *args, **kwargs):
        """ذخیره با اعمال منطق خودکار"""
        # اگر این انتساب فعلی می‌شود، انتساب قبلی را غیرفعال کن
        if self.is_current and not self.pk:
            with transaction.atomic():
                # بستن انتساب‌های قبلی
                StaffAssignment.objects.filter(
                    staff=self.staff,
                    is_current=True
                ).update(
                    is_current=False,
                    end_date=self.start_date
                )
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def duration_days(self):
        """مدت زمان انتساب به روز"""
        if self.end_date:
            return (self.end_date - self.start_date).days
        return (timezone.now().date() - self.start_date).days


class TransferHistory(models.Model):
    """تاریخچه جابجایی پرسنل بین بخش‌ها"""
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='transfer_history',
        verbose_name='پرسنل'
    )
    from_section = models.ForeignKey(
        Section,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transfers_from',
        verbose_name='از بخش'
    )
    to_section = models.ForeignKey(
        Section,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transfers_to',
        verbose_name='به بخش'
    )
    transfer_date = models.DateField(verbose_name='تاریخ جابجایی')
    reason = models.TextField(blank=True, null=True, verbose_name='دلیل جابجایی')
    approved_by = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='تأیید شده توسط'
    )
    notes = models.TextField(blank=True, null=True, verbose_name='یادداشت‌ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    
    class Meta:
        db_table = 'transfer_history'
        verbose_name = 'تاریخچه جابجایی'
        verbose_name_plural = 'تاریخچه جابجایی‌ها'
        ordering = ['-transfer_date', '-created_at']
        indexes = [
            models.Index(fields=['staff', '-transfer_date']),
            models.Index(fields=['from_section']),
            models.Index(fields=['to_section']),
            models.Index(fields=['transfer_date']),
        ]
    
    def __str__(self):
        from_name = self.from_section.name if self.from_section else 'بدون بخش'
        to_name = self.to_section.name if self.to_section else 'بدون بخش'
        return f"{self.staff.full_name}: {from_name} → {to_name} ({self.transfer_date})"
    
    def clean(self):
        """اعتبارسنجی"""
        # بخش مبدأ و مقصد نباید یکی باشند
        if self.from_section and self.to_section and self.from_section == self.to_section:
            raise ValidationError(
                'بخش مبدأ و مقصد نمی‌توانند یکسان باشند'
            )


# توابع کمکی

@transaction.atomic
def transfer_staff(staff, new_section, transfer_date=None, reason=None, approved_by=None):
    """
    جابجایی پرسنل به بخش جدید
    
    Args:
        staff: شی Staff
        new_section: شی Section جدید
        transfer_date: تاریخ جابجایی (پیش‌فرض: امروز)
        reason: دلیل جابجایی
        approved_by: تأیید کننده
    
    Returns:
        tuple: (StaffAssignment جدید, TransferHistory)
    """
    if transfer_date is None:
        transfer_date = timezone.now().date()
    
    # گرفتن بخش فعلی
    current_assignment = StaffAssignment.objects.filter(
        staff=staff,
        is_current=True
    ).first()
    
    old_section = current_assignment.section if current_assignment else None
    
    # ایجاد رکورد تاریخچه
    transfer = TransferHistory.objects.create(
        staff=staff,
        from_section=old_section,
        to_section=new_section,
        transfer_date=transfer_date,
        reason=reason,
        approved_by=approved_by
    )
    
    # ایجاد انتساب جدید (save متد خودش انتساب قبلی رو می‌بنده)
    new_assignment = StaffAssignment.objects.create(
        staff=staff,
        section=new_section,
        start_date=transfer_date,
        is_current=True
    )
    
    return new_assignment, transfer


def get_section_staff_list(section, include_phones=True):
    """
    لیست پرسنل یک بخش با اطلاعات تماس
    
    Args:
        section: شی Section
        include_phones: شامل شماره تلفن‌ها
    
    Returns:
        QuerySet
    """
    queryset = Staff.objects.filter(
        assignments__section=section,
        assignments__is_current=True,
        is_active=True
    ).distinct()
    
    if include_phones:
        queryset = queryset.prefetch_related('phones')
    
    return queryset


def get_staff_transfer_timeline(staff):
    """
    تایم‌لاین کامل جابجایی‌های یک پرسنل
    
    Args:
        staff: شی Staff
    
    Returns:
        QuerySet از TransferHistory
    """
    return TransferHistory.objects.filter(
        staff=staff
    ).select_related('from_section', 'to_section').order_by('transfer_date')
