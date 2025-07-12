"""
Dashboard Configuration
إعدادات لوحة التحكم الحكومية المتقدمة
"""

from typing import Dict, Any, List
from datetime import timedelta
import os

# ==================== DASHBOARD SETTINGS ====================

# إعدادات عامة للوحة التحكم
DASHBOARD_CONFIG = {
    "name": "لوحة التحكم الحكومية - Makroji",
    "version": "2.0.0",
    "description": "نظام تحليلي متقدم لإدارة النقل العام",
    "admin_required": True,
    "refresh_interval": 300,  # 5 دقائق
    "max_data_points": 1000,
    "timezone": "Asia/Riyadh"
}

# ==================== ANALYTICS SETTINGS ====================

# إعدادات التحليلات
ANALYTICS_CONFIG = {
    "real_time": {
        "enabled": True,
        "update_interval": 60,  # ثانية واحدة
        "cache_duration": 300,  # 5 دقائق
        "max_history_days": 30
    },
    "predictive": {
        "enabled": True,
        "forecast_days": 7,
        "confidence_threshold": 0.8,
        "min_data_points": 7,
        "algorithm": "linear_regression"
    },
    "geographic": {
        "enabled": True,
        "precision": 3,  # دقة الإحداثيات
        "max_hotspots": 20,
        "coverage_radius_km": 5
    },
    "user_behavior": {
        "enabled": True,
        "session_timeout": 3600,  # ساعة واحدة
        "activity_threshold": 5,  # عدد العمليات
        "segmentation_enabled": True
    }
}

# ==================== PERFORMANCE SETTINGS ====================

# إعدادات الأداء
PERFORMANCE_CONFIG = {
    "caching": {
        "enabled": True,
        "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379"),
        "default_ttl": 3600,  # ساعة واحدة
        "max_memory": "512mb"
    },
    "database": {
        "connection_pool_size": 20,
        "max_overflow": 30,
        "pool_timeout": 30,
        "pool_recycle": 3600
    },
    "api": {
        "rate_limit": 100,  # طلب في الدقيقة
        "timeout": 30,  # ثانية
        "max_payload_size": "10mb"
    }
}

# ==================== VISUALIZATION SETTINGS ====================

# إعدادات الرسوم البيانية
VISUALIZATION_CONFIG = {
    "charts": {
        "default_colors": [
            "#2196F3",  # أزرق
            "#4CAF50",  # أخضر
            "#FF9800",  # برتقالي
            "#F44336",  # أحمر
            "#9C27B0",  # بنفسجي
            "#607D8B",  # رمادي
            "#795548",  # بني
            "#FF5722"   # أحمر برتقالي
        ],
        "chart_height": 220,
        "responsive": True,
        "animation": True
    },
    "maps": {
        "default_center": {
            "lat": 24.7136,
            "lng": 46.6753
        },
        "default_zoom": 10,
        "tile_provider": "openstreetmap"
    }
}

# ==================== ALERT SETTINGS ====================

# إعدادات التنبيهات
ALERT_CONFIG = {
    "enabled": True,
    "channels": ["email", "sms", "push"],
    "thresholds": {
        "system_health": {
            "critical": 0.8,  # أقل من 80%
            "warning": 0.9   # أقل من 90%
        },
        "response_time": {
            "critical": 5000,  # أكثر من 5 ثوان
            "warning": 2000   # أكثر من 2 ثانية
        },
        "error_rate": {
            "critical": 0.05,  # أكثر من 5%
            "warning": 0.02   # أكثر من 2%
        },
        "complaints": {
            "critical": 50,   # أكثر من 50 شكوى
            "warning": 20     # أكثر من 20 شكوى
        }
    },
    "recipients": {
        "admin": ["admin@makroji.gov.sa"],
        "technical": ["tech@makroji.gov.sa"],
        "management": ["management@makroji.gov.sa"]
    }
}

# ==================== EXPORT SETTINGS ====================

# إعدادات التصدير
EXPORT_CONFIG = {
    "formats": ["pdf", "excel", "csv", "json"],
    "max_file_size": "50mb",
    "retention_days": 90,
    "compression": True,
    "templates": {
        "monthly_report": "templates/monthly_report.html",
        "performance_report": "templates/performance_report.html",
        "complaints_report": "templates/complaints_report.html"
    }
}

# ==================== SECURITY SETTINGS ====================

# إعدادات الأمان
SECURITY_CONFIG = {
    "authentication": {
        "jwt_secret": os.getenv("JWT_SECRET", "your-secret-key"),
        "jwt_expiry": 3600,  # ساعة واحدة
        "refresh_expiry": 604800,  # أسبوع واحد
        "max_login_attempts": 5,
        "lockout_duration": 900  # 15 دقيقة
    },
    "authorization": {
        "admin_roles": ["super_admin", "admin"],
        "analyst_roles": ["analyst", "data_scientist"],
        "viewer_roles": ["viewer", "reporter"]
    },
    "data_protection": {
        "encryption_enabled": True,
        "pii_masking": True,
        "audit_logging": True,
        "data_retention_days": 2555  # 7 سنوات
    }
}

# ==================== FEATURE FLAGS ====================

# أعلام الميزات
FEATURE_FLAGS = {
    "advanced_analytics": True,
    "predictive_insights": True,
    "geographic_intelligence": True,
    "real_time_monitoring": True,
    "complaint_analysis": True,
    "system_health": True,
    "export_reports": True,
    "alerts": True,
    "mobile_dashboard": True,
    "api_documentation": True
}

# ==================== CUSTOMIZATION SETTINGS ====================

# إعدادات التخصيص
CUSTOMIZATION_CONFIG = {
    "branding": {
        "logo_url": "/static/images/logo.png",
        "primary_color": "#2196F3",
        "secondary_color": "#4CAF50",
        "accent_color": "#FF9800"
    },
    "localization": {
        "default_language": "ar",
        "supported_languages": ["ar", "en"],
        "date_format": "DD/MM/YYYY",
        "time_format": "HH:mm",
        "currency": "SAR"
    },
    "dashboard_layout": {
        "default_theme": "light",
        "available_themes": ["light", "dark", "auto"],
        "sidebar_collapsed": False,
        "widgets_per_row": 3
    }
}

# ==================== INTEGRATION SETTINGS ====================

# إعدادات التكامل
INTEGRATION_CONFIG = {
    "external_apis": {
        "google_maps": {
            "enabled": True,
            "api_key": os.getenv("GOOGLE_MAPS_API_KEY"),
            "usage_limit": 10000
        },
        "weather": {
            "enabled": False,
            "api_key": os.getenv("WEATHER_API_KEY"),
            "update_interval": 3600
        },
        "traffic": {
            "enabled": True,
            "api_key": os.getenv("TRAFFIC_API_KEY"),
            "update_interval": 300
        }
    },
    "notifications": {
        "email": {
            "enabled": True,
            "smtp_host": os.getenv("SMTP_HOST"),
            "smtp_port": int(os.getenv("SMTP_PORT", "587")),
            "smtp_user": os.getenv("SMTP_USER"),
            "smtp_password": os.getenv("SMTP_PASSWORD")
        },
        "sms": {
            "enabled": False,
            "provider": "twilio",
            "account_sid": os.getenv("TWILIO_ACCOUNT_SID"),
            "auth_token": os.getenv("TWILIO_AUTH_TOKEN")
        },
        "push": {
            "enabled": True,
            "firebase_key": os.getenv("FIREBASE_KEY")
        }
    }
}

# ==================== MONITORING SETTINGS ====================

# إعدادات المراقبة
MONITORING_CONFIG = {
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file_rotation": "daily",
        "max_files": 30
    },
    "metrics": {
        "enabled": True,
        "collector": "prometheus",
        "port": 9090,
        "endpoint": "/metrics"
    },
    "health_checks": {
        "enabled": True,
        "interval": 60,
        "timeout": 10,
        "endpoints": [
            "/health",
            "/ready",
            "/live"
        ]
    }
}

# ==================== HELPER FUNCTIONS ====================

def get_dashboard_config() -> Dict[str, Any]:
    """الحصول على إعدادات لوحة التحكم"""
    return DASHBOARD_CONFIG

def get_analytics_config() -> Dict[str, Any]:
    """الحصول على إعدادات التحليلات"""
    return ANALYTICS_CONFIG

def get_performance_config() -> Dict[str, Any]:
    """الحصول على إعدادات الأداء"""
    return PERFORMANCE_CONFIG

def get_visualization_config() -> Dict[str, Any]:
    """الحصول على إعدادات الرسوم البيانية"""
    return VISUALIZATION_CONFIG

def get_alert_config() -> Dict[str, Any]:
    """الحصول على إعدادات التنبيهات"""
    return ALERT_CONFIG

def get_export_config() -> Dict[str, Any]:
    """الحصول على إعدادات التصدير"""
    return EXPORT_CONFIG

def get_security_config() -> Dict[str, Any]:
    """الحصول على إعدادات الأمان"""
    return SECURITY_CONFIG

def get_feature_flags() -> Dict[str, bool]:
    """الحصول على أعلام الميزات"""
    return FEATURE_FLAGS

def get_customization_config() -> Dict[str, Any]:
    """الحصول على إعدادات التخصيص"""
    return CUSTOMIZATION_CONFIG

def get_integration_config() -> Dict[str, Any]:
    """الحصول على إعدادات التكامل"""
    return INTEGRATION_CONFIG

def get_monitoring_config() -> Dict[str, Any]:
    """الحصول على إعدادات المراقبة"""
    return MONITORING_CONFIG

def is_feature_enabled(feature_name: str) -> bool:
    """التحقق من تفعيل ميزة معينة"""
    return FEATURE_FLAGS.get(feature_name, False)

def get_cache_ttl(cache_type: str) -> int:
    """الحصول على وقت التخزين المؤقت"""
    cache_ttls = {
        "real_time": 60,
        "analytics": 3600,
        "predictions": 7200,
        "geographic": 1800,
        "complaints": 900,
        "system": 300
    }
    return cache_ttls.get(cache_type, 3600)

def get_chart_colors() -> List[str]:
    """الحصول على ألوان الرسوم البيانية"""
    return VISUALIZATION_CONFIG["charts"]["default_colors"]

def get_alert_thresholds() -> Dict[str, Dict[str, float]]:
    """الحصول على حدود التنبيهات"""
    return ALERT_CONFIG["thresholds"]

# ==================== VALIDATION FUNCTIONS ====================

def validate_config() -> List[str]:
    """التحقق من صحة الإعدادات"""
    errors = []
    
    # التحقق من إعدادات قاعدة البيانات
    if PERFORMANCE_CONFIG["database"]["connection_pool_size"] < 1:
        errors.append("حجم تجمع الاتصالات يجب أن يكون أكبر من 0")
    
    # التحقق من إعدادات API
    if PERFORMANCE_CONFIG["api"]["rate_limit"] < 1:
        errors.append("حد معدل الطلبات يجب أن يكون أكبر من 0")
    
    # التحقق من إعدادات التنبيهات
    for threshold_type, thresholds in ALERT_CONFIG["thresholds"].items():
        for level, value in thresholds.items():
            if value < 0:
                errors.append(f"قيمة {threshold_type}.{level} يجب أن تكون موجبة")
    
    return errors

def get_config_summary() -> Dict[str, Any]:
    """الحصول على ملخص الإعدادات"""
    return {
        "dashboard": {
            "name": DASHBOARD_CONFIG["name"],
            "version": DASHBOARD_CONFIG["version"],
            "admin_required": DASHBOARD_CONFIG["admin_required"]
        },
        "features": {
            "enabled_features": [k for k, v in FEATURE_FLAGS.items() if v],
            "total_features": len(FEATURE_FLAGS)
        },
        "performance": {
            "caching_enabled": PERFORMANCE_CONFIG["caching"]["enabled"],
            "rate_limit": PERFORMANCE_CONFIG["api"]["rate_limit"]
        },
        "security": {
            "authentication_enabled": True,
            "encryption_enabled": SECURITY_CONFIG["data_protection"]["encryption_enabled"]
        }
    }

# ==================== ENVIRONMENT SPECIFIC CONFIGS ====================

# إعدادات بيئة التطوير
DEVELOPMENT_CONFIG = {
    "debug": True,
    "log_level": "DEBUG",
    "cache_enabled": False,
    "rate_limit": 1000,
    "database_pool_size": 5
}

# إعدادات بيئة الإنتاج
PRODUCTION_CONFIG = {
    "debug": False,
    "log_level": "WARNING",
    "cache_enabled": True,
    "rate_limit": 100,
    "database_pool_size": 20
}

def get_environment_config(environment: str = "development") -> Dict[str, Any]:
    """الحصول على إعدادات البيئة"""
    if environment == "production":
        return PRODUCTION_CONFIG
    return DEVELOPMENT_CONFIG 