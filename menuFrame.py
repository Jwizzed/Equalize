from typing import Optional, Any
import customtkinter as ct
from PIL import Image
from facadeController import FacadeController


class MenuFrame(ct.CTkFrame):
    """The app frame inside the application contains the menu and information.
"""

    def __init__(self, parent: ct.CTk, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Set the attributes
        self._facade: FacadeController = FacadeController()  # FacadeController
        self._parent: ct.CTk = parent  # Set the parent

    @property
    def facade(self) -> FacadeController:
        """FacadeController"""
        return self._facade

    @property
    def parent(self) -> ct.CTk:
        """Parent"""
        return self._parent


class RightMenuFrame(ct.CTkFrame):
    """Right menu frame"""

    def __init__(self, parent: ct.CTk, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Set the attributes
        self._facade: FacadeController = FacadeController()  # FacadeController
        self._parent: ct.CTk = parent  # Set the parent
        self._eq_img_path: str = self.facade.get_eq_img_path()
        self.color_index: int = 1  # title_label color index
        self.eq_text_index: int = 0  # title_label text index
        self.eq_text_adder: int = 1  # title_label text adder
        self.eq_text: str = ""  # Equalize motion text

        # Set the widgets
        self.eq_img: Optional[ct.CTkImage] = None  # Equalize misc
        self.eq_lbl: Optional[ct.CTkLabel] = None  # Equalize misc label
        self.colors: Any = self.facade.get_colors()  # title_label colors
        self.title_lbl: Optional[ct.CTkLabel] = None  # title_label

    @property
    def parent(self) -> ct.CTk:
        """Parent"""

        return self._parent

    @property
    def facade(self) -> FacadeController:
        """FacadeController"""

        return self._facade

    @property
    def eq_img_path(self) -> str:
        """Equalize misc image path"""

        return self._eq_img_path

    def start_right_frame(self, start_command=None) -> None:
        """Create a right side frame with a command"""

        self.create_widgets(start_command)
        self.change_title_lbl_color()
        self.change_title_lbl_text()
        self.facade.change_appearance(self, y_pad=200)
        self.facade.create_music_btn(self, y_pad=20, x_pad=(50, 0))

    def create_widgets(self, start_command) -> None:
        """Initialize the widgets"""

        self.create_title_lbl()
        self.create_eq_img()
        self.create_start_btn(start_command)
        self.create_info_btn()

    def create_title_lbl(self) -> None:
        """Create the title label"""

        self.title_lbl = ct.CTkLabel(self,
                                     text="Equalize",
                                     font=ct.CTkFont(
                                         family="Mali",
                                         size=40,
                                         weight="bold",
                                     )
                                     )

        self.title_lbl.grid(row=1, column=1, pady=40, sticky="nsew")

    def create_eq_img(self) -> None:
        """Create the equalize image"""

        self.facade.create_img_lbl(self, text="", img_path=self.eq_img_path,
                                   img_size=(200, 100), row=2, column=1,
                                   x_pad=20, y_pad=(5, 40))

    def create_start_btn(self, command=None) -> None:
        """Create the start button"""

        self.facade.create_btn(self, text="Start", command=command,
                               row=3, column=1, size=20, x_pad=20,
                               y_pad=(30, 20), sticky="ns")

    def create_info_btn(self) -> None:
        """Create the info button"""

        info_text = self.facade.get_info_text()
        self.facade.create_btn(self, text="Info", command=lambda:
        self.facade.create_top_screen("What is Equalize?", info_text,
                                      which="info"),
                               row=6, size=20, column=1, x_pad=20,
                               y_pad=(10, 0), sticky="ns")

    def change_title_lbl_color(self) -> None:
        """Change the title label color"""

        self.color_index += 1

        if self.color_index == len(self.colors):
            self.colors = self.colors[::-1]
            self.color_index = 0

        self.after(50, self.change_title_lbl_color)

    def change_title_lbl_text(self) -> None:
        """Change the title label text"""

        self.title_lbl.configure(text_color=self.colors[self.color_index][0])
        eq_text_list = ["E", "Q", "U", "A", "L", "I", "Z", "E"]

        if self.eq_text_index == 1:
            self.eq_text_adder = 1

        elif self.eq_text_index == len(eq_text_list):
            self.eq_text_adder = -1

        self.eq_text_index += self.eq_text_adder
        self.eq_text = "".join(eq_text_list[:self.eq_text_index])
        self.title_lbl.configure(text=self.eq_text)
        self.after(500, self.change_title_lbl_text)


class LeftMenuFrame(ct.CTkFrame):
    """Left menu frame"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Set the attributes
        self._facade: FacadeController = FacadeController()  # FacadeController
        self._parent: ct.CTk = parent  # Set the parent

        # Set the widgets
        self.menu_img: Optional[ct.CTkImage] = None  # menu misc
        self.menu_img_lbl: Optional[ct.CTkLabel] = None  # menu misc label
        self._menu_img_path: str = self.facade.get_menu_img_path()  # Set the path

    @property
    def menu_img_path(self) -> str:
        """Menu misc image path"""

        return self._menu_img_path

    @menu_img_path.setter
    def menu_img_path(self, value: str) -> None:
        """Set the menu misc image path"""

        self._menu_img_path = value

    @property
    def parent(self) -> ct.CTk:
        """Parent"""

        return self._parent

    @property
    def facade(self) -> FacadeController:
        """FacadeController"""

        return self._facade

    def start_left_frame(self) -> None:
        """Start the left frame"""

        self.menu_img = ct.CTkImage(
            light_image=Image.open(self.menu_img_path),
            dark_image=Image.open(self.menu_img_path),
            size=(700, 700))
        self.menu_img_lbl = ct.CTkLabel(self, text="", image=self.menu_img)
        self.menu_img_lbl.grid(row=1, column=1, sticky="nsew")
