"""
Example usage of E.L.E.S. Models

This file demonstrates how to use the various prediction and risk assessment
models provided by the E.L.E.S. system.
"""

from models import (
    SurvivalPredictor, SurvivalContext,
    RiskScoreCalculator, RiskProfile,
    RegenTimeEstimator, RecoveryContext
)


def example_survival_prediction():
    """Example of using the SurvivalPredictor model."""
    print("=== Survival Prediction Example ===")

    # Create survival predictor
    predictor = SurvivalPredictor()

    # Define a pandemic scenario context
    context = SurvivalContext(
        event_type="pandemic",
        severity=4,
        duration_years=3.0,
        affected_area_km2=50000000,  # Global pandemic
        population_in_area=7800000000,  # World population
        geographic_factors={
            'climate_suitability': 0.7,
            'isolation': 0.3,
            'resource_density': 0.6
        },
        infrastructure_damage=0.2,
        food_system_disruption=0.4,
        medical_system_impact=0.6,
        social_stability=0.5
    )

    # Predict survival rates
    result = predictor.predict(context)

    print(f"Immediate survival rate: {result['immediate_survival_rate']:.1%}")
    print(f"Long-term survival rate: {result['long_term_survival_rate']:.1%}")
    print(f"Expected survivors: {result['expected_survivors']:,.0f}")
    print(f"Key risks: {', '.join(result['key_risks'])}")
    print()


def example_risk_assessment():
    """Example of using the RiskScoreCalculator model."""
    print("=== Risk Assessment Example ===")

    # Create risk calculator
    calculator = RiskScoreCalculator()

    # Define asteroid impact risk profile
    profile = RiskProfile(
        event_type="asteroid",
        probability_per_year=1e-6,  # 1 in a million per year
        expected_casualties=100000000,  # 100 million
        economic_impact_usd=10e12,  # $10 trillion
        affected_area_km2=1000000,  # 1 million km²
        duration_years=5.0,
        recovery_time_years=50.0,
        global_impact_score=0.8,
        detectability=0.7,
        preventability=0.3,
        mitigation_potential=0.4
    )

    # Calculate risk scores
    result = calculator.compute(profile)

    print(f"Overall risk score: {result['overall_risk_score']:.2f}")
    print(f"Expected annual impact: ${result['expected_annual_impact']:,.0f}")
    print(f"Risk ranking: {result['risk_ranking']}")
    print(f"Mitigation priority: {result['mitigation_priority']}")
    print()


def example_recovery_estimation():
    """Example of using the RegenTimeEstimator model."""
    print("=== Recovery Time Estimation Example ===")

    # Create regeneration estimator
    estimator = RegenTimeEstimator()

    # Define nuclear war recovery context
    context = RecoveryContext(
        event_type="nuclear_war",
        severity=5,
        initial_damage={
            'population': 0.7,
            'infrastructure': 0.8,
            'economy': 0.9,
            'technology': 0.5,
            'agriculture': 0.6,
            'healthcare': 0.8
        },
        surviving_population=2000000000,  # 2 billion survivors
        surviving_infrastructure=0.2,
        available_resources={
            'food': 0.3,
            'water': 0.5,
            'energy': 0.2,
            'materials': 0.4
        },
        external_aid=0.1,  # Limited external aid
        geographic_factors={
            'climate_suitability': 0.6,
            'natural_resources': 0.7
        },
        technology_preservation=0.4,
        social_cohesion=0.3
    )

    # Estimate recovery times
    result = estimator.estimate(context)

    print(f"Total recovery time: {result['overall_metrics']['total_recovery_time']:.0f} years")
    print(f"Population recovery: {result['system_recovery_times']['population']['total_time']:.0f} years")
    print(f"Technology recovery: {result['system_recovery_times']['technology']['total_time']:.0f} years")
    print(f"Critical bottlenecks: {len(result['critical_bottlenecks'])}")

    print("\nRecovery strategies:")
    for strategy in result['recovery_strategies'][:3]:
        print(f"  - {strategy}")
    print()


def example_integrated_analysis():
    """Example of integrated analysis using multiple models."""
    print("=== Integrated Analysis Example ===")

    # Analyze a supervolcano eruption scenario
    event_type = "supervolcano"

    # 1. Risk Assessment
    risk_profile = RiskProfile(
        event_type=event_type,
        probability_per_year=1e-5,
        expected_casualties=500000000,
        economic_impact_usd=20e12,
        affected_area_km2=5000000,
        duration_years=10.0,
        recovery_time_years=200.0,
        global_impact_score=0.9,
        detectability=0.6,
        preventability=0.1,
        mitigation_potential=0.2
    )

    risk_calculator = RiskScoreCalculator()
    risk_result = risk_calculator.compute(risk_profile)

    # 2. Survival Prediction
    survival_context = SurvivalContext(
        event_type=event_type,
        severity=5,
        duration_years=10.0,
        affected_area_km2=5000000,
        population_in_area=500000000,
        geographic_factors={'isolation': 0.4, 'resources': 0.6},
        infrastructure_damage=0.7,
        food_system_disruption=0.8,
        medical_system_impact=0.6,
        social_stability=0.4
    )

    survival_predictor = SurvivalPredictor()
    survival_result = survival_predictor.predict(survival_context)

    # 3. Recovery Estimation
    recovery_context = RecoveryContext(
        event_type=event_type,
        severity=5,
        initial_damage={
            'population': 0.6,
            'infrastructure': 0.7,
            'agriculture': 0.8,
            'ecosystem': 0.9
        },
        surviving_population=int(survival_result['expected_survivors']),
        surviving_infrastructure=0.3,
        available_resources={'food': 0.2, 'water': 0.4},
        external_aid=0.3,
        geographic_factors={'climate_suitability': 0.3},
        technology_preservation=0.6,
        social_cohesion=0.4
    )

    regen_estimator = RegenTimeEstimator()
    recovery_result = regen_estimator.estimate(recovery_context)

    # Integrated summary
    print(f"Scenario: {event_type.title()} Eruption")
    print(f"Risk Score: {risk_result['overall_risk_score']:.2f}")
    print(f"Survival Rate: {survival_result['long_term_survival_rate']:.1%}")
    print(f"Expected Survivors: {survival_result['expected_survivors']:,.0f}")
    print(f"Recovery Time: {recovery_result['overall_metrics']['total_recovery_time']:.0f} years")
    print(f"Mitigation Priority: {risk_result['mitigation_priority']}")


if __name__ == "__main__":
    """Run all examples."""
    print("E.L.E.S. Models Example Usage\n")

    example_survival_prediction()
    example_risk_assessment()
    example_recovery_estimation()
    example_integrated_analysis()

    print("All examples completed successfully!")
