import os
from django.db import models
from uuid import uuid4

def unique_file_name(instance, filename):
    # استخراج پسوند فایل
    ext = filename.split('.')[-1]
    # ایجاد نام منحصر به فرد بر اساس UUID
    unique_name = f"{uuid4().hex}.{ext}"
    
    # مسیر ذخیره سازی فایل در پوشه media با استفاده از نام مدل و نام فیلد
    if hasattr(instance, 'file'):
        model_name = instance._meta.model_name.lower()
        field_name = 'file'  # یا نام فیلد مربوط به FileField
        return os.path.join(model_name, field_name, unique_name)
    else:
        raise ValueError("No FileField found in the model.")
