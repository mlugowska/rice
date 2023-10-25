from typing import List

from scipy.special import hyp2f1


def expected_sfs(n: int, mu: float, r: float, z: float) -> List[int]:
    ESn = []
    for k in range(1, n):
        ESn_k = (mu / r) * (((n - k - 1) / (k * (k + 1))) * hyp2f1(1, 2, k + 2, z) + (2 / k) * hyp2f1(1, 1, k + 1, z))
        ESn.append(ESn_k)
    return ESn


def cumulative_expected_sfs(n: int, ESn: List[int]) -> List[int]: # E[Kn(n)]
    return [sum(ESn[:k + 1]) for k in range(n - 1)]


def cumulative_expected_sfs_Lambert(n: int, mu: float, r: float, b: float, p: float): # E[Kn(n)]
    return [mu * k * r / b / p for k in range(1, n)]


def expected_95_percentyl(n: int, ESn: List[int]) -> List[float]:
    K = sum(ESn)
    return [
        ESn[k] + 1.645 * ((ESn[k] * (1 - (ESn[k] / K))) ** (1 / 2))
        for k in range(n - 1)
    ]
