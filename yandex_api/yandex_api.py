
from typing import List
from yandex_music import Client, Playlist
from dataclasses import dataclass
from datetime import datetime
from calendar import month_abbr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


@dataclass
class TrackMainData:
    title: str
    artists: List[str]
    genre: str
    year: int
    content_warning: str
    duration_ms: int
    likes_count: int
    timestamp: str


# def func(pct, allvals):
#     absolute = int(pct/100.*np.sum(allvals))
#     return "{:.1f}%\n({:d} g)".format(pct, absolute)


    # print(tracks_df["genre"].value_counts().index)
    # print(tracks_df["genre"].value_counts().values)
    # print(sum(tracks_df["genre"].value_counts().values))
    # plt.hist(tracks_df["year"], bins=len(tracks_df["year"].unique()))
    # plt.hist(tracks_df["year"], bins=8)
    # plt.hist(tracks_df["year"])
    # plt.pie(tracks_df["genre"].value_counts().values,
    #         labels=tracks_df["genre"].value_counts().index,
    #         wedgeprops=dict(width=0.5),
    #         startangle=-40)

    # fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    # labels = tracks_df["genre"].value_counts().index
    # data = tracks_df["genre"].value_counts().values

    # # labels = tracks_df["artists"].explode().value_counts().index
    # # data = tracks_df["artists"].explode().value_counts().values

    # wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)

    # bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.1)
    # kw = dict(arrowprops=dict(arrowstyle="-"),
    #           bbox=bbox_props, zorder=0, va="center")

    # for i, p in enumerate(wedges):
    #     ang = (p.theta2 - p.theta1)/2. + p.theta1
    #     y = np.sin(np.deg2rad(ang))
    #     x = np.cos(np.deg2rad(ang))
    #     horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    #     connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    #     kw["arrowprops"].update({"connectionstyle": connectionstyle})
    #     ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
    #                 horizontalalignment=horizontalalignment, **kw)

    # ax.set_title("genre")

    # plt.show()
    # art = tracks_df["artists"].explode().value_counts()
    # gnr = tracks_df["genre"].value_counts()
    # yr = tracks_df["year"].value_counts()


def genre_stat(tracks_df: pd.DataFrame) -> None:
    plt.pie(tracks_df["genre"].value_counts().values,
            labels=np.array(tracks_df['genre'].value_counts().index) + [' ' + ''.join(item) + '%' for item in (np.array(tracks_df['genre'].value_counts().values) / tracks_df['genre'].size * 100).round(2).astype(str)],
            wedgeprops=dict(width=0.5),
            startangle=-40)
    plt.legend(ncol=2, bbox_to_anchor=(1.4, 1.15), borderaxespad=0)
    # plt.show()
    # plot whatever you need...
    # now, before saving to file:
    figure = plt.gcf() # get current figure
    figure.set_size_inches(30, 20)
    # when saving, specify the DPI
    plt.savefig("yandex-music-stat.png", dpi = 150)


def date_likes_count_heatmap(tracks_df: pd.DataFrame) -> None:
    likes_dates = tracks_df["timestamp"].to_numpy()
    for _ in range(len(likes_dates)):
        likes_dates[_] = "-".join(likes_dates[_].split('-')[0:2])
    dates, likes_count = np.unique(likes_dates, return_counts=True)
    likes_count_by_date = np.asarray((dates, likes_count)).T
    # plt.hist(likes_dates, bins=len(np.unique(likes_dates)), orientation="horizontal")
    # plt.show()
    likes_count_by_date_normalized = np.array([[f"{2019+y}-{m}" if m >= 10 else f"{2019+y}-0{m}", 0] for y in range(6) for m in range(1, 13)])
    for _ in range(len(likes_count_by_date_normalized)):
        for i in likes_count_by_date:
            if likes_count_by_date_normalized[_][0] == i[0]:
                likes_count_by_date_normalized[_] = i
    likes_count_norm_by_month = np.array([int(i[1]) for i in likes_count_by_date_normalized])
    likes_count_norm_by_month = likes_count_norm_by_month.reshape(6, 12)
    print(likes_count_by_date)
    print(likes_count_by_date_normalized)
    print(likes_count_norm_by_month)

    # Plot
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years = [f"{2019+year}" for year in range(6)]
    print(years)
    fig, ax = plt.subplots()
    im = ax.imshow(likes_count_norm_by_month)
    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(months)), labels=months)
    ax.set_yticks(np.arange(len(years)), labels=years)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(years)):
        for j in range(len(months)):
            text = ax.text(j, i, likes_count_norm_by_month[i, j],
                        ha="center", va="center", color="w")

    ax.set_title("Harvest of local farmers (in tons/year)")
    fig.tight_layout()
    plt.show()



def get_playlist_df(yandex_music_playlist_link: str) -> pd.DataFrame:
    ymc = Client().init()
    # https://music.yandex.ru/users/kirichrus98/playlists/3
    # playlist = ymc.users_playlists(user_id="kirichrus98", kind=3)
    playlist = ymc.users_playlists(user_id=yandex_music_playlist_link.split('/')[-3], kind=yandex_music_playlist_link.split('/')[-1])
    tracks: List[TrackMainData] = [TrackMainData(title=ts.track.title,
                                                 artists=[artist.name.replace('$', 'S') for artist in ts.track.artists],
                                                 genre=ts.track.albums[0].genre,
                                                 year=ts.track.albums[0].year,
                                                 content_warning=ts.track.content_warning,
                                                 duration_ms=ts.track.duration_ms,
                                                 likes_count=ts.track.albums[0].likes_count,
                                                 timestamp=ts.timestamp) for ts in playlist.tracks]
    tracks_df: pd.DataFrame = pd.DataFrame([track.__dict__ for track in tracks])
    # genre_stat(tracks_df)
    # date_likes_count_heatmap(tracks_df)
    # print(np.array([1, 2, 3, 4]) - 1)
    # print("done")
    return tracks_df


# genre_stat(get_playlist_df("https://music.yandex.ru/users/kirichrus98/playlists/3"))
