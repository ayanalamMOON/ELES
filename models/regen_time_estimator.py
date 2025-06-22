"""
Regeneration Time Estimator for E.L.E.S.

This module provides models for estimating recovery and regeneration times
following extinction-level events.
"""

import math
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class RecoveryPhase(Enum):
    """Phases of recovery following an extinction event."""
    IMMEDIATE_RESPONSE = "immediate_response"      # 0-1 years
    STABILIZATION = "stabilization"               # 1-5 years
    SHORT_TERM_RECOVERY = "short_term_recovery"   # 5-25 years
    MEDIUM_TERM_RECOVERY = "medium_term_recovery" # 25-100 years
    LONG_TERM_RECOVERY = "long_term_recovery"     # 100-1000 years
    ECOSYSTEM_RESTORATION = "ecosystem_restoration" # 1000+ years


class RecoverySystem(Enum):
    """Systems that need to recover after an extinction event."""
    POPULATION = "population"
    INFRASTRUCTURE = "infrastructure"
    ECONOMY = "economy"
    TECHNOLOGY = "technology"
    AGRICULTURE = "agriculture"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    GOVERNANCE = "governance"
    ECOSYSTEM = "ecosystem"
    CLIMATE = "climate"


@dataclass
class RecoveryContext:
    """Context information for recovery time estimation."""
    event_type: str
    severity: int
    initial_damage: Dict[str, float]  # System damage levels (0-1)
    surviving_population: int
    surviving_infrastructure: float  # Fraction remaining (0-1)
    available_resources: Dict[str, float]
    external_aid: float  # Level of external assistance (0-1)
    geographic_factors: Dict[str, float]
    technology_preservation: float  # Fraction of tech knowledge preserved (0-1)
    social_cohesion: float  # Level of social organization (0-1)


class RegenTimeEstimator:
    """
    Advanced recovery and regeneration time estimation model.

    Estimates recovery times for different systems and phases
    following extinction-level events.
    """

    def __init__(self):
        """Initialize the regeneration time estimator."""
        # Base recovery times (in years) for different systems at 50% damage
        self.base_recovery_times = {
            RecoverySystem.POPULATION: 50,
            RecoverySystem.INFRASTRUCTURE: 25,
            RecoverySystem.ECONOMY: 15,
            RecoverySystem.TECHNOLOGY: 30,
            RecoverySystem.AGRICULTURE: 10,
            RecoverySystem.HEALTHCARE: 20,
            RecoverySystem.EDUCATION: 35,
            RecoverySystem.GOVERNANCE: 12,
            RecoverySystem.ECOSYSTEM: 200,
            RecoverySystem.CLIMATE: 500
        }

        # Recovery scaling factors by event type
        self.event_scaling_factors = {
            'asteroid': {
                'infrastructure': 1.5,  # Physical damage
                'climate': 0.8,         # Temporary climate effects
                'ecosystem': 1.2
            },
            'supervolcano': {
                'climate': 3.0,         # Long-term climate effects
                'agriculture': 2.5,     # Ash and climate impact
                'ecosystem': 2.0
            },
            'pandemic': {
                'population': 2.0,      # Direct population impact
                'healthcare': 1.5,      # System strain
                'economy': 1.3
            },
            'climate_collapse': {
                'ecosystem': 5.0,       # Fundamental change
                'agriculture': 4.0,     # Crop system collapse
                'climate': 10.0         # Irreversible changes
            },
            'nuclear_war': {
                'infrastructure': 3.0,  # Massive destruction
                'technology': 2.0,      # Knowledge loss
                'population': 1.8
            },
            'ai_extinction': {
                'technology': 10.0,     # Tech dependence lost
                'governance': 5.0,      # Control systems
                'infrastructure': 3.0
            },
            'gamma_ray_burst': {
                'ecosystem': 8.0,       # Ozone/UV damage
                'agriculture': 4.0,     # Food chain collapse
                'climate': 2.0
            }
        }

        # Phase durations (baseline in years)
        self.phase_durations = {
            RecoveryPhase.IMMEDIATE_RESPONSE: 1,
            RecoveryPhase.STABILIZATION: 4,
            RecoveryPhase.SHORT_TERM_RECOVERY: 20,
            RecoveryPhase.MEDIUM_TERM_RECOVERY: 75,
            RecoveryPhase.LONG_TERM_RECOVERY: 900,
            RecoveryPhase.ECOSYSTEM_RESTORATION: 5000
        }

    def estimate(self, context: RecoveryContext) -> Dict[str, Any]:
        """
        Estimate comprehensive recovery times.

        Args:
            context: RecoveryContext with event and damage information

        Returns:
            Dictionary with recovery time estimates and analysis
        """
        # Calculate system-specific recovery times
        system_recovery = self._estimate_system_recovery(context)

        # Calculate phase-based recovery timeline
        phase_timeline = self._estimate_phase_timeline(context)

        # Calculate overall recovery metrics
        overall_metrics = self._calculate_overall_metrics(system_recovery, context)

        # Generate recovery scenarios
        scenarios = self._generate_recovery_scenarios(context, system_recovery)

        # Identify critical bottlenecks
        bottlenecks = self._identify_bottlenecks(system_recovery)

        return {
            'system_recovery_times': system_recovery,
            'phase_timeline': phase_timeline,
            'overall_metrics': overall_metrics,
            'recovery_scenarios': scenarios,
            'critical_bottlenecks': bottlenecks,
            'recovery_strategies': self._suggest_recovery_strategies(context, bottlenecks),
            'confidence_intervals': self._calculate_confidence_intervals(system_recovery)
        }

    def estimate_comparative(self, contexts: List[RecoveryContext]) -> Dict[str, Any]:
        """
        Compare recovery times across multiple scenarios.

        Args:
            contexts: List of RecoveryContext objects to compare

        Returns:
            Comparative recovery analysis
        """
        scenario_estimates = []

        for context in contexts:
            estimate = self.estimate(context)
            scenario_estimates.append({
                'context': context,
                'estimate': estimate
            })

        # Find fastest and slowest recovery scenarios
        sorted_by_total = sorted(
            scenario_estimates,
            key=lambda x: x['estimate']['overall_metrics']['total_recovery_time']
        )

        return {
            'scenario_comparisons': scenario_estimates,
            'fastest_recovery': sorted_by_total[0] if sorted_by_total else None,
            'slowest_recovery': sorted_by_total[-1] if sorted_by_total else None,
            'recovery_time_statistics': self._calculate_recovery_statistics(scenario_estimates)
        }

    def _estimate_system_recovery(self, context: RecoveryContext) -> Dict[str, Dict[str, float]]:
        """Estimate recovery times for each system."""
        system_times = {}

        for system in RecoverySystem:
            base_time = self.base_recovery_times[system]

            # Get damage level for this system
            damage_level = context.initial_damage.get(system.value, 0.5)

            # Apply damage scaling (exponential relationship)
            damage_scaling = math.exp(damage_level * 2)  # More damage = exponentially longer recovery

            # Apply event-specific scaling
            event_scaling = self.event_scaling_factors.get(context.event_type, {}).get(system.value, 1.0)

            # Apply context modifiers
            context_modifier = self._calculate_context_modifier(context, system)

            # Calculate final recovery time
            recovery_time = base_time * damage_scaling * event_scaling * context_modifier

            system_times[system.value] = {
                'base_time': base_time,
                'damage_scaling': damage_scaling,
                'event_scaling': event_scaling,
                'context_modifier': context_modifier,
                'total_time': recovery_time,
                'confidence': self._calculate_system_confidence(system, context)
            }

        return system_times

    def _estimate_phase_timeline(self, context: RecoveryContext) -> Dict[str, Dict[str, Any]]:
        """Estimate timeline for recovery phases."""
        phase_timeline = {}
        cumulative_time = 0

        for phase in RecoveryPhase:
            base_duration = self.phase_durations[phase]

            # Apply severity scaling
            severity_scaling = 1.0 + (context.severity - 3) * 0.5  # Scale around severity 3

            # Apply population and resource scaling
            population_factor = max(0.5, context.surviving_population / 1e8)  # Normalize to 100M
            resource_factor = np.mean(list(context.available_resources.values())) if context.available_resources else 0.5
              # Calculate phase duration
            phase_duration = base_duration * severity_scaling / (population_factor * resource_factor)

            phase_timeline[phase.value] = {
                'duration': phase_duration,
                'start_time': cumulative_time,
                'end_time': cumulative_time + phase_duration,
                'key_activities': self._get_phase_activities(phase, context),
                'success_probability': self._calculate_phase_success_probability(phase, context)
            }

            cumulative_time += phase_duration

        return phase_timeline

    def _calculate_overall_metrics(self, system_recovery: Dict, context: RecoveryContext) -> Dict[str, float]:
        """Calculate overall recovery metrics."""
        system_times = [data['total_time'] for data in system_recovery.values()]

        return {
            'total_recovery_time': max(system_times),  # Limited by slowest system
            'average_recovery_time': float(np.mean(system_times)),
            'critical_path_time': self._calculate_critical_path(system_recovery),
            'civilization_rebuild_time': self._estimate_civilization_rebuild(context, system_recovery),
            'population_recovery_time': system_recovery.get('population', {}).get('total_time', 100),
            'technology_recovery_time': system_recovery.get('technology', {}).get('total_time', 50)
        }

    def _calculate_context_modifier(self, context: RecoveryContext, system: RecoverySystem) -> float:
        """Calculate context-specific modifiers for recovery time."""
        modifier = 1.0

        # External aid factor
        aid_benefit = 1.0 - (context.external_aid * 0.3)  # Up to 30% reduction
        modifier *= aid_benefit

        # Social cohesion factor
        cohesion_benefit = 1.0 - (context.social_cohesion * 0.2)  # Up to 20% reduction
        modifier *= cohesion_benefit

        # Technology preservation factor (applies mainly to tech-dependent systems)
        if system in [RecoverySystem.TECHNOLOGY, RecoverySystem.INFRASTRUCTURE, RecoverySystem.HEALTHCARE]:
            tech_benefit = 1.0 - (context.technology_preservation * 0.4)  # Up to 40% reduction
            modifier *= tech_benefit

        # Geographic factors
        climate_factor = context.geographic_factors.get('climate_suitability', 0.5)
        resource_factor = context.geographic_factors.get('natural_resources', 0.5)
        geo_modifier = 2.0 - (climate_factor + resource_factor)  # Range 1.0-2.0
        modifier *= geo_modifier

        return max(0.1, modifier)  # Don't go below 10% of base time

    def _generate_recovery_scenarios(self, context: RecoveryContext,
                                   system_recovery: Dict) -> Dict[str, Dict[str, float]]:
        """Generate optimistic, realistic, and pessimistic recovery scenarios."""
        scenarios = {}

        # Get base recovery time
        base_time = max(data['total_time'] for data in system_recovery.values())

        scenarios['optimistic'] = {
            'description': 'Best-case scenario with ideal conditions',
            'total_time': base_time * 0.6,
            'assumptions': [
                'Maximum external aid',
                'High social cooperation',
                'Favorable environmental conditions',
                'Preserved critical knowledge'
            ]
        }

        scenarios['realistic'] = {
            'description': 'Most likely scenario based on current conditions',
            'total_time': base_time,
            'assumptions': [
                'Moderate external aid',
                'Average social cohesion',
                'Normal environmental variability',
                'Partial knowledge preservation'
            ]
        }

        scenarios['pessimistic'] = {
            'description': 'Worst-case scenario with additional complications',
            'total_time': base_time * 2.0,
            'assumptions': [
                'Limited external aid',
                'Social fragmentation',
                'Adverse environmental conditions',
                'Significant knowledge loss'
            ]
        }

        return scenarios

    def _identify_bottlenecks(self, system_recovery: Dict) -> List[Dict[str, Any]]:
        """Identify critical bottlenecks in recovery process."""
        bottlenecks = []

        # Sort systems by recovery time
        sorted_systems = sorted(
            system_recovery.items(),
            key=lambda x: x[1]['total_time'],
            reverse=True
        )

        # Top 3 slowest systems are potential bottlenecks
        for system_name, data in sorted_systems[:3]:
            bottlenecks.append({
                'system': system_name,
                'recovery_time': data['total_time'],
                'severity': 'critical' if data['total_time'] > 100 else 'moderate',
                'key_factors': self._identify_key_factors(system_name, data)
            })

        return bottlenecks

    def _suggest_recovery_strategies(self, context: RecoveryContext,
                                   bottlenecks: List[Dict]) -> List[str]:
        """Suggest strategies to accelerate recovery."""
        strategies = []

        for bottleneck in bottlenecks:
            system = bottleneck['system']

            if system == 'population':
                strategies.append("Prioritize healthcare and food security")
                strategies.append("Establish protected population centers")

            elif system == 'infrastructure':
                strategies.append("Focus on critical infrastructure first")
                strategies.append("Use modular and resilient designs")

            elif system == 'technology':
                strategies.append("Preserve and protect technical knowledge")
                strategies.append("Establish technology preservation centers")

            elif system == 'ecosystem':
                strategies.append("Implement ecosystem restoration programs")
                strategies.append("Protect remaining biodiversity hotspots")

        return strategies

    def _calculate_confidence_intervals(self, system_recovery: Dict) -> Dict[str, Tuple[float, float]]:
        """Calculate confidence intervals for recovery estimates."""
        intervals = {}

        for system, data in system_recovery.items():
            base_time = data['total_time']
            confidence = data['confidence']

            # Lower confidence = wider interval
            interval_width = base_time * (1.0 - confidence)

            intervals[system] = (
                max(0, base_time - interval_width),
                base_time + interval_width
            )

        return intervals

    def _calculate_system_confidence(self, system: RecoverySystem, context: RecoveryContext) -> float:
        """Calculate confidence level for system recovery estimate."""
        base_confidence = 0.7

        # Adjust based on available data
        if system.value in context.initial_damage:
            base_confidence += 0.1

        if system.value in context.available_resources:
            base_confidence += 0.1

        # Adjust based on event type (some are better understood)
        well_studied_events = ['pandemic', 'asteroid', 'nuclear_war']
        if context.event_type in well_studied_events:
            base_confidence += 0.1

        return min(1.0, base_confidence)

    def _get_phase_activities(self, phase: RecoveryPhase, context: RecoveryContext) -> List[str]:
        """Get key activities for each recovery phase."""
        activities = {
            RecoveryPhase.IMMEDIATE_RESPONSE: [
                "Emergency medical care",
                "Search and rescue operations",
                "Temporary shelter establishment",
                "Communication system restoration"
            ],
            RecoveryPhase.STABILIZATION: [
                "Food and water distribution",
                "Basic infrastructure repair",
                "Community organization",
                "Security establishment"
            ],
            RecoveryPhase.SHORT_TERM_RECOVERY: [
                "Housing reconstruction",
                "Economic system restart",
                "Education system restoration",
                "Local government re-establishment"
            ],
            RecoveryPhase.MEDIUM_TERM_RECOVERY: [
                "Industrial capacity rebuilding",
                "Trade network restoration",
                "Advanced infrastructure development",
                "Cultural institution rebuilding"
            ],
            RecoveryPhase.LONG_TERM_RECOVERY: [
                "Full economic development",
                "Advanced technology restoration",
                "International system rebuilding",
                "Quality of life improvements"
            ],
            RecoveryPhase.ECOSYSTEM_RESTORATION: [
                "Biodiversity restoration",
                "Climate stabilization",
                "Soil and water rehabilitation",
                "Natural habitat reconstruction"
            ]
        }

        return activities.get(phase, [])

    def _calculate_phase_success_probability(self, phase: RecoveryPhase, context: RecoveryContext) -> float:
        """Calculate probability of successfully completing each phase."""
        base_probabilities = {
            RecoveryPhase.IMMEDIATE_RESPONSE: 0.9,
            RecoveryPhase.STABILIZATION: 0.8,
            RecoveryPhase.SHORT_TERM_RECOVERY: 0.7,
            RecoveryPhase.MEDIUM_TERM_RECOVERY: 0.6,
            RecoveryPhase.LONG_TERM_RECOVERY: 0.5,
            RecoveryPhase.ECOSYSTEM_RESTORATION: 0.4
        }

        base_prob = base_probabilities.get(phase, 0.5)

        # Adjust based on context
        context_modifier = (
            context.social_cohesion * 0.3 +
            context.external_aid * 0.2 +
            context.technology_preservation * 0.2 +
            (context.surviving_population / 1e8) * 0.3  # Normalize to 100M
        )

        return min(1.0, base_prob + context_modifier - 0.5)

    def _calculate_critical_path(self, system_recovery: Dict) -> float:
        """Calculate critical path through interdependent systems."""
        # Simplified critical path - systems that depend on each other
        dependencies = {
            'governance': ['population'],
            'economy': ['population', 'infrastructure'],
            'technology': ['population', 'infrastructure', 'education'],
            'healthcare': ['infrastructure', 'technology'],
            'education': ['infrastructure', 'governance']
        }

        critical_time = 0
        for system, deps in dependencies.items():
            if system in system_recovery:
                system_time = system_recovery[system]['total_time']
                dep_time = max([
                    system_recovery.get(dep, {}).get('total_time', 0)
                    for dep in deps
                ] + [0])
                critical_time = max(critical_time, system_time + dep_time * 0.5)

        return critical_time

    def _estimate_civilization_rebuild(self, context: RecoveryContext, system_recovery: Dict) -> float:
        """Estimate time to rebuild technological civilization."""
        key_systems = ['population', 'infrastructure', 'technology', 'governance', 'economy']
        key_times = [
            system_recovery.get(system, {}).get('total_time', 100)
            for system in key_systems
        ]

        # Civilization rebuild requires all key systems
        base_rebuild_time = max(key_times)

        # Add time for integration and advanced development
        integration_time = base_rebuild_time * 0.3

        return base_rebuild_time + integration_time

    def _identify_key_factors(self, system_name: str, data: Dict) -> List[str]:
        """Identify key factors affecting system recovery time."""
        factors = []

        if data['damage_scaling'] > 2.0:
            factors.append("High initial damage")

        if data['event_scaling'] > 1.5:
            factors.append("Event-specific complications")

        if data['context_modifier'] > 1.2:
            factors.append("Unfavorable context conditions")

        if data['confidence'] < 0.6:
            factors.append("High uncertainty")

        return factors

    def _calculate_recovery_statistics(self, scenario_estimates: List[Dict]) -> Dict[str, float]:
        """Calculate statistics across recovery scenarios."""
        recovery_times = [
            estimate['estimate']['overall_metrics']['total_recovery_time']
            for estimate in scenario_estimates
        ]

        return {
            'mean_recovery_time': float(np.mean(recovery_times)),
            'median_recovery_time': float(np.median(recovery_times)),
            'std_recovery_time': float(np.std(recovery_times)),
            'min_recovery_time': float(np.min(recovery_times)),
            'max_recovery_time': float(np.max(recovery_times))
        }
