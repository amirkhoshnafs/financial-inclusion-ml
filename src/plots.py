import matplotlib.pyplot as plt


def pct_labels(values):
    return [f'{100 * x:.1f}%' for x in values]


def save_rate_bar(
    df,
    group_col,
    rate_col,
    out_path,
    title,
    xlabel='Account ownership rate',
    ylabel='',
    horizontal=True,
):
    plot_df=df.copy()
    plot_df=plot_df.dropna(subset=[group_col, rate_col])

    fig, ax=plt.subplots(figsize=(8,5))

    if horizontal:
        ax.barh(plot_df[group_col].astype(str), plot_df[rate_col])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(0,1)

        for i, value in enumerate(plot_df[rate_col]):
            ax.text(value + 0.01, i, f'{100 * value:.1f}%', va='center')
    else:
        ax.bar(plot_df[group_col].astype(str), plot_df[rate_col])
        ax.set_ylabel(xlabel)
        ax.set_xlabel(ylabel)
        ax.set_ylim(0,1)

        for i, value in enumerate(plot_df[rate_col]):
            ax.text(i, value + 0.01, f'{100 * value:.1f}%', ha='center')

        ax.tick_params(axis='x', rotation=30)

    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160, bbox_inches='tight')
    plt.close(fig)