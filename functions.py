# -*- coding: utf-8 -*-
"""
Inventory Problem

This file contains the implementation of the InventorySystemBase, InventorySystemInfinite,
and InventorySystemFinite classes.

Author: Ghazaleh Khalili (@gkhalili)
Created: 2022
"""

import numpy as np
from scipy import stats

class InventorySystemBase:
    """
    Base inventory system class with shared functions.

    Methods:
        __init__(S, D, h, e, c, lambda_): Initialize the inventory system.
        C(s, a): Cost function.
    """

    def __init__(self, S, D, h, e, c, lambda_):
        """
        Initialize the inventory system.

        Args:
            S (list): List of possible states.
            D (list): List of possible demand values.
            h (float): Holding cost per unit.
            e (float): Penalty cost per unit shortage.
            c (float): Cost per unit order.
            lambda_ (float): Poisson distribution parameter lambda_bda.
        """
        self.S = S
        self.D = D
        self.h = h
        self.e = e
        self.c = c
        self.lambda_ = lambda_

    def C(self, s, a):
        """
        Cost function.

        Args:
            s (int): Current state.
            a (int): Action.

        Returns:
            float: Cost of taking action a in state s.
        """
        d = np.array(self.D)
        prob = stats.poisson.pmf(d, self.lambda_)
        holding_cost = np.sum(np.maximum(s + a - d, 0) * prob)
        penalty_cost = np.sum(np.maximum(d - s - a, 0) * prob)
        return -self.h * holding_cost - self.e * penalty_cost - self.c * a


class InventorySystemInfinite(InventorySystemBase):
    """
    An inventory system class for infinite-horizon problems using value iteration.

    Methods:
        __init__(S, D, h, e, c, lambda_): Initialize the inventory system.
        P(s_next, s, a): Transition probability function.
        value_iteration(): Value iteration algorithm.
    """

    def P(self, s_next, s, a):
        """
        Transition probability function.

        Args:
            s_next (int): Next state.
            s (int): Current state.
            a (int): Action.

        Returns:
            float: Transition probability from state s to s_next given action a.
        """
        if s_next > 0 and s_next <= s + a:
            d = s + a - s_next
            return stats.poisson.pmf(d, self.lambda_)
        elif s_next == 0:
            d = s + a
            cdf_upper = stats.poisson.cdf(self.D[-1], self.lambda_)
            cdf_lower = stats.poisson.cdf(d - 1, self.lambda_) if d > 0 else 0
            return cdf_upper - cdf_lower
        else:
            return 0

    def value_iteration(self):
        """
        Value iteration algorithm for infinite-horizon problems.

        Returns:
            dict: Dictionary mapping each state to its corresponding value function.
            dict: Dictionary mapping each state to its corresponding optimal action.
            float: Optimal cost.
        """
        V = {s: 0 for s in self.S}
        optimal_policy = {s: 0 for s in self.S}
        epsilon = 1e-1
        i = 0
        while i < 100:
            i += 1
            print('\n i =', i)
            oldV = V.copy()
            for s in self.S:
                Q = {}
                A = np.arange(max(self.S) - s + 1)
                for a in A:
                    Q[a] = self.C(s, a) + sum(self.P(s_next, s, a) * oldV[s_next] for s_next in self.S)
                V[s] = max(Q.values())
                optimal_policy[s] = max(Q, key=Q.get)
            if all(np.linalg.norm(oldV[s] - V[s]) < epsilon for s in self.S) or i == 100:
                optimal_cost = -sum(V.values()) / len(V)
                break
        return V, optimal_policy, optimal_cost


class InventorySystemFinite(InventorySystemBase):
    """
    An inventory system class for finite-horizon problems using backward dynamic programming.

    Methods:
        __init__(S, D, h, e, c, lambda_): Initialize the inventory system.
        backward_DP(T): Backward dynamic programming algorithm.
    """

    def backward_DP(self, T):
        """
        Backward dynamic programming algorithm for finite-horizon problems.

        Args:
            T (int): Time horizon.

        Returns:
            dict: Dictionary mapping each state and time to its corresponding value function.
            dict: Dictionary mapping each state and time to its corresponding optimal action.
            float: Optimal cost.
        """
        big_M = 1e+6
        #step 0:
        V = {(t,s): 0 for t in range(T+1) for s in self.S}
        optimal_policy = {(t,s): 0 for t in range(T+1) for s in self.S}
        N = max(self.S) #the maximum possible state
        t = T
        #step 1a:
        while t:       
            print('\n t =', t)
            t -= 1
            #step 2a:
            for s in self.S:
                #step 2b:
                V[t,s] = - big_M
                #step 4a:
                Q = {}
                #step 3a:
                A = np.arange(N - s + 1)
                for a in A:
                    #step 4b:
                    Q[a] = self.C(s, a)
                    #step 4c:
                    for d in self.D:
                        s_next = max(0, s + a - d)
                        Q[a] += stats.poisson.pmf(d, self.lambda_) * V[t+1,s_next]
                    
                    #step 4c:
                    if Q[a] > V[t,s]:
                        #step 3b:
                        V[t,s] = max(Q.values()) 
                        #step 3c:
                        optimal_policy[t,s] = max(Q, key=Q.get) 
        return V, optimal_policy
