from tkinter import colorchooser
from tkinter import ttk
from typing import Optional, Any

import customtkinter as ct
import networkx as nx
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from facadeController import FacadeController


class PlotFrame(ct.CTkToplevel):
    """This class is responsible for creating the plot frame."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        # Set the window
        self.geometry("1300x700+70+50")
        self.resizable(False, False)

        # Set the attributes
        self._facade: FacadeController = FacadeController()
        self.figure: Any = None
        self.options: dict = {}
        self.df: Any = self.facade.get_df()

        # Set the widgets
        self.canvas: Optional[FigureCanvasTkAgg] = None
        self.tree: Optional[ttk.Treeview] = None
        self.entry: Optional[ct.CTkEntry] = None
        self.prop_frame: Optional[ct.CTkFrame] = None
        self.graph_frame: Optional[ct.CTkFrame] = None
        self.option_frame: Optional[ct.CTkFrame] = None
        self.opt_2: ct.StringVar = ct.StringVar(value="Plot Type")
        self.opt_3: ct.StringVar = ct.StringVar(value="Value")
        self.opt_4: ct.StringVar = ct.StringVar(value="Value 2")

        # Set the tabs
        self.tab_view = ct.CTkTabview(self, height=660, width=1260)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.tab_view.add("DataFrame")
        self.create_tree()

        # Set a condition to create the plot tab (Visualize only)
        if kwargs.get("page_num", 2) == 2:
            self.tab_view.add("Plot")
            self.create_opt_frame()
            self.create_graph_frame()
            self.create_prop_frame()

        # add widgets on tabs
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.facade.create_btn(self, text="Close", row=1, column=0,
                               command=self.destroy, size=10, y_pad=(0, 10))

    @property
    def facade(self) -> FacadeController:
        """FacadeController"""
        return self._facade

    def create_tree(self) -> None:
        """This method is responsible for creating the treeview."""

        self.init_tree()
        text = ct.StringVar(value="Insert column")
        frame = ct.CTkFrame(self.tab_view.tab("DataFrame"), height=90,
                            width=550)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.facade.create_text_lbl(frame,
                                    text="Query (Optional)", row=0,
                                    column=0, size=15, y_pad=5)
        self.entry = ct.CTkEntry(frame, width=350)

        self.entry.insert(0, "ISO in ['ISL','SWE'] or 0.05 > GII > 0.01")
        self.entry.grid(row=1, column=0, padx=10, pady=2)

        self.facade.create_opt_menu(frame, variable=text,
                                    command=lambda x: self.entry.insert(ct.END,
                                                                        x),
                                    value=self.facade.get_df().columns, row=1,
                                    column=1, y_pad=10)

        self.facade.create_btn(frame, text="Confirm",
                               row=1, column=2, command=lambda: self.init_tree(
                self.entry.get()),
                               size=15, y_pad=10)
        self.facade.create_btn(frame, text="Reset", row=1, column=3,
                               command=lambda: self.entry.delete(0, ct.END),
                               size=15, y_pad=10)

    def init_tree(self, event: str = None) -> None:
        """This method is responsible for initializing the treeview."""

        style = ttk.Style()
        columns = None
        rows = None

        # set style according to the appearance mode
        if ct.get_appearance_mode() == "Dark":
            style.configure("Treeview", background="Black", foreground="white",
                            fieldbackground="#C47AFF")
            style.map("Treeview", background=[("selected", "#C47AFF")])
        else:
            style.configure("Treeview", background="White", foreground="black",
                            fieldbackground="#E80F88")
            style.map("Treeview", background=[("selected", "#E80F88")])

        # get columns and rows
        try:
            columns = tuple(self.facade.get_df(event).columns)
            rows = tuple(self.facade.get_df(event).values.tolist())
        except SyntaxError:
            self.entry.delete(0, ct.END)
            self.entry.insert(0, "Invalid input, try again")
            self.after(1200, self.update_entry)

        self.tree = ttk.Treeview(self.tab_view.tab("DataFrame"),
                                 columns=columns,
                                 show='headings', height=20)

        scrollbar = ttk.Scrollbar(self.tab_view.tab("DataFrame"),
                                  orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # set column headings
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=98, anchor="center")

        self.tree.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # insert values into a tree
        for row in rows:
            self.tree.insert(parent='', index=0, values=row)

    def update_entry(self) -> None:
        """This method is responsible for updating the entry widget."""

        self.entry.delete(0, ct.END)
        self.entry.insert(0, "ISO in ['ISL','SWE'] or 0.05 > GII > 0.01")

    def opt_changed(self, value) -> None:
        """This method is responsible for changing the options in the"""

        self.options[value[0]] = value[1]
        self.reset_widget()
        if self.options["Graph"] == "Distribution":
            self.opt_3.set("Value")
            self.create_dist_opt()

        elif self.options["Graph"] == "Everyday":
            self.opt_3.set("Value")
            self.create_everyday_opt()

        elif self.options["Graph"] == "Correlation":
            self.opt_3.set("Value 1")
            self.opt_4.set("Value 2")
            self.create_corr_opt()

        elif self.options["Graph"] == "Network":
            self.opt_3.set("Value")
            self.create_network_opt()

    def create_dist_opt(self, value=None) -> None:
        """This method is responsible for creating the options for the
        distribution graph."""

        self.plot_dis_graph()
        if value:
            self.options[value[0]] = value[1]
        if self.options.get("Graph") == "Distribution":
            self.facade.create_opt_menu(self.option_frame, variable=self.opt_2,
                                        command=lambda x: self.create_dist_opt(
                                            ("Plot", x)),
                                        value=self.facade.get_dis_plot(),
                                        row=2, column=0)

        if self.options.get("Plot") in self.facade.get_dis_plot():
            self.facade.create_opt_menu(self.option_frame, variable=self.opt_3,
                                        command=lambda x: self.create_dist_opt(
                                            ("Column", x)),
                                        value=self.facade.get_columns()[2:-1],
                                        row=4, column=0)

            self.create_prop_btn(command=self.plot_dis_graph)

    def create_everyday_opt(self, value=None) -> None:
        """This method is responsible for creating the options for the
        everyday graph."""

        self.plot_everyday_graph()
        if value:
            self.options[value[0]] = value[1]
        if self.options.get("Graph") == "Everyday":
            self.facade.create_opt_menu(self.option_frame, variable=self.opt_2,
                                        command=lambda
                                            x: self.create_everyday_opt(
                                            ("Plot", x)),
                                        value=self.facade.get_every_plot(),
                                        row=2, column=0)

        if self.options.get("Plot") in self.facade.get_every_plot():
            self.facade.create_opt_menu(self.option_frame, variable=self.opt_3,
                                        command=lambda
                                            x: self.create_everyday_opt(
                                            ("Column", x)),
                                        value=self.facade.get_columns()[2:-1],
                                        row=4,
                                        column=0)

            self.create_prop_btn(command=self.plot_everyday_graph)

    def create_corr_opt(self, value=None) -> None:
        """This method is responsible for creating the options for the
        correlation graph."""

        self.plot_corr_graph()
        if value:
            self.options[value[0]] = value[1]

        if self.options.get("Graph", "Correlation") == "Correlation":
            self.facade.create_opt_menu(self.option_frame, variable=self.opt_2,
                                        command=lambda
                                            x: self.create_corr_opt(
                                            ("Plot", x)),
                                        value=self.facade.get_corr_plot(),
                                        row=2, column=0)

        if self.options.get("Plot") in self.facade.get_corr_plot():
            self.facade.create_opt_menu(self.option_frame, variable=self.opt_3,
                                        command=lambda
                                            x: self.create_corr_opt(
                                            ("Column1", x)),
                                        value=self.facade.get_columns()[2:-1],
                                        row=4,
                                        column=0)
            self.facade.create_opt_menu(self.option_frame, variable=self.opt_4,
                                        command=lambda
                                            x: self.create_corr_opt(
                                            ("Column2", x)),
                                        value=self.facade.get_columns()[2:-1],
                                        row=6,
                                        column=0)

            self.create_prop_btn(command=self.plot_corr_graph)

    def create_network_opt(self, value=None) -> None:
        """This method is responsible for creating the options for the
        network graph."""

        self.plot_network_graph()
        if value:
            self.options[value[0]] = value[1]
        if self.options.get("Graph") == "Network":
            self.facade.create_opt_menu(self.option_frame, variable=self.opt_2,
                                        command=lambda
                                            x: self.create_network_opt(
                                            ("NPlot", x)),
                                        value=self.facade.get_network_plot(),
                                        row=2, column=0)

        if self.options.get("NPlot") in self.facade.get_network_plot():
            self.facade.create_opt_menu(self.option_frame, variable=self.opt_3,
                                        command=lambda
                                            x: self.create_network_opt(
                                            ("Column1", x)),
                                        value=self.facade.get_columns()[2:-1],
                                        row=4,
                                        column=0)

            layout = self.options.get("NPlot", "spring_layout")
            func = self.facade.get_network_func(layout)
            self.create_prop_btn(command=lambda: self.plot_network_graph(func))

    def plot_dis_graph(self) -> None:
        """This method is responsible for plotting the distribution graph."""

        if self.figure:  # Clear the figure if it is not empty
            self.figure.clf()

        colors = self.get_colors()
        sns.set_style("darkgrid")
        if self.options.get("Plot", "histplot") != "boxplot":
            plot = self.facade.get_plot_func(
                self.options.get("Plot", "histplot"))(
                data=self.df,
                x=self.df[self.options.get("Column", "GII")],
                hue='Human_development',
                palette=colors,
            )
        else:
            plot = self.facade.get_plot_func(
                self.options.get("Plot", "histplot"))(
                data=self.df,
                y=self.df[self.options.get("Column", "GII")],
                hue='Human_development',
                palette=colors,
            )
        plot.set(
            title=f"A graph show the frequency of {self.options.get('Column', 'GII').replace('_', ' ')}")
        self.figure = plot.get_figure()
        plot.set_xlabel(self.options.get('Column', 'GII'))
        plot.set_ylabel("Frequency")

        self.create_canvas()

    def plot_everyday_graph(self) -> None:
        """This method is responsible for plotting the everyday graph."""

        if self.figure:  # Clear the figure if it is not empty
            self.figure.clf()

        sns.set_style("darkgrid")
        fig = plt.figure()
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        colors = self.get_colors()

        if self.options.get("Plot") == "stackbar":  # Plot the stacked bar plot
            # Calculate the average of values in each country
            # (In case that there are duplicated country)

            col_sum = self.df.groupby("ISO")[
                self.options.get("Column", "GII")].mean()

            # Select the top 10 columns based on the average of values
            top_10_cols = col_sum.sort_values(ascending=False)[
                          :10].index.tolist()

            # Create a pivot table with only the top 10 columns
            pivot_table = self.df.pivot_table(index="Human_development",
                                              columns="ISO",
                                              values=self.options.get("Column",
                                                                      "GII"),
                                              aggfunc="sum")[top_10_cols]

            # Plot the stacked bar plot
            ax = pivot_table.plot(kind="bar", stacked=True, figsize=(7, 5),
                                  )

            # Set the title and labels
            ax.set_title(
                f"A graph showing proportion of {self.options.get('Column', 'GII')} of Top 10 Human Development by ISO")
            ax.set_xlabel("Human Development")
            ax.set_ylabel("Proportion")
            ax.legend(loc='best')

        else:  # Plot the pie chart
            ax.pie(self.df.groupby("Human_development")[
                       self.options.get("Column", "GII")].agg("sum"),
                   labels=self.df.Human_development.unique(),
                   autopct='%1.1f%%',
                   startangle=90,
                   colors=colors)
            ax.axis('equal')
            ax.set_title(f'A graph show proportion of {self.options.get("Column", "GII")} of Human Development')

        self.figure = ax.get_figure()
        self.create_canvas()

    def plot_corr_graph(self) -> None:
        """This method is responsible for plotting the correlation graph."""

        if self.figure:  # Clear the figure if it is not empty
            self.figure.clf()

        sns.set_style("darkgrid")
        colors = self.get_colors()
        plot = self.facade.get_plot_func(self.options.get("Plot",
                                                          "scatterplot")) \
            (self.df, x=self.options.get("Column1", "GII"),
             y=self.options.get("Column2", "Rank"),
             hue="Human_development",
             palette=colors, )

        plot.set(title=f"A graph show the correlation of {self.options.get('Column1', 'GII')} and {self.options.get('Column2', 'Rank')}".replace('_', ' '))
        self.figure = plot.get_figure()
        plot.set_xlabel(self.options.get('Column1', 'GII'))
        plot.set_ylabel(self.options.get('Column2', 'Rank'))

        self.create_canvas()

    def plot_network_graph(self, layout=nx.circular_layout) -> None:
        """This method is responsible for plotting the network graph."""

        if self.figure:  # Clear the figure if it is not empty
            self.figure.clf()

        col = self.options.get("Column1", "GII")
        colors = self.get_colors()
        G2 = self.facade.get_network_graph(col, colors[0], colors[1],
                                           colors[2], colors[3])

        node_colors_list = [G2.nodes[n].get('color', 'black') for n in G2.nodes()]
        edge_width_list = [G2.edges[n]['weight'] / 50 for n in G2.edges()]
        edge_labels = nx.get_edge_attributes(G2, "weight")

        pos2 = layout(G2)
        nx.draw_networkx_nodes(G2, pos2, node_size=400,
                               node_color=node_colors_list)
        nx.draw_networkx_edges(G2, pos2, width=edge_width_list)
        nx.draw_networkx_labels(G2, pos2, font_size=15)
        nx.draw_networkx_edge_labels(G2, pos2, edge_labels)
        plt.title(f"Random {col} and Human Development relation of 15 countries")
        self.create_canvas()

    def create_color_chooser(self, frame, row: int = 1, num: int = 0) -> None:
        """This method is responsible for creating the color chooser."""

        color = colorchooser.askcolor()

        if num == 0:  # Set the color of the first color chooser
            self.options["Color"] = color[1]
            self.facade.create_text_lbl(frame,
                                        text=self.facade.get_current_color(
                                            color), size=18, row=row, column=0,
                                        y_pad=0, text_color=color[1])

        else:  # Set the color of the second color chooser
            self.options[f"Color{num}"] = color[1]
            self.facade.create_text_lbl(frame,
                                        text=self.options.get(f"Color{num}",
                                                              ""), size=18,
                                        row=row, column=0, y_pad=0,
                                        text_color=color[1])

    def create_canvas(self) -> None:
        """This method is responsible for creating the canvas."""

        self.figure.set_facecolor("gray")
        self.canvas = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20,
                                         sticky="nsew")

    def create_opt_frame(self) -> None:
        """This method is responsible for creating the option frame."""

        self.option_frame = ct.CTkFrame(self.tab_view.tab("Plot"), height=580,
                                        width=200)
        self.option_frame.grid(row=0, column=0, padx=(20, 0), pady=20,
                               sticky="nsw")

        self.facade.create_text_lbl(self.option_frame,
                                    text="Choose the graph type",
                                    size=15, row=0, column=0, x_pad=0,
                                    y_pad=20)
        opt_1 = ct.StringVar(value="Graph Type")
        self.facade.create_opt_menu(self.option_frame, variable=opt_1, row=1,
                                    command=lambda x: self.opt_changed(
                                        ("Graph", x)),
                                    value=["Distribution", "Everyday",
                                           "Correlation", "Network"])

    def create_graph_frame(self) -> None:
        """This method is responsible for creating the graph frame."""

        plt.figure(figsize=(7, 5))
        self.graph_frame = ct.CTkFrame(self.tab_view.tab("Plot"), height=580,
                                       width=800)
        self.graph_frame.grid(row=0, column=1, padx=5, pady=20, sticky="nsew")
        self.plot_dis_graph()

    def create_prop_frame(self) -> None:
        """This method is responsible for creating the property frame."""

        self.prop_frame = ct.CTkFrame(self.tab_view.tab("Plot"), height=580,
                                      width=200)
        self.prop_frame.grid(row=0, column=2, padx=(0, 20), pady=20,
                             sticky="nse")

    def create_prop_btn(self, command=None) -> None:
        """This method is responsible for creating the property button."""

        self.facade.create_btn(self.prop_frame, text="Pick color 1", row=0,
                               column=0, size=15,
                               command=lambda: self.create_color_chooser(
                                   self.prop_frame, row=1, num=1))
        self.facade.create_btn(self.prop_frame, text="Pick color 2", row=2,
                               column=0, size=15,
                               command=lambda: self.create_color_chooser(
                                   self.prop_frame, row=3, num=2))
        self.facade.create_btn(self.prop_frame, text="Pick color 3", row=4,
                               column=0, size=15,
                               command=lambda: self.create_color_chooser(
                                   self.prop_frame, row=5, num=3))
        self.facade.create_btn(self.prop_frame, text="Pick color 4", row=6,
                               column=0, size=15,
                               command=lambda: self.create_color_chooser(
                                   self.prop_frame, row=7, num=4))

        self.facade.create_btn(self.prop_frame, text="Plot", row=9,
                               column=0, command=command,
                               size=15)

    def get_colors(self) -> list:
        """This method is responsible for getting the colors."""

        color1 = self.options.get("Color1", "#39B5E0")
        color2 = self.options.get("Color2", "#FB2576")
        color3 = self.options.get("Color3", "#C9F4AA")
        color4 = self.options.get("Color4", "#F5EA5A")
        return [color1, color2, color3, color4]

    def reset_widget(self) -> None:
        """This method is responsible for resetting the widget."""

        for widget in self.option_frame.winfo_children()[2:]:
            widget.destroy()
        for widget in self.prop_frame.winfo_children():
            widget.destroy()
