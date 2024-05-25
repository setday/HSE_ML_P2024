import matplotlib.pyplot


def main():
    dpi = 96
    win_width = 800
    win_height = 400

    figure = matplotlib.pyplot.figure(figsize=(win_width / dpi, win_height / dpi))
    axes = figure.add_axes((0.1, 0.15, 0.8, 0.7))
    axes.spines[["top", "bottom", "left", "right"]].set_visible(True)

    f = open("plot.txt", "r")
    x = []
    y_m = []
    y_a = []
    for line in f:
        a, b, c = line.split()
        x.append(float(a))
        y_m.append(float(b))
        y_a.append(float(c))

    axes.plot(x, y_m)
    axes.plot(x, y_a)

    axes.grid(which="minor", alpha=0.35)
    axes.grid(which="major", alpha=0.7)
    matplotlib.pyplot.show()


if __name__ == "__main__":
    main()
