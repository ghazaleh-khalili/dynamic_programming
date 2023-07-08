"""
Inventory Problem

This file contains the execution code for solving the Bellman's equation for an inventory problem
using value iteration for the infinite-horizon problem
and backward dynamic programming for the finite-horizon problem.
Demand is assumed to follow Poission distribution.

Author: Ghazaleh Khalili (@gkhalili)
Created: 2022
"""

import functions
import numpy as np

"""
Define the problem parameters:
S: List of possible states.
D: List of possible demand values.
h: Holding cost per unit.
e: Penalty cost per unit shortage.
c: Cost per unit order.
lambda_: Mean (and parameter lambda) of the Poisson distribution.
T: planning horizon (finite)
"""

h = 1
c = 1
e = 2

lambda_ = 10.0  # Mean (and parameter lambda) of the Poisson distribution
sigma = np.sqrt(lambda_)  # Standard deviation of the Poisson distribution
D = [*range(int(lambda_ + 3 * sigma + 1))]

N = int(lambda_)  # Inventory capacity (the maximum possible state)
S = [*range(N + 1)]

T = 5  # for finite

# Create an instance of the InventorySystemInfinite class
infinite_system = functions.InventorySystemInfinite(S, D, h, e, c, lambda_)

# Perform value iteration on the infinite-horizon problem
V, optimal_policy, optimal_cost = infinite_system.value_iteration()

# Create an instance of the InventorySystemFinite class
finite_system = functions.InventorySystemFinite(S, D, h, e, c, lambda_)

# Perform backward dynamic programming on the finite-horizon problem
V_t, optimal_policy_t, optimal_cost_t = finite_system.backward_DP(T)
