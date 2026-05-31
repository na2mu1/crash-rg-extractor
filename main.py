import streamlit as st
import time
import re
import json
from playwright.sync_api import sync_playwright

# Config লোড
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

st.set_page_config(page_title="N1ebajee RG Extractor", layout="centered")
st.title("🚀 N1ebajee Aviator RG Extractor")
st.caption("অটোমেটিক • প্রতি রাউন্ডের RG নাম্বার দেখাবে")

if st.button("🚀 অ্যাপ শুরু করো", type="primary", use_container_width=True):
    with st.spinner("ব্রাউজার খুলছে..."):
        with sync_playwright() as p:
            # ব্রাউজার চালু (দেখা যাবে)
            browser = p.chromium.launch(headless=False, slow_mo=400)
            page = browser.new_page()
            page.goto(config["url"])
            
            st.success("✅ ব্রাউজার খোলা হয়েছে!")
            st.info("**এখন করণীয়:**\n1. লগইন করো\n2. Aviator গেমে যাও\n3. 'Previous' ট্যাব ওপেন করে রাখো")
            
            last_rg = None
            placeholder = st.empty()
            status = st.empty()
            
            while True:
                try:
                    # Aviator গেমের RG নাম্বার খুঁজে বের করার চেষ্টা (আপডেটেড)
                    page.wait_for_timeout(800)
                    
                    # বিভিন্ন সম্ভাব্য উপায়ে RG নাম্বার খুঁজবে
                    texts = page.evaluate("""
                        () => {
                            return Array.from(document.querySelectorAll('*'))
                                .map(el => el.textContent || '')
                                .filter(text => /\b\d{6,}\b/.test(text));
                        }
                    """)
                    
                    for text in texts[-10:]:  # শেষ কয়েকটা চেক
                        match = re.search(r'(\d{6,})', text)
                        if match:
                            current_rg = match.group(1)
                            if current_rg != last_rg and len(current_rg) >= 6:
                                last_rg = current_rg
                                placeholder.success(f"""
                                🆕 **নতুন রাউন্ড শুরু হয়েছে!**

                                **RG Number:** `{current_rg}`
                                """)
                                st.balloons()
                                break
                except:
                    status.info("মনিটরিং চলছে...")
                
                time.sleep(1)        btn_frame = CTkFrame(self.root, fg_color="transparent")
        btn_frame.pack(pady=25)
        
        self.start_btn = CTkButton(btn_frame, text="▶ START", width=180, height=55, 
                                  fg_color="#00cc66", hover_color="#00ff88", font=CTkFont(size=16, weight="bold"),
                                  command=self.start_extraction)
        self.start_btn.pack(side="left", padx=15)
        
        self.stop_btn = CTkButton(btn_frame, text="⛔ STOP", width=180, height=55, 
                                 fg_color="#ff3333", hover_color="#ff5555", font=CTkFont(size=16, weight="bold"),
                                 command=self.stop_extraction, state="disabled")
        self.stop_btn.pack(side="left", padx=15)
        
        # Auto Refresh
        self.auto_refresh = BooleanVar(value=True)
        CTkCheckBox(self.root, text="Auto Refresh (প্রতি ৫ সেকেন্ড)", 
                   variable=self.auto_refresh, font=CTkFont(size=14)).pack(pady=10)
        
        # Result Box
        CTkLabel(self.root, text="Log & Result:", font=CTkFont(size=16)).pack(anchor="w", padx=50, pady=(20,5))
        self.result_text = CTkTextbox(self.root, width=750, height=280, font=CTkFont(size=13))
        self.result_text.pack(padx=50, pady=10)
        
    def show_popup(self, rg_text):
        """Popup Window"""
        popup = CTkToplevel(self.root)
        popup.title("✅ RG Number Found!")
        popup.geometry("500x300")
        popup.configure(fg_color="#1a1a1a")
        popup.grab_set()  # Make it modal
        
        CTkLabel(popup, text="🎉 RG Number পাওয়া গেছে!", 
                font=CTkFont(size=20, weight="bold"), text_color="#00ff88").pack(pady=20)
        
        rg_label = CTkLabel(popup, text=rg_text, font=CTkFont(size=18), text_color="yellow")
        rg_label.pack(pady=10)
        
        CTkButton(popup, text="কপি করুন", width=200, height=50, fg_color="#00aa66",
                 command=lambda: self.copy_to_clipboard(rg_text, popup)).pack(pady=20)
        
        # Play sound
        try:
            winsound.Beep(800, 300)
            winsound.Beep(1000, 300)
        except:
            pass
    
    def copy_to_clipboard(self, text, popup=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.log("📋 কপি করা হয়েছে!")
        if popup:
            popup.destroy()
    
    def start_extraction(self):
        url = self.url_entry.get().strip()
        if not url:
            self.log("❌ লিংক দিন")
            return
        
        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        thread = threading.Thread(target=self.extract_rg, args=(url,))
        thread.daemon = True
        thread.start()
    
    def stop_extraction(self):
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        self.log("🛑 থেমে গেছে")
    
    def extract_rg(self, url):
        try:
            self.log("🌐 ব্রাউজার খুলছে...")
            
            options = Options()
            # options.add_argument("--headless")   # চাইলে এটা অন করতে পারো (ব্রাউজার দেখা যাবে না)
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            self.driver.get(url)
            self.log("✅ পেজ লোড হয়েছে। RG খোঁজা হচ্ছে...")
            
            start_time = time.time()
            
            while self.is_running and (time.time() - start_time) < 90:  # ৯০ সেকেন্ড পর্যন্ত
                try:
                    elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'RG') or contains(text(), 'Round') or contains(text(), 'Channel') or contains(text(), '#')]")
                    
                    for el in elements:
                        text = el.text.strip()
                        if len(text) > 3 and any(k in text.lower() for k in ['rg', 'round', 'channel', '#', 'id']):
                            self.log(f"🎯 পাওয়া গেছে: {text}")
                            self.show_popup(text)   # Popup দেখাবে
                            return
                    
                    if self.auto_refresh.get():
                        time.sleep(5)
                        self.driver.refresh()
                        self.log("🔄 পেজ রিফ্রেশ করা হচ্ছে...")
                    else:
                        time.sleep(3)
                        
                except:
                    time.sleep(3)
            
            self.log("⏰ সময় শেষ। আবার চেষ্টা করুন।")
            
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            self.stop_extraction()
    
    def log(self, message):
        self.result_text.insert("end", f"{message}\n")
        self.result_text.see("end")

if __name__ == "__main__":
    app = CrashRGExtractor()
    app.root.mainloop()
