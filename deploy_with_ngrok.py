"""
Deploy application using Ngrok for quick online access
نشر التطبيق باستخدام Ngrok للوصول السريع عبر الإنترنت
"""
import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], 
                              capture_output=True, 
                              text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def download_ngrok_instructions():
    """Show instructions to download ngrok"""
    print("\n" + "="*60)
    print("❌ Ngrok غير مثبت!")
    print("="*60)
    print("\n📥 لتثبيت Ngrok:")
    print("\n1️⃣ اذهب إلى: https://ngrok.com/download")
    print("2️⃣ حمّل النسخة المناسبة لنظام Windows")
    print("3️⃣ فك الضغط عن الملف")
    print("4️⃣ ضع ملف ngrok.exe في مجلد المشروع")
    print("   أو أضفه إلى PATH")
    print("\n5️⃣ سجل حساب مجاني على: https://dashboard.ngrok.com/signup")
    print("6️⃣ احصل على Auth Token من: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("7️⃣ نفذ الأمر:")
    print("   ngrok config add-authtoken YOUR_TOKEN")
    print("\n" + "="*60)
    
    # Open ngrok website
    response = input("\n❓ هل تريد فتح موقع Ngrok الآن؟ (y/n): ")
    if response.lower() == 'y':
        webbrowser.open('https://ngrok.com/download')

def start_flask_app():
    """Start Flask application in background"""
    print("\n🚀 تشغيل تطبيق Flask...")
    
    # Start Flask in a separate process
    flask_process = subprocess.Popen(
        [sys.executable, 'run.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    return flask_process

def start_ngrok():
    """Start ngrok tunnel"""
    print("\n🌐 إنشاء نفق Ngrok...")
    print("⏳ انتظر قليلاً...")
    
    try:
        # Start ngrok
        ngrok_process = subprocess.Popen(
            ['ngrok', 'http', '5000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("\n" + "="*60)
        print("✅ تم تشغيل Ngrok بنجاح!")
        print("="*60)
        print("\n📋 للحصول على الرابط:")
        print("   1. افتح متصفح جديد")
        print("   2. اذهب إلى: http://localhost:4040")
        print("   3. انسخ الرابط الذي يبدأ بـ https://")
        print("\n💡 أو افتح: https://dashboard.ngrok.com/endpoints")
        print("\n⚠️ ملاحظات:")
        print("   - الرابط يعمل من أي مكان في العالم")
        print("   - الرابط يتغير كل مرة تشغل فيها ngrok")
        print("   - لإيقاف التطبيق: اضغط Ctrl+C")
        print("="*60)
        
        # Open ngrok dashboard
        import time
        time.sleep(3)
        webbrowser.open('http://localhost:4040')
        
        # Wait for user to stop
        print("\n⏸️ اضغط Ctrl+C لإيقاف التطبيق...")
        ngrok_process.wait()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ إيقاف التطبيق...")
        ngrok_process.terminate()
    except Exception as e:
        print(f"\n❌ خطأ: {e}")

def main():
    """Main function"""
    print("="*60)
    print("🌐 نشر التطبيق على الإنترنت باستخدام Ngrok")
    print("="*60)
    
    # Check if ngrok is installed
    if not check_ngrok_installed():
        download_ngrok_instructions()
        return
    
    print("\n✅ Ngrok مثبت!")
    
    # Start Flask app
    flask_process = start_flask_app()
    
    # Wait a bit for Flask to start
    import time
    time.sleep(3)
    
    # Start ngrok
    try:
        start_ngrok()
    finally:
        # Clean up
        print("\n🧹 تنظيف...")
        flask_process.terminate()
        print("✅ تم إيقاف التطبيق")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ تم الإيقاف بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nاضغط Enter للخروج...")

