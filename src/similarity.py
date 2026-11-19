"""
Tactical Similarity Engine
Normalizes team metric vectors via z-score and computes Cosine & Euclidean distances
to identify tactical twins and stylistic analogues across the dataset.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

SIMILARITY_FEATURE_KEYS = [
    "npxg_per_90",
    "shot_quality_xg_per_shot",
    "box_touches_per_90",
    "field_tilt_pct",
    "xt_per_90",
    "deep_completions_per_90",
    "direct_speed_ms",
    "pass_success_under_pressure_pct",
    "progressive_passes_per_90",
    "ppda",
    "defensive_line_height_m",
    "padj_interceptions_tackles_per_90",
    "high_turnovers_per_90",
    "xga_per_90"
]


class TeamSimilarityEngine:
    def __init__(self, league_df: pd.DataFrame, team_metadata: Dict[str, Dict[str, Any]]):
        self.raw_df = league_df.copy()
        self.team_metadata = team_metadata
        self.feature_keys = [k for k in SIMILARITY_FEATURE_KEYS if k in self.raw_df.columns]
        
        self.scaler = StandardScaler()
        self.z_scores = pd.DataFrame(
            self.scaler.fit_transform(self.raw_df[self.feature_keys]),
            index=self.raw_df.index,
            columns=self.feature_keys
        )
        
        # Precompute pair-wise matrices
        self.cosine_matrix = pd.DataFrame(
            cosine_similarity(self.z_scores),
            index=self.raw_df.index,
            columns=self.raw_df.index
        )
        self.euclidean_matrix = pd.DataFrame(
            euclidean_distances(self.z_scores),
            index=self.raw_df.index,
            columns=self.raw_df.index
        )

    def find_top_similar(self, team_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Returns top_k most tactically similar teams based on cosine similarity and Euclidean distance.
        """
        if team_id not in self.z_scores.index:
            return []
            
        target_z = self.z_scores.loc[team_id]
        results = []
        
        # Max euclidean distance across the dataset for normalization
        max_euclid = float(self.euclidean_matrix.values.max()) or 1.0
        
        for candidate_id in self.raw_df.index:
            if candidate_id == team_id:
                continue
                
            cos_sim = float(self.cosine_matrix.loc[team_id, candidate_id])
            # Bound cosine similarity between -1 and 1, convert to match percentage 0-100%
            match_pct = max(0.0, min(100.0, ((cos_sim + 1.0) / 2.0) * 100.0))
            
            euclid_dist = float(self.euclidean_matrix.loc[team_id, candidate_id])
            # Euclidean proximity score (1 - normalized distance)
            euclid_proximity = max(0.0, min(100.0, (1.0 - (euclid_dist / max_euclid)) * 100.0))
            
            # Harmonic blend score: 70% Cosine (directional style), 30% Euclidean (magnitude)
            composite_score = round(0.7 * match_pct + 0.3 * euclid_proximity, 1)
            
            cand_meta = self.team_metadata.get(candidate_id, {})
            cand_z = self.z_scores.loc[candidate_id]
            
            # Find top 2 metrics where they are closest in z-space
            z_diffs = (target_z - cand_z).abs().sort_values()
            closest_traits = [z_diffs.index[0], z_diffs.index[1]]
            
            results.append({
                "team_id": candidate_id,
                "team_name": cand_meta.get("name", candidate_id),
                "league": cand_meta.get("league", "League"),
                "country": cand_meta.get("country", ""),
                "badge_color": cand_meta.get("primary_color", "#10b981"),
                "manager": cand_meta.get("manager", "Tactician"),
                "tactical_archetype": cand_meta.get("archetype", "Balanced"),
                "cosine_similarity": round(cos_sim, 4),
                "match_percentage": round(match_pct, 1),
                "euclidean_distance": round(euclid_dist, 2),
                "composite_score": composite_score,
                "shared_traits": closest_traits
            })
            
        results.sort(key=lambda x: x["composite_score"], reverse=True)
        return results[:top_k]
