from typing import List

from matplotlib import pyplot as plt


def make_plot(semilog: bool, regular: bool, x: range, y: List[float or int], linetype: str, label: str,
              linewidth: float) -> None:
    if semilog:
        plt.semilogy(x, y, linetype, label=label, linewidth=linewidth)
    elif regular:
        plt.plot(x, y, linetype, label=label, linewidth=linewidth)


def plot_sfs(n: int, rep: str, filename: str, semilog: bool = True, bar: bool = False, regular: bool = False,
             ESn: List[int] = None, Sn: List[int] = None, Q_95: List[int] = None, EKn: List[int] = None,
             Kn: List[int] = None):
    x = range(1, n)

    if ESn:
        make_plot(semilog=semilog, regular=regular, x=x, y=ESn, linetype='k-', label='E[$S_{n}$(k)]', linewidth=0.75)

    if Sn:
        if semilog and bar or regular and bar:
            plt.bar(range(1, n), Sn, color='#264b96', label='$S_{n}$(k)')
        elif semilog:
            plt.semilogy(x, Sn, 'k^', marker='o', fillstyle='none', label='$S_{n}$(k)')
        elif regular:
            plt.plot(range(1, n), Sn, 'k^', marker='o', fillstyle='none', label='$S_{n}$(k)')

    if Q_95:
        make_plot(semilog=semilog, regular=regular, x=x, y=Q_95, linetype='k--', label='$Q_{95}$(k)', linewidth=0.5)

    if EKn:
        make_plot(semilog=semilog, regular=regular, x=x, y=EKn, linetype='k--', label='E[$K_{n}$(m)]', linewidth=0.5)

    if Kn:
        make_plot(semilog=semilog, regular=regular, x=x, y=Kn, linetype='k:', label='$K_{n}$(m)', linewidth=0.5)

    # ---- plot style
    if semilog:
        plt.ylabel('log($S_{n}$(k))')
    else:
        plt.ylabel('$S_{n}$(k)')
    plt.xlabel('k')
    plt.title(f'Simulation {rep}')
    plt.grid(visible=True)
    plt.rcParams['axes.formatter.min_exponent'] = 2
    plt.legend()

    plt.savefig(filename, dpi=300)
    plt.clf()
    plt.close()
