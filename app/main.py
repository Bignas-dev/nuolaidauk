# Disable GStreamer to avoid compilation issues
import os
import tempfile
import cairosvg

os.environ['KIVY_AUDIO'] = 'sdl2'
os.environ['KIVY_VIDEO'] = 'null'
os.environ['KIVY_MEDIA'] = 'sdl2'
os.environ['KIVY_IMAGE'] = 'pil,sdl2'
os.environ['KIVY_CAMERA'] = 'opencv'
os.environ['KIVY_CLIPBOARD'] = 'sdl2'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from app.config import CONFIG

class BarcodeButton(Button):
    def __init__(self, barcode_name, barcode_path, **kwargs):
        super(BarcodeButton, self).__init__(**kwargs)
        self.barcode_name = barcode_name
        self.barcode_path = barcode_path
        self.text = barcode_name
        self.size_hint_y = None
        self.height = dp(70)
        self.background_normal = ""
        self.background_color = (0.95, 0.95, 0.95, 1) if CONFIG.get("default_theme", "Dark") == "Light" else (0.3, 0.3, 0.3, 1)
        self.color = CONFIG["text_color"] if CONFIG.get("default_theme", "Dark") == "Light" else CONFIG["text_color_dark"]
        self.halign = "center"

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        self.load_barcodes()

        # Main layout
        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        # Title bar
        title_bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(60))
        
        # Title
        title = Label(
            text=CONFIG["app_name"],
            font_size=dp(20),
            halign="center",
            valign="middle",
            color=CONFIG["text_color"] if CONFIG.get("default_theme", "Dark") == "Light" else CONFIG["text_color_dark"],
            bold=True
        )
        title_bar.add_widget(title)
        
        layout.add_widget(title_bar)

        # Search input
        self.search_input = TextInput(
            hint_text="Search barcodes...",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.95, 0.95, 0.95, 1) if CONFIG.get("default_theme", "Dark") == "Light" else (0.3, 0.3, 0.3, 1),
            foreground_color=CONFIG["text_color"] if CONFIG.get("default_theme", "Dark") == "Light" else CONFIG["text_color_dark"],
            padding=(dp(10), dp(10)),
            cursor_color=CONFIG["primary_color"]
        )
        self.search_input.bind(text=self.filter_barcodes)
        layout.add_widget(self.search_input)

        # Scrollable barcode list
        scroll_view = ScrollView()
        self.barcode_grid = GridLayout(
            cols=1, 
            spacing=dp(10), 
            size_hint_y=None, 
            padding=[dp(10), dp(10)]
        )
        self.barcode_grid.bind(minimum_height=self.barcode_grid.setter("height"))

        scroll_view.add_widget(self.barcode_grid)
        layout.add_widget(scroll_view)

        self.add_widget(layout)
        
        # Set background color based on theme
        with self.canvas.before:
            Color(*CONFIG["secondary_color"] if CONFIG.get("default_theme", "Dark") == "Light" else CONFIG["secondary_color_dark"])
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.update_barcode_list()
        
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

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
                            "code": name.capitalize(),
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
        app = App.get_running_app()
        barcode_screen = app.root.get_screen("barcode")
        barcode_screen.set_barcode(instance.barcode_path, instance.barcode_name)
        app.root.current = "barcode"

class BarcodeScreen(Screen):
    def __init__(self, **kwargs):
        super(BarcodeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        self.is_fullscreen = platform == "android"
        self.temp_png_path = None

        # Top bar
        self.top_bar = BoxLayout(size_hint_y=None, height=dp(60), padding=(dp(5), dp(5)))
        top_bar_opacity = 0 if self.is_fullscreen else 1
        self.top_bar.opacity = top_bar_opacity

        # Back button
        self.back_button = Button(
            text="Back",
            size_hint=(None, None),
            size=(dp(80), dp(50)),
            background_color=CONFIG["primary_color"]
        )
        self.back_button.bind(on_release=self.go_back)

        # Title label
        self.title_label = Label(
            text="Barcode View",
            font_size=dp(16),
            halign="center",
            size_hint_x=1,
            color=CONFIG["text_color"] if CONFIG.get("default_theme", "Dark") == "Light" else CONFIG["text_color_dark"]
        )

        # Add widgets to top bar
        self.top_bar.add_widget(self.back_button)
        self.top_bar.add_widget(self.title_label)
        self.layout.add_widget(self.top_bar)

        # Barcode image display
        self.image = Image(allow_stretch=True, keep_ratio=True)
        self.layout.add_widget(self.image)

        self.add_widget(self.layout)
        
        # Set background color based on theme
        with self.canvas.before:
            Color(*CONFIG["secondary_color"] if CONFIG.get("default_theme", "Dark") == "Light" else CONFIG["secondary_color_dark"])
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Bind tap events for Android fullscreen mode
        if self.is_fullscreen:
            self.image.bind(on_touch_down=self.show_controls)
            
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

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
        App.get_running_app().root.current = "search"

    def show_controls(self, instance, touch):
        # Show/hide controls on tap (Android only)
        if self.is_fullscreen:
            if self.top_bar.opacity == 0:
                # Show controls
                self.top_bar.opacity = 1
                self.top_bar.size_hint_y = None
                self.top_bar.height = dp(60)
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

class BarcodeApp(App):
    def build(self):
        # Apply app configuration
        self.title = CONFIG["app_name"]
        
        # Set window background color
        Window.clearcolor = CONFIG["secondary_color"] if CONFIG.get("default_theme", "Dark") == "Light" else CONFIG["secondary_color_dark"]

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

if __name__ == "__main__":
    BarcodeApp().run()
