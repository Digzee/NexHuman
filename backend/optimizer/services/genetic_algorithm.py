import math
import random
from statistics import mean, stdev


class GeneticAlgorithmOptimizer:
    """
    Genetic algorithm for long-only cryptocurrency
    portfolio optimisation.
    """

    ANNUALISATION_DAYS = 365

    def __init__(
        self,
        asset_returns,
        population_size=100,
        generations=100,
        mutation_rate=0.10,
        elite_count=5,
        tournament_size=3,
        max_weight=0.60,
        risk_free_rate=0.0,
        seed=None,
    ):
        self.asset_returns = asset_returns
        self.symbols = list(asset_returns.keys())

        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_count = elite_count
        self.tournament_size = tournament_size
        self.max_weight = max_weight
        self.risk_free_rate = risk_free_rate

        self.random = random.Random(seed)

        if len(self.symbols) < 2:
            raise ValueError(
                "At least two assets are required "
                "for optimisation."
            )

        if (
            self.max_weight
            * len(self.symbols)
            < 1.0
        ):
            raise ValueError(
                "The maximum asset weight is "
                "infeasible for the number of assets."
            )      

    def optimise(self):
        population = [
            self._create_individual()
            for _ in range(self.population_size)
        ]

        for _ in range(self.generations):
            ranked = sorted(
                population,
                key=self._fitness,
                reverse=True,
            )

            next_population = [
                individual[:]
                for individual in ranked[
                    : self.elite_count
                ]
            ]

            while (
                len(next_population)
                < self.population_size
            ):
                parent_a = self._tournament_selection(
                    population
                )

                parent_b = self._tournament_selection(
                    population
                )

                child = self._blend_crossover(
                    parent_a,
                    parent_b,
                )

                child = self._mutate(child)
                child = self._repair_weights(child)

                next_population.append(child)

            population = next_population

        best = max(
            population,
            key=self._fitness,
        )

        metrics = self.calculate_metrics(best)

        return {
            "weights": {
                symbol: weight
                for symbol, weight in zip(
                    self.symbols,
                    best,
                )
            },
            **metrics,
        }

    def equal_weight_baseline(self):
        weight = 1 / len(self.symbols)

        weights = [
            weight
            for _ in self.symbols
        ]

        return {
            "weights": {
                symbol: weight
                for symbol in self.symbols
            },
            **self.calculate_metrics(weights),
        }

    def _create_individual(self):
        weights = [
            self.random.random()
            for _ in self.symbols
        ]

        return self._repair_weights(weights)

    def _tournament_selection(
        self,
        population,
    ):
        competitors = self.random.sample(
            population,
            min(
                self.tournament_size,
                len(population),
            ),
        )

        return max(
            competitors,
            key=self._fitness,
        )

    def _blend_crossover(
        self,
        parent_a,
        parent_b,
    ):
        alpha = self.random.random()

        return [
            alpha * weight_a
            + (1 - alpha) * weight_b
            for weight_a, weight_b in zip(
                parent_a,
                parent_b,
            )
        ]

    def _mutate(self, individual):
        mutated = individual[:]

        for index in range(len(mutated)):
            if (
                self.random.random()
                < self.mutation_rate
            ):
                mutated[index] += (
                    self.random.gauss(
                        0,
                        0.05,
                    )
                )

        return mutated

    def _repair_weights(self, weights):
        repaired = [
            max(0.0, weight)
            for weight in weights
        ]

        for _ in range(20):
            total = sum(repaired)

            if total <= 0:
                repaired = [
                    1 / len(repaired)
                    for _ in repaired
                ]
            else:
                repaired = [
                    weight / total
                    for weight in repaired
                ]

            excess = 0.0

            for index, weight in enumerate(
                repaired
            ):
                if weight > self.max_weight:
                    excess += (
                        weight - self.max_weight
                    )

                    repaired[index] = (
                        self.max_weight
                    )

            if excess <= 1e-12:
                break

            available = [
                index
                for index, weight in enumerate(
                    repaired
                )
                if weight < self.max_weight
            ]

            if not available:
                break

            capacity = sum(
                self.max_weight - repaired[index]
                for index in available
            )

            if capacity <= 0:
                break

            for index in available:
                share = (
                    (
                        self.max_weight
                        - repaired[index]
                    )
                    / capacity
                )

                repaired[index] += (
                    excess * share
                )

        total = sum(repaired)

        if total <= 0:
            raise ValueError(
                "Unable to construct valid weights."
            )

        return [
            weight / total
            for weight in repaired
        ]

    def _fitness(self, weights):
        metrics = self.calculate_metrics(
            weights
        )

        volatility = metrics["volatility"]

        if volatility <= 0:
            return float("-inf")

        return metrics["sharpe_ratio"]

    def calculate_metrics(self, weights):
        portfolio_returns = (
            self._portfolio_daily_returns(
                weights
            )
        )

        if len(portfolio_returns) < 2:
            return {
                "expected_return": 0.0,
                "volatility": 0.0,
                "sharpe_ratio": 0.0,
            }

        daily_return = mean(
            portfolio_returns
        )

        daily_volatility = stdev(
            portfolio_returns
        )

        annual_return = (
            daily_return
            * self.ANNUALISATION_DAYS
        )

        annual_volatility = (
            daily_volatility
            * math.sqrt(
                self.ANNUALISATION_DAYS
            )
        )

        if annual_volatility <= 0:
            sharpe_ratio = 0.0
        else:
            sharpe_ratio = (
                annual_return
                - self.risk_free_rate
            ) / annual_volatility

        return {
            "expected_return": annual_return,
            "volatility": annual_volatility,
            "sharpe_ratio": sharpe_ratio,
        }

    def _portfolio_daily_returns(
        self,
        weights,
    ):
        series_length = min(
            len(self.asset_returns[symbol])
            for symbol in self.symbols
        )

        return [
            sum(
                weights[index]
                * self.asset_returns[symbol][day]
                for index, symbol in enumerate(
                    self.symbols
                )
            )
            for day in range(series_length)
        ]