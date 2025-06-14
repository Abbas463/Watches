import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import time
import math

class AdvancedAnalogClock(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Analog Clock")
        self.geometry("800x600")  # Increased height for better display
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
        
        # Analog clock canvas
        self.clock_size = 300
        self.clock_canvas = tk.Canvas(
            self.main_frame,
            width=self.clock_size,
            height=self.clock_size,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.clock_canvas.pack(pady=20)
        
        # Draw clock face
        self.center_x = self.clock_size // 2
        self.center_y = self.clock_size // 2
        self.clock_radius = self.clock_size // 2 - 10
        
        # AM/PM indicator
        self.ampm_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Helvetica", 24),
            text_color=self.accent_color
        )
        self.ampm_label.pack()
        
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
        
    def draw_clock_face(self):
        # Clear canvas
        self.clock_canvas.delete("all")
        
        # Draw clock face
        self.clock_canvas.create_oval(
            self.center_x - self.clock_radius,
            self.center_y - self.clock_radius,
            self.center_x + self.clock_radius,
            self.center_y + self.clock_radius,
            outline=self.text_color,
            width=2
        )
        
        # Draw hour markers
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            inner_x = self.center_x + (self.clock_radius - 20) * math.cos(angle)
            inner_y = self.center_y + (self.clock_radius - 20) * math.sin(angle)
            outer_x = self.center_x + self.clock_radius * math.cos(angle)
            outer_y = self.center_y + self.clock_radius * math.sin(angle)
            
            self.clock_canvas.create_line(
                inner_x, inner_y,
                outer_x, outer_y,
                fill=self.text_color,
                width=3
            )
            
            # Add hour numbers
            if i == 0:
                num = 12
            else:
                num = i
                
            text_x = self.center_x + (self.clock_radius - 40) * math.cos(angle)
            text_y = self.center_y + (self.clock_radius - 40) * math.sin(angle)
            
            self.clock_canvas.create_text(
                text_x, text_y,
                text=str(num),
                fill=self.text_color,
                font=("Helvetica", 12, "bold")
            )
        
        # Draw minute markers
        for i in range(60):
            if i % 5 != 0:  # Skip hour markers
                angle = math.radians(i * 6 - 90)
                inner_x = self.center_x + (self.clock_radius - 10) * math.cos(angle)
                inner_y = self.center_y + (self.clock_radius - 10) * math.sin(angle)
                outer_x = self.center_x + self.clock_radius * math.cos(angle)
                outer_y = self.center_y + self.clock_radius * math.sin(angle)
                
                self.clock_canvas.create_line(
                    inner_x, inner_y,
                    outer_x, outer_y,
                    fill=self.text_color,
                    width=1
                )
    
    def update_clock(self):
        now = datetime.now()
        
        # Get current time
        hour = now.hour % 12
        minute = now.minute
        second = now.second
        ampm = "AM" if now.hour < 12 else "PM"
        
        # Update date and info labels
        date_str = now.strftime("%A, %B %d, %Y")
        self.date_label.configure(text=date_str)
        self.ampm_label.configure(text=ampm)
        
        day_of_week = now.strftime("%A")
        week_number = now.strftime("%U")
        self.day_of_week_label.configure(text=f"Day: {day_of_week}")
        self.week_number_label.configure(text=f"Week: {week_number}")
        
        # Draw clock face
        self.draw_clock_face()
        
        # Calculate angles for clock hands
        hour_angle = math.radians((hour * 30) + (minute * 0.5) - 90)
        minute_angle = math.radians((minute * 6) + (second * 0.1) - 90)
        second_angle = math.radians(second * 6 - 90)
        
        # Draw hour hand
        hour_length = self.clock_radius * 0.5
        hour_x = self.center_x + hour_length * math.cos(hour_angle)
        hour_y = self.center_y + hour_length * math.sin(hour_angle)
        self.clock_canvas.create_line(
            self.center_x, self.center_y,
            hour_x, hour_y,
            fill=self.primary_color,
            width=6,
            capstyle=tk.ROUND
        )
        
        # Draw minute hand
        minute_length = self.clock_radius * 0.7
        minute_x = self.center_x + minute_length * math.cos(minute_angle)
        minute_y = self.center_y + minute_length * math.sin(minute_angle)
        self.clock_canvas.create_line(
            self.center_x, self.center_y,
            minute_x, minute_y,
            fill=self.primary_color,
            width=4,
            capstyle=tk.ROUND
        )
        
        # Draw second hand with animation effect
        pulse_intensity = 0.5 + (math.sin(self.animation_phase * math.pi) * 0.5)
        second_color = self.fade_color(self.secondary_color, "#FFFFFF", pulse_intensity)
        
        second_length = self.clock_radius * 0.8
        second_x = self.center_x + second_length * math.cos(second_angle)
        second_y = self.center_y + second_length * math.sin(second_angle)
        self.clock_canvas.create_line(
            self.center_x, self.center_y,
            second_x, second_y,
            fill=second_color,
            width=2,
            capstyle=tk.ROUND
        )
        
        # Draw center circle
        self.clock_canvas.create_oval(
            self.center_x - 8, self.center_y - 8,
            self.center_x + 8, self.center_y + 8,
            fill=self.secondary_color,
            outline=self.secondary_color
        )
        
        # Update animation variables
        self.animation_phase += 0.1 * self.animation_direction
        if self.animation_phase > 1 or self.animation_phase < 0:
            self.animation_direction *= -1
        
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
        self.clock_canvas.configure(bg=self.bg_color)
        self.date_label.configure(text_color=self.text_color)
        self.ampm_label.configure(text_color=self.accent_color)
        self.day_of_week_label.configure(text_color=self.text_color)
        self.week_number_label.configure(text_color=self.text_color)
    
    def toggle_fullscreen(self):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

if __name__ == "__main__":
    app = AdvancedAnalogClock()
    app.mainloop()