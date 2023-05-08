import random

import numpy as np
import pandas as pd


class BirthDeath:
    def __init__(self, b: float, d: float, N0: int, mu: float = None) -> None:
        """
        initialize the population

        :param b: float, birth rate per individual
        :param d: float, death rate per individual
        :param mu: float, mutation rate per individual
        :param N0: int, initial population size
        """
        self.b = b
        self.d = d
        self.mu = mu
        self.N = N0  # current population size / number of individuals / number of cells
        self.t = 0.  # time since beginning of simulation
        self.N_history = [N0]  # list to record history of number of individuals
        self.t_history = [0.]  # list to record time of all events
        self.c = []  # list to record cells where the event occurs
        self.events = []
        self.t_events = []
        self.is_extinct = self.extinct()

        # check for valid parameter values
        assert self.N > 0, "Population size must be greater than zero"
        assert self.b >= 0 and self.d >= 0, "Birth and death rates must be non-negative"

        if self.mu is not None:
            assert self.mu >= 0, "Mutation rate must be non-negative"

    def compute_analytic_solution(self, dt: np.ndarray) -> np.ndarray:
        """
        Compute the analytic solution for the population size.

        :param dt: np.ndarray, time intervals for computing the solution
        :return: np.ndarray, the analytic solution for the population size
        """
        if not isinstance(dt, np.ndarray):
            raise TypeError("dt must be an np.ndarray")
        return self.N * np.exp((self.b - self.d) * dt)

    def next_event(self, clone_1, clone_2):
        """
        generate the expected waiting time and identity of the next event

        :param:
        T: float, simulation time horizon

        :return:
        t: float, waiting time before next event (birth, death or mutation)
        event: int, 0 means birth, 1 means death, and 2 means mutation
        """

        random.seed(10)
        # --------- get clone data
        if clone_1:
            N_1, b_1, d_1 = clone_1.get('N'), clone_1.get('b'), clone_1.get('d')
            lambda_1 = N_1 * (b_1 + d_1 + self.mu)
        else:
            N_1, b_1, d_1, lambda_1 = 0, 0, 0, 0

        if clone_2:
            N_2, b_2, d_2 = clone_2.get('N'), clone_2.get('b'), clone_2.get('d')
            lambda_2 = N_2 * (b_2 + d_2 + self.mu)
        else:
            N_2, b_2, d_2, lambda_2 = 0, 0, 0, 0

        N_0 = self.N - N_1 - N_2
        lambda_0 = N_0 * (self.b + self.d + self.mu)

        # --------- probability of the next event for each clone
        p_0 = lambda_0 / (lambda_0 + lambda_1 + lambda_2)
        p_1 = lambda_1 / (lambda_0 + lambda_1 + lambda_2)
        p_2 = lambda_2 / (lambda_0 + lambda_1 + lambda_2)

        # --------- choose clone for the next event
        u_clone = np.random.uniform(0, 1)  # random number from uniform dist

        if u_clone <= p_0:
            clone = 0
            N_i = N_0
        elif u_clone <= (p_0 + p_1):
            clone = 1
            N_i = N_1
        elif u_clone <= 1:
            clone = 2
            N_i = N_2

        # --------- time to next event
        b_rate = (N_0 * self.b) + (N_1 * b_1) + (N_2 * b_2)  # total birth rate
        d_rate = (N_0 * self.d) + (N_1 * d_1) + (N_2 * d_2)  # total death rate

        if self.mu:
            mu_rate = self.N * self.mu  # total mutation rate
            rate = b_rate + d_rate + mu_rate  # parameter N(b + d + mu)
        else:
            rate = b_rate + d_rate

        t = np.random.exponential(scale=1 / rate)  # t ~ exp(N(b + d + mu)) lub t ~ exp(N(b + d))

        # --------- choose cell with the event
        u_c = np.random.uniform(0, 1)  # random number from uniform dist
        c_i = int(np.ceil(N_i * u_c))  # cell where the event occures

        # --------- determine the next event type
        u_event = np.random.uniform(0, 1)  # random number from uniform dist
        if self.mu:
            event = 2 if u_event * rate <= mu_rate else 0 if u_event * rate <= (b_rate + mu_rate) else 1
        else:
            event = 0 if u_event * rate <= b_rate else 1
        return t, event, c_i, clone

    def count_N_in_timestep(self, df: pd.DataFrame, k_i: int, m_dt: np.ndarray) -> pd.DataFrame:
        """

        :param k_i: int, number of simulations
        :param df: DataFrame
        :param m_dt: array of times; time sampling from 0 to T with step 0.05
        :return: df
        """

        for m in m_dt:
            for index, t_i in enumerate(self.t_history):
                if (
                        index < len(self.t_history) - 1
                        and t_i <= m < self.t_history[index + 1]
                ):
                    df.at[k_i, m] = self.N_history[index]
            if m > self.t_history[-1]:
                df.at[k_i, m] = self.N
        return df

    def extinct(self):
        return self.N == 0
