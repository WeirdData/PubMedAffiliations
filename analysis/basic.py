import csv
from collections import Counter, defaultdict

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from SecretColors import palette

from constants import *
from models.objects import PubMedEntry


def get_data() -> list:
    all_entries = []
    with open(DATASET_FILE) as f:
        data = csv.reader(f)
        for line in data:
            if line[0] != "Title":  # Remove Header
                all_entries.append(PubMedEntry(line))
    return all_entries


def plot_year_wise_publications():
    p = palette.Palette()
    year = Counter()
    labels = []
    values = []
    for d in get_data():
        year.update({d.year})

    for y in year.most_common():
        labels.append(y[0])
        values.append(y[1])

    ind = range(len(labels))
    plt.bar(ind, values, color=p.cerulean())
    plt.xticks(ind, labels, rotation=90)
    plt.ylabel("Number of publications")
    plt.tight_layout()
    plt.savefig("year_wise.png", type="png", dpi=300)
    plt.show()


def journal_over_years():
    number_of_journals = 3
    p = palette.Palette()
    year_data = defaultdict(Counter)
    for d in get_data():
        year_data[d.year].update({d.journal})

    year_label = []
    year_values = []
    year_journals = []
    global_color = defaultdict(list)

    for y in year_data:
        total = 0
        current_year = []
        for t in year_data[y].most_common():
            total += t[1]
            if len(current_year) < number_of_journals:
                current_year.append(t)

        temp_values = []
        temp_name = []
        for c in current_year:
            temp_values.append(c[1] * 100 / total)
            temp_name.append(c[0])
            global_color[c[0]].append(1)

        year_label.append(f"{y}\n({total})")
        year_values.append(temp_values)
        year_journals.append(temp_name)

    color_palette = p.random(no_of_colors=len(global_color), grade=40)
    colors = {}
    for g in global_color:
        colors[g] = color_palette[0]
        color_palette.pop(0)
    ind = range(len(year_label))
    year_values = np.asanyarray(year_values).T
    year_journals = np.asanyarray(year_journals).T
    fig = plt.figure()
    ax = fig.add_subplot(111)

    bar_patch = []
    left_margin = np.zeros(len(year_label))
    for i, v in enumerate(year_values):
        c = []
        for journal in year_journals[i]:
            c.append(colors[journal])
        bar_patch.append(ax.barh(ind, v, left=left_margin, color=c))
        left_margin += v

    plt.yticks(ind, year_label)

    for j in range(len(bar_patch)):
        for i, patch in enumerate(bar_patch[j].get_children()):
            point = patch.get_xy()
            x = 0.5 * patch.get_width() + point[0]
            y = 0.5 * patch.get_height() + point[1]
            ax.text(x, y, f"{patch.get_width()}%", ha='center')

    legend_patches = []
    for key in colors:
        legend_patches.append(mpatches.Patch(color=colors[key], label=key))

    plt.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.xlabel("Percentage of all paper published in given year")
    plt.ylabel("Year (total no of papers published)")
    plt.savefig("year_top_journals.png", type="png", dpi=300)
    plt.show()


def get_statistics():
    number_of_journals = 5
    data = get_data()
    journals = Counter()
    year = Counter()
    for d in get_data():
        journals.update({d.journal})
        year.update({d.year})

    print("Total number of Papers : {0}\n--------------".format(len(data)))
    print(f"Total number of distinct journals : {len(journals)}\nTop {number_of_journals} journals")
    for j in journals.most_common(number_of_journals):
        print(j)


def run():
    journal_over_years()
