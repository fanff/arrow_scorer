

from matplotlib import pyplot as plt
import pandas as pd
from models import Session


def arrow_score_df(s:Session):
    all_scores = []
    for i, arrow_set in enumerate(s.sets, start=1):
        all_scores.append([a.score for a in arrow_set.arrows])

    columns=[f"Arrow {i+1}" for i in range(s.arrows_per_set)]
    index = [i+1 for i in range(len(all_scores))]
    df = pd.DataFrame(all_scores, columns=columns
                    , index=index )

    # sum all scores of each row
    df["Set"] = df.sum(axis=1)

    # partial sum of the "Set" column
    df["Total"] = df["Set"].cumsum()
    return df


def plot_pos(arrows):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_title("Arrow Impact Points")

    xs = [a.x for a in arrows]
    ys = [a.y for a in arrows]
    scores = [a.score for a in arrows]

    scatter = ax.scatter(xs, ys, c=scores, cmap='viridis', s=100, edgecolor='black')
    plt.colorbar(scatter, label="Score")
    return fig