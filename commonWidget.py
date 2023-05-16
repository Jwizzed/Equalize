import os
from threading import Thread
from typing import Callable
import customtkinter as ct
import pygame
from PIL import Image


class CommonWidget:
    """A class that contains common widgets"""
    music_state: bool = False  # Music state

    def __init__(self):
        self.music_path: str = os.path.join(os.getcwd(), "misc", "sound",
                                            "Lofi.mp3")
        self.state: bool = True
        if not CommonWidget.music_state:
            self.init_music()
            CommonWidget.music_state = True

    def init_music(self):
        """Initialize the music"""

        pygame.mixer.init()
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        self.toggle_music()

    def toggle_music(self):
        """Toggle the music"""
        self.state = not self.state
        if self.state:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def create_music_btn(self, frame: ct.CTkFrame = None,
                         x_pad: int | tuple = 30,
                         y_pad: int | tuple = 20,
                         grid_row=9, grid_col=1) -> ct.CTkSwitch:
        """Create a music button"""

        switch = ct.CTkSwitch(frame, text="Music (on/off)",
                              state="normal",
                              command=self.toggle_music)
        switch.toggle()
        return switch.grid(row=grid_row,
                           column=grid_col,
                           sticky="nsew",
                           padx=x_pad,
                           pady=y_pad)

    @staticmethod
    def run_task(text: str) -> Callable:
        """Function decorator to run a task in a new thread"""

        def wrapper(func: Callable) -> Callable:
            time = text.count(".") * 100

            def inner(self) -> None:
                """Inner function"""

                if "..." in text:
                    self.withdraw()
                self.task = Thread(target=func)
                self.top_level = ct.CTkToplevel()
                self.top_level.title("Loading Element")
                self.top_level.geometry("280x155+500+300")
                self.top_frame = ct.CTkFrame(self.top_level)
                self.top_frame.grid(row=0, column=0, padx=20, pady=20,
                                    sticky="nsew")
                self.top_bar = ct.CTkProgressBar(self.top_frame,
                                                 orientation="horizontal",
                                                 width=200,
                                                 mode="indeterminate")
                self.top_bar.grid(row=1, column=0, padx=20, pady=20,
                                  sticky="nsew")
                self.top_bar.start()
                self.top_label = ct.CTkLabel(self.top_frame, text=text)
                self.top_label.grid(row=2, column=0, padx=20, pady=20,
                                    sticky="nsew")
                self.top_level.update()
                self.task.start()
                self.top_level.after(time, lambda: check_task(self))

            def check_task(self) -> None:
                """Check if the task is alive"""

                if self.task.is_alive():
                    self.top_level.after(time, lambda: self.check_task())
                else:
                    self.top_bar.stop()
                    self.top_label.configure(text="Done")
                    self.top_level.after(250,
                                         lambda: run_func(self))

            def run_func(self) -> None:
                """Run the function"""

                self.top_level.destroy()
                func(self)
                if "..." in text:
                    self.deiconify()

            return inner

        return wrapper

    @staticmethod
    def change_appearance(frame: ct.CTkFrame = None, x_pad: int | tuple = 30,
                          y_pad: int | tuple = 20,
                          grid_row=8, grid_col=1) -> None:
        """Change the appearance of the application"""

        appearance_label = ct.CTkLabel(frame, text="Appearance mode : ",
                                       font=ct.CTkFont(
                                           family="Mali",
                                           size=15,
                                           weight="bold"),
                                       anchor="s"
                                       )
        appearance_label.grid(row=grid_row - 1, column=grid_col,
                              pady=(y_pad / 2, 10),
                              sticky="ns")

        appearance = ct.CTkOptionMenu(
            frame, values=["Dark", "Light", "System"],
            command=ct.set_appearance_mode,
            font=ct.CTkFont(family="Mali", size=17, weight="bold"),
            anchor="center")

        appearance.grid(row=grid_row, column=grid_col, padx=x_pad,
                        pady=10, sticky="s")

    @staticmethod
    def create_font(size: int = 25) -> ct.CTkFont:
        """Create a font"""

        return ct.CTkFont(family="Mali", size=size, weight="bold")

    @staticmethod
    def create_text_lbl(frame, text: str, size: int = 25, wraplength=0,
                        justify="center", row: int = 0, column: int = 0,
                        x_pad: int | tuple = 30, y_pad: int | tuple = 30,
                        anchor="s", text_color: str = None,
                        sticky: str = "nsew"):
        """Create a text label"""

        if text_color is None:
            return ct.CTkLabel(frame, text=text, wraplength=wraplength,
                               justify=justify,
                               font=ct.CTkFont(family="Mali", size=size,
                                               weight="bold"),
                               anchor=anchor
                               ).grid(row=row, column=column, padx=x_pad,
                                      pady=y_pad,
                                      sticky=sticky)
        else:
            return ct.CTkLabel(frame, text=text, wraplength=wraplength,
                               justify=justify, text_color=text_color,
                               font=ct.CTkFont(family="Mali", size=size,
                                               weight="bold"),
                               anchor=anchor
                               ).grid(row=row, column=column, padx=x_pad,
                                      pady=y_pad,
                                      sticky=sticky)

    @staticmethod
    def create_img_lbl(frame, text: str = "", img_path: str = "",
                       size: int = 25, anchor: str = "w",
                       img_size: tuple = (300, 225),
                       compound="left", row: int = 0, column: int = 0,
                       x_pad: int | tuple = 30, y_pad: int | tuple = 30) \
            -> ct.CTkLabel:
        """Create an image label"""

        eq_img = ct.CTkImage(
            light_image=Image.open(img_path),
            dark_image=Image.open(img_path),
            size=img_size)

        return ct.CTkLabel(frame, text=text,
                           image=eq_img,
                           compound=compound,
                           corner_radius=1,
                           anchor=anchor,
                           font=ct.CTkFont(
                               family="Mali",
                               size=size,
                               weight="bold",
                           ),
                           ).grid(row=row, column=column,
                                  padx=x_pad, pady=y_pad, sticky="nsew")

    @staticmethod
    def create_btn(frame, text: str, command, size: int = 25, row: int = 0,
                   column: int = 0, x_pad: int | tuple = 30,
                   border_spacing: int = 0,
                   y_pad: int | tuple = 30, image=None,
                   sticky: str = "nsew") -> ct.CTkButton:
        """Create a button"""

        return ct.CTkButton(frame, text=text, command=command, image=image,
                            border_spacing=border_spacing,
                            font=ct.CTkFont(family="Mali", size=size,
                                            weight="bold")
                            ).grid(row=row, column=column, padx=x_pad,
                                   pady=y_pad, sticky=sticky)

    @staticmethod
    def create_img_btn(frame, text: str = "", img_path: str = "",
                       size: int = 25, anchor: str = "center", command=None,
                       img_size: tuple = (50, 30), height: int = 50,
                       border_spacing: int = 0, border_width: int = 0,
                       corner_radius: int = 0,
                       sticky: str = "nsew",
                       compound="left", row: int = 0, column: int = 0,
                       x_pad: int | tuple = 30, y_pad: int | tuple = 30) \
            -> ct.CTkButton:
        """Create an image button"""

        eq_img = ct.CTkImage(
            light_image=Image.open(img_path),
            dark_image=Image.open(img_path),
            size=img_size)

        return ct.CTkButton(frame, text=text,
                            command=command,
                            border_spacing=border_spacing,
                            image=eq_img,
                            height=height,
                            compound=compound,
                            border_width=border_width,
                            corner_radius=corner_radius,
                            anchor=anchor,
                            font=ct.CTkFont(
                                family="Mali",
                                size=size,
                                weight="bold",
                            ),
                            ).grid(row=row, column=column,
                                   padx=x_pad, pady=y_pad, sticky=sticky)

    @staticmethod
    def create_top_screen(upper_text: str, lower_text: str, height: int = 300,
                          width: int = 500, which: str = "") -> None:
        """Create a top screen"""

        # Set window properties
        info_window = ct.CTkToplevel()
        info_window.title("Info")
        info_window.geometry(f"{width}x{height}")
        info_window.resizable(True, True)
        info_window.grid_columnconfigure(0, weight=1)

        # Create info frame
        info_frame_1 = ct.CTkFrame(info_window)
        info_frame_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        info_frame_2 = ct.CTkFrame(info_window)
        info_frame_2.grid(row=1, column=0, padx=20, sticky="nsew")

        # Create info label
        frame_1_label = ct.CTkLabel(info_frame_1, text=upper_text,
                                    font=ct.CTkFont(
                                        family="Mali", size=20,
                                        weight="bold"))
        frame_1_label.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        if which == "info":  # Check if the info window is for info or else
            frame_2_label = ct.CTkLabel(info_frame_2, text=lower_text,
                                        justify="left",
                                        font=ct.CTkFont(
                                            family="Mali", size=15,
                                            weight="bold")
                                        )
            frame_2_label.grid(row=0, column=0, padx=20, sticky="nsew")

        else:
            scrollable = ct.CTkScrollableFrame(info_frame_2,
                                               height=height - height // 3,
                                               width=width - width // 10)
            scrollable.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            frame_2_label = ct.CTkLabel(scrollable, text=lower_text,
                                        justify="left",
                                        font=ct.CTkFont(
                                            family="Mali", size=15,
                                            weight="bold")
                                        )
            frame_2_label.grid(row=0, column=0, padx=20, sticky="nsew")

        # Create exit button
        exit_btn = ct.CTkButton(info_window, text="Exit",
                                command=info_window.destroy,
                                font=ct.CTkFont(
                                    family="Mali", size=15,
                                    weight="bold")
                                )
        exit_btn.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    @staticmethod
    def create_opt_menu(frame, *args, **kwargs) -> ct.CTkOptionMenu:
        """Create an option menu"""

        value = kwargs.pop('value', [])
        command = kwargs.pop('command', None)
        row = kwargs.pop('row', 0)
        column = kwargs.pop('column', 0)
        x_pad = kwargs.pop('x_pad', 30)
        y_pad = kwargs.pop('y_pad', 30)
        variable = kwargs.pop('variable', None)
        sticky = kwargs.pop('sticky', 'nsew')

        return ct.CTkOptionMenu(frame, variable=variable, values=value,
                                command=command,
                                font=ct.CTkFont(family='Mali', size=15,
                                                weight='bold'),
                                *args, **kwargs
                                ).grid(row=row, column=column, padx=x_pad,
                                       pady=y_pad, sticky=sticky)

    @staticmethod
    def set_var(var: ct.StringVar = "", value: str = "") -> None:
        """Set a Var"""

        var.set(value)
