import tkinter as tk
from datetime import datetime, timedelta
import os
import pandas as pd
from datetime import date
import snscrape.modules.twitter as sntwitter
import threading
import itertools
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def tweet_count_plot(start_date, end_date, search_term):
    delta = timedelta(days=1)
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    dates = []
    tweet_count = []
    links = pd.DataFrame()
    while start <= end:
        dates.append(start.date())
        start += delta
    for d in dates:
        end_d = d + delta
        os.system(f"snscrape --since {d} twitter-search '{search_term} until:{end_d}' > tweet-count.txt")
        if os.stat("tweet-count.txt").st_size == 0:
            counter = 0
        else:
            links_df = pd.read_csv('tweet-count.txt', names=['link'])
            links = links.append(links_df)
            counter = links_df.size
        tweet_count.append(counter)

    df = pd.DataFrame({'Date': dates, 'Counts': tweet_count})
    df['Date'] = pd.to_datetime(df['Date']) 
    df['Search_Term'] = search_term
    return df


class TweetCountPlotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Tweet Count Plot")

        # Search term label and entry
        self.search_term_label = tk.Label(master, text="Search term:")
        self.search_term_label.pack()
        self.search_term_entry = tk.Entry(master)
        self.search_term_entry.pack()

        # Start date label and entry
        self.start_date_label = tk.Label(master, text="Start date (YYYY-MM-DD):")
        self.start_date_label.pack()
        self.start_date_entry = tk.Entry(master)
        self.start_date_entry.pack()

        # End date label and entry
        self.end_date_label = tk.Label(master, text="End date (YYYY-MM-DD):")
        self.end_date_label.pack()
        self.end_date_entry = tk.Entry(master)
        self.end_date_entry.pack()

        # Button to plot tweet counts
        self.plot_button = tk.Button(master, text="Plot", command=self.plot_tweet_counts)
        self.plot_button.pack()

        # Matplotlib figure and canvas
        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

    def plot_tweet_counts(self):
        # Get input values from entries
        search_term = self.search_term_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        # Call the tweet_count_plot function to get the tweet count data
        tweet_counts = tweet_count_plot(start_date, end_date, search_term)

        # Clear the previous plot
        self.fig.clear()

        # Plot the tweet count data using pandas
        tweet_counts.plot(x='Date', y='Counts', ax=self.fig.gca())

        # Refresh the canvas
        self.canvas.draw()


# Create the GUI window
root = tk.Tk()
my_gui = TweetCountPlotGUI(root)
root.mainloop()
