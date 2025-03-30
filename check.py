import asyncio
from playwright.async_api import async_playwright

async def login_to_getruck():
    # הפרטים להתחברות
    url = "https://platform-v51.getruck.co.il/login/"
    username = "jafora@getruck.co"
    password = "Jafor2024"
    
    # יצירת מופע של Playwright
    async with async_playwright() as playwright:
        # הפעלת דפדפן
        browser = await playwright.chromium.launch(headless=False)  # שינוי ל-True לריצה ללא ממשק גרפי
        
        # יצירת עמוד חדש
        page = await browser.new_page()
        
        try:
            # כניסה לאתר
            print("מתחבר לאתר...")
            await page.goto(url)
            
            # המתנה לטעינת דף ההתחברות
            await page.wait_for_selector('input[type="email"]')
            
            # הזנת שם משתמש וסיסמה
            print("מזין פרטי התחברות...")
            await page.fill('input[type="email"]', username)
            await page.fill('input[type="password"]', password)
            
            # לחיצה על כפתור ההתחברות
            print("מתחבר...")
            login_button = await page.query_selector('button[type="submit"]')
            await login_button.click()
            
            # המתנה לטעינת הדף אחרי התחברות
            await page.wait_for_load_state("networkidle")
            
            # בדיקה אם ההתחברות הצליחה
            if page.url != url:  # אם הURL השתנה, כנראה שההתחברות הצליחה
                print("התחברות הצליחה!")
            else:
                print("התחברות נכשלה.")
            
            # כאן לא נדרשת המתנה נוספת כי יש לנו המתנה של 15 שניות בסוף התהליך
            
        except Exception as e:
            print(f"שגיאה: {str(e)}")
        
        # השארת הדפדפן פתוח ל-15 שניות
        print("התחברות הושלמה. הדפדפן יישאר פתוח למשך 15 שניות...")
        await asyncio.sleep(15)
        
        # סגירת הדפדפן לאחר ההמתנה
        await browser.close()
        print("הדפדפן נסגר.")

    # הרצת הפונקציה
if __name__ == "__main__":
    asyncio.run(login_to_getruck())
    print("התוכנית הסתיימה.")