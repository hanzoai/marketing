"""Genetic algorithm optimizer for campaign parameters."""

import random
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np
from deap import base, creator, tools, algorithms

from ..core.config import settings
from ..core.models import OptimizationResult


@dataclass
class SearchSpace:
    """Defines the parameter search space."""
    name: str
    min_val: float
    max_val: float
    dtype: type = float


class GeneticOptimizer:
    """
    Genetic algorithm optimizer for marketing campaigns.

    Explores solution space across multiple dimensions:
    - Budget allocation across platforms
    - Audience targeting parameters
    - Bid strategies
    - Creative variants
    - Timing/scheduling
    """

    def __init__(
        self,
        search_space: list[SearchSpace],
        fitness_func: Callable[[list[float]], tuple[float,]],
        population_size: int = settings.optimizer_population_size,
        generations: int = settings.optimizer_generations,
        mutation_rate: float = settings.optimizer_mutation_rate,
        crossover_rate: float = settings.optimizer_crossover_rate,
    ):
        self.search_space = search_space
        self.fitness_func = fitness_func
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self._setup_deap()

    def _setup_deap(self) -> None:
        """Initialize DEAP genetic algorithm components."""
        # Create fitness class (maximize)
        if not hasattr(creator, "FitnessMax"):
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        if not hasattr(creator, "Individual"):
            creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()

        # Attribute generators for each parameter
        for i, param in enumerate(self.search_space):
            self.toolbox.register(
                f"attr_{i}",
                random.uniform,
                param.min_val,
                param.max_val,
            )

        # Structure initializers
        attrs = [getattr(self.toolbox, f"attr_{i}") for i in range(len(self.search_space))]
        self.toolbox.register(
            "individual",
            tools.initCycle,
            creator.Individual,
            attrs,
            n=1,
        )
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        # Operators
        self.toolbox.register("evaluate", self.fitness_func)
        self.toolbox.register("mate", tools.cxBlend, alpha=0.5)
        self.toolbox.register(
            "mutate",
            tools.mutGaussian,
            mu=0,
            sigma=0.2,
            indpb=0.2,
        )
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def optimize(self, parallel: bool = False) -> list[OptimizationResult]:
        """
        Run genetic algorithm optimization.

        Returns optimization results for each generation.
        """
        results: list[OptimizationResult] = []

        # Initialize population
        pop = self.toolbox.population(n=self.population_size)

        # Hall of fame to track best individuals
        hof = tools.HallOfFame(1)

        # Statistics
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        # Run evolution
        pop, logbook = algorithms.eaSimple(
            pop,
            self.toolbox,
            cxpb=self.crossover_rate,
            mutpb=self.mutation_rate,
            ngen=self.generations,
            stats=stats,
            halloffame=hof,
            verbose=False,
        )

        # Convert logbook to results
        for gen, record in enumerate(logbook):
            best_ind = hof[0] if hof else pop[0]
            results.append(
                OptimizationResult(
                    generation=gen,
                    best_fitness=record.get("max", 0.0),
                    best_params=self._decode_individual(best_ind),
                    population_stats={
                        "avg": record.get("avg", 0.0),
                        "std": record.get("std", 0.0),
                        "min": record.get("min", 0.0),
                        "max": record.get("max", 0.0),
                    },
                    convergence=record.get("std", 1.0) < 0.01,
                )
            )

        return results

    def _decode_individual(self, individual: list[float]) -> dict[str, Any]:
        """Convert individual to named parameters."""
        return {
            param.name: param.dtype(val)
            for param, val in zip(self.search_space, individual)
        }

    def optimize_multi_platform(
        self,
        platforms: list[str],
        total_budget: float,
        target_metrics: dict[str, float],
    ) -> dict[str, Any]:
        """
        Optimize budget allocation across multiple ad platforms.

        Uses genetic algorithm to find optimal distribution.
        """
        # Define search space for budget percentages
        search_space = [
            SearchSpace(name=f"{p}_budget_pct", min_val=0.0, max_val=1.0)
            for p in platforms
        ]

        # Add bid multipliers
        search_space.extend([
            SearchSpace(name=f"{p}_bid_mult", min_val=0.5, max_val=2.0)
            for p in platforms
        ])

        def fitness(individual: list[float]) -> tuple[float,]:
            # Normalize budget percentages to sum to 1
            budget_pcts = individual[:len(platforms)]
            total = sum(budget_pcts)
            if total > 0:
                budget_pcts = [p / total for p in budget_pcts]

            # Simulate performance (replace with real data)
            score = sum(
                pct * mult
                for pct, mult in zip(budget_pcts, individual[len(platforms):])
            )
            return (score,)

        optimizer = GeneticOptimizer(
            search_space=search_space,
            fitness_func=fitness,
        )

        results = optimizer.optimize()
        best = results[-1] if results else None

        if best:
            # Normalize final budget allocation
            params = best.best_params
            budget_pcts = [params[f"{p}_budget_pct"] for p in platforms]
            total = sum(budget_pcts)

            return {
                "allocation": {
                    p: {
                        "budget": total_budget * (pct / total),
                        "bid_multiplier": params[f"{p}_bid_mult"],
                    }
                    for p, pct in zip(platforms, budget_pcts)
                },
                "fitness": best.best_fitness,
                "generations": best.generation,
            }

        return {"error": "Optimization failed"}
