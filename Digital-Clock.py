import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import time
import math

class AdvancedDigitalClock(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Digital Clock")
        self.geometry("800x400")
        self.resizable(False, False)
        
        # Modern color scheme
        self.bg_color = "#121212"
        self.primary_color = "#4FC3F7"
        self.secondary_color = "#FF4081"
        self.text_color = "#E0E0E0"
        self.accent_color = "#7C4DFF"
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=self.bg_color)
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Date display
        self.date_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Helvetica", 24),
            text_color=self.text_color
        )
        self.date_label.pack(pady=(0, 20))
        
        # Time display
        self.time_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.time_frame.pack(expand=True)
        
        self.hour_label = ctk.CTkLabel(
            self.time_frame,
            text="",
            font=("Helvetica", 80, "bold"),
            text_color=self.primary_color
        )
        self.hour_label.pack(side=tk.LEFT)
        
        self.colon_label = ctk.CTkLabel(
            self.time_frame,
            text=":",
            font=("Helvetica", 80, "bold"),
            text_color=self.text_color
        )
        self.colon_label.pack(side=tk.LEFT, padx=5)
        
        self.minute_label = ctk.CTkLabel(
            self.time_frame,
            text="",
            font=("Helvetica", 80, "bold"),
            text_color=self.primary_color
        )
        self.minute_label.pack(side=tk.LEFT)
        
        self.second_colon_label = ctk.CTkLabel(
            self.time_frame,
            text=":",
            font=("Helvetica", 80, "bold"),
            text_color=self.text_color
        )
        self.second_colon_label.pack(side=tk.LEFT, padx=5)
        
        self.second_label = ctk.CTkLabel(
            self.time_frame,
            text="",
            font=("Helvetica", 80, "bold"),
            text_color=self.secondary_color
        )
        self.second_label.pack(side=tk.LEFT)
        
        # AM/PM indicator
        self.ampm_label = ctk.CTkLabel(
            self.time_frame,
            text="",
            font=("Helvetica", 24),
            text_color=self.accent_color
        )
        self.ampm_label.pack(side=tk.LEFT, padx=10, pady=(0, 15))
        
        # Additional info (day of week, week number)
        self.info_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.info_frame.pack(pady=(20, 0))
        
        self.day_of_week_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("Helvetica", 18),
            text_color=self.text_color
        )
        self.day_of_week_label.pack(side=tk.LEFT, padx=10)
        
        self.week_number_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("Helvetica", 18),
            text_color=self.text_color
        )
        self.week_number_label.pack(side=tk.LEFT, padx=10)
        
        # Animation variables
        self.animation_phase = 0
        self.animation_direction = 1
        
        # Start the clock
        self.update_clock()
        
        # Configure window to be always on top
        self.attributes('-topmost', True)
        self.after(2000, lambda: self.attributes('-topmost', False))
        
        # Add right-click menu
        self.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Change Theme", command=self.change_theme)
        self.context_menu.add_command(label="Toggle Fullscreen", command=self.toggle_fullscreen)
        self.context_menu.add_command(label="Exit", command=self.destroy)
        
    def update_clock(self):
        now = datetime.now()
        
        # Update time
        hour = now.strftime("%I")
        minute = now.strftime("%M")
        second = now.strftime("%S")
        ampm = now.strftime("%p")
        
        # Remove leading zero from hour if needed
        if hour.startswith("0"):
            hour = hour[1:]
        
        self.hour_label.configure(text=hour)
        self.minute_label.configure(text=minute)
        self.second_label.configure(text=second)
        self.ampm_label.configure(text=ampm)
        
        # Update date
        date_str = now.strftime("%A, %B %d, %Y")
        self.date_label.configure(text=date_str)
        
        # Update additional info
        day_of_week = now.strftime("%A")
        week_number = now.strftime("%U")
        self.day_of_week_label.configure(text=f"Day: {day_of_week}")
        self.week_number_label.configure(text=f"Week: {week_number}")
        
        # Animation effects
        self.animation_phase += 0.1 * self.animation_direction
        if self.animation_phase > 1 or self.animation_phase < 0:
            self.animation_direction *= -1
        
        # Pulse effect on seconds
        pulse_intensity = 0.5 + (math.sin(self.animation_phase * math.pi) * 0.5)
        pulse_color = self.fade_color(self.secondary_color, "#FFFFFF", pulse_intensity)
        self.second_label.configure(text_color=pulse_color)
        
        # Colon blink effect
        if int(second) % 2 == 0:
            self.colon_label.configure(text_color=self.text_color)
            self.second_colon_label.configure(text_color=self.text_color)
        else:
            self.colon_label.configure(text_color=self.bg_color)
            self.second_colon_label.configure(text_color=self.bg_color)
        
        # Schedule next update
        self.after(200, self.update_clock)
    
    def fade_color(self, color1, color2, ratio):
        """Blend between two hex colors"""
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def change_theme(self):
        # Cycle through different color themes
        themes = [
            {"bg": "#121212", "primary": "#4FC3F7", "secondary": "#FF4081", "text": "#E0E0E0", "accent": "#7C4DFF"},
            {"bg": "#0A0A0A", "primary": "#00BCD4", "secondary": "#FF5252", "text": "#F5F5F5", "accent": "#E040FB"},
            {"bg": "#1A1A1A", "primary": "#18FFFF", "secondary": "#FF6E40", "text": "#FFFFFF", "accent": "#B388FF"},
            {"bg": "#212121", "primary": "#64FFDA", "secondary": "#FF1744", "text": "#EEEEEE", "accent": "#651FFF"}
        ]
        
        current_theme = {
            "bg": self.bg_color,
            "primary": self.primary_color,
            "secondary": self.secondary_color,
            "text": self.text_color,
            "accent": self.accent_color
        }
        
        next_theme = themes[(themes.index(current_theme) + 1) % len(themes)] if current_theme in themes else themes[0]
        
        self.bg_color = next_theme["bg"]
        self.primary_color = next_theme["primary"]
        self.secondary_color = next_theme["secondary"]
        self.text_color = next_theme["text"]
        self.accent_color = next_theme["accent"]
        
        self.configure(fg_color=self.bg_color)
        self.date_label.configure(text_color=self.text_color)
        self.hour_label.configure(text_color=self.primary_color)
        self.minute_label.configure(text_color=self.primary_color)
        self.second_label.configure(text_color=self.secondary_color)
        self.colon_label.configure(text_color=self.text_color)
        self.second_colon_label.configure(text_color=self.text_color)
        self.ampm_label.configure(text_color=self.accent_color)
        self.day_of_week_label.configure(text_color=self.text_color)
        self.week_number_label.configure(text_color=self.text_color)
    
    def toggle_fullscreen(self):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

if __name__ == "__main__":
    app = AdvancedDigitalClock()
    app.mainloop()