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
    with open(FILE_PUBMED, encoding="utf8") as f:
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
    total = 0
    for d in get_data():
        year.update({d.year})
        if d.year == 1980:
            total += 1
    for y in year.most_common():
        labels.append(y[0])
        values.append(y[1])
    zipped = zip(labels, values)
    zipped = sorted(zipped)
    zipped.reverse()
    labels, values = zip(*zipped)
    labels = list(labels)
    ind = range(len(labels))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.bar(ind, values, color=p.cerulean())
    plt.xticks(ind, labels, rotation=90)
    plt.ylabel("Number of publications")
    plt.xlabel("Year (till 11 March 2019)")
    plt.tight_layout()
    plt.savefig("year_wise.png", type="png", dpi=300)
    plt.show()


def journal_over_years():
    number_of_journals = 3
    p = palette.Palette(remove_white=True)
    year_data = defaultdict(Counter)
    for d in get_data():
        if 2019 > d.year > 1999:
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

        year_label.append(f"{y}")
        year_values.append(temp_values)
        year_journals.append(temp_name)

    zipped = zip(year_label, year_values, year_journals)
    zipped = sorted(zipped)
    year_label, year_values, year_journals = zip(*zipped)
    color_palette = []
    for f in p:
        color_palette.append(f)
    if len(color_palette) < len(global_color):
        color_palette.extend(p.random(no_of_colors=len(global_color), grade=40))

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
            y = 0.4 * patch.get_height() + point[1]
            # ax.text(x, y, f"{round(patch.get_width(), 1)}%", ha='center')

    legend_patches = []
    for key in colors:
        legend_patches.append(mpatches.Patch(color=colors[key], label=key))

    plt.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.xlabel("Percentage of all paper published in given year")
    plt.ylabel("Year")
    plt.savefig("year_top_journals.png", type="png", dpi=300)
    plt.show()


def author_per_year():
    p = palette.Palette()
    year = defaultdict(int)
    articles = defaultdict(int)
    labels = []
    values = []
    for d in get_data():
        if d.year > 1979:
            year[d.year] += len(d.authors)
            articles[d.year] += 1

    for y in year:
        labels.append(y)
        values.append(year[y] / articles[y])
    zipped = zip(labels, values)
    zipped = sorted(zipped)
    zipped.reverse()
    labels, values = zip(*zipped)
    labels = list(labels)
    ind = range(len(labels))
    plt.bar(ind, values, color=p.green())
    plt.xticks(ind, labels, rotation=90)
    plt.ylabel("Number of authors per article")
    plt.xlabel("Year (till 11 March 2019)")
    plt.tight_layout()
    plt.grid(axis='y', color="k", alpha=0.5, linestyle="--")
    plt.savefig("author_wise.png", type="png", dpi=300)
    plt.show()


def get_statistics():
    number_of_journals = 5
    data = get_data()
    journals = Counter()
    year = Counter()
    authors = 0
    for d in get_data():
        journals.update({d.journal})
        year.update({d.year})
        authors += len(d.authors)

    print("Total number of Papers : {0}\n--------------".format(len(data)))
    print(f"Total number of distinct journals : {len(journals)}\nTop {number_of_journals} journals")
    for j in journals.most_common(number_of_journals):
        print(j)
    print(f"-------------------\nTotal number of authors : {authors}")
    print(f"Authors per article : {authors / len(data)}")
    print(year[2018])


def budget_plot():
    p = palette.Palette()
    data = []
    with open(FILE_BUDGET_DATA) as f:
        for line in csv.reader(f):
            data.append(line[4:])

    ind = range(len(data[0]))
    plt.bar(ind, [round(float(x), 2) for x in data[2]], color=p.blue(), label="World")
    plt.bar(ind, [round(float(x), 2) for x in data[1]], color=p.orange(), label="India")
    plt.ylabel("% of GDP")
    plt.xlabel("Year")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
               ncol=2, fancybox=True, shadow=True)
    plt.xticks(ind, data[0], rotation=90)
    plt.show()


def run():
    get_statistics()
