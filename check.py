import tkinter as tk
from tkinter import ttk, messagebox
from playwright.sync_api import sync_playwright
import time
import threading

class AutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GeTruck אוטומציה")
        self.root.geometry("400x500")
        self.root.configure(bg='#f0f0f0')
        
        # משתנים לשמירת נתונים
        self.email_var = tk.StringVar(value='jafora@getruck.co')
        self.password_var = tk.StringVar(value='Jafor2024')
        self.plan_name_var = tk.StringVar(value='דניאל')
        
        self.create_widgets()
        
    def create_widgets(self):
        # כותרת
        title_label = ttk.Label(self.root, text="מערכת אוטומציה GeTruck", font=('Helvetica', 16))
        title_label.pack(pady=20)
        
        # מסגרת לפרטי התחברות
        login_frame = ttk.LabelFrame(self.root, text="פרטי התחברות")
        login_frame.pack(padx=20, pady=10, fill="x")
        
        ttk.Label(login_frame, text="אימייל:").pack(padx=5, pady=5)
        ttk.Entry(login_frame, textvariable=self.email_var).pack(padx=5, pady=5, fill="x")
        
        ttk.Label(login_frame, text="סיסמה:").pack(padx=5, pady=5)
        ttk.Entry(login_frame, textvariable=self.password_var, show="*").pack(padx=5, pady=5, fill="x")
        
        # מסגרת לפרטי תכנון
        plan_frame = ttk.LabelFrame(self.root, text="פרטי תכנון")
        plan_frame.pack(padx=20, pady=10, fill="x")
        
        ttk.Label(plan_frame, text="שם התכנון:").pack(padx=5, pady=5)
        ttk.Entry(plan_frame, textvariable=self.plan_name_var).pack(padx=5, pady=5, fill="x")
        
        # כפתורי פעולה
        ttk.Button(self.root, text="התחל אוטומציה", command=self.start_automation).pack(pady=20)
        ttk.Button(self.root, text="עצור", command=self.stop_automation).pack(pady=10)
        
        # תיבת סטטוס
        self.status_text = tk.Text(self.root, height=6, width=40)
        self.status_text.pack(padx=20, pady=10)
        
    def log_status(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        
    def start_automation(self):
        # הפעלת האוטומציה בthread נפרד
        self.automation_thread = threading.Thread(target=self.run_automation)
        self.automation_thread.start()
        
    def stop_automation(self):
        self.log_status("עוצר את האוטומציה...")
        # כאן אפשר להוסיף לוגיקה לעצירת האוטומציה
        
    def run_automation(self):
        try:
            self.log_status("מתחיל אוטומציה...")
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                
                # התחברות
                self.log_status("מתחבר למערכת...")
                page.goto('https://platform-v51.getruck.co.il/login/')
                page.fill('input[type="email"]', self.email_var.get())
                page.fill('input[type="password"]', self.password_var.get())
                page.click('button[data-test-id="Button"]')
                time.sleep(5)
                
                # בחירת סניף
                self.log_status("בוחר סניף...")
                page.click('div[data-test-id="Drop-Down"]')
                time.sleep(1)
                page.click('span._item_6wn44_1:has-text("סניף 70")')
                
                # יצירת תכנון חדש
                self.log_status("יוצר תכנון חדש...")
                page.click('button:has-text("תכנון חדש")')
                page.fill('input[data-test-id="CreatePlan-Modal-Ul-Input"]', 
                         self.plan_name_var.get())
                
                self.log_status("האוטומציה הסתיימה בהצלחה!")
                
                # השארת הדפדפן פתוח
                while True:
                    time.sleep(1)
                    
        except Exception as e:
            self.log_status(f"שגיאה: {str(e)}")
            messagebox.showerror("שגיאה", f"קרתה שגיאה: {str(e)}")

def main():
    root = tk.Tk()
    app = AutomationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()