import os
from typing import Any
import pandas as pd
import seaborn as sns
import networkx as nx
from commonWidget import CommonWidget
from model import Analysis


class FacadeController(CommonWidget):
    """Facade controller"""

    def __init__(self):
        super().__init__()
        self.model: Analysis = Analysis()  # Analysis model

    def get_statistic(self) -> dict:
        """Get the descriptive statistics"""

        return self.model.get_descriptive_statistics()

    def get_df(self, event: str = "") -> pd.DataFrame:
        """Get the dataframe"""

        if event:
            return self.model.df.query(event).applymap(
                lambda x: float(f'{x:.2f}') if isinstance(x, float) else x)

        return self.model.df.applymap(
            lambda x: float(f'{x:.2f}') if isinstance(x, float) else x)

    def get_columns(self) -> list:
        """Get the columns"""

        return self.model.df.columns

    def get_rows(self) -> list:
        """Get the rows"""

        return self.model.df.applymap(
            lambda x: f'{x:.2f}' if isinstance(x, float)
            else x).values.tolist()

    def get_network_graph(self, col, color1: str, color2: str, color3: str,
                          color4: str) -> nx.Graph:
        """Get the network graph"""

        return self.model.get_network_graph(col, color1, color2, color3,
                                            color4)

    def regression(self, mode: str = "", option: dict = None,
                   value: dict = None) -> Any:
        """Regression"""

        return self.model.regression(mode, option, value)

    @staticmethod
    def get_dir_path() -> str:
        """Get the directory path"""

        return os.getcwd()

    @staticmethod
    def get_graph_path() -> str:
        """Get the graph path"""

        return os.path.join(os.getcwd(), "misc")

    @staticmethod
    def get_color_csv_path() -> str:
        """Get the color csv path"""

        return os.path.join(os.getcwd(), "data", "colors.csv")

    @staticmethod
    def get_theme_path() -> str:
        """Get the theme path"""

        return os.path.join(os.getcwd(), "data", "theme.json")

    @staticmethod
    def get_colors() -> Any:
        """Get the colors"""

        return pd.read_csv(
            os.path.join(FacadeController.get_color_csv_path())).values

    @staticmethod
    def get_eq_img_path() -> str:
        """Get the equalize image path"""

        return os.path.join(os.getcwd(), "misc", "img",
                            "gender.png")

    @staticmethod
    def get_menu_img_path() -> str:
        """Get the menu image path"""

        return os.path.join(os.getcwd(), "misc", "img", "title.jpg")

    @staticmethod
    def get_info_text() -> str:
        """Get the info text"""

        return "Equalize is a data analysis program that uses\n the " \
               "gender inequality index\n dataset to analyze and " \
               "visualize.\n\n **The color in the program is just a " \
               "theme, it has no \nsignificant meaning at all."

    @staticmethod
    def get_warning_text() -> str:
        """Get the warning text"""

        return "**This is a scroll frame make sure you scroll " \
               "up before going to the other section."

    @staticmethod
    def get_home_text_1() -> str:
        """Get the home text 1"""

        return "Equalize is a program that can analyze " \
               "and visualize the Gender Inequality Index for over 190 " \
               "countries, in 2021. The program aims to explore data on " \
               "gender disparities in health, education, and economic " \
               "opportunities to identify trends and patterns and then " \
               "visualize them to make it easy to compare and understand."

    @staticmethod
    def get_home_text_2() -> str:
        """Get the home text 2"""

        return "The Gender Inequality Index (GII) " \
               "dataset provides a comprehensive measure of gender " \
               "inequality across countries, capturing gender disparities " \
               "in health, education, and economic opportunities."

    @staticmethod
    def get_home_text_3() -> str:
        """Get the home text 3 (Data Source)"""

        return "https://www.kaggle.com/datasets/gianinamariapetrascu/gender-" \
               "inequality-index"

    @staticmethod
    def get_corr_text() -> str:
        """Get the correlation text"""

        return "The graph shows the correlation of all data."

    @staticmethod
    def get_data_text() -> str:
        """Get the data text (Data dictionary)"""

        return "Country: The country name.\n\n" \
               "Human_development: Human development category: " \
               "Low - Very High.\n\n" \
               "GII: Gender Inequality Index.\n\n" \
               "Rank: The Country Rank base on GII.\n\n" \
               "Maternal_mortality: Deaths per 100,000 live births.\n\n" \
               "Adolescent_birth_rate: Births per 1,000 women ages " \
               "15–19.\n\n" \
               "Seats_parliament: Share of seats in parliament " \
               "(% held by women).\n\n" \
               "F_secondary_educ: Females with at least some secondary " \
               "education (% ages 25 and older).\n\n" \
               "M_secondary_educ: Males with at least some secondary " \
               "education (% ages 25 and older).\n\n" \
               "F_Labour_force: Female - Labour force participation " \
               "rate (% ages 15 and older).\n\n" \
               "M_Labour_force: Male - Labour force participation " \
               "rate (% ages 15 and older)."

    @staticmethod
    def get_visual_text() -> str:
        """Get the visual text"""

        return "In this section, There will be a button below that going to " \
               "bring you to the visualized screen and there will have some" \
               " of options and properties that you can choose from, In the" \
               " visualized screen, there will have 2 main tabs, the first " \
               "one is the data table tab which going to help you to decide " \
               "to choose a plot property, another one is the plotting tab " \
               "which going to generate a beautiful easy to understand graph " \
               "for you."

    @staticmethod
    def get_regression_text_1() -> str:
        """Get the regression text 1"""

        return "Have you ever tried analyzing a large amount of " \
               "data? If so, this section will be right up your alley. We " \
               "will be using machine learning techniques, specifically " \
               "Linear Regression, to predict data rather than just analyzing" \
               " it."

    @staticmethod
    def get_regression_text_2() -> str:
        """Get the regression text 2"""

        return "First, select a type of regression you want " \
               "to perform, which can be either Simple Linear Regression or" \
               " Multiple Linear Regression. The former predicts one value" \
               " based on one other value, while the latter predicts one" \
               " value based on multiple values. After selecting the" \
               " regression type, choose any data that you are interested" \
               " in and click on the 'Predict' button to get the predicted" \
               " results."

    @staticmethod
    def get_dis_plot() -> list:
        """Get the distribution plot choices"""

        return ["histplot", "kdeplot", "ecdfplot", "rugplot", "boxplot"]

    @staticmethod
    def get_every_plot() -> list:
        """Get the every plot choices"""

        return ["pie", "stackbar"]

    @staticmethod
    def get_corr_plot() -> list:
        """Get the correlation plot choices"""

        return ["scatterplot", "lineplot"]

    @staticmethod
    def get_plot_func(string: str) -> Any:
        """Get the plot function"""

        plot_dict = {
            "relplot": sns.relplot,
            "histplot": sns.histplot,
            "kdeplot": sns.kdeplot,
            "ecdfplot": sns.ecdfplot,
            "rugplot": sns.rugplot,
            "catplot": sns.catplot,
            "stripplot": sns.stripplot,
            "swarmplot": sns.swarmplot,
            "boxenplot": sns.boxenplot,
            "pointplot": sns.pointplot,
            "countplot": sns.countplot,
            "lineplot": sns.lineplot,
            "barplot": sns.barplot,
            "scatterplot": sns.scatterplot,
            "boxplot": sns.boxplot,
            "violinplot": sns.violinplot,
            "pie": sns.histplot,
            "stackbar": sns.histplot

        }
        return plot_dict[string]

    @staticmethod
    def get_network_plot() -> list:
        """Get the network plot choices"""

        return ["circular",
                "random",
                "shell",
                "spring",
                "spectral",
                "planar",
                "fruchterman",
                "spiral",
                "arf"]

    @staticmethod
    def get_network_func(string: str) -> Any:
        """Get the network function"""

        net_dict = {
            "circular": nx.circular_layout,
            "random": nx.random_layout,
            "shell": nx.shell_layout,
            "spring": nx.spring_layout,
            "spectral": nx.spectral_layout,
            "planar": nx.planar_layout,
            "fruchterman": nx.fruchterman_reingold_layout,
            "spiral": nx.spiral_layout,
            "arf": nx.arf_layout
        }
        return net_dict[string]

    @staticmethod
    def get_current_color(color: tuple) -> str:
        """Get the current color"""

        return f"Current color:\n" \
               f"r: {color[0][0]}\n" \
               f"g: {color[0][1]}\n" \
               f"b: {color[0][2]}\n" \
               f"Hex: {color[1]}"

    @staticmethod
    def get_visual_icon_path() -> str:
        """Get the visual icon path"""

        return os.path.join(os.getcwd(), "misc", "img",
                            "graph.png")

    @staticmethod
    def get_home_icon_path() -> str:
        """Get the home icon path"""

        return os.path.join(os.getcwd(), "misc", "img",
                            "home.png")

    @staticmethod
    def get_regression_icon_path() -> str:
        """Get the regression icon path"""

        return os.path.join(FacadeController.get_dir_path(), "misc", "img",
                            "robot.png")

    @staticmethod
    def get_graph_img_path(path: str = "") -> str:
        """Get the graph image path"""

        return os.path.join(os.getcwd(), "misc", "graph", path)
