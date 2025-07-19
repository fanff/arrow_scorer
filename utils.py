from matplotlib import gridspec, pyplot as plt
import numpy as np
import pandas as pd
from models import Session


def arrow_score_df(s: Session):
    all_scores = []
    for i, arrow_set in enumerate(s.sets, start=1):
        all_scores.append([a.score for a in arrow_set.arrows])

    columns = [f"{i+1}" for i in range(s.arrows_per_set)]
    index = [i + 1 for i in range(len(all_scores))]
    df = pd.DataFrame(all_scores, columns=columns, index=index)

    # sum all scores of each row
    df["Set"] = df.sum(axis=1)

    # partial sum of the "Set" column
    df["Total"] = df["Set"].cumsum()
    return df


def draw_target(ax):
    """
    Draws a standard archery target on the provided Axes.
    """
    rings = [(1.0, "blue"), (0.8, "red"), (0.6, "red"), (0.4, "gold"), (0.2, "gold")]

    for radius, color in rings:
        # Filled circle
        circle = plt.Circle((0, 0), radius, color=color, fill=True)
        ax.add_artist(circle)
        # Black outline
        outline = plt.Circle((0, 0), radius, color="black", fill=False)
        ax.add_artist(outline)


def gaussian_pdf(x, mu, sigma):
    return (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def plot_pos(arrows):
    xs = np.array([a.x / 5.0 for a in arrows])
    ys = np.array([a.y / 5.0 for a in arrows])

    fig = plt.figure(figsize=(6, 6))
    gs = gridspec.GridSpec(
        2, 2, width_ratios=[1, 4], height_ratios=[1, 4], wspace=0.05, hspace=0.05
    )

    ax_histx = fig.add_subplot(gs[0, 1])
    ax_histy = fig.add_subplot(gs[1, 0])
    ax_main = fig.add_subplot(gs[1, 1])

    # Hide spines and ticks from histograms
    for ax in [ax_histx, ax_histy]:
        ax.tick_params(direction="in", top=True, right=True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # Plot main target with arrows
    ax_main.set_aspect("equal")
    ax_main.set_xlim(-1.1, 1.1)
    ax_main.set_ylim(-1.1, 1.1)
    fig.patch.set_facecolor("none")
    ax_main.set_facecolor("none")
    draw_target(ax_main)
    ax_main.scatter(xs, ys, c="black", s=30)
    ax_main.axis("off")

    # Histogram for X (top)
    ax_histx.hist(xs, bins=30, density=True, alpha=0.5, color="gray")
    mu_x, std_x = np.mean(xs), np.std(xs)
    x_vals = np.linspace(-1.1, 1.1, 200)
    ax_histx.plot(x_vals, gaussian_pdf(x_vals, mu_x, std_x), "r--")

    ax_histx.set_xlim(-1.1, 1.1)
    ax_histx.axis("off")

    # Histogram for Y (right, reversed)
    ax_histy.hist(
        ys, bins=30, density=True, orientation="horizontal", alpha=0.5, color="gray"
    )
    mu_y, std_y = np.mean(ys), np.std(ys)
    y_vals = np.linspace(-1.1, 1.1, 200)
    ax_histy.plot(gaussian_pdf(y_vals, mu_y, std_y), y_vals, "r--")

    ax_histy.set_ylim(-1.1, 1.1)
    ax_histy.yaxis.tick_right()  # Move Y-axis ticks to the right
    ax_histy.yaxis.set_label_position("right")  # Move Y-axis labels to the right
    ax_histy.invert_xaxis()  # Reverse the Y-axis direction
    ax_histy.axis("off")

    return fig, mu_x, std_x, mu_y, std_y


def pos_to_score_range(mu):
    """Convert a position to a score range.
    assumes mu is in the range [-1,1]
    """
    # Each ring is 0.2 wide, center is 10, edge is 1
    abs_mu = abs(mu)
    lower_ring = max(1, 11 - (abs_mu / 0.2))
    upper_ring = max(1, 11 - (abs_mu / 0.2) + 1)
    if lower_ring == upper_ring:
        return f"{upper_ring}"
    return lower_ring
