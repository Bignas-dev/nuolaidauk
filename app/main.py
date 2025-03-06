# Disable GStreamer to avoid compilation issues
import os
os.environ['KIVY_AUDIO'] = 'sdl2'
os.environ['KIVY_VIDEO'] = 'null'
os.environ['KIVY_MEDIA'] = 'sdl2'
os.environ['KIVY_IMAGE'] = 'pil,sdl2'
os.environ['KIVY_CAMERA'] = 'opencv'
os.environ['KIVY_CLIPBOARD'] = 'sdl2'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard

import os
import tempfile
import cairosvg

from app.config import CONFIG


class BarcodeButton(MDCard):
    def __init__(self, barcode_name, barcode_path, **kwargs):
        super(BarcodeButton, self).__init__(**kwargs)
        self.barcode_name = barcode_name
        self.barcode_path = barcode_path
        self.size_hint_y = None
        self.height = 70

        # Card will automatically adapt to theme changes
        self.elevation = 1
        self.radius = [8, 8, 8, 8]
        self.padding = [10, 10]

        # Create layout for card content
        content = MDBoxLayout(orientation="vertical")
        name_label = MDLabel(
            text=barcode_name, theme_text_color="Primary", font_size="16sp"
        )
        content.add_widget(name_label)
        self.add_widget(content)


class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        self.load_barcodes()

        layout = MDBoxLayout(orientation="vertical", padding=10, spacing=10)

        # Title bar
        title_bar = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=60)

        # Spacer for left side
        left_spacer = MDBoxLayout(size_hint_x=0.2)
        title_bar.add_widget(left_spacer)

        # Title in the center
        title = MDLabel(
            text=CONFIG["app_name"],
            font_size="20sp",
            theme_text_color="Primary",
            halign="center",
            bold=True,
            size_hint_x=0.6,
        )
        title_bar.add_widget(title)

        # Theme toggle button on right
        right_box = MDBoxLayout(size_hint_x=0.2)
        current_theme = CONFIG.get("default_theme", "Light")
        self.theme_icon = (
            "weather-night" if current_theme == "Light" else "weather-sunny"
        )
        self.theme_button = MDIconButton(
            icon=self.theme_icon,
            theme_text_color="Primary",
            pos_hint={"center_x": 1, "center_y": 0.5},
        )
        self.theme_button.bind(on_release=self.toggle_theme)
        right_box.add_widget(self.theme_button)
        title_bar.add_widget(right_box)

        layout.add_widget(title_bar)

        # Search input
        search_box = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height=60, spacing=5
        )
        self.search_input = MDTextField(
            hint_text="Search barcodes...",
            multiline=False,
            size_hint_x=1,
            mode="outlined",
        )
        self.search_input.bind(text=self.filter_barcodes)
        search_box.add_widget(self.search_input)

        layout.add_widget(search_box)

        # Scrollable barcode list
        scroll_view = ScrollView()
        self.barcode_grid = MDGridLayout(
            cols=1, spacing=10, size_hint_y=None, padding=[10, 10]
        )
        self.barcode_grid.bind(minimum_height=self.barcode_grid.setter("height"))

        scroll_view.add_widget(self.barcode_grid)
        layout.add_widget(scroll_view)

        self.add_widget(layout)
        self.update_barcode_list()

    def load_barcodes(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        barcode_dir = os.path.join(base_dir, "data", "barcodes")

        self.barcodes = []
        if os.path.exists(barcode_dir):
            for file in os.listdir(barcode_dir):
                if file.endswith(".svg"):
                    name = os.path.splitext(file)[0]
                    self.barcodes.append(
                        {
                            "name": name,
                            "path": os.path.join(barcode_dir, file),
                            "code": name.capitalize(),  # Use capitalized name instead of code
                        }
                    )

    def update_barcode_list(self, search_text=""):
        self.barcode_grid.clear_widgets()

        for barcode in self.barcodes:
            if search_text.lower() in barcode["name"].lower():
                btn = BarcodeButton(
                    barcode_name=barcode["code"],
                    barcode_path=barcode["path"],
                )
                btn.bind(on_release=self.show_barcode)
                self.barcode_grid.add_widget(btn)

    def filter_barcodes(self, instance, value):
        self.update_barcode_list(value)

    def show_barcode(self, instance):
        app = MDApp.get_running_app()
        barcode_screen = app.root.get_screen("barcode")
        barcode_screen.set_barcode(instance.barcode_path, instance.barcode_name)
        app.root.current = "barcode"

    def toggle_theme(self, instance):
        app = MDApp.get_running_app()
        # Toggle between Light and Dark themes
        new_theme = "Dark" if app.theme_cls.theme_style == "Light" else "Light"
        app.switch_theme(new_theme)

        # Update the icon based on the new theme
        self.theme_button.icon = (
            "weather-night" if new_theme == "Light" else "weather-sunny"
        )


class BarcodeScreen(Screen):
    def __init__(self, **kwargs):
        super(BarcodeScreen, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical")
        self.is_fullscreen = platform == "android"  # Auto fullscreen on Android
        self.temp_png_path = None

        # Top bar with buttons (initially hidden on Android)
        self.top_bar = MDBoxLayout(size_hint_y=None, height=60, padding=[5, 5])
        top_bar_opacity = 0 if self.is_fullscreen else 1
        self.top_bar.opacity = top_bar_opacity

        # Back button
        self.back_button = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            md_bg_color=CONFIG["primary_color"],
        )
        self.back_button.bind(on_release=self.go_back)

        # Title label
        self.title_label = MDLabel(
            text="Barcode View",
            theme_text_color="Primary",
            font_size="16sp",
            halign="center",
            size_hint_x=1,
        )

        # Add widgets to top bar
        self.top_bar.add_widget(self.back_button)
        self.top_bar.add_widget(self.title_label)

        # No fullscreen button needed since Android auto-fullscreens
        self.layout.add_widget(self.top_bar)

        # Barcode image display
        self.image = Image(allow_stretch=True, keep_ratio=True)
        self.layout.add_widget(self.image)

        self.add_widget(self.layout)

        # Bind tap events for Android fullscreen mode
        if self.is_fullscreen:
            self.image.bind(on_touch_down=self.show_controls)

    def set_barcode(self, image_path, title):
        # Convert SVG to PNG if it's an SVG file
        if image_path.lower().endswith(".svg"):
            # Create temporary file for the PNG
            tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            tmp_file.close()

            # Convert SVG to PNG
            cairosvg.svg2png(url=image_path, write_to=tmp_file.name, scale=2.0)

            # Clean up previous temp file if it exists
            if self.temp_png_path and os.path.exists(self.temp_png_path):
                try:
                    os.unlink(self.temp_png_path)
                except:
                    pass

            # Store the path to the new temp file
            self.temp_png_path = tmp_file.name

            # Set the image source to the PNG file
            self.image.source = self.temp_png_path
        else:
            # For non-SVG files, use the path directly
            self.image.source = image_path

        self.title_label.text = title

    def go_back(self, instance):
        MDApp.get_running_app().root.current = "search"

    # We don't need toggle_fullscreen method as we auto-fullscreen on Android
    # and only allow showing/hiding controls

    def show_controls(self, instance, touch):
        # Show/hide controls on tap (Android only)
        if self.is_fullscreen:
            if self.top_bar.opacity == 0:
                # Show controls
                self.top_bar.opacity = 1
                self.top_bar.size_hint_y = None
                self.top_bar.height = 60
                return True
            else:
                # Hide controls on second tap
                self.top_bar.opacity = 0
                self.top_bar.size_hint_y = 0
                self.top_bar.height = 0
                return True

    def on_leave(self):
        # Clean up temporary PNG file when leaving the screen
        if self.temp_png_path and os.path.exists(self.temp_png_path):
            try:
                os.unlink(self.temp_png_path)
                self.temp_png_path = None
            except:
                pass


class BarcodeApp(MDApp):
    def build(self):
        # Apply app configuration
        self.title = CONFIG["app_name"]

        # Set initial theme style based on config
        initial_theme = CONFIG.get("default_theme", "Light")
        self.theme_cls.theme_style = initial_theme

        # Set colors based on theme
        self.apply_theme_colors(initial_theme)

        # Set fullscreen for Android devices automatically
        if platform == "android":
            Window.fullscreen = "auto"
        elif CONFIG["fullscreen"]:
            Window.fullscreen = "auto"

        # Set up screen manager
        sm = ScreenManager()
        sm.add_widget(SearchScreen(name="search"))
        sm.add_widget(BarcodeScreen(name="barcode"))

        return sm

    def apply_theme_colors(self, theme):
        """Apply colors based on the current theme"""
        if theme == "Light":
            self.theme_cls.primary_color = CONFIG["primary_color"]
            Window.clearcolor = CONFIG["secondary_color"]
            self.text_color = CONFIG["text_color"]
        else:  # Dark
            self.theme_cls.primary_color = CONFIG["primary_color_dark"]
            Window.clearcolor = CONFIG["secondary_color_dark"]
            self.text_color = CONFIG["text_color_dark"]

        # Set accent color
        self.theme_cls.accent_palette = "Amber"

    def switch_theme(self, theme):
        """Switch between light and dark themes"""
        self.theme_cls.theme_style = theme
        self.apply_theme_colors(theme)


if __name__ == "__main__":
    BarcodeApp().run()
