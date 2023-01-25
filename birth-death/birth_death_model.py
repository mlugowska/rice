import numpy as np

import pandas as pd


class BirthDeath:
    def __init__(self, b: float, d: float, N0: int) -> None:
        """
        initialize the population

        :param b: float, birth rate per individual
        :param d: float, death rate per individual
        :param N0: int, initial population size
        """
        self.b = b
        self.d = d
        self.N = N0  # current population size / number of individuals / number of cells
        self.t = 0.  # time since beginning of simulation
        self.N_history = [N0]  # list to record history of number of individuals
        self.t_history = [0.]  # list to record time of all events
        self.c = []  # list to record cells where the event occurs
        self.events = []
        self.t_events = []
        self.is_extinct = self.extinct()

    def analytic(self, dt: np.ndarray):
        return self.N * np.exp((self.b - self.d) * dt)

    def next_event(self):
        """
        generate the expected waiting time and identity of the next event

        :param:
        T: float, simulation time horizon

        :return:
        t: float, waiting time before next event (birth or death)
        event: int, 0 means birth and 1 means death
        """
        b_rate = self.N * self.b  # total birth rate
        d_rate = self.N * self.d  # total death rate

        """
        Method 1. to determine next event type

        # scale param: is an inverse of rate (odwrotność współczynnika)
        t_b = np.random.exponential(
            scale=1 / b_rate)  # draw a random number from exponential dist as expected birth time
        t_d = np.random.exponential(
            scale=1 / d_rate)  # draw a random number from exponential dist as expected death time

        if t_b < t_d:  # birth happens first
            event = 0  # 0 to label birth
            return t_b, event
        event = 1  # death happens first, 1 to label death
        return t_d, event

        """
        # """
        # Method 2. to determine next event type

        rate = b_rate + d_rate  # parameter (birth + death)

        t = np.random.exponential(scale=1 / rate)  # t ~ exp(birth + death)

        u = np.random.default_rng().uniform(0, 1)  # random number from uniform dist
        c_i = int(np.ceil(self.N * u))  # cell where the event occures

        if (u * rate) <= b_rate:
            event = 0
            return t, event, c_i
        event = 1
        return t, event, c_i
        # """

    def run(self, T: float) -> None:
        """
        Simulation of continuous-time birth-and-death processes at birth and death event times

        :param T: float, simulation time. All events up to and including this time are
        included in the output.
        """

        while True:
            # self.t < T:
            if self.N == 0:  # population is extinct
                break

            t_i, event, c_i = self.next_event()  # draw next even
            self.t += t_i  # update current time

            if self.t > T:  # next event occurs after simulation time
                break

            if event == 0:  # birth happens
                self.N += 1  # increase population size by 1
            elif event == 1:  # death happens
                self.N -= 1  # decrease population size by 1

            self.t_history.append(self.t)  # record time of event
            self.t_events.append(t_i)  # record time point of event (dt(i))
            self.N_history.append(self.N)  # record population size after event
            self.c.append(c_i)
            self.events.append(event)

    def count_N_in_timestep(self, df: pd.DataFrame, k_i: int, m_dt: np.ndarray) -> pd.DataFrame:
        """

        :param k_i: int, number of simulations
        :param df: DataFrame
        :param m_dt: array of times; time sampling from 0 to T with step 0.05
        :return: df
        """

        for m in m_dt:
            for index, t_i in enumerate(self.t_history):
                if index < len(self.t_history) - 1:
                    if t_i <= m < self.t_history[index + 1]:
                        df.at[k_i, m] = self.N_history[index]
        return df

    def extinct(self):
        return True if self.N == 0 else False