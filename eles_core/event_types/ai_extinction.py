import math
from typing import Dict, Any


class AIExtinction:
    """AI extinction scenario simulation class."""

    def __init__(self, ai_level: int, development_speed: float = 1.0,
                 alignment_probability: float = 0.5, control_measures: int = 3):
        """
        Initialize AI extinction parameters.

        Args:
            ai_level: AI capability level (1-10 scale)
            development_speed: Speed of AI development (multiplier)
            alignment_probability: Probability AI remains aligned (0-1)
            control_measures: Number of control measures in place (0-10)
        """
        self.ai_level = ai_level
        self.development_speed = development_speed
        self.alignment_probability = alignment_probability
        self.control_measures = control_measures

    def simulate(self) -> Dict[str, Any]:
        """Run AI extinction simulation."""
        results = {}

        # Basic parameters
        results['ai_level'] = self.ai_level
        results['development_speed'] = self.development_speed
        results['alignment_probability'] = self.alignment_probability
        results['control_measures'] = self.control_measures

        # Calculate risk factors
        risk_assessment = self._calculate_risk_assessment()
        results.update(risk_assessment)

        # Timeline analysis
        timeline = self._calculate_timeline()
        results.update(timeline)

        # Scenario outcomes
        scenarios = self._calculate_scenarios()
        results.update(scenarios)

        # Mitigation effectiveness
        mitigation = self._assess_mitigation()
        results.update(mitigation)

        return results

    def _calculate_risk_assessment(self) -> Dict[str, Any]:
        """Calculate AI risk assessment."""
        assessment = {}

        # Base risk from capability level
        capability_risk = min(1.0, self.ai_level / 10)

        # Development speed risk multiplier
        speed_risk_multiplier = math.log(self.development_speed + 1) + 1

        # Alignment risk
        misalignment_risk = 1 - self.alignment_probability

        # Control measures mitigation
        control_mitigation = min(0.9, self.control_measures / 10)

        # Combined extinction risk
        base_extinction_risk = capability_risk * misalignment_risk * speed_risk_multiplier
        mitigated_risk = base_extinction_risk * (1 - control_mitigation)

        assessment['capability_risk'] = capability_risk
        assessment['misalignment_risk'] = misalignment_risk
        assessment['extinction_probability'] = min(1.0, mitigated_risk)
        assessment['risk_level'] = self._get_risk_level(mitigated_risk)

        return assessment

    def _get_risk_level(self, risk: float) -> str:
        """Convert numerical risk to categorical level."""
        if risk > 0.7:
            return "Extinction-Level"
        elif risk > 0.5:
            return "Catastrophic"
        elif risk > 0.3:
            return "Severe"
        elif risk > 0.1:
            return "Moderate"
        else:
            return "Low"

    def _calculate_timeline(self) -> Dict[str, Any]:
        """Calculate development timeline."""
        timeline = {}

        # Time to AGI (Artificial General Intelligence)
        if self.ai_level >= 8:
            timeline['agi_timeline_years'] = 0  # Already achieved
        else:
            base_time = (8 - self.ai_level) * 5  # 5 years per level
            timeline['agi_timeline_years'] = max(1, int(base_time / self.development_speed))

        # Time to ASI (Artificial Superintelligence)
        if self.ai_level >= 10:
            timeline['asi_timeline_years'] = 0  # Already achieved
        else:
            agi_time = timeline['agi_timeline_years']
            asi_additional = (10 - max(8, self.ai_level)) * 2  # 2 years per level beyond AGI
            timeline['asi_timeline_years'] = agi_time + max(1, int(asi_additional / self.development_speed))

        # Critical decision window
        timeline['critical_window_years'] = min(5, timeline['agi_timeline_years'])

        return timeline

    def _calculate_scenarios(self) -> Dict[str, Any]:
        """Calculate different outcome scenarios."""
        scenarios = {}

        extinction_prob = self._calculate_risk_assessment()['extinction_probability']

        # Scenario probabilities
        scenarios['human_extinction_prob'] = extinction_prob * 0.8  # 80% of catastrophic outcomes = extinction
        scenarios['civilization_collapse_prob'] = extinction_prob * 0.15  # 15% = civilization collapse
        scenarios['dystopian_control_prob'] = extinction_prob * 0.05  # 5% = dystopian control
        scenarios['beneficial_outcome_prob'] = 1 - extinction_prob

        # Specific scenario descriptions
        if self.ai_level >= 9:
            scenarios['most_likely_scenario'] = self._get_high_capability_scenario()
        elif self.ai_level >= 6:
            scenarios['most_likely_scenario'] = self._get_moderate_capability_scenario()
        else:
            scenarios['most_likely_scenario'] = self._get_low_capability_scenario()

        return scenarios

    def _get_high_capability_scenario(self) -> str:
        """Get scenario for high AI capability."""
        if self.alignment_probability > 0.8:
            return "AI assists in solving global challenges, human flourishing"
        elif self.alignment_probability > 0.4:
            return "AI power struggle, partial human survival"
        else:
            return "Rapid human extinction via AI optimization"

    def _get_moderate_capability_scenario(self) -> str:
        """Get scenario for moderate AI capability."""
        if self.alignment_probability > 0.7:
            return "Gradual beneficial AI integration"
        elif self.alignment_probability > 0.3:
            return "AI-human conflict, technological disruption"
        else:
            return "Gradual human displacement and extinction"

    def _get_low_capability_scenario(self) -> str:
        """Get scenario for low AI capability."""
        if self.alignment_probability > 0.5:
            return "Narrow AI continues to benefit humanity"
        else:
            return "AI systems cause economic and social disruption"

    def _assess_mitigation(self) -> Dict[str, Any]:
        """Assess mitigation strategies."""
        mitigation = {}

        # Technical mitigation
        if self.control_measures >= 7:
            mitigation['technical_safety'] = "Strong safety measures implemented"
        elif self.control_measures >= 4:
            mitigation['technical_safety'] = "Moderate safety measures"
        else:
            mitigation['technical_safety'] = "Insufficient safety measures"

        # Governance mitigation
        if self.control_measures >= 6:
            mitigation['governance'] = "International AI governance frameworks"
        elif self.control_measures >= 3:
            mitigation['governance'] = "National AI regulations"
        else:
            mitigation['governance'] = "Minimal AI oversight"

        # Research priorities
        needed_research = []
        if self.alignment_probability < 0.7:
            needed_research.append("AI alignment research")
        if self.control_measures < 5:
            needed_research.append("AI safety verification")
            needed_research.append("Robustness testing")
        if self.ai_level > 6:
            needed_research.append("AI governance frameworks")

        mitigation['critical_research_areas'] = needed_research

        return mitigation

    def get_ai_capability_description(self) -> str:
        """Get description of AI capability level."""
        descriptions = {
            1: "Basic automation and simple pattern recognition",
            2: "Advanced pattern recognition, basic language processing",
            3: "Sophisticated language models, basic reasoning",
            4: "Multi-modal AI, advanced reasoning in specific domains",
            5: "Human-level performance in most cognitive tasks",
            6: "Superhuman performance in most domains",
            7: "Advanced general intelligence exceeding humans",
            8: "Artificial General Intelligence (AGI)",
            9: "Early Artificial Superintelligence (ASI)",
            10: "Advanced ASI with recursive self-improvement"
        }
        return descriptions.get(self.ai_level, "Unknown capability level")

    def get_historical_parallels(self) -> Dict[str, str]:
        """Get historical parallels for AI development."""
        return {
            'nuclear_weapons': 'Rapid development of world-ending technology',
            'industrial_revolution': 'Fundamental transformation of human society',
            'printing_press': 'Information revolution changing power structures',
            'fire_discovery': 'Technology that enabled human dominance'
        }

    def get_key_uncertainties(self) -> list:
        """Get key uncertainties in AI development."""
        uncertainties = [
            "Timeline to AGI achievement",
            "Difficulty of AI alignment",
            "Effectiveness of safety measures",
            "International cooperation on AI governance",
            "AI recursive self-improvement speed",
            "Economic disruption and social response"
        ]

        if self.ai_level >= 7:
            uncertainties.extend([
                "AI goal interpretation and implementation",
                "Human-AI coexistence possibilities"
            ])

        return uncertainties
