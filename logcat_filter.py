#!/usr/bin/env python3
import subprocess
import sys
import re
import time

def get_app_pid(package_name):
    """Получаем PID процесса приложения (работает на всех ОС)"""
    print(f"Поиск процесса для пакета: {package_name}")
    
    try:
        # Получаем список процессов
        result = subprocess.run(['adb', 'shell', 'ps'], capture_output=True, text=True)
        
        # Ищем строки с именем пакета
        for line in result.stdout.split('\n'):
            if package_name in line:
                # Извлекаем PID (второй столбец)
                parts = line.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    return parts[1]
    except Exception as e:
        print(f"Ошибка при получении PID: {e}")
    
    return None

def run_logcat_filtered(package_name):
    """Запускает logcat и фильтрует на уровне Python"""
    
    # Запускаем logcat
    logcat_process = subprocess.Popen(
        ['adb', 'logcat', '-v', 'brief'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    print("\n--- Начало вывода логов (Ctrl+C для остановки) ---\n")
    
    pid = None
    try:
        for line in logcat_process.stdout:
            line = line.strip()
            
            # Если PID еще не найден, ищем его каждую строку
            if not pid and package_name in line:
                pid = get_app_pid(package_name)
                if pid:
                    print(f"✅ Найден PID приложения: {pid}\n")
            
            # Фильтруем по PID или по имени пакета в сообщении
            if f"({pid})" in line or package_name in line:
                print(line)
                
    except KeyboardInterrupt:
        print("\n\n--- Остановка сбора логов ---")
        logcat_process.terminate()
        sys.exit(0)

def main():
    if len(sys.argv) != 2:
        print("Использование: python logcat_filter_win.py <имя_пакета>")
        print("Пример: python logcat_filter.py mobile.test.sound")
        sys.exit(1)
    
    package_name = sys.argv[1]
    
    # Проверка доступности ADB
    try:
        subprocess.run(['adb', 'version'], check=True, capture_output=True)
    except:
        print("❌ Ошибка: ADB не найден. Добавьте его в PATH.")
        sys.exit(1)
    
    # Проверка подключения устройства
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    if "device" not in result.stdout:
        print("❌ Устройство не подключено. Запустите adb devices")
        sys.exit(1)
    
    run_logcat_filtered(package_name)

if __name__ == "__main__":
    main()