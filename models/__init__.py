"""
Models Module for E.L.E.S.

This module contains predictive models and risk assessment tools for the
Extinction-Level Event Simulator.

Models:
    - survival_predictor.py: Survival probability prediction models
    - risk_score_calculator.py: Risk assessment and scoring models
    - regen_time_estimator.py: Recovery time estimation models
"""

# Import main model classes
from .survival_predictor import (
    SurvivalPredictor,
    SurvivalContext,
    SurvivalFactors
)

from .risk_score_calculator import (
    RiskScoreCalculator,
    RiskProfile,
    RiskCategory
)

from .regen_time_estimator import (
    RegenTimeEstimator,
    RecoveryContext,
    RecoveryPhase,
    RecoverySystem
)

# Version information
__version__ = "0.1.0"

# Module description
__description__ = "Predictive models and risk assessment tools for E.L.E.S."

# Export public API
__all__ = [
    # Main model classes
    'SurvivalPredictor',
    'RiskScoreCalculator',
    'RegenTimeEstimator',

    # Context and data classes
    'SurvivalContext',
    'RiskProfile',
    'RecoveryContext',

    # Enums
    'SurvivalFactors',
    'RiskCategory',
    'RecoveryPhase',
    'RecoverySystem'
]

# Convenience functions
def create_survival_predictor() -> SurvivalPredictor:
    """Create a new SurvivalPredictor instance."""
    return SurvivalPredictor()

def create_risk_calculator() -> RiskScoreCalculator:
    """Create a new RiskScoreCalculator instance."""
    return RiskScoreCalculator()

def create_regen_estimator() -> RegenTimeEstimator:
    """Create a new RegenTimeEstimator instance."""
    return RegenTimeEstimator()

def get_model_info() -> dict:
    """Get information about available models."""
    return {
        'survival_predictor': {
            'description': 'Predicts human survival probabilities under extinction scenarios',
            'class': 'SurvivalPredictor'
        },
        'risk_calculator': {
            'description': 'Calculates comprehensive risk scores for extinction events',
            'class': 'RiskScoreCalculator'
        },
        'regen_estimator': {
            'description': 'Estimates recovery and regeneration times post-extinction',
            'class': 'RegenTimeEstimator'
        }
    }
