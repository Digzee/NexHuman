from .genetic_algorithm import (
    GeneticAlgorithmOptimizer,
)


class OptimizationService:
    """Configure and execute NexHuman portfolio optimisation."""

    PROFILE_CONFIG = {
        "low": {
            "max_weight": 0.35,
        },
        "moderate": {
            "max_weight": 0.45,
        },
        "high": {
            "max_weight": 0.60,
        },
    }

    POPULATION_SIZE = 100
    GENERATIONS = 100

    @classmethod
    def optimise(
        cls,
        asset_returns,
        risk_profile,
        seed=None,
    ):
        config = cls.PROFILE_CONFIG.get(
            risk_profile
        )

        if config is None:
            raise ValueError(
                "Unsupported investor risk profile."
            )

        optimizer = GeneticAlgorithmOptimizer(
            asset_returns=asset_returns,
            population_size=(
                cls.POPULATION_SIZE
            ),
            generations=cls.GENERATIONS,
            max_weight=config["max_weight"],
            seed=seed,
        )

        optimized = optimizer.optimise()

        baseline = (
            optimizer.equal_weight_baseline()
        )

        return {
            "optimized": optimized,
            "baseline": baseline,
            "configuration": {
                "population_size": (
                    cls.POPULATION_SIZE
                ),
                "generations": (
                    cls.GENERATIONS
                ),
                "max_weight": (
                    config["max_weight"]
                ),
            },
        }