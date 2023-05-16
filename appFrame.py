from typing import Optional, Any
import customtkinter as ct
from PIL import Image
from plotFrame import PlotFrame
from facadeController import FacadeController


class AppFrame(ct.CTkFrame):
    """App frame"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Setting the attributes
        self._parent: Any = parent  # App
        self._nss: Optional[NavigationSubFrame] = None  # Navigation sub screen
        self._wss: Optional[WindowSubFrame] = None  # Window sub screen
        self._facade: FacadeController = FacadeController()  # FacadeController

        # Setting the colors
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Setting the frames
        self.start_window_sub_screen()
        self.start_navigation_screen()

    @property
    def parent(self) -> Any:
        """Parent"""

        return self._parent

    @property
    def nss(self) -> Optional["NavigationSubFrame"]:
        """Navigation sub screen"""

        return self._nss

    @nss.setter
    def nss(self, value) -> None:
        """Navigation sub screen"""

        self._nss = value

    @property
    def wss(self) -> Optional["WindowSubFrame"]:
        """Window sub screen"""

        return self._wss

    @wss.setter
    def wss(self, value) -> None:
        """Window sub screen"""

        self._wss = value

    @property
    def facade(self) -> FacadeController:
        """FacadeController"""

        return self._facade

    def start_navigation_screen(self) -> None:
        """Start navigation screen"""

        self.nss = NavigationSubFrame(self)
        self.nss.create_eq_element(self.parent.welcome_screen)
        self.nss.create_home_element(self.wss.create_home_sub_frame)
        self.nss.create_visual_element(self.wss.create_visual_sub_frame)
        self.nss.create_regression_element(
            self.wss.create_regression_sub_frame)

    def start_window_sub_screen(self) -> None:
        """Start window sub screen"""

        self.wss = WindowSubFrame(self)
        self.wss.create_home_sub_frame()


class NavigationSubFrame(ct.CTkFrame):
    """Navigation sub screen"""

    def __init__(self, parent: AppFrame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Setting the attributes
        self._parent: AppFrame = parent  # AppFrame
        self._facade = FacadeController()  # FacadeController
        self.eq_img_path: str = self.facade.get_eq_img_path()  # Path to equalize icon
        self.visual_icon_path: str = self.facade.get_visual_icon_path()  # Path to visual icon
        self.home_icon_path: str = self.facade.get_home_icon_path()  # Path to home icon
        self.regression_icon_path: str = self.facade.get_regression_icon_path()  # Path to regression icon
        self.create_initial_frame()  # Create initial frame

    @property
    def parent(self) -> AppFrame:
        """AppFrame"""

        return self._parent

    @property
    def facade(self) -> FacadeController:
        """FacadeController"""

        return self._facade

    def create_initial_frame(self) -> None:
        """Create initial frame"""

        self.configure(border_color="gray", border_width=1)
        self.grid(row=0, column=0, sticky="nsew")
        self.facade.change_appearance(self, y_pad=470, grid_col=0)
        self.facade.create_music_btn(self, y_pad=20, grid_col=0)

    def create_eq_element(self, command=None) -> None:
        """Create equalize element"""

        eq_img = ct.CTkImage(
            light_image=Image.open(self.eq_img_path),
            dark_image=Image.open(self.eq_img_path),
            size=(50, 30))

        return ct.CTkButton(self, text='Equalize',
                            command=command,
                            border_spacing=0,
                            fg_color="transparent",
                            hover_color=None,
                            image=eq_img,
                            height=50,
                            compound='left',
                            border_width=0,
                            corner_radius=0,
                            anchor='center',
                            font=self.facade.create_font()
                            ).grid(row=0, column=0,
                                   padx=20, pady=30, sticky="nsew")

    def create_home_element(self, command=None) -> None:
        """Create home element"""

        self.facade.create_img_btn(self, text="Home", command=command,
                                   img_path=self.home_icon_path, height=50,
                                   img_size=(30, 20), anchor="center",
                                   border_width=0, corner_radius=0,
                                   row=1, column=0, size=20, x_pad=0,
                                   border_spacing=4, compound="left",
                                   y_pad=0, sticky="nsew")

    def create_visual_element(self, command=None) -> None:
        """Create visual element"""

        self.facade.create_img_btn(self, text="Visualize", command=command,
                                   img_path=self.visual_icon_path, height=50,
                                   img_size=(30, 20), anchor="center",
                                   border_width=0, corner_radius=0,
                                   row=2, column=0, size=20, x_pad=0,
                                   border_spacing=4, compound="left",
                                   y_pad=0, sticky="nsew")

    def create_regression_element(self, command=None) -> None:
        """Create regression element"""

        self.facade.create_img_btn(self, text="Regression", command=command,
                                   img_path=self.regression_icon_path,
                                   height=50,
                                   img_size=(30, 20), anchor="center",
                                   border_width=0, corner_radius=0,
                                   row=3, column=0, size=20, x_pad=0,
                                   border_spacing=4, compound="left",
                                   y_pad=0, sticky="nsew")


class WindowSubFrame(ct.CTkScrollableFrame):
    """Window sub screen"""

    def __init__(self, parent: ct.CTkFrame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Setting the attributes
        self._facade: FacadeController = FacadeController()  # FacadeController
        self._parent: ct.CTkFrame = parent  # AppFrame
        self.entry1: Optional[ct.CTkEntry] = None  # Entry
        self.entry2: Optional[ct.CTkEntry] = None  # Entry
        self.entry3: Optional[ct.CTkEntry] = None  # Entry
        self.input_frame: Optional[ct.CTkFrame] = None  # Input frame
        self.header_lbl: Optional[ct.CTkLabel] = None  # Header label
        self.text_lbl: Optional[ct.CTkLabel] = None  # Text label
        self.plot_frame: Optional[PlotFrame] = None  # Plot frame

        # Manage the grid
        self.configure(border_color="gray", border_width=1)
        self.grid(row=0, column=1, padx=10, sticky="nsew")

        # Create the data container
        self.options: dict = {"target": "GII",
                              "input1": "Adolescent_birth_rate",
                              "input2": "Seats_parliament",
                              "input3": "F_Labour_force"}

        self.values: dict = {"input1": 0.0,
                             "input2": 0.0,
                             "input3": 0.0}

    @property
    def parent(self) -> ct.CTkFrame:
        """AppFrame"""

        return self._parent

    @property
    def facade(self) -> FacadeController:
        """FacadeController"""

        return self._facade

    @FacadeController.run_task("Loading..")
    def create_home_sub_frame(self) -> None:
        """Create home sub frame"""

        self.reset_widget(self)  # Reset the widget

        # Create the texts
        text_1 = self.facade.get_home_text_1()
        text_2 = self.facade.get_home_text_2()
        text_3 = self.facade.get_home_text_3()
        data_text = self.facade.get_data_text()
        stat_text = self.facade.get_statistic()
        corr_text = self.facade.get_corr_text()
        warn_text = self.facade.get_warning_text()

        # Create the images
        img_2 = self.facade.get_graph_img_path("GII_his.png")
        img_3 = self.facade.get_graph_img_path("pie.png")
        img_4 = self.facade.get_graph_img_path("stack_bar.png")
        img_5 = self.facade.get_graph_img_path("heatmap.png")
        network1 = self.facade.get_graph_img_path("netw1.png")
        network2 = self.facade.get_graph_img_path("netw2.png")

        # Create the elements
        self.header_lbl = ct.CTkLabel(self, text="Information",
                                      font=self.facade.create_font(25))

        self.header_lbl.grid(row=0, column=0, padx=20, pady=30, sticky="nsew")
        self.facade.create_text_lbl(self, text=warn_text, size=16, row=2,
                                    wraplength=660)

        self.facade.create_text_lbl(self, text="📌What is Equalize?", size=20,
                                    justify="left", row=3, column=0)
        self.facade.create_text_lbl(self, text=text_1, size=18, wraplength=660,
                                    justify="left", row=4, column=0)

        self.facade.create_text_lbl(self, text="📌About Dataset", size=20,
                                    justify="left", row=5, column=0)
        self.facade.create_text_lbl(self, text=text_2, size=18, wraplength=660,
                                    justify="left", row=6, column=0)
        self.facade.create_btn(self, text="Data Dictionary",
                               command=lambda: self.facade.create_top_screen(
                                   "Data Dictionary", data_text, width=1000,
                                   height=600, which='info'), size=18, row=7,
                               column=0, )

        self.facade.create_btn(self, text="Descriptive Statistics",
                               command=lambda: self.facade.create_top_screen(
                                   "Descriptive Statistics", stat_text,
                                   width=300,
                                   height=600), size=18, row=8, column=0, )

        self.facade.create_text_lbl(self, text="📌Dataset Source", size=20,
                                    justify="left", row=9, column=0)
        self.facade.create_text_lbl(self, text=text_3, size=18, wraplength=660,
                                    justify="left", row=10, column=0)

        self.facade.create_text_lbl(self, text=". . .", size=18,
                                    justify="left", row=11, column=0)

        self.facade.create_text_lbl(self, text="Sample Graph", size=25,
                                    justify="left", row=12, column=0)

        self.facade.create_text_lbl(self, text="Distribution Graphs",
                                    anchor="w", size=20,
                                    row=13,
                                    column=0)

        self.facade.create_img_lbl(self, img_path=img_2,
                                   text="\tThe histogram shows the\n\t"
                                        "distribution of GII",
                                   size=18, row=14, column=0)

        self.facade.create_text_lbl(self, text="Everyday Graphs", anchor="w",
                                    size=20,
                                    row=16, column=0)

        self.facade.create_img_lbl(self, img_path=img_3,
                                   text="\tA graph show proportion \n\tof "
                                        "GII of \n\tHuman Development",
                                   size=18, row=17, column=0)

        self.facade.create_img_lbl(self, img_path=img_4,
                                   text="\tProportions of GII,\n\tFemale "
                                        "Seconday Education\n\tand\n\tMale "
                                        "Secondary Education",
                                   size=18, row=18, column=0)

        self.facade.create_text_lbl(self, text="Network Graphs", anchor="w",
                                    size=20,
                                    row=19, column=0)

        self.facade.create_img_lbl(self, img_path=network1,
                                   text="\tGraph shows relation\n\tbetween "
                                        "Country,\n\tHuman Development,\n\t"
                                        "and Seats parliament.",
                                   size=18, row=20, column=0)

        self.facade.create_img_lbl(self, img_path=network2,
                                   text="\tGraph shows relation\n\tbetween "
                                        "Country,\n\tHuman Development,"
                                        "\n\tand\n\tAdolescent Birth Rate.",
                                   size=18, row=21, column=0)

        self.facade.create_text_lbl(self, text="Correlation", anchor="w",
                                    size=20,
                                    row=22, column=0)
        self.facade.create_text_lbl(self, text=corr_text, size=18, row=23)
        self.facade.create_img_lbl(self, img_path=img_5, row=24,
                                   anchor="center", img_size=(500, 400))

    def create_visual_sub_frame(self) -> None:
        """Create the visual sub frame"""

        self.reset_widget(self)  # Reset the frame
        text = self.facade.get_visual_text()  # Get the text
        self.header_lbl = ct.CTkLabel(self, text="Visualize",
                                      font=self.facade.create_font(25))

        self.header_lbl.grid(row=0, column=0, padx=20, pady=30, sticky="nsew")

        self.facade.create_text_lbl(self, text="📌Quick tour",
                                    size=20, justify="left", row=1,
                                    column=0)

        self.facade.create_text_lbl(self, text=text, wraplength=660,
                                    size=18, justify="left", row=2,
                                    column=0)

        self.facade.create_btn(self, text="Enter the visualize screen",
                               command=self.enter_tab_view, row=3, column=0,
                               size=18)

    def create_regression_sub_frame(self) -> None:
        """Create the regression sub frame"""

        self.reset_widget(self) # Reset the frame
        text1 = self.facade.get_regression_text_1()
        text2 = self.facade.get_regression_text_2()
        var = ct.StringVar()
        var.set("Select a model")
        self.header_lbl = ct.CTkLabel(self, text="Regression",
                                      font=self.facade.create_font(25))
        self.header_lbl.grid(row=0, column=0, padx=20, pady=30,
                             sticky="nsew")
        self.facade.create_text_lbl(self, text="📌Overview",
                                    size=20, justify="left", row=1,
                                    column=0)
        self.facade.create_text_lbl(self, text=text1,
                                    size=18, justify="left", row=2,
                                    column=0, wraplength=660)
        self.facade.create_text_lbl(self, text="📌How to use it?",
                                    size=20, justify="left", row=3,
                                    column=0)
        self.facade.create_text_lbl(self, text=text2,
                                    size=18, justify="left", row=4,
                                    column=0, wraplength=660)

        self.facade.create_btn(self, text="Open the data table",
                               command=lambda: self.enter_tab_view(1), row=5,
                               column=0,
                               size=18)

        self.facade.create_text_lbl(self, text="Select model: ",
                                    row=7, column=0, size=18)
        self.facade.create_opt_menu(self, value=["Simple Linear Regression",
                                                 "Multiple Linear Regression"],
                                    variable=var,
                                    command=self.linear_regression_opt,
                                    row=9, column=0)

    def linear_regression_opt(self, var: str = "") -> None:
        """Create the linear regression options"""

        self.input_frame = ct.CTkFrame(self, width=600, height=0)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid(row=21, column=0, sticky="nsew")
        self.facade.create_opt_menu(self.input_frame,
                                    value=self.facade.get_columns()[2:-1],
                                    command=lambda x:
                                    self.options.update({"input1": x}),
                                    row=1, column=0)
        self.reset_widget(self.input_frame)

        self.facade.create_text_lbl(self, text="Select a prediction target ",
                                    row=13, column=0, size=18)

        self.facade.create_opt_menu(self,
                                    value=self.facade.get_columns()[2:-1],
                                    command=lambda x:
                                    self.options.update({"target": x}),
                                    row=15, column=0)

        self.facade.create_text_lbl(self, text="Select an input(s)",
                                    row=16, column=0, size=18)
        self.input_frame = ct.CTkFrame(self, width=600, height=200)
        self.input_frame.grid_columnconfigure(0, weight=2)
        self.input_frame.grid_columnconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(2, weight=1)
        self.input_frame.grid(row=19, column=0, sticky="nsew")

        self.facade.create_opt_menu(self.input_frame,
                                    value=self.facade.get_columns()[2:-1],
                                    command=lambda x:
                                    self.options.update({"input1": x}),
                                    row=1, column=0, sticky="nsew")

        self.facade.create_text_lbl(self.input_frame, text="Value 1:",
                                    row=1, column=1, size=18, x_pad=(20, 10))

        self.entry1 = ct.CTkEntry(self.input_frame, width=200)
        self.entry1.grid(row=1, column=2)

        if var == "Multiple Linear Regression":
            self.facade.create_opt_menu(self.input_frame,
                                        value=self.facade.get_columns()[2:-1],
                                        command=lambda x:
                                        self.options.update({"input2": x}),
                                        row=2, column=0)
            self.facade.create_text_lbl(self.input_frame, text="Value 2:",
                                        row=2, column=1, size=18,
                                        x_pad=(20, 10))

            self.entry2 = ct.CTkEntry(self.input_frame, width=200)
            self.entry2.grid(row=2, column=2)

            self.facade.create_opt_menu(self.input_frame,
                                        value=self.facade.get_columns()[2:-1],
                                        command=lambda x:
                                        self.options.update({"input3": x}),
                                        row=4, column=0)
            self.facade.create_text_lbl(self.input_frame, text="Value 3:",
                                        row=4, column=1, size=18,
                                        x_pad=(20, 10))

            self.entry3 = ct.CTkEntry(self.input_frame, width=200)
            self.entry3.grid(row=4, column=2)

        self.facade.create_btn(self.input_frame, text="Predict",
                               command=lambda: self.create_predict_label(var),
                               row=5,
                               column=0, size=18, sticky="nsew")

    def create_predict_label(self, model: str = "") -> None:
        """Create the predicted value label"""

        if model == "Simple Linear Regression":
            self.values.update({"input1": float(self.entry1.get())})
        else:
            self.values.update({"input1": float(self.entry1.get()),
                                "input2": float(self.entry2.get()),
                                "input3": float(self.entry3.get())})
        value = self.facade.regression(model, self.options, self.values)
        self.facade.create_text_lbl(self.input_frame, text="Predicted value:",
                                    row=5, column=1, size=18)
        self.facade.create_text_lbl(self.input_frame, text=value,
                                    row=5, column=2, size=18)

    def enter_tab_view(self, page: int = 2) -> None:
        """Enter the tab view"""

        self.plot_frame = PlotFrame(self, page_num=page)

    @staticmethod
    def reset_widget(frame) -> None:
        """Reset the widget"""

        if frame:
            if frame.winfo_children():
                for widget in frame.winfo_children():
                    widget.destroy()
