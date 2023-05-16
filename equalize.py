from typing import Optional
import customtkinter as ct
from appFrame import AppFrame
from facadeController import FacadeController
from menuFrame import MenuFrame, RightMenuFrame, LeftMenuFrame


class App(ct.CTk):
    """Main application class"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._facade: FacadeController = FacadeController()

        # Set window properties
        self.title("Gender Inequality")
        self.geometry(f"1000x700+{220}+{50}")
        self.resizable(False, False)
        ct.set_default_color_theme(self.facade.get_theme_path())

        # Setting the attributes
        self.frame: Optional[ct.CTkFrame] = None  # Frame
        self.right_frame: Optional[ct.CTkFrame] = None  # right frame
        self.left_frame: Optional[ct.CTkFrame] = None  # left frame

        # Run the welcome screen
        self.welcome_screen()

    @property
    def facade(self) -> FacadeController:
        """FacadeController"""
        return self._facade

    def welcome_screen(self) -> None:
        """Create a welcome screen"""
        # Check if the frame
        if self.frame is not None:
            self.frame.destroy()

        # Create big frame
        self.frame = MenuFrame(self)
        self.frame.grid(row=0, column=0, padx=(20, 0), pady=20, sticky="nsew")

        # Create left frame
        self.left_frame = LeftMenuFrame(self)
        self.left_frame.grid(row=0, column=1, padx=(20, 0), pady=20, sticky="nsew")
        self.left_frame.start_left_frame()

        # Create right frame
        self.right_frame = RightMenuFrame(self)
        self.right_frame.grid(row=0, column=2, padx=(10, 20), pady=20, sticky="nsew")
        self.right_frame.start_right_frame(self.start_new_screen)

        # Allocate extra space to make the frame fit the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def start_new_screen(self) -> None:
        """Start a new screen"""
        self.frame.destroy()
        self.right_frame.destroy()
        self.left_frame.destroy()
        self.frame = AppFrame(self)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
