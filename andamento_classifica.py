import argparse
import pandas as pd
import math
import matplotlib.pyplot as plt

from Giornata import Giornata
from Calendario import Calendario

# gestisce parametri da linea di comando
def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0 or ivalue > 38:
        raise argparse.ArgumentTypeError("%s non è una giornata valida" % value)
    return ivalue

parser = argparse.ArgumentParser(
    description='Genera immagini dell\'andamento della classifica del fantacalcio')
parser.add_argument('file', help='Il nome del file excel del calendario della competizione')
parser.add_argument('-q', help='Non mostrare immagine', action='store_true')
parser.add_argument('-f1', help='Genera anche immagine classifica Formula 1', action='store_true')
parser.add_argument(
    '-asta',
    help='Specifica la prima giornata successiva all\'asta di riparazione',
    type=check_positive)
parser.add_argument(
    '-until',
    help='Specifica fino a che giornata plottare la classifica',
    type=check_positive)
args = parser.parse_args()
# importa file excel come dataframe
df = pd.read_excel(args.file,
                   header=None,
                   usecols='A:E,G:K',
                   skiprows=[0,1,2,3])

# calcola numero di squadre
N = None # numero di partite ad ogni giornata
i = 0
while (N is None):
    if ('Giornata lega' in df.iloc[i,0]):
        N = i
    i += 1
num_squadre = N*2

# genera lista di Giornate
giornate = []
for row in range(0, df.shape[0], N+1):
    for col in [0, 5]:
        g = df.iloc[row:row+N, col:col+5]
        if (isinstance(g.iloc[0,-1], float)):
            if (math.isnan(g.iloc[0,-1])): break
        if (g.iloc[0,-1] == '-'): break
        giornate.append(Giornata(g))

# genera Calendario
calendario = Calendario(giornate)
team_points = calendario.get_team_points_map()
# print(calendario.get_team_points_map())

# plot punti competizione a calendario
colors = ['#808080', 'b', 'g', 'r', 'c', 'm', 'y', 'k']
markers = ['.', 's', '*', 'o', 'v', 'H', 'p', 'd']
try:
    split = args.file.split('_')[1:]
    title = '_'.join(split)
    title = title[:-5]
except:
    title = ''

legend = []
max_point = 0
days = len(team_points[list(team_points.keys())[0]])
plot_days = args.until if args.until else days
fig = plt.figure(figsize=(6 + 0.2*plot_days , 4 + 0.1*plot_days))
for idx, team in enumerate(team_points):
    if max(team_points[team]) > max_point:
        max_point = max(team_points[team])
    xs = list(range(plot_days))
    plt.plot(xs, team_points[team][:plot_days], color=colors[idx], marker=markers[idx])
    plt.text(plot_days-0.95, team_points[team][plot_days-1], str(team_points[team][plot_days-1]))
    legend += [team]
plt.legend(legend, loc='upper left')
plt.title(title)
plt.xlabel('Giornate')
plt.ylabel('Punti in classifica')
plt.xticks(xs)
if (args.asta):
    plt.vlines(args.asta - 1, 0, max_point, linestyles='dashed')
    plt.annotate('Asta', (args.asta - 1.1, max_point-1), ha='right')
if (not args.q): plt.show()
fig.savefig('Giornata' + str(plot_days-1) + '.png') # salva immagine

# genera immagine classifica formula 1
if (args.f1):
    team_f1points = calendario.get_team_f1points_map()
    fig = plt.gcf()
    legend = []
    max_point = 0
    days = len(team_f1points[list(team_f1points.keys())[0]])
    plot_days = args.until if args.until else days
    fig = plt.figure(figsize=(6 + 0.2*plot_days , 4 + 0.1*plot_days))
    for idx, team in enumerate(team_f1points):
        if max(team_f1points[team]) > max_point:
            max_point = max(team_f1points[team])
        xs = list(range(plot_days))
        plt.plot(xs, team_f1points[team], color=colors[idx], marker=markers[idx])
        plt.text(plot_days-0.95, team_f1points[team][plot_days-1], str(team_f1points[team][plot_days-1]))
        legend += [team]
    plt.legend(legend, loc='upper left')
    plt.title(f'{title} Formula 1')
    plt.xlabel('Giornate')
    plt.ylabel('Punti in classifica')
    plt.xticks(xs)
    if (args.asta):
        plt.vlines(args.asta - 1, 0, max_point, linestyles='dashed')
        plt.annotate('Asta', (args.asta - 1.1, max_point-1), ha='right')
    if (not args.q): plt.show()
    fig.savefig('Giornata' + str(plot_days-1) + '_Formula1.png') # salva immagine
