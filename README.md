# Dynamic Programming for Inventory Systems
<!-- TOC depthFrom:2 -->

- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
- [Constructor](#constructor)
- [Member Functions](#member-functions)
- [Performance Test](#performance-test)
- [Version history](#version-history)
- [Feedback](#feedback)
- [Author and copyright](#author-and-copyright)

<!-- /TOC -->

# Inventory Problem Solver

This repository contains code that solves the inventory problem using dynamic programming. The inventory problem is a practical example of a Markov Decision Process (MDP), where a decision maker (DM) has to make replenishment decisions for a product over a certain number of time periods.

## Problem Description

The inventory problem involves the DM making inventory decisions at the beginning of each period. The ordered quantities are assumed to be received instantly (zero lead time), and the demand for that period is realized afterward. The goal is to optimize the inventory decisions to minimize costs.

### State Variable

At the beginning of each period, the DM observes the inventory level, which is represented as the state variable 𝑆𝑡, where 𝑡 is the period index.

### Action Variable

The ordering quantity for each period, to be used between periods 𝑡 and 𝑡+1, is represented as the action variable 𝑎𝑡.

### Cost Function

In this problem, we deal with a cost function rather than a reward function. The cost associated with each period 𝑡 in the planning horizon can be formulated as follows:

𝐶𝑡(𝑆𝑡,𝑎𝑡) = ℎ(𝑆𝑡+𝑎𝑡−𝐷̂𝑡+1)+ + 𝑒(𝐷̂𝑡+1−𝑆𝑡−𝑎𝑡)+ + 𝑐𝑎𝑡   (3)

where 𝑆𝑡 and 𝑎𝑡 are the state and action in period 𝑡, respectively, 𝐷̂𝑡+1 is the realized demand of that period, ℎ is the holding cost per unit (for unsold units), 𝑒 is the unit backlog cost (for unsatisfied demand), and 𝑐 is the ordering cost per unit. Note that (𝑥)+=𝑚𝑎𝑥(0,𝑥).

### Bellman's Equation

Bellman's equation is a fundamental equation in dynamic programming. In this inventory problem, we modify the equation to accommodate the cost function:

𝑉𝑡(𝑆𝑡) = 𝑚𝑖𝑛𝑎𝑡∈𝐴𝑡[𝐶𝑡(𝑆𝑡,𝑎𝑡) + 𝛾Σ𝑃(𝑆𝑡+1=𝑠′|𝑆𝑡=𝑠,𝑎𝑡=𝑎)𝑉𝑡+1(𝑠′)]   (4)

where 𝑉𝑡(𝑆𝑡) is the value function for period 𝑡, 𝐴𝑡 is the set of possible actions in period 𝑡, 𝛾 is the discount factor, and 𝑃(𝑆𝑡+1=𝑠′|𝑆𝑡,𝑎𝑡) is the transition probability from state 𝑆𝑡 to 𝑆𝑡+1 given action 𝑎𝑡.

### Transition Function

The transition function describes the change in the inventory level from period 𝑡 to period 𝑡+1. In this problem, the transition function is as follows:

𝑆𝑡+1 = (𝑆𝑡 + 𝑎𝑡 − 𝐷̂𝑡+1)+   (6)

where (𝑥)+ represents the positive part of 𝑥, ensuring that the inventory level cannot be negative.

## Getting Started

To use the inventory problem solver, follow these steps:

1. Install the necessary dependencies (if any).
2. Run the main program, providing the required input data.
3. The program will output the optimal inventory decisions and the associated costs.

Make sure to adjust the input data and parameters according to your specific problem instance.

## Contributing

If you'd like to contribute to this inventory problem solver, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch to your fork.
4. Submit a pull request, explaining your changes and their benefits.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

Special thanks to [Name] for their contribution to the development of this inventory problem solver.

