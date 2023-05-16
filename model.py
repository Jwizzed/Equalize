import os
import networkx as nx
import numpy as np
import pandas as pd
import pycountry
from typing import Any
from sklearn.linear_model import LinearRegression


class Analysis:
    """This class is used to analyze the data and to perform the regression"""

    def __init__(self):
        # Set the attributes
        self.csv_path: str = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data",
            "Gender_Inequality_Index.csv")
        self.orig_df: pd = pd.read_csv(self.csv_path)
        self.df: Any = self.orig_df.copy()
        self.model: LinearRegression = LinearRegression()

        # Initialize the data
        self.prepare_data()

    def prepare_data(self) -> None:
        """Prepare the data for the analysis"""

        all_country = self.df['Country']
        countries = {country.name: country.alpha_3 for country in
                     pycountry.countries}
        self.df['ISO'] = [countries.get(country) for country in all_country]
        self.df = self.df.dropna()
        self.df = self.df.applymap(
            lambda x: f'{x:.2f}' if isinstance(x, float) else x)
        self.df = self.df.astype({
            "Human_development": "category",
            "GII": "float32",
            "Rank": "float32",
            "Maternal_mortality": "float32",
            "Adolescent_birth_rate": "float32",
            "Seats_parliament": "float32",
            "F_secondary_educ": "float32",
            "M_secondary_educ": "float32",
            "F_Labour_force": "float32",
            "M_Labour_force": "float32",
        })

    def get_descriptive_statistics(self) -> str:
        """Get the descriptive statistics"""

        text = ""
        for column in self.df.describe().columns:
            text += column
            text += ":\n"
            text += f"mean {np.mean(self.df.loc[:, column]):.2f}\n"
            text += f"std {np.std(self.df.loc[:, column]):.2f}\n"
            text += f"min {np.min(self.df.loc[:, column]):.2f}\n"
            text += f"max {np.max(self.df.loc[:, column]):.2f}\n"
            text += f"25% {np.quantile(self.df.loc[:, column], 0.25):.2f}\n"
            text += f"50% {np.quantile(self.df.loc[:, column], 0.5):.2f}\n"
            text += f"75% {np.quantile(self.df.loc[:, column], 0.75):.2f}\n"
            text += "\n"
        return text

    def get_network_graph(self, col: str, color1: str, color2: str,
                          color3: str, color4: str) -> nx.Graph:
        """Get the network graph"""

        G = nx.Graph()  # Create an empty graph
        for row_index in self.df.sample(15).index:
            temp_1 = self.df.loc[row_index, "Human_development"]
            G.add_node(temp_1)
            temp_2 = self.df.loc[row_index, "ISO"]
            G.add_node(temp_2)
            if col == "GII":
                weight = round(self.df.loc[row_index, col] * 40, 2)
            else:
                weight = self.df.loc[row_index, col]

            if temp_1 == "Very high":
                G.nodes[temp_1]['color'] = color1

            elif temp_1 == "High":
                G.nodes[temp_1]['color'] = color2

            elif temp_1 == "Medium":
                G.nodes[temp_1]['color'] = color3

            elif temp_1 == "Low":
                G.nodes[temp_1]['color'] = color4

            G.nodes[temp_2]['color'] = "#EA168E"
            G.add_weighted_edges_from([(temp_1, temp_2, weight)])
        return G

    def regression(self, mode: str = "", options: dict = None,
                   values: dict = None) -> float:
        """Perform the regression"""

        result: float = 0.0
        if mode == "Simple Linear Regression":
            X = self.df[[options["input1"]]]
            y = self.df[options["target"]]
            self.model.fit(X, y)
            result = self.model.predict([[values["input1"]]])

        elif mode == "Multiple Linear Regression":
            X = self.df[[options["input1"], options["input2"], options["input3"]]]
            y = self.df[options["target"]]
            self.model.fit(X, y)
            result = self.model.predict([[values["input1"], values["input2"],
                                   values["input3"]]])
        return round(result[0], 4)
