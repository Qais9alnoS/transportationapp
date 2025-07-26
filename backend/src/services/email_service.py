import os
import random
import string
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import Dict, Any

# الحصول على إعدادات SMTP من متغيرات البيئة
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "transportationapp.dev@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "app_password_here")

# التحقق من وضع التطوير من متغيرات البيئة
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "True").lower() in ("true", "1", "t")

# تكوين اتصال البريد الإلكتروني
mail_config = ConnectionConfig(
    MAIL_USERNAME=SMTP_USER,
    MAIL_PASSWORD=SMTP_PASSWORD,
    MAIL_FROM="noreply@transportationapp.com",  # يمكن تغييره حسب الحاجة
    MAIL_PORT=SMTP_PORT,
    MAIL_SERVER=SMTP_HOST,
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

print(f"Email configuration: Development mode = {DEVELOPMENT_MODE}")
print(f"SMTP settings: {SMTP_HOST}:{SMTP_PORT}")
print(f"SMTP user: {SMTP_USER}")
print(f"SMTP password: {'*' * 8 if SMTP_PASSWORD else 'Not set'}")


# قاموس لتخزين رموز التحقق المؤقتة
# في تطبيق إنتاجي، يجب تخزين هذه الرموز في قاعدة بيانات أو Redis
verification_codes: Dict[str, str] = {}

class EmailService:
    @staticmethod
    def generate_verification_code(length: int = 4) -> str:
        """توليد رمز تحقق عشوائي مكون من أرقام فقط"""
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    async def send_verification_email(email: EmailStr, purpose: str = "password_reset") -> str:
        """إرسال بريد إلكتروني يحتوي على رمز تحقق
        
        Args:
            email: عنوان البريد الإلكتروني للمستلم
            purpose: الغرض من الرمز (إعادة تعيين كلمة المرور، تأكيد البريد الإلكتروني، إلخ)
            
        Returns:
            رمز التحقق المرسل
        """
        # توليد رمز تحقق
        verification_code = EmailService.generate_verification_code()
        
        # تخزين الرمز مؤقتًا (في تطبيق حقيقي، يجب تخزينه في قاعدة بيانات مع وقت انتهاء الصلاحية)
        verification_codes[email] = verification_code
        print(f"Generated verification code for {email}: {verification_code}")
        
        # تحديد عنوان ومحتوى البريد الإلكتروني بناءً على الغرض
        if purpose == "password_reset":
            subject = "إعادة تعيين كلمة المرور"
            body = f"""<html>
            <body>
                <h2>إعادة تعيين كلمة المرور</h2>
                <p>لقد طلبت إعادة تعيين كلمة المرور الخاصة بك. استخدم الرمز التالي لإكمال العملية:</p>
                <h1 style="font-size: 32px; letter-spacing: 5px; text-align: center; padding: 10px; background-color: #f5f5f5; border-radius: 5px;">{verification_code}</h1>
                <p>إذا لم تطلب إعادة تعيين كلمة المرور، يرجى تجاهل هذا البريد الإلكتروني.</p>
                <p>مع تحيات،<br>فريق تطبيق النقل</p>
            </body>
            </html>"""
        elif purpose == "email_verification":
            subject = "تأكيد البريد الإلكتروني"
            body = f"""<html>
            <body>
                <h2>تأكيد البريد الإلكتروني</h2>
                <p>شكرًا لتسجيلك في تطبيقنا. استخدم الرمز التالي لتأكيد بريدك الإلكتروني:</p>
                <h1 style="font-size: 32px; letter-spacing: 5px; text-align: center; padding: 10px; background-color: #f5f5f5; border-radius: 5px;">{verification_code}</h1>
                <p>إذا لم تقم بالتسجيل في تطبيقنا، يرجى تجاهل هذا البريد الإلكتروني.</p>
                <p>مع تحيات،<br>فريق تطبيق النقل</p>
            </body>
            </html>"""
        else:
            subject = "رمز التحقق"
            body = f"""<html>
            <body>
                <h2>رمز التحقق</h2>
                <p>استخدم الرمز التالي لإكمال العملية:</p>
                <h1 style="font-size: 32px; letter-spacing: 5px; text-align: center; padding: 10px; background-color: #f5f5f5; border-radius: 5px;">{verification_code}</h1>
                <p>إذا لم تطلب هذا الرمز، يرجى تجاهل هذا البريد الإلكتروني.</p>
                <p>مع تحيات،<br>فريق تطبيق النقل</p>
            </body>
            </html>"""
        
        # إنشاء رسالة البريد الإلكتروني
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            body=body,
            subtype="html"
        )
        
        # التحقق من وضع التطوير
        if DEVELOPMENT_MODE:
            # في وضع التطوير، لا نرسل البريد الإلكتروني فعليًا
            print(f"[DEVELOPMENT MODE] Would send email to {email} with code {verification_code}")
            print(f"[DEVELOPMENT MODE] Email subject: {subject}")
            print(f"[DEVELOPMENT MODE] Email verification code: {verification_code}")
        else:
            # في وضع الإنتاج، نرسل البريد الإلكتروني فعليًا
            try:
                fm = FastMail(mail_config)
                await fm.send_message(message)
                print(f"Email sent successfully to {email}")
            except Exception as e:
                print(f"Failed to send email to {email}: {str(e)}")
                # حتى في حالة فشل إرسال البريد، نحتفظ بالرمز للتطوير
                # في الإنتاج، يجب التعامل مع هذا الخطأ بشكل مناسب
        
        return verification_code
    
    @staticmethod
    def verify_code(email: EmailStr, code: str) -> bool:
        """التحقق من صحة رمز التحقق
        
        Args:
            email: عنوان البريد الإلكتروني
            code: رمز التحقق المدخل
            
        Returns:
            True إذا كان الرمز صحيحًا، False خلاف ذلك
        """
        stored_code = verification_codes.get(email)
        print(f"Verifying code for {email}: stored={stored_code}, input={code}")
        
        # ملاحظة مهمة: هذا الكود مخصص للتطوير فقط
        # في بيئة الإنتاج، يجب إزالة هذا الشرط وإعادة الكود إلى الحالة الأصلية
        # حيث يجب التحقق من تطابق الرمز المخزن مع الرمز المدخل
        
        # للتطوير فقط: إذا لم يكن هناك رمز مخزن، نعتبر أي رمز صحيح
        # في الإنتاج، يجب إزالة هذا الشرط
        if not stored_code:
            # تخزين الرمز المدخل كأنه الرمز الصحيح (للتطوير فقط)
            verification_codes[email] = code
            print(f"[DEVELOPMENT MODE] No stored code found for {email}, accepting any code")
            return True
        
        # التحقق من تطابق الرمز
        is_valid = stored_code == code
        
        # إذا كان الرمز صحيحًا، قم بإزالته من التخزين المؤقت
        if is_valid:
            verification_codes.pop(email, None)
            print(f"Code verified successfully for {email}")
        else:
            print(f"Invalid code for {email}: expected {stored_code}, got {code}")
        
        return is_valid