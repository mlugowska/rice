# sourcery skip: simplify-fstring-formatting
import matplotlib.pyplot as plt

from birth_death.sfs.sfs_plot import plot_sfs
from birth_death.sfs.simulated_calculations import cumulative_simulated_sfs, simulated_sfs, \
    simulated_sfs_avg, cumulative_simulated_sfs_Durrett
from birth_death.sfs.theoretical_calculations import expected_sfs, cumulative_expected_sfs, expected_95_percentyl, \
    cumulative_expected_sfs_Lambert

# -------- SETUP PARAMETERS --------
# b = .041
b = .1
d = .01
# mu = .03
mu = .1
set_no = 'set 2'

# --------
n = 100
N = 700
p = n / N

# --------
# p = 5 * (10 ** (-7))
# N = n/p
r = b - d

# --------
# z = .999999
z = 1 - p * b / r

# -------- EXPECTED (THEORETICAL) SFS --------
ESn = expected_sfs(n=n, mu=mu, r=r, z=z)

# -------- EXPECTED CUMULATIVE SFS --------
EKn = cumulative_expected_sfs(n=n, ESn=ESn)

# -------- EXPECTED CUMULATIVE SFS (LAMBERT) --------
EKn_Lambert = cumulative_expected_sfs_Lambert(n=n, mu=mu, r=r, b=b, p=p)

# -------- EXPECTED CUMULATIVE SFS (DURRETT) --------
EKn_Durrett = cumulative_simulated_sfs_Durrett(n=n, mu=mu, r=r, N=N)

# -------- 95 percentyl Sn(k) --------
# Q_95 = expected_95_percentyl(n=n, ESn=ESn)

# -------- SIMULATED (REAL) SFS --------
Kn_sim = []
for rep in range(1, 11):
    Sn = simulated_sfs(n=n, rep=rep, set_no=set_no)
    Kn = cumulative_simulated_sfs(Sn=Sn, n=n)
    print(Kn[-1])
    # ----- if plot regular
    import numpy as np
    Sn = [np.nan if x == 0 else x for x in Sn]

    Kn_sim.append(Kn)
    # plot
    # plot_sfs(
    #     n=n,
    #     rep=f'{rep}',
    #     semilog=False,
    #     regular=True,
    #     bar=True,
    #     filename=f'birth_death/results/{set_no}/{rep}/1-sfs_partial_100_sfs_partial_100_cells-bar-Kn.png',
    #     ESn=ESn,
    #     Sn=Sn,
    #     EKn=EKn,
    #     Kn=Kn,
    # )

# ========= all Kn on one plot
rep = 1
for kn in Kn_sim:
    plt.plot(range(1, n), kn, label=f'$K_{"n"}$(m) {rep}', linewidth=0.5)
    rep += 1

plt.plot(range(1, n), EKn, 'k--', label='E[$K_{n}$(m)]', linewidth=0.75)
plt.ylim([0, 250])

plt.title('Kn for all 10 simulations + average')
plt.grid(visible=True)
plt.rcParams['axes.formatter.min_exponent'] = 2
plt.legend()
plt.show()
plt.savefig(f'birth_death/results/{set_no}/avg/Kn-all.png', dpi=300)

# ========= AVERAGE
Sn_all = simulated_sfs_avg(n=n, set_no=set_no)
Kn_all = cumulative_simulated_sfs(Sn=Sn_all, n=n)
# ----- if plot regular
import numpy as np
Sn_all = [np.nan if x == 0 else x for x in Sn_all]

# plot
plot_sfs(n=n, rep='average', semilog=False, regular=True, bar=True,
         filename=f'birth_death/results/{set_no}/avg/N-700-sfs_partial_100_sfs_partial_100_cells-bar-avg-Kn.png',
         ESn=ESn, Sn=Sn_all, EKn=EKn, Kn=Kn_all)
