import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from model import Slot, Plano
sns.set_theme()
sns.set_style("white")


def slots_to_data_frame(segments: list[Slot]) -> pd.DataFrame:
    if segments[0].start.month == segments[-1].end.month:
        date_format = "%d."
    else:
        date_format = "%m.%d."

    data = [
        [s.start.strftime(date_format),
         s.start.strftime("%H:%M"),
         s.participants]
        for s in segments]

    df = pd.DataFrame(data, columns=["date", "time", "participants"])
    df = df.pivot("time", "date", "participants")
    return df


def create_heatmap(segments: list[Slot], size=(5, 6), background="#fff"):
    width = size[0]
    height = size[1]
    # "canvas padding"
    padding = .07
    date_offset = .25 - .01
    time_offset = .55 - .01

    # converting list to heatmap friendly format
    df = slots_to_data_frame(segments)
    # setting "canvas" size and background
    plt.figure(figsize=(width, height), facecolor=background)

    # adding heatmap figure
    ax = sns.heatmap(df, cbar=False,)
    # removing graph background
    ax.set_facecolor("#0000")
    # removing axes labels
    plt.xlabel("")
    plt.ylabel("")
    # adjusting padding
    plt.subplots_adjust(
        left=(padding+time_offset)/width,
        right=1-padding/width,
        top=1-padding/height,
        bottom=(padding+date_offset)/height)
    return plt


if __name__ == "__main__":
    from test_models import TestPlanoModel
    from datetime import datetime

    Plano.data = TestPlanoModel.mocked_data
    start = time.time()
    plot = create_heatmap(Plano.occupancy(datetime.now(), datetime.now(), 123)[:4*7*7])
    plot.show()
    print((time.time() - start) * 1000)
