"""
Tactical Metric Normalization & Advanced Analytics Engine
Implements:
- Sigrid Turnbull Possession-Adjusted (PAdj) Defensive Action Calculations
- Passes Per Defensive Action (PPDA)
- Percentile Ranking & Metric Scaling across League Baselines
- Net Delta & Tactical Superiority Evaluations
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional

METRIC_DEFINITIONS = {
    # Attacking
    "npxg_per_90": {
        "name": "Non-Penalty xG / 90",
        "category": "Attacking",
        "description": "Expected goals created from open play and non-penalty set pieces per 90 mins.",
        "higher_is_better": True,
        "format": "{:.2f}",
        "unit": "xG"
    },
    "shot_quality_xg_per_shot": {
        "name": "Shot Quality (xG/Shot)",
        "category": "Attacking",
        "description": "Average expected goal value per shot taken. Reflects shot selection and chance quality.",
        "higher_is_better": True,
        "format": "{:.3f}",
        "unit": "xG"
    },
    "box_touches_per_90": {
        "name": "Penalty Box Touches / 90",
        "category": "Attacking",
        "description": "Touches inside the opponent's 18-yard penalty box per 90 mins.",
        "higher_is_better": True,
        "format": "{:.1f}",
        "unit": "touches"
    },
    "field_tilt_pct": {
        "name": "Field Tilt %",
        "category": "Attacking",
        "description": "Share of total passes made in the attacking final third (territorial dominance).",
        "higher_is_better": True,
        "format": "{:.1f}%",
        "unit": "%"
    },
    "xt_per_90": {
        "name": "Expected Threat (xT) / 90",
        "category": "Attacking",
        "description": "Net progressive threat generated through passing and carrying actions moving ball to dangerous zones.",
        "higher_is_better": True,
        "format": "{:.2f}",
        "unit": "xT"
    },

    # Possession & Buildup
    "deep_completions_per_90": {
        "name": "Deep Completions / 90",
        "category": "Possession",
        "description": "Non-cross passes completed within 20m of the opponent's goal line.",
        "higher_is_better": True,
        "format": "{:.1f}",
        "unit": "passes"
    },
    "direct_speed_ms": {
        "name": "Direct Speed (m/s)",
        "category": "Possession",
        "description": "Pace of forward ball progression in meters per second during sustained sequences.",
        "higher_is_better": False,  # Lower indicates patient positional play, higher indicates vertical counter-attack
        "format": "{:.2f}",
        "unit": "m/s"
    },
    "pass_success_under_pressure_pct": {
        "name": "Pass Success Under Pressure %",
        "category": "Possession",
        "description": "Retention accuracy when the passer is actively challenged by opponent within 3m.",
        "higher_is_better": True,
        "format": "{:.1f}%",
        "unit": "%"
    },
    "progressive_passes_per_90": {
        "name": "Progressive Passes / 90",
        "category": "Possession",
        "description": "Completed passes that advance the ball towards the opponent's goal by >= 10m (or into penalty area).",
        "higher_is_better": True,
        "format": "{:.1f}",
        "unit": "passes"
    },

    # Defensive & Pressing
    "ppda": {
        "name": "PPDA (Passes Per Defensive Action)",
        "category": "Defending",
        "description": "Opponent passes allowed per defensive action in opponent's defensive 60%. Lower = more aggressive press.",
        "higher_is_better": False,  # Lower PPDA = higher press intensity
        "format": "{:.1f}",
        "unit": "passes"
    },
    "defensive_line_height_m": {
        "name": "Defensive Line Height (m)",
        "category": "Defending",
        "description": "Average distance (meters from own goal line) where defensive actions and offside lines originate.",
        "higher_is_better": True,
        "format": "{:.1f}m",
        "unit": "m"
    },
    "padj_interceptions_tackles_per_90": {
        "name": "PAdj Interceptions + Tackles / 90",
        "category": "Defending",
        "description": "Tackles and interceptions standardized to 50% possession using Sigrid Turnbull formula.",
        "higher_is_better": True,
        "format": "{:.1f}",
        "unit": "actions"
    },
    "high_turnovers_per_90": {
        "name": "High Turnovers Won / 90",
        "category": "Defending",
        "description": "Possession regains won within 40m of the opponent's goal line.",
        "higher_is_better": True,
        "format": "{:.1f}",
        "unit": "regains"
    },
    "xga_per_90": {
        "name": "Expected Goals Against (xGA) / 90",
        "category": "Defending",
        "description": "Expected goals conceded from opponent chances per 90 mins.",
        "higher_is_better": False,  # Lower conceded is better
        "format": "{:.2f}",
        "unit": "xGA"
    }
}


def calculate_padj(raw_stat: float, team_possession_pct: float) -> float:
    """
    Computes Possession-Adjusted (PAdj) metric using Sigrid Turnbull methodology:
        PAdj Metric = (Raw Metric / Opponent Possession %) * 50%
    where Opponent Possession % = 100 - team_possession_pct.
    """
    opp_possession = max(5.0, 100.0 - team_possession_pct)
    padj = (raw_stat / opp_possession) * 50.0
    return round(float(padj), 2)


def compute_percentiles(df: pd.DataFrame, metric_keys: List[str]) -> pd.DataFrame:
    """
    Computes percentile ranks (0 - 100) for given metrics across the league dataset.
    Takes into account whether lower or higher values represent better performance.
    """
    percentile_df = pd.DataFrame(index=df.index)
    
    for key in metric_keys:
        if key not in df.columns:
            continue
        meta = METRIC_DEFINITIONS.get(key, {})
        higher_better = meta.get("higher_is_better", True)
        
        # Rank: min_rank to 100
        # For lower_is_better (e.g. PPDA, xGA), we invert so 100 = best in league
        if higher_better:
            percentile_df[key] = df[key].rank(pct=True) * 100.0
        else:
            percentile_df[key] = (1.0 - df[key].rank(pct=True) + (1.0 / len(df))) * 100.0
            percentile_df[key] = percentile_df[key].clip(lower=1.0, upper=99.9)
            
    return percentile_df.round(1)


def compare_teams_metrics(team_a_data: Dict[str, Any], team_b_data: Dict[str, Any], 
                          league_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Generates structured comparison between Team A and Team B with percentiles and net deltas.
    """
    metric_keys = list(METRIC_DEFINITIONS.keys())
    percentile_df = compute_percentiles(league_df, metric_keys)
    
    team_a_id = team_a_data["id"]
    team_b_id = team_b_data["id"]
    
    results = []
    
    for key in metric_keys:
        meta = METRIC_DEFINITIONS[key]
        val_a = team_a_data["metrics"].get(key, 0.0)
        val_b = team_b_data["metrics"].get(key, 0.0)
        
        pct_a = float(percentile_df.loc[team_a_id, key]) if team_a_id in percentile_df.index else 50.0
        pct_b = float(percentile_df.loc[team_b_id, key]) if team_b_id in percentile_df.index else 50.0
        
        delta = val_a - val_b
        higher_better = meta.get("higher_is_better", True)
        
        # Determine advantage
        if abs(delta) < 1e-4:
            advantage = "Neutral"
        elif higher_better:
            advantage = team_a_data["name"] if delta > 0 else team_b_data["name"]
        else:
            advantage = team_a_data["name"] if delta < 0 else team_b_data["name"]
            
        results.append({
            "key": key,
            "name": meta["name"],
            "category": meta["category"],
            "description": meta["description"],
            "unit": meta["unit"],
            "higher_is_better": higher_better,
            "format": meta["format"],
            "val_a": val_a,
            "val_b": val_b,
            "pct_a": pct_a,
            "pct_b": pct_b,
            "delta": round(float(delta), 2),
            "pct_delta": round(float(pct_a - pct_b), 1),
            "advantage": advantage
        })
        
    return results
