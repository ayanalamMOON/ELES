"""
Survival Predictor Model for E.L.E.S.

This module provides models for predicting human survival probabilities
under various extinction-level event scenarios.
"""

import math
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class SurvivalFactors(Enum):
    """Key factors affecting survival probability."""
    DISTANCE_FROM_IMPACT = "distance_from_impact"
    INFRASTRUCTURE_RESILIENCE = "infrastructure_resilience"
    FOOD_SECURITY = "food_security"
    MEDICAL_ACCESS = "medical_access"
    SOCIAL_COHESION = "social_cohesion"
    GOVERNMENT_PREPAREDNESS = "government_preparedness"
    GEOGRAPHIC_LOCATION = "geographic_location"
    POPULATION_DENSITY = "population_density"
    RESOURCE_AVAILABILITY = "resource_availability"
    CLIMATE_SUITABILITY = "climate_suitability"


@dataclass
class SurvivalContext:
    """Context information for survival prediction."""
    event_type: str
    severity: int
    duration_years: float
    affected_area_km2: float
    population_in_area: int
    geographic_factors: Dict[str, float]
    infrastructure_damage: float  # 0-1 scale
    food_system_disruption: float  # 0-1 scale
    medical_system_impact: float  # 0-1 scale
    social_stability: float  # 0-1 scale


class SurvivalPredictor:
    """
    Advanced survival probability prediction model.

    Uses multiple factors to predict survival rates under different
    extinction event scenarios.
    """

    def __init__(self):
        """Initialize the survival predictor with default parameters."""
        self.base_survival_rates = {
            'asteroid': 0.85,
            'supervolcano': 0.70,
            'climate_collapse': 0.60,
            'pandemic': 0.75,
            'gamma_ray_burst': 0.40,
            'ai_extinction': 0.30,
            'nuclear_war': 0.50,
            'cosmic': 0.45
        }

        # Factor weights for survival calculation
        self.factor_weights = {
            SurvivalFactors.DISTANCE_FROM_IMPACT: 0.25,
            SurvivalFactors.INFRASTRUCTURE_RESILIENCE: 0.20,
            SurvivalFactors.FOOD_SECURITY: 0.15,
            SurvivalFactors.MEDICAL_ACCESS: 0.10,
            SurvivalFactors.SOCIAL_COHESION: 0.10,
            SurvivalFactors.GOVERNMENT_PREPAREDNESS: 0.08,
            SurvivalFactors.GEOGRAPHIC_LOCATION: 0.07,
            SurvivalFactors.POPULATION_DENSITY: 0.05
        }

    def predict(self, context: SurvivalContext) -> Dict[str, Any]:
        """
        Predict survival probability for given context.

        Args:
            context: SurvivalContext object with event parameters

        Returns:
            Dictionary with survival predictions and analysis
        """
        base_rate = self.base_survival_rates.get(context.event_type, 0.50)

        # Calculate factor-based adjustments
        adjustments = self._calculate_factor_adjustments(context)

        # Apply severity scaling
        severity_modifier = self._get_severity_modifier(context.severity)

        # Calculate immediate survival rate
        immediate_survival = max(0.01, min(0.99,
            base_rate * severity_modifier * adjustments['combined_factor']))

        # Calculate long-term survival (accounting for duration)
        long_term_survival = self._calculate_long_term_survival(
            immediate_survival, context)

        # Population-specific analysis
        population_analysis = self._analyze_population_survival(context)

        return {
            'immediate_survival_rate': immediate_survival,
            'long_term_survival_rate': long_term_survival,
            'expected_survivors': int(context.population_in_area * long_term_survival),
            'population_analysis': population_analysis,
            'factor_contributions': adjustments['individual_factors'],
            'confidence_level': self._calculate_confidence(context),
            'risk_factors': self._identify_key_risks(context),
            'survival_timeline': self._generate_survival_timeline(context)
        }

    def predict_regional(self, contexts: List[SurvivalContext]) -> Dict[str, Any]:
        """
        Predict survival across multiple regions.

        Args:
            contexts: List of SurvivalContext objects for different regions

        Returns:
            Aggregated regional survival analysis
        """
        regional_results = []
        total_population = 0
        total_survivors = 0

        for context in contexts:
            result = self.predict(context)
            regional_results.append({
                'context': context,
                'result': result
            })
            total_population += context.population_in_area
            total_survivors += result['expected_survivors']

        global_survival_rate = total_survivors / total_population if total_population > 0 else 0

        return {
            'global_survival_rate': global_survival_rate,
            'total_population': total_population,
            'total_survivors': total_survivors,
            'regional_breakdown': regional_results,
            'worst_affected_regions': self._identify_worst_regions(regional_results),
            'safest_regions': self._identify_safest_regions(regional_results)
        }

    def _calculate_factor_adjustments(self, context: SurvivalContext) -> Dict[str, Any]:
        """Calculate adjustments based on survival factors."""
        factors = {}
          # Distance factor (for localized events)
        distance_from_impact = getattr(context, 'distance_from_epicenter_km', None)
        if distance_from_impact is not None:
            distance_factor = min(1.0, distance_from_impact / 1000)
            factors[SurvivalFactors.DISTANCE_FROM_IMPACT] = distance_factor
        else:
            factors[SurvivalFactors.DISTANCE_FROM_IMPACT] = 0.5

        # Infrastructure resilience
        factors[SurvivalFactors.INFRASTRUCTURE_RESILIENCE] = 1.0 - context.infrastructure_damage

        # Food security
        factors[SurvivalFactors.FOOD_SECURITY] = 1.0 - context.food_system_disruption

        # Medical access
        factors[SurvivalFactors.MEDICAL_ACCESS] = 1.0 - context.medical_system_impact

        # Social cohesion
        factors[SurvivalFactors.SOCIAL_COHESION] = context.social_stability

        # Government preparedness (based on development level)
        prep_factor = context.geographic_factors.get('development_index', 0.5)
        factors[SurvivalFactors.GOVERNMENT_PREPAREDNESS] = prep_factor

        # Geographic location (climate, natural resources)
        geo_factor = (
            context.geographic_factors.get('climate_suitability', 0.5) +
            context.geographic_factors.get('natural_resources', 0.5)
        ) / 2
        factors[SurvivalFactors.GEOGRAPHIC_LOCATION] = geo_factor

        # Population density (lower density often better for survival)
        density_factor = max(0.1, 1.0 - (context.population_in_area / context.affected_area_km2) / 1000)
        factors[SurvivalFactors.POPULATION_DENSITY] = density_factor

        # Calculate weighted combination
        combined = sum(
            factors[factor] * self.factor_weights[factor]
            for factor in factors
        )

        return {
            'individual_factors': factors,
            'combined_factor': combined
        }

    def _get_severity_modifier(self, severity: int) -> float:
        """Get survival modifier based on event severity."""
        modifiers = {
            1: 0.95,  # Minimal impact
            2: 0.85,  # Local disaster
            3: 0.70,  # Regional catastrophe
            4: 0.50,  # Continental crisis
            5: 0.25,  # Global catastrophe
            6: 0.05   # Extinction-level event
        }
        return modifiers.get(severity, 0.50)

    def _calculate_long_term_survival(self, immediate_rate: float,
                                    context: SurvivalContext) -> float:
        """Calculate long-term survival accounting for duration effects."""
        # Survival decreases over time due to resource depletion, disease, etc.
        duration_factor = math.exp(-context.duration_years / 10)  # 10-year half-life

        # Additional factors for specific event types
        event_factors = {
            'pandemic': 0.9,  # Medical advances help
            'climate_collapse': 0.7,  # Gradual adaptation possible
            'nuclear_war': 0.6,  # Radiation and fallout effects
            'ai_extinction': 0.3,  # Little hope for recovery
            'gamma_ray_burst': 0.4  # Environmental damage persists
        }

        event_modifier = event_factors.get(context.event_type, 0.8)

        return immediate_rate * duration_factor * event_modifier

    def _analyze_population_survival(self, context: SurvivalContext) -> Dict[str, Any]:
        """Analyze survival by population demographics."""
        base_survival = self.predict(context)['long_term_survival_rate']

        # Age-based survival rates
        age_survival = {
            'children_0_15': base_survival * 0.8,  # More vulnerable
            'adults_16_64': base_survival * 1.0,   # Baseline
            'elderly_65_plus': base_survival * 0.6  # Most vulnerable
        }

        # Skills-based survival rates
        skill_survival = {
            'medical_professionals': base_survival * 1.3,
            'engineers_technicians': base_survival * 1.2,
            'farmers_food_producers': base_survival * 1.4,
            'military_security': base_survival * 1.1,
            'general_population': base_survival * 1.0
        }

        # Geographic survival differences
        location_survival = {
            'urban_centers': base_survival * 0.7,  # Resource competition
            'suburban_areas': base_survival * 1.0,  # Baseline
            'rural_areas': base_survival * 1.2,    # More self-sufficient
            'remote_areas': base_survival * 1.3    # Isolated but resilient
        }

        return {
            'by_age_group': age_survival,
            'by_skill_set': skill_survival,
            'by_location_type': location_survival
        }

    def _calculate_confidence(self, context: SurvivalContext) -> float:
        """Calculate confidence level in prediction."""
        # Higher confidence for well-studied scenarios
        confidence_by_type = {
            'asteroid': 0.8,
            'pandemic': 0.9,
            'climate_collapse': 0.7,
            'nuclear_war': 0.8,
            'supervolcano': 0.6,
            'gamma_ray_burst': 0.4,
            'ai_extinction': 0.3,
            'cosmic': 0.4
        }

        base_confidence = confidence_by_type.get(context.event_type, 0.5)

        # Adjust based on data quality
        data_quality_factors = [
            1.0 if context.population_in_area > 0 else 0.8,
            1.0 if context.affected_area_km2 > 0 else 0.8,
            1.0 if len(context.geographic_factors) > 2 else 0.9
        ]

        return float(base_confidence * np.prod(data_quality_factors))

    def _identify_key_risks(self, context: SurvivalContext) -> List[str]:
        """Identify primary risk factors for the scenario."""
        risks = []

        if context.infrastructure_damage > 0.7:
            risks.append("Critical infrastructure collapse")

        if context.food_system_disruption > 0.6:
            risks.append("Food system failure")

        if context.medical_system_impact > 0.5:
            risks.append("Healthcare system breakdown")

        if context.social_stability < 0.4:
            risks.append("Social disorder and conflict")

        if context.severity >= 5:
            risks.append("Cascading system failures")

        if context.duration_years > 5:
            risks.append("Long-term resource depletion")

        return risks

    def _generate_survival_timeline(self, context: SurvivalContext) -> Dict[str, float]:
        """Generate survival rate timeline."""
        timeline = {}
        base_rate = self.predict(context)['immediate_survival_rate']

        # Generate timeline for key periods
        periods = {
            '1_month': 0.95,
            '6_months': 0.85,
            '1_year': 0.75,
            '2_years': 0.65,
            '5_years': 0.50,
            '10_years': 0.40,
            '20_years': 0.35
        }

        for period, decay_factor in periods.items():
            timeline[period] = base_rate * decay_factor

        return timeline

    def _identify_worst_regions(self, regional_results: List[Dict]) -> List[Dict]:
        """Identify regions with lowest survival rates."""
        sorted_regions = sorted(
            regional_results,
            key=lambda x: x['result']['long_term_survival_rate']
        )
        return sorted_regions[:3]  # Return worst 3

    def _identify_safest_regions(self, regional_results: List[Dict]) -> List[Dict]:
        """Identify regions with highest survival rates."""
        sorted_regions = sorted(
            regional_results,
            key=lambda x: x['result']['long_term_survival_rate'],
            reverse=True
        )
        return sorted_regions[:3]  # Return best 3
