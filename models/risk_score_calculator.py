"""
Risk Score Calculator for E.L.E.S.

This module provides comprehensive risk assessment and scoring models
for extinction-level events.
"""

import math
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class RiskCategory(Enum):
    """Risk assessment categories."""
    PROBABILITY = "probability"
    IMPACT_MAGNITUDE = "impact_magnitude"
    POPULATION_EXPOSURE = "population_exposure"
    INFRASTRUCTURE_VULNERABILITY = "infrastructure_vulnerability"
    RECOVERY_DIFFICULTY = "recovery_difficulty"
    CASCADING_EFFECTS = "cascading_effects"
    PREPAREDNESS_LEVEL = "preparedness_level"
    WARNING_TIME = "warning_time"


@dataclass
class RiskProfile:
    """Comprehensive risk profile for an extinction event."""
    event_type: str
    probability_per_year: float
    expected_casualties: int
    economic_impact_usd: float
    affected_area_km2: float
    duration_years: float
    recovery_time_years: float
    global_impact_score: float  # 0-1 scale
    detectability: float  # 0-1 scale (1 = easily detectable)
    preventability: float  # 0-1 scale (1 = easily preventable)
    mitigation_potential: float  # 0-1 scale (1 = highly mitigatable)


class RiskScoreCalculator:
    """
    Advanced risk assessment and scoring system.

    Calculates comprehensive risk scores using multiple methodologies
    including expected value, severity indices, and comparative rankings.
    """

    def __init__(self):
        """Initialize risk calculator with standard parameters."""
        self.risk_weights = {
            RiskCategory.PROBABILITY: 0.20,
            RiskCategory.IMPACT_MAGNITUDE: 0.25,
            RiskCategory.POPULATION_EXPOSURE: 0.15,
            RiskCategory.INFRASTRUCTURE_VULNERABILITY: 0.10,
            RiskCategory.RECOVERY_DIFFICULTY: 0.10,
            RiskCategory.CASCADING_EFFECTS: 0.10,
            RiskCategory.PREPAREDNESS_LEVEL: 0.05,
            RiskCategory.WARNING_TIME: 0.05
        }

        # Standard probability estimates (per year)
        self.standard_probabilities = {
            'asteroid': {
                'city_killer': 1e-4,     # 100m+ asteroid
                'regional': 1e-6,        # 1km+ asteroid
                'global': 1e-8           # 10km+ asteroid
            },
            'supervolcano': {
                'vei_7': 1e-4,           # Large caldera eruption
                'vei_8': 1e-5            # Supervolcano eruption
            },
            'pandemic': {
                'severe': 1e-2,          # Severe pandemic
                'extreme': 1e-3          # Civilization-threatening
            },
            'climate_collapse': {
                'tipping_point': 1e-1,   # Climate tipping cascade
                'runaway': 1e-3          # Runaway greenhouse
            },
            'gamma_ray_burst': {
                'galactic': 1e-5,        # Within galaxy
                'nearby': 1e-8           # Within 1000 ly
            },
            'ai_extinction': {
                'misaligned_agi': 1e-1,  # This century
                'hard_takeoff': 1e-2     # Rapid capability growth
            },
            'nuclear_war': {
                'regional': 1e-3,        # Regional nuclear conflict
                'global': 1e-4           # Full global exchange
            }
        }

    def compute(self, risk_profile: RiskProfile) -> Dict[str, Any]:
        """
        Compute comprehensive risk assessment.

        Args:
            risk_profile: RiskProfile object with event parameters

        Returns:
            Dictionary with risk scores and detailed analysis
        """
        # Calculate individual risk components
        risk_components = self._calculate_risk_components(risk_profile)

        # Calculate composite scores
        composite_scores = self._calculate_composite_scores(risk_components)

        # Expected value calculations
        expected_values = self._calculate_expected_values(risk_profile)

        # Risk rankings and comparisons
        rankings = self._calculate_risk_rankings(risk_profile)

        # Risk mitigation analysis
        mitigation_analysis = self._analyze_mitigation_potential(risk_profile)

        return {
            'overall_risk_score': composite_scores['weighted_average'],
            'risk_level': self._categorize_risk_level(composite_scores['weighted_average']),
            'risk_components': risk_components,
            'composite_scores': composite_scores,
            'expected_values': expected_values,
            'rankings': rankings,
            'mitigation_analysis': mitigation_analysis,
            'recommendations': self._generate_recommendations(risk_profile, composite_scores)
        }

    def compare_scenarios(self, profiles: List[RiskProfile]) -> Dict[str, Any]:
        """
        Compare risk across multiple scenarios.

        Args:
            profiles: List of RiskProfile objects to compare

        Returns:
            Comparative risk analysis
        """
        scenario_scores = []

        for profile in profiles:
            score_data = self.compute(profile)
            scenario_scores.append({
                'profile': profile,
                'scores': score_data
            })

        # Sort by overall risk score
        sorted_scenarios = sorted(
            scenario_scores,
            key=lambda x: x['scores']['overall_risk_score'],
            reverse=True
        )

        # Calculate relative risks
        relative_risks = self._calculate_relative_risks(scenario_scores)

        return {
            'ranked_scenarios': sorted_scenarios,
            'relative_risks': relative_risks,
            'highest_risk': sorted_scenarios[0] if sorted_scenarios else None,
            'lowest_risk': sorted_scenarios[-1] if sorted_scenarios else None,
            'risk_distribution': self._analyze_risk_distribution(scenario_scores)
        }

    def _calculate_risk_components(self, profile: RiskProfile) -> Dict[str, float]:
        """Calculate individual risk component scores."""
        components = {}

        # Probability component (log scale normalization)
        prob_score = min(1.0, -math.log10(max(1e-10, profile.probability_per_year)) / 10)
        components[RiskCategory.PROBABILITY.value] = prob_score

        # Impact magnitude (based on casualties and economic damage)
        casualty_score = min(1.0, profile.expected_casualties / 1e9)  # Normalize to 1B
        economic_score = min(1.0, profile.economic_impact_usd / 1e14)  # Normalize to $100T
        components[RiskCategory.IMPACT_MAGNITUDE.value] = (casualty_score + economic_score) / 2

        # Population exposure (based on affected area and global population)
        area_fraction = min(1.0, profile.affected_area_km2 / 1.5e8)  # Earth's land area
        components[RiskCategory.POPULATION_EXPOSURE.value] = area_fraction

        # Infrastructure vulnerability
        infra_score = min(1.0, profile.global_impact_score)
        components[RiskCategory.INFRASTRUCTURE_VULNERABILITY.value] = infra_score

        # Recovery difficulty (based on recovery time)
        recovery_score = min(1.0, profile.recovery_time_years / 1000)  # Normalize to 1000 years
        components[RiskCategory.RECOVERY_DIFFICULTY.value] = recovery_score

        # Cascading effects (derived from duration and global impact)
        cascade_score = min(1.0, (profile.duration_years * profile.global_impact_score) / 50)
        components[RiskCategory.CASCADING_EFFECTS.value] = cascade_score

        # Preparedness level (inverse of detectability and preventability)
        prep_score = 1.0 - ((profile.detectability + profile.preventability) / 2)
        components[RiskCategory.PREPAREDNESS_LEVEL.value] = prep_score

        # Warning time (inverse of detectability)
        warning_score = 1.0 - profile.detectability
        components[RiskCategory.WARNING_TIME.value] = warning_score

        return components

    def _calculate_composite_scores(self, components: Dict[str, float]) -> Dict[str, float]:
        """Calculate composite risk scores using different methodologies."""
        # Weighted average
        weighted_avg = sum(
            components[category.value] * self.risk_weights[category]
            for category in RiskCategory
        )

        # Geometric mean (emphasizes balanced risks)
        geometric_mean = np.prod([
            max(0.01, components[category.value])
            for category in RiskCategory
        ]) ** (1.0 / len(RiskCategory))

        # Maximum component (worst-case approach)
        max_component = max(components.values())

        # Minimum component (best-case approach)
        min_component = min(components.values())

        # Root mean square
        rms = math.sqrt(sum(
            components[category.value] ** 2
            for category in RiskCategory
        ) / len(RiskCategory))

        return {
            'weighted_average': weighted_avg,
            'geometric_mean': float(geometric_mean),
            'maximum_component': max_component,
            'minimum_component': min_component,
            'root_mean_square': rms
        }

    def _calculate_expected_values(self, profile: RiskProfile) -> Dict[str, float]:
        """Calculate expected value metrics."""
        annual_probability = profile.probability_per_year

        return {
            'expected_annual_casualties': annual_probability * profile.expected_casualties,
            'expected_annual_economic_loss': annual_probability * profile.economic_impact_usd,
            'expected_lifetime_probability': 1.0 - (1.0 - annual_probability) ** 70,  # 70-year lifetime
            'years_until_occurrence': 1.0 / annual_probability if annual_probability > 0 else float('inf')
        }

    def _calculate_risk_rankings(self, profile: RiskProfile) -> Dict[str, Any]:
        """Calculate relative risk rankings."""
        # Compare against standard scenarios
        standard_events = [
            ('car_accident_death', 1e-4, 1, 0),
            ('lightning_strike', 1e-6, 1, 0),
            ('plane_crash', 1e-7, 300, 1e9),
            ('nuclear_plant_accident', 1e-6, 1000, 1e11)
        ]

        risk_comparison = []
        for name, prob, casualties, economic in standard_events:
            relative_prob = profile.probability_per_year / prob
            relative_impact = profile.expected_casualties / casualties
            risk_comparison.append({
                'reference_event': name,
                'probability_ratio': relative_prob,
                'impact_ratio': relative_impact,
                'overall_ratio': relative_prob * relative_impact
            })

        return {
            'probability_percentile': self._calculate_probability_percentile(profile.probability_per_year),
            'impact_percentile': self._calculate_impact_percentile(profile.expected_casualties),
            'comparisons': risk_comparison
        }

    def _analyze_mitigation_potential(self, profile: RiskProfile) -> Dict[str, Any]:
        """Analyze potential for risk mitigation."""
        mitigation_score = (
            profile.detectability * 0.3 +
            profile.preventability * 0.4 +
            profile.mitigation_potential * 0.3
        )

        strategies = []

        if profile.detectability > 0.7:
            strategies.append("Early warning systems")

        if profile.preventability > 0.5:
            strategies.append("Prevention measures")

        if profile.mitigation_potential > 0.6:
            strategies.append("Impact mitigation")

        # Cost-benefit analysis
        mitigation_value = mitigation_score * profile.expected_casualties * 1e6  # Value of statistical life

        return {
            'mitigation_score': mitigation_score,
            'potential_strategies': strategies,
            'estimated_mitigation_value': mitigation_value,
            'priority_level': self._determine_mitigation_priority(mitigation_score, profile)
        }

    def _categorize_risk_level(self, risk_score: float) -> str:
        """Categorize overall risk level."""
        if risk_score >= 0.8:
            return "EXTREME"
        elif risk_score >= 0.6:
            return "HIGH"
        elif risk_score >= 0.4:
            return "MODERATE"
        elif risk_score >= 0.2:
            return "LOW"
        else:
            return "MINIMAL"

    def _generate_recommendations(self, profile: RiskProfile, scores: Dict[str, float]) -> List[str]:
        """Generate risk management recommendations."""
        recommendations = []

        if scores['weighted_average'] > 0.7:
            recommendations.append("Immediate attention required - high priority risk")

        if profile.detectability < 0.3:
            recommendations.append("Invest in detection and monitoring systems")

        if profile.preventability > 0.5:
            recommendations.append("Focus on prevention strategies")

        if profile.mitigation_potential > 0.6:
            recommendations.append("Develop comprehensive mitigation plans")

        if profile.recovery_time_years > 100:
            recommendations.append("Establish long-term recovery frameworks")

        return recommendations

    def _calculate_relative_risks(self, scenario_scores: List[Dict]) -> Dict[str, float]:
        """Calculate relative risk ratios between scenarios."""
        if len(scenario_scores) < 2:
            return {}

        baseline = scenario_scores[0]['scores']['overall_risk_score']
        return {
            f"{score['profile'].event_type}_relative_risk":
            score['scores']['overall_risk_score'] / baseline
            for score in scenario_scores
        }

    def _analyze_risk_distribution(self, scenario_scores: List[Dict]) -> Dict[str, float]:
        """Analyze distribution of risks across scenarios."""
        scores = [s['scores']['overall_risk_score'] for s in scenario_scores]

        return {
            'mean_risk': float(np.mean(scores)),
            'median_risk': float(np.median(scores)),
            'std_deviation': float(np.std(scores)),
            'min_risk': float(np.min(scores)),
            'max_risk': float(np.max(scores)),
            'risk_range': float(np.max(scores) - np.min(scores))
        }

    def _calculate_probability_percentile(self, probability: float) -> float:
        """Calculate percentile ranking for probability."""
        # Simplified percentile calculation
        return min(100, max(0, -math.log10(probability) * 10))

    def _calculate_impact_percentile(self, casualties: int) -> float:
        """Calculate percentile ranking for impact."""
        # Simplified percentile calculation
        return min(100, max(0, math.log10(max(1, casualties)) * 10))

    def _determine_mitigation_priority(self, mitigation_score: float, profile: RiskProfile) -> str:
        """Determine priority level for mitigation efforts."""
        combined_score = mitigation_score * profile.probability_per_year * profile.expected_casualties

        if combined_score > 1e3:
            return "CRITICAL"
        elif combined_score > 1e2:
            return "HIGH"
        elif combined_score > 1e1:
            return "MEDIUM"
        else:
            return "LOW"
