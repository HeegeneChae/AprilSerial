import sys
import threading
import time
import tkinter as tk
from tkinter import ttk


# 8세그먼트 형태 표시를 위한 커스텀 위젯
class SevenSegmentDisplay(tk.Canvas):
    def __init__(self, parent, width=200, height=50):
        super().__init__(parent, width=width, height=height, bg='whitesmoke')
        self.width = width
        self.height = height
        self.segment_data = " "
        self.update_display("12:34:56")

    def update_display(self, text):
        self.segment_data = text
        self.delete("all")
        self.create_text(self.width // 2, self.height // 2, text=self.segment_data, font=("Courier", 30), fill="dimgrey")


# Dummy Serial Function (for GUI Testing Without Hardware)
def send_command(command):
    print(f"Sent Command: {command}")


def process_serial_data(data):
    print(f"Received Data: {data}")
    if data.startswith("TIME:"):
        time_value = data.split(":")[1]
        seven_segment.update_display(time_value)  # HH:MM:SS 표시
    elif data.startswith("TIMER:"):
        timer_value = data.split(":")[1]
        seven_segment.update_display(timer_value)  # TIMER 값 표시
    elif data.startswith("ADC:"):
        adc_value = int(data.split(":")[1])
        adc_progress['value'] = adc_value
        adc_label.config(text=f"{adc_value}")
        seven_segment.update_display(str(adc_value))  # ADC 값 표시
    elif data.startswith("LED:"):
        led_index = int(data.split(":")[1])
        current_color = led_buttons[led_index].cget("bg")
        new_color = "green" if current_color == "red" else "red"
        led_buttons[led_index].config(bg=new_color)


def request_time():
    process_serial_data("TIME:12:34:56")


def request_timer():
    process_serial_data("TIMER:00:05:00")


def request_adc():
    process_serial_data("ADC:2013")


def reset_display():
    seven_segment.update_display("12:34:56")
    adc_progress['value'] = 0
    adc_label.config(text="0")


def toggle_led(index):
    process_serial_data(f"LED:{index}")


# GUI Setup
root = tk.Tk()
root.title("STM32 Control GUI")
root.geometry("400x400")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Left Side (LED Buttons)
led_frame = tk.Frame(main_frame)
led_frame.pack(side=tk.LEFT, padx=10)
led_buttons = []
for i in range(4):
    btn = tk.Button(led_frame, text=f"LED {i + 1}", width=10, bg="red", command=lambda i=i: toggle_led(i))
    btn.pack(pady=2)
    led_buttons.append(btn)

# Center (Time and ADC Display)
center_frame = tk.Frame(main_frame)
center_frame.pack(side=tk.LEFT, expand=True)

# Time Display (8세그먼트 형태 표시)
time_frame = tk.Frame(center_frame)
time_frame.pack()
seven_segment = SevenSegmentDisplay(time_frame, width=200, height=50)
seven_segment.pack()

# ADC Progress Bar (Vertical, Right Side)
adc_frame = tk.Frame(center_frame)
adc_frame.pack(pady=10, side=tk.RIGHT)

# Vertical Progress Bar
adc_progress = ttk.Progressbar(adc_frame, length=100, mode='determinate', maximum=100, orient=tk.VERTICAL)
adc_progress.pack(side=tk.LEFT)

# Labels below the progress bar (0%, 50%, 100%)
adc_labels = tk.Frame(adc_frame)
adc_labels.pack(side=tk.LEFT, padx=5)

# 0%, 50%, 100% labels positioned relative to the progress bar
tk.Label(adc_labels, text="100%", anchor='s').pack(side=tk.TOP)  # 100% at the top
tk.Label(adc_labels, text="50%", anchor='center').pack(side=tk.TOP)  # 50% in the middle
tk.Label(adc_labels, text="0%", anchor='n').pack(side=tk.BOTTOM)  # 0% at the bottom

# Display ADC Value separately on the left
adc_value_frame = tk.Frame(center_frame)
adc_value_frame.pack(pady=10, side=tk.LEFT)

adc_label = tk.Label(adc_value_frame, text="0")  # ADC 값만 왼쪽으로 분리
adc_label.pack()


# Bottom (Switch Buttons)
switch_frame = tk.Frame(root)
switch_frame.pack(side=tk.BOTTOM, pady=10)
tk.Button(switch_frame, text="RTC TIME", command=request_time).pack(side=tk.LEFT, padx=5)
tk.Button(switch_frame, text="Timer", command=request_timer).pack(side=tk.LEFT, padx=5)
tk.Button(switch_frame, text="ADC Read", command=request_adc).pack(side=tk.LEFT, padx=5)
tk.Button(switch_frame, text="Reset", command=reset_display).pack(side=tk.LEFT, padx=5)
tk.Button(switch_frame, text="Spare", command=lambda: print("Spare Button Pressed")).pack(side=tk.LEFT, padx=5)

root.mainloop()
