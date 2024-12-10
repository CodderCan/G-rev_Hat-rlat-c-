import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import threading
import time
import os

# Dosyadaki görevleri yükle (varsa)
def load_tasks():
    try:
        with open("tasks.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Dosya yoksa veya boşsa, yeni liste döndür

# Dosyaya görevleri kaydet
def save_tasks():
    with open("tasks.json", "w", encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False)

# Yapmanız gereken işler listesi
tasks = load_tasks()

# Bildirim gönderme kilidi
notification_lock = threading.Lock()

# Zaman kontrolü ve bildirim gönderme fonksiyonu
def check_reminders():
    global tasks
    try:
        current = datetime.now()
        tasks_to_remove = []
        
        for task in tasks:
            try:
                task_time = datetime.strptime(task['time'], "%Y-%m-%d %H:%M:%S")
                
                # Sadece gelecek veya şu anki zamandaki görevler için bildirim gönder
                if current >= task_time:
                    with notification_lock:
                        # Bildirim Gönder
                        show_notification(f"Yapmanız gereken iş: {task['task']}")
                        tasks_to_remove.append(task)
            except ValueError:
                print(f"Hatalı tarih formatı: {task['time']}")
        
        # Bildirimi gönderilen görevleri listeden çıkar
        for task in tasks_to_remove:
            tasks.remove(task)
        
        # Görev listesini güncelle
        if tasks_to_remove:
            save_tasks()
            update_task_listbox()
    
    except Exception as e:
        print(f"Görev kontrol hatası: {e}")

# Bildirim zamanlayıcısı
def start_reminder_thread():
    def run_check():
        while True:
            check_reminders()
            time.sleep(5)  # 5 saniyede bir kontrol et
    
    # Daemon thread oluştur (arkplan görevi)
    reminder_thread = threading.Thread(target=run_check, daemon=True)
    reminder_thread.start()

# Bildirim gösteren fonksiyon
def show_notification(message):
    try:
        # Ana pencere açıksa bildirim gönder
        if window.state() == 'normal':
            messagebox.showinfo("Görev Hatırlatıcı", message)
        else:
            # Pencere kapalıysa tkinter dışında bildirim gönder
            tk.messagebox.showinfo("Görev Hatırlatıcı", message)
    except Exception as e:
        print(f"Bildirim hatası: {e}")

# Yeni bir görev eklemek için fonksiyon
def add_task():
    task_description = task_entry.get()
    task_time = time_entry.get()
    
    # Kullanıcı gerekli alanları doldurmuş mu kontrol et
    if not task_description or not task_time:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
        return
    
    # Zamanın geçerli formatta olup olmadığını kontrol et
    try:
        datetime.strptime(task_time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        messagebox.showerror("Hata", "Zaman formatı yanlış! Lütfen 'YYYY-MM-DD HH:MM:SS' formatını kullanın.")
        return
    
    # Yeni görevi ekle
    tasks.append({"task": task_description, "time": task_time})
    
    # Görevleri dosyaya kaydet
    save_tasks()

    # Görev listesini güncelle
    update_task_listbox()

    # Girdi alanlarını temizle
    task_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

# Görevleri ekranda listele
def update_task_listbox():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, f"{task['task']} - {task['time']}")

# Ana pencereyi oluştur
window = tk.Tk()
window.title("Yapılacaklar Listesi")

# Görev eklemek için UI elemanları
task_label = tk.Label(window, text="Yapmanız gereken iş:")
task_label.pack(pady=5)

task_entry = tk.Entry(window, width=50)
task_entry.pack(pady=5)

time_label = tk.Label(window, text="Hatırlatma zamanı (YYYY-MM-DD HH:MM:SS):")
time_label.pack(pady=5)

time_entry = tk.Entry(window, width=50)
time_entry.pack(pady=5)

add_button = tk.Button(window, text="Görev Ekle", command=add_task)
add_button.pack(pady=10)

# Görev listesi gösterimi
task_listbox = tk.Listbox(window, width=60, height=10)
task_listbox.pack(pady=10)

# Başlangıçta görevleri listbox'a ekleyelim
update_task_listbox()

# Bildirim thread'ini başlat
start_reminder_thread()

# Ana döngüyü başlat
window.mainloop()