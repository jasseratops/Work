import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

import math
import time

# Initalize script constants

ymin = -1.1
ymax = 1.1

linesPerPlot = 3

samplesPerFrame = 4
framesPerSecond = 30
secondsPerPlot = 4

# Calculate dependent constants
samplesPerSecond = samplesPerFrame * framesPerSecond
samplesPerPlot = samplesPerSecond * secondsPerPlot
secondsPerSample = 1.0 / samplesPerSecond
millisPerFrame = 1000.0 / framesPerSecond


# Define core functions

def makeLine(ax, maxt, dt, ymin, ymax, color):
    """Make an empty Line2D for the initial chart."""
    nvalues = int(round(maxt / dt))

    tdata = [dt * tm for tm in range(nvalues)]
    ydata = [0 for tm in range(nvalues)]

    line = Line2D(tdata, ydata, color=color)
    ax.add_line(line)
    ax.set_ylim(ymin, ymax)

    return line


def makeChart(ax, maxt, dt, linesPerPlot, ymin, ymax):
    """Make a chart and return a list of the lines it contains."""
    colors = ['r', 'b', 'g', 'k']

    # Make the lines and store in a list.
    lines = []
    for iline in range(0, linesPerPlot):
        lines.append(makeLine(ax, maxt, dt, ymin, ymax, colors[iline % len(colors)]))

    ax.set_xlim(0, maxt)

    return lines


def initDisplay(lines):
    """Init display."""
    return lines


def updateLine(line, ys):
    """Update the data in one line, popping off the last value."""
    tdata, ydata = line.get_data()
    for y in ys:
        ydata.append(y)
        ydata.pop(0)
    line.set_data(tdata, ydata)

    return line


def updateLines(lines, arrays):
    """Update individual lines and return a sequence of artists to the animator."""
    artists = []
    for iline in range(len(lines)):
        artists.append(updateLine(lines[iline], arrays[iline]))

    return artists


def emitData(linesPerPlot, samplesPerFrame):
    """Create the data that will be plotted."""
    nsample = 0
    while True:
        samples = [[] for i in range(linesPerPlot)]
        for isample in range(samplesPerFrame):
            nsample = nsample + 1
            for iline in range(linesPerPlot):
                pi_increment = (math.pi / (10.0 * (iline + 1)))
                samples[iline].append(math.sin(nsample * pi_increment))

        yield samples


# Make chart.
fig, ax = plt.subplots()
lines = makeChart(ax, secondsPerPlot, secondsPerSample, linesPerPlot, ymin, ymax)

# Start the animator.
update = lambda samples: updateLines(lines, samples)
emitter = lambda: emitData(linesPerPlot, samplesPerFrame)
init = lambda: initDisplay(lines)

ani = animation.FuncAnimation(fig, update, emitter, init_func=init, interval=millisPerFrame, blit=True)

plt.show()