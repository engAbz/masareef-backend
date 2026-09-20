import requests
import json
import os
from datetime import datetime

# 1. استدعاء المفتاح السري بأمان من متغيرات البيئة (لن يظهر في الكود أبداً)
API_KEY = os.getenv("EXCHANGE_API_KEY")

if not API_KEY:
    raise ValueError("🚨 خطأ قاتل: مفتاح API غير موجود! تأكد من إعداد GitHub Secrets.")

API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

def fetch_and_update_rates():
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] جاري الاتصال بالخادم لجلب الأسعار...")
        response = requests.get(API_URL, timeout=15) # تحديد وقت أقصى للاتصال
        response.raise_for_status() # إيقاف السكربت فوراً إذا كان هناك خطأ في الاتصال
        
        data = response.json()
        all_rates = data.get("conversion_rates", {})
        
        target_currencies = [
            "IQD", "SAR", "AED", "KWD", "QAR", "OMR", "BHD", "JOD", "EGP", "LBP",
            "SYP", "MAD", "TND", "DZD", "LYD", "TRY", "USD", "EUR", "GBP", "JPY",
            "CNY", "CAD", "AUD", "CHF", "RUB", "INR", "BRL", "MXN"
        ]
        
        filtered_rates = {code: all_rates[code] for code in target_currencies if code in all_rates}
        
        # التعديلات اليدوية لأسعار السوق الموازي (يمكنك تغيير الرقم يومياً هنا إذا أردت)
        # filtered_rates["IQD"] = 1530.0 

        output_data = {
            "timestamp": data.get("time_last_update_unix", int(datetime.now().timestamp())),
            "base": "USD",
            "rates": filtered_rates
        }
        
        # حفظ الملف 
        with open("rates.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print("✅ تم تحديث ملف rates.json بنجاح!")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء جلب البيانات: {e}")
        raise e # لكي يظهر الخطأ باللون الأحمر في سجلات GitHub

if __name__ == "__main__":
    fetch_and_update_rates()
