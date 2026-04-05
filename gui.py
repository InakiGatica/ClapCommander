import sounddevice as sd
import settings
import os
import customtkinter as ctk

# Set dark mode globally
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class ConfigWindow:
    def __init__(self, on_save=None):
        self.on_save = on_save
        self.root = ctk.CTk()
        self.root.title("ClapCommander")
        self.root.geometry("480x700")

        # Container with padding - scrollable
        container = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header = ctk.CTkLabel(
            container,
            text="⚡ ClapCommander",
            font=("SF Pro Display", 20, "bold"),
            text_color="#e74c3c"
        )
        header.pack(pady=(0, 10))

        # Separator
        separator = ctk.CTkFrame(container, height=2, fg_color="#e74c3c")
        separator.pack(fill="x", pady=(0, 15))

        # Microphone section
        lbl_mic = ctk.CTkLabel(container, text="Microphone", font=("SF Pro Display", 14, "bold"))
        lbl_mic.pack(anchor="w")

        devices = sd.query_devices()
        input_devices = []
        for i, dev in enumerate(devices):
            if isinstance(dev, dict) and dev.get('max_input_channels', 0) > 0:
                input_devices.append(f"{i}: {dev['name']}")

        self.mic_combo = ctk.CTkComboBox(container, values=input_devices, width=440)
        current_device = settings.get("device_index", 2)
        matching = [d for d in input_devices if d.startswith(f"{current_device}:")]
        if matching:
            self.mic_combo.set(matching[0])
        elif input_devices:
            self.mic_combo.set(input_devices[0])
        self.mic_combo.pack(pady=(5, 15))

        # Energy Threshold section
        lbl_thresh = ctk.CTkLabel(container, text="Energy Threshold", font=("SF Pro Display", 14, "bold"))
        lbl_thresh.pack(anchor="w")

        thresh_frame = ctk.CTkFrame(container, fg_color="transparent")
        thresh_frame.pack(fill="x", pady=(5, 0))

        self.thresh_slider = ctk.CTkSlider(
            thresh_frame,
            from_=0.01,
            to=0.50,
            number_of_steps=49,
            width=350
        )
        self.thresh_slider.set(settings.get("energy_threshold", 0.15))

        self.thresh_value = ctk.CTkLabel(
            thresh_frame,
            text=f"{self.thresh_slider.get():.2f}",
            text_color="#e74c3c",
            font=("SF Pro Display", 12, "bold")
        )
        self.thresh_slider.pack(side="left")
        self.thresh_value.pack(side="left", padx=10)

        self.thresh_slider.configure(command=lambda v: self.thresh_value.configure(text=f"{v:.2f}"))

        lbl_hint = ctk.CTkLabel(container, text="Lower = more sensitive", text_color="gray60", font=("SF Pro Display", 10))
        lbl_hint.pack(anchor="w", pady=(0, 15))

        # Actions section
        lbl_actions = ctk.CTkLabel(container, text="Actions", font=("SF Pro Display", 14, "bold"))
        lbl_actions.pack(anchor="w")

        # Double clap URL
        lbl_url = ctk.CTkLabel(container, text="Double Clap URL")
        lbl_url.pack(anchor="w", pady=(10, 0))
        self.url_entry = ctk.CTkEntry(container, width=440)
        self.url_entry.insert(0, settings.get("double_clap_url", "https://www.youtube.com"))
        self.url_entry.pack(pady=5)

        # Music file
        lbl_music = ctk.CTkLabel(container, text="Music File")
        lbl_music.pack(anchor="w", pady=(10, 0))
        music_frame = ctk.CTkFrame(container, fg_color="transparent")
        music_frame.pack(fill="x", pady=5)
        self.music_entry = ctk.CTkEntry(music_frame, width=350)
        self.music_entry.insert(0, settings.get("music_path", "ironman.mp3"))
        self.music_entry.pack(side="left")
        btn_browse = ctk.CTkButton(
            music_frame,
            text="Browse",
            width=80,
            fg_color="#e74c3b",
            hover_color="#c0392b",
            command=self._browse_music
        )
        btn_browse.pack(side="left", padx=5)

        # Dynamic apps list
        lbl_apps = ctk.CTkLabel(container, text="Apps to Open")
        lbl_apps.pack(anchor="w", pady=(10, 0))

        self.app_entries = []
        self.apps_frame = ctk.CTkFrame(container, fg_color="transparent")
        self.apps_frame.pack(fill="x", pady=5)

        existing_apps = settings.get("apps", [
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Users\Iña\AppData\Local\Discord\Update.exe"
        ])
        for app_path in existing_apps:
            self._add_app_row(app_path)

        btn_add = ctk.CTkButton(
            container,
            text="+ Add App",
            fg_color="transparent",
            border_width=1,
            border_color="#e74c3c",
            text_color="#e74c3c",
            hover_color="#2a2a2a",
            height=30,
            command=lambda: self._add_app_row("")
        )
        btn_add.pack(pady=(0, 10))

        # Triple Clap Action
        lbl_triple = ctk.CTkLabel(container, text="Triple Clap Action")
        lbl_triple.pack(anchor="w", pady=(10, 0))
        self.triple_combo = ctk.CTkComboBox(container, values=["Lock PC", "Mute/Unmute", "Nothing"])
        self.triple_combo.set(settings.get("triple_clap_action", "Lock PC"))
        self.triple_combo.pack(pady=5)

        # Second Double Clap Action
        lbl_second = ctk.CTkLabel(container, text="Second Double Clap")
        lbl_second.pack(anchor="w")
        self.second_double_combo = ctk.CTkComboBox(container, values=["Stop music + close detector", "Nothing"])
        self.second_double_combo.set(settings.get("second_double_clap_action", "Stop music + close detector"))
        self.second_double_combo.pack(pady=5)

        # Save button
        btn_save = ctk.CTkButton(
            container,
            text="Save Settings",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=("SF Pro Display", 14, "bold"),
            height=40,
            command=self._save
        )
        btn_save.pack(pady=20, fill="x")

    def _add_app_row(self, path=""):
        row = ctk.CTkFrame(self.apps_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        entry = ctk.CTkEntry(row, width=380)
        entry.insert(0, path)
        entry.pack(side="left")
        btn_remove = ctk.CTkButton(
            row,
            text="✕",
            width=40,
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=lambda r=row, e=entry: self._remove_app_row(r, e)
        )
        btn_remove.pack(side="left", padx=5)
        self.app_entries.append(entry)

    def _remove_app_row(self, row, entry):
        self.app_entries.remove(entry)
        row.destroy()

    def _browse_music(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            filetypes=[("Audio files", "*.mp3 *.wav"), ("All files", "*.*")]
        )
        if path:
            self.music_entry.delete(0, "end")
            self.music_entry.insert(0, path)

    def _save(self):
        device_str = self.mic_combo.get()
        device_index = int(device_str.split(":")[0])

        data = {
            "device_index": device_index,
            "energy_threshold": round(self.thresh_slider.get(), 2),
            "double_clap_url": self.url_entry.get(),
            "music_path": self.music_entry.get(),
            "apps": [e.get() for e in self.app_entries if e.get().strip()],
            "triple_clap_action": self.triple_combo.get(),
            "second_double_clap_action": self.second_double_combo.get(),
            "calibration_seconds": settings.get("calibration_seconds", 3),
            "cooldown": settings.get("cooldown", 1.5),
            "min_interval": settings.get("min_interval", 0.15),
            "max_interval": settings.get("max_interval", 1.0)
        }

        settings.save_settings(data)
        print("Settings saved.")

        if self.on_save:
            self.on_save()

        self.root.destroy()

    def show(self):
        self.root.mainloop()


def is_first_run() -> bool:
    return not os.path.exists(settings.SETTINGS_PATH)