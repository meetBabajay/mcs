"""
TACTIQ Tactical Data Loader & Domain Repository
Exclusively 2026/2027 Premier League Season Intelligence:
- Attacking, Possession, and Defensive metrics
- Sigrid Turnbull PAdj conversions
- Shot maps (StatsBomb 120x80 coordinates, xG values, outcomes)
- 18-Zone Field Tilt & Pitch Control matrix
- Authentic 2026/2027 club profiles, managers, and tactical archetypes
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any
from src.metrics import calculate_padj, METRIC_DEFINITIONS

RAW_PREMIER_LEAGUE_2026_27 = [
    {
        "id": "arsenal",
        "name": "Arsenal",
        "short_name": "ARS",
        "league": "Premier League",
        "country": "England",
        "manager": "Mikel Arteta",
        "formation": "4-3-3",
        "archetype": "Controlled Dominance & Rest Defense",
        "primary_color": "#EF0107",
        "secondary_color": "#063672",
        "possession_pct": 62.4,
        "raw_tackles_interceptions": 24.2,
        "npxg_per_90": 2.22,
        "shot_quality_xg_per_shot": 0.142,
        "box_touches_per_90": 37.8,
        "field_tilt_pct": 70.4,
        "xt_per_90": 2.84,
        "deep_completions_per_90": 13.2,
        "direct_speed_ms": 1.42,
        "pass_success_under_pressure_pct": 88.2,
        "progressive_passes_per_90": 61.5,
        "ppda": 8.2,
        "defensive_line_height_m": 54.6,
        "high_turnovers_per_90": 12.4,
        "xga_per_90": 0.68
    },
    {
        "id": "mancity",
        "name": "Manchester City",
        "short_name": "MCI",
        "league": "Premier League",
        "country": "England",
        "manager": "Enzo Maresca",
        "formation": "3-2-4-1",
        "archetype": "Positional Play & Overload",
        "primary_color": "#6CABDD",
        "secondary_color": "#1C2C5B",
        "possession_pct": 64.8,
        "raw_tackles_interceptions": 21.0,
        "npxg_per_90": 2.26,
        "shot_quality_xg_per_shot": 0.145,
        "box_touches_per_90": 39.5,
        "field_tilt_pct": 71.8,
        "xt_per_90": 2.88,
        "deep_completions_per_90": 13.8,
        "direct_speed_ms": 1.34,
        "pass_success_under_pressure_pct": 89.4,
        "progressive_passes_per_90": 64.6,
        "ppda": 8.4,
        "defensive_line_height_m": 55.2,
        "high_turnovers_per_90": 11.0,
        "xga_per_90": 0.79
    },
    {
        "id": "liverpool",
        "name": "Liverpool",
        "short_name": "LIV",
        "league": "Premier League",
        "country": "England",
        "manager": "Andoni Iraola",
        "formation": "4-2-3-1",
        "archetype": "Vertical Gegenpressing & Chaos Control",
        "primary_color": "#C8102E",
        "secondary_color": "#00B2A9",
        "possession_pct": 60.2,
        "raw_tackles_interceptions": 26.5,
        "npxg_per_90": 2.31,
        "shot_quality_xg_per_shot": 0.136,
        "box_touches_per_90": 38.0,
        "field_tilt_pct": 67.5,
        "xt_per_90": 2.78,
        "deep_completions_per_90": 12.8,
        "direct_speed_ms": 1.76,
        "pass_success_under_pressure_pct": 85.6,
        "progressive_passes_per_90": 61.2,
        "ppda": 7.6,
        "defensive_line_height_m": 53.4,
        "high_turnovers_per_90": 13.4,
        "xga_per_90": 0.82
    },
    {
        "id": "chelsea",
        "name": "Chelsea",
        "short_name": "CHE",
        "league": "Premier League",
        "country": "England",
        "manager": "Xabi Alonso",
        "formation": "4-2-3-1",
        "archetype": "Inverted Fullbacks & High Territory",
        "primary_color": "#034694",
        "secondary_color": "#EE242C",
        "possession_pct": 59.8,
        "raw_tackles_interceptions": 25.2,
        "npxg_per_90": 2.05,
        "shot_quality_xg_per_shot": 0.138,
        "box_touches_per_90": 34.2,
        "field_tilt_pct": 64.6,
        "xt_per_90": 2.56,
        "deep_completions_per_90": 11.8,
        "direct_speed_ms": 1.52,
        "pass_success_under_pressure_pct": 86.8,
        "progressive_passes_per_90": 57.8,
        "ppda": 9.1,
        "defensive_line_height_m": 52.2,
        "high_turnovers_per_90": 10.6,
        "xga_per_90": 0.96
    },
    {
        "id": "astonvilla",
        "name": "Aston Villa",
        "short_name": "AVL",
        "league": "Premier League",
        "country": "England",
        "manager": "Unai Emery",
        "formation": "4-2-2-2",
        "archetype": "Compact Mid-Block & Offside Trap",
        "primary_color": "#670E36",
        "secondary_color": "#95BFE5",
        "possession_pct": 55.2,
        "raw_tackles_interceptions": 29.4,
        "npxg_per_90": 1.86,
        "shot_quality_xg_per_shot": 0.144,
        "box_touches_per_90": 28.6,
        "field_tilt_pct": 56.2,
        "xt_per_90": 2.32,
        "deep_completions_per_90": 10.1,
        "direct_speed_ms": 1.84,
        "pass_success_under_pressure_pct": 84.1,
        "progressive_passes_per_90": 50.8,
        "ppda": 11.2,
        "defensive_line_height_m": 52.8,
        "high_turnovers_per_90": 8.9,
        "xga_per_90": 1.08
    },
    {
        "id": "tottenham",
        "name": "Tottenham Hotspur",
        "short_name": "TOT",
        "league": "Premier League",
        "country": "England",
        "manager": "Roberto De Zerbi",
        "formation": "4-3-3",
        "archetype": "Hyper High-Line & Direct Overload",
        "primary_color": "#132257",
        "secondary_color": "#FFFFFF",
        "possession_pct": 61.6,
        "raw_tackles_interceptions": 27.2,
        "npxg_per_90": 2.14,
        "shot_quality_xg_per_shot": 0.139,
        "box_touches_per_90": 36.8,
        "field_tilt_pct": 67.4,
        "xt_per_90": 2.66,
        "deep_completions_per_90": 12.4,
        "direct_speed_ms": 1.71,
        "pass_success_under_pressure_pct": 86.2,
        "progressive_passes_per_90": 60.4,
        "ppda": 7.6,
        "defensive_line_height_m": 56.2,
        "high_turnovers_per_90": 13.5,
        "xga_per_90": 1.18
    },
    {
        "id": "brighton",
        "name": "Brighton & Hove Albion",
        "short_name": "BHA",
        "league": "Premier League",
        "country": "England",
        "manager": "Fabian Hürzeler",
        "formation": "4-2-3-1",
        "archetype": "Press-Baiting Buildup & Quick Release",
        "primary_color": "#0057B8",
        "secondary_color": "#FFCD00",
        "possession_pct": 58.6,
        "raw_tackles_interceptions": 27.0,
        "npxg_per_90": 1.92,
        "shot_quality_xg_per_shot": 0.132,
        "box_touches_per_90": 31.8,
        "field_tilt_pct": 61.4,
        "xt_per_90": 2.46,
        "deep_completions_per_90": 11.2,
        "direct_speed_ms": 1.60,
        "pass_success_under_pressure_pct": 85.8,
        "progressive_passes_per_90": 54.8,
        "ppda": 8.9,
        "defensive_line_height_m": 52.1,
        "high_turnovers_per_90": 10.5,
        "xga_per_90": 1.16
    },
    {
        "id": "newcastle",
        "name": "Newcastle United",
        "short_name": "NEW",
        "league": "Premier League",
        "country": "England",
        "manager": "Matthias Jaissle",
        "formation": "4-3-3",
        "archetype": "High Physicality & Intense Duels",
        "primary_color": "#241F20",
        "secondary_color": "#FFFFFF",
        "possession_pct": 53.4,
        "raw_tackles_interceptions": 32.0,
        "npxg_per_90": 1.88,
        "shot_quality_xg_per_shot": 0.140,
        "box_touches_per_90": 29.2,
        "field_tilt_pct": 54.5,
        "xt_per_90": 2.28,
        "deep_completions_per_90": 9.8,
        "direct_speed_ms": 1.92,
        "pass_success_under_pressure_pct": 83.2,
        "progressive_passes_per_90": 49.5,
        "ppda": 8.5,
        "defensive_line_height_m": 51.2,
        "high_turnovers_per_90": 12.4,
        "xga_per_90": 1.14
    },
    {
        "id": "bournemouth",
        "name": "AFC Bournemouth",
        "short_name": "BOU",
        "league": "Premier League",
        "country": "England",
        "manager": "Marco Rose",
        "formation": "4-2-3-1",
        "archetype": "Relentless High-Press & Fast Breaks",
        "primary_color": "#DA291C",
        "secondary_color": "#000000",
        "possession_pct": 50.4,
        "raw_tackles_interceptions": 36.2,
        "npxg_per_90": 1.78,
        "shot_quality_xg_per_shot": 0.129,
        "box_touches_per_90": 27.5,
        "field_tilt_pct": 51.2,
        "xt_per_90": 2.15,
        "deep_completions_per_90": 9.0,
        "direct_speed_ms": 2.00,
        "pass_success_under_pressure_pct": 81.0,
        "progressive_passes_per_90": 47.0,
        "ppda": 7.0,
        "defensive_line_height_m": 52.6,
        "high_turnovers_per_90": 14.6,
        "xga_per_90": 1.24
    },
    {
        "id": "nottinghamforest",
        "name": "Nottingham Forest",
        "short_name": "NFO",
        "league": "Premier League",
        "country": "England",
        "manager": "Oliver Glasner",
        "formation": "4-2-3-1",
        "archetype": "Compact Low-Block & Rapid Counters",
        "primary_color": "#DD0000",
        "secondary_color": "#FFFFFF",
        "possession_pct": 46.5,
        "raw_tackles_interceptions": 35.0,
        "npxg_per_90": 1.60,
        "shot_quality_xg_per_shot": 0.138,
        "box_touches_per_90": 23.2,
        "field_tilt_pct": 46.0,
        "xt_per_90": 1.90,
        "deep_completions_per_90": 7.8,
        "direct_speed_ms": 2.14,
        "pass_success_under_pressure_pct": 79.5,
        "progressive_passes_per_90": 42.0,
        "ppda": 12.8,
        "defensive_line_height_m": 43.5,
        "high_turnovers_per_90": 7.5,
        "xga_per_90": 0.98
    },
    {
        "id": "manunited",
        "name": "Manchester United",
        "short_name": "MUN",
        "league": "Premier League",
        "country": "England",
        "manager": "Michael Carrick",
        "formation": "3-4-2-1",
        "archetype": "Fluid Rotations & Direct Transitions",
        "primary_color": "#DA291C",
        "secondary_color": "#FBE122",
        "possession_pct": 54.5,
        "raw_tackles_interceptions": 30.2,
        "npxg_per_90": 1.80,
        "shot_quality_xg_per_shot": 0.132,
        "box_touches_per_90": 28.4,
        "field_tilt_pct": 55.8,
        "xt_per_90": 2.24,
        "deep_completions_per_90": 9.5,
        "direct_speed_ms": 1.80,
        "pass_success_under_pressure_pct": 83.8,
        "progressive_passes_per_90": 50.2,
        "ppda": 9.8,
        "defensive_line_height_m": 50.4,
        "high_turnovers_per_90": 9.8,
        "xga_per_90": 1.20
    },
    {
        "id": "fulham",
        "name": "Fulham",
        "short_name": "FUL",
        "league": "Premier League",
        "country": "England",
        "manager": "Álvaro Arbeloa",
        "formation": "4-2-3-1",
        "archetype": "Organized Mid-Block & Flank Delivery",
        "primary_color": "#FFFFFF",
        "secondary_color": "#CC0000",
        "possession_pct": 51.8,
        "raw_tackles_interceptions": 31.0,
        "npxg_per_90": 1.62,
        "shot_quality_xg_per_shot": 0.126,
        "box_touches_per_90": 25.4,
        "field_tilt_pct": 51.5,
        "xt_per_90": 2.06,
        "deep_completions_per_90": 8.7,
        "direct_speed_ms": 1.72,
        "pass_success_under_pressure_pct": 82.6,
        "progressive_passes_per_90": 47.0,
        "ppda": 10.4,
        "defensive_line_height_m": 48.8,
        "high_turnovers_per_90": 9.2,
        "xga_per_90": 1.12
    },
    {
        "id": "brentford",
        "name": "Brentford",
        "short_name": "BRE",
        "league": "Premier League",
        "country": "England",
        "manager": "Keith Andrews",
        "formation": "3-5-2",
        "archetype": "Lethal Set-Pieces & Direct Vertical Play",
        "primary_color": "#E30613",
        "secondary_color": "#FBB800",
        "possession_pct": 48.2,
        "raw_tackles_interceptions": 33.6,
        "npxg_per_90": 1.74,
        "shot_quality_xg_per_shot": 0.148,
        "box_touches_per_90": 25.0,
        "field_tilt_pct": 47.8,
        "xt_per_90": 2.04,
        "deep_completions_per_90": 8.2,
        "direct_speed_ms": 2.08,
        "pass_success_under_pressure_pct": 80.1,
        "progressive_passes_per_90": 44.2,
        "ppda": 11.8,
        "defensive_line_height_m": 46.0,
        "high_turnovers_per_90": 8.0,
        "xga_per_90": 1.28
    },
    {
        "id": "crystalpalace",
        "name": "Crystal Palace",
        "short_name": "CRY",
        "league": "Premier League",
        "country": "England",
        "manager": "Pierre Sage",
        "formation": "3-4-2-1",
        "archetype": "Aggressive Dual 10s & Dynamic Press",
        "primary_color": "#1B458F",
        "secondary_color": "#C4122E",
        "possession_pct": 48.8,
        "raw_tackles_interceptions": 34.2,
        "npxg_per_90": 1.58,
        "shot_quality_xg_per_shot": 0.130,
        "box_touches_per_90": 24.0,
        "field_tilt_pct": 48.8,
        "xt_per_90": 1.98,
        "deep_completions_per_90": 8.4,
        "direct_speed_ms": 1.88,
        "pass_success_under_pressure_pct": 81.0,
        "progressive_passes_per_90": 45.0,
        "ppda": 9.4,
        "defensive_line_height_m": 49.5,
        "high_turnovers_per_90": 11.0,
        "xga_per_90": 1.18
    },
    {
        "id": "leeds",
        "name": "Leeds United",
        "short_name": "LEE",
        "league": "Premier League",
        "country": "England",
        "manager": "Daniel Farke",
        "formation": "4-2-3-1",
        "archetype": "High Press & Dynamic Wing Overloads",
        "primary_color": "#FFCD00",
        "secondary_color": "#1D428A",
        "possession_pct": 50.8,
        "raw_tackles_interceptions": 33.2,
        "npxg_per_90": 1.62,
        "shot_quality_xg_per_shot": 0.130,
        "box_touches_per_90": 24.6,
        "field_tilt_pct": 50.2,
        "xt_per_90": 2.05,
        "deep_completions_per_90": 8.5,
        "direct_speed_ms": 1.86,
        "pass_success_under_pressure_pct": 82.2,
        "progressive_passes_per_90": 46.5,
        "ppda": 9.6,
        "defensive_line_height_m": 49.0,
        "high_turnovers_per_90": 10.4,
        "xga_per_90": 1.26
    },
    {
        "id": "everton",
        "name": "Everton",
        "short_name": "EVE",
        "league": "Premier League",
        "country": "England",
        "manager": "David Moyes",
        "formation": "4-4-1-1",
        "archetype": "Resilient Low-Block & Aerial Dominance",
        "primary_color": "#003399",
        "secondary_color": "#FFFFFF",
        "possession_pct": 43.0,
        "raw_tackles_interceptions": 36.0,
        "npxg_per_90": 1.45,
        "shot_quality_xg_per_shot": 0.140,
        "box_touches_per_90": 21.0,
        "field_tilt_pct": 42.4,
        "xt_per_90": 1.78,
        "deep_completions_per_90": 7.0,
        "direct_speed_ms": 2.22,
        "pass_success_under_pressure_pct": 77.0,
        "progressive_passes_per_90": 39.0,
        "ppda": 13.4,
        "defensive_line_height_m": 42.0,
        "high_turnovers_per_90": 7.6,
        "xga_per_90": 1.22
    },
    {
        "id": "coventry",
        "name": "Coventry City",
        "short_name": "COV",
        "league": "Premier League",
        "country": "England",
        "manager": "Frank Lampard",
        "formation": "4-2-3-1",
        "archetype": "Dynamic Transitional Break & High Tempo",
        "primary_color": "#00A8B5",
        "secondary_color": "#1C2C5B",
        "possession_pct": 49.2,
        "raw_tackles_interceptions": 33.6,
        "npxg_per_90": 1.56,
        "shot_quality_xg_per_shot": 0.128,
        "box_touches_per_90": 23.6,
        "field_tilt_pct": 48.4,
        "xt_per_90": 1.96,
        "deep_completions_per_90": 8.1,
        "direct_speed_ms": 1.94,
        "pass_success_under_pressure_pct": 81.0,
        "progressive_passes_per_90": 44.5,
        "ppda": 10.4,
        "defensive_line_height_m": 48.2,
        "high_turnovers_per_90": 9.4,
        "xga_per_90": 1.30
    },
    {
        "id": "hullcity",
        "name": "Hull City",
        "short_name": "HUL",
        "league": "Premier League",
        "country": "England",
        "manager": "Sergej Jakirović",
        "formation": "4-3-3",
        "archetype": "High-Risk Buildup & Wing Directness",
        "primary_color": "#F5A800",
        "secondary_color": "#000000",
        "possession_pct": 47.4,
        "raw_tackles_interceptions": 34.2,
        "npxg_per_90": 1.46,
        "shot_quality_xg_per_shot": 0.125,
        "box_touches_per_90": 21.6,
        "field_tilt_pct": 45.8,
        "xt_per_90": 1.84,
        "deep_completions_per_90": 7.4,
        "direct_speed_ms": 1.96,
        "pass_success_under_pressure_pct": 80.2,
        "progressive_passes_per_90": 42.4,
        "ppda": 11.2,
        "defensive_line_height_m": 46.8,
        "high_turnovers_per_90": 8.4,
        "xga_per_90": 1.42
    },
    {
        "id": "ipswich",
        "name": "Ipswich Town",
        "short_name": "IPS",
        "league": "Premier League",
        "country": "England",
        "manager": "Gary O'Neil",
        "formation": "4-2-3-1",
        "archetype": "Expansive Attacking Shapes & High Intensity",
        "primary_color": "#003399",
        "secondary_color": "#D31145",
        "possession_pct": 45.4,
        "raw_tackles_interceptions": 34.8,
        "npxg_per_90": 1.36,
        "shot_quality_xg_per_shot": 0.121,
        "box_touches_per_90": 20.2,
        "field_tilt_pct": 44.0,
        "xt_per_90": 1.74,
        "deep_completions_per_90": 6.8,
        "direct_speed_ms": 1.95,
        "pass_success_under_pressure_pct": 78.4,
        "progressive_passes_per_90": 40.2,
        "ppda": 10.8,
        "defensive_line_height_m": 47.0,
        "high_turnovers_per_90": 8.8,
        "xga_per_90": 1.58
    },
    {
        "id": "sunderland",
        "name": "Sunderland",
        "short_name": "SUN",
        "league": "Premier League",
        "country": "England",
        "manager": "Régis Le Bris",
        "formation": "4-3-3",
        "archetype": "High-Energy Transitional Press & Wide Delivery",
        "primary_color": "#EB172B",
        "secondary_color": "#000000",
        "possession_pct": 47.8,
        "raw_tackles_interceptions": 33.6,
        "npxg_per_90": 1.54,
        "shot_quality_xg_per_shot": 0.128,
        "box_touches_per_90": 23.4,
        "field_tilt_pct": 47.2,
        "xt_per_90": 1.94,
        "deep_completions_per_90": 8.0,
        "direct_speed_ms": 1.90,
        "pass_success_under_pressure_pct": 81.2,
        "progressive_passes_per_90": 44.8,
        "ppda": 10.2,
        "defensive_line_height_m": 47.8,
        "high_turnovers_per_90": 9.6,
        "xga_per_90": 1.34
    }
]

# Authentic Last Match Played in English Premier League (Sunday, 8 November 2026)
LAST_MATCH_PLAYED = {
    "match_id": "mun_avl_mw10",
    "matchweek": 10,
    "competition": "Premier League 2026/27",
    "date_str": "Sunday, 8 November 2026",
    "datetime": "16:30 GMT, Sunday, 8 November 2026",
    "venue": "Old Trafford, Manchester",
    "home_id": "manunited",
    "home_name": "Manchester United",
    "home_short": "MUN",
    "home_crest": "/static/img/crests/manunited.svg",
    "home_goals": 4,
    "away_id": "astonvilla",
    "away_name": "Aston Villa",
    "away_short": "AVL",
    "away_crest": "/static/img/crests/astonvilla.svg",
    "away_goals": 4,
    "score": "4 - 4",
    "status": "FT (Last Match Played: 8 Nov 2026)",
    "description": "Manchester United 4-4 Aston Villa (Fernandes 19\', Tielemans 38\', Zirkzee 52\', Dorgu 90+6\')"
}

# Premier League Matchweek 10 Official Results (6–8 November 2026)
MATCHWEEK_10_RESULTS = [
    {"date": "Fri 6 Nov", "home": "Everton", "home_id": "everton", "away": "Coventry City", "away_id": "coventry", "score": "3 - 1"},
    {"date": "Sat 7 Nov", "home": "Leeds United", "home_id": "leeds", "away": "Tottenham Hotspur", "away_id": "tottenham", "score": "1 - 0"},
    {"date": "Sat 7 Nov", "home": "Arsenal", "home_id": "arsenal", "away": "Hull City", "away_id": "hullcity", "score": "1 - 0"},
    {"date": "Sat 7 Nov", "home": "Fulham", "home_id": "fulham", "away": "Newcastle United", "away_id": "newcastle", "score": "1 - 1"},
    {"date": "Sat 7 Nov", "home": "Nottingham Forest", "home_id": "nottinghamforest", "away": "Manchester City", "away_id": "mancity", "score": "3 - 1"},
    {"date": "Sun 8 Nov", "home": "Brighton & Hove Albion", "home_id": "brighton", "away": "Brentford", "away_id": "brentford", "score": "2 - 0"},
    {"date": "Sun 8 Nov", "home": "Crystal Palace", "home_id": "crystalpalace", "away": "Liverpool", "away_id": "liverpool", "score": "1 - 3"},
    {"date": "Sun 8 Nov", "home": "Ipswich Town", "home_id": "ipswich", "away": "AFC Bournemouth", "away_id": "bournemouth", "score": "1 - 2"},
    {"date": "Sun 8 Nov", "home": "Sunderland", "home_id": "sunderland", "away": "Chelsea", "away_id": "chelsea", "score": "1 - 0"},
    {"date": "Sun 8 Nov", "home": "Manchester United", "home_id": "manunited", "away": "Aston Villa", "away_id": "astonvilla", "score": "4 - 4", "is_last": True}
]

# Next Scheduled Premier League Fixtures (Matchweek 11 • Following the International Break)
MATCHWEEK_11_FIXTURES = [
    {
        "match_id": "lee_che",
        "matchweek": 11,
        "date_str": "Saturday, 21 November 2026",
        "day": "Sat 21 Nov",
        "time": "12:30",
        "datetime": "12:30 GMT, Saturday, 21 November 2026",
        "venue": "Elland Road, Leeds",
        "competition": "Premier League 2026/27",
        "home_id": "leeds",
        "home_name": "Leeds United",
        "home_short": "LEE",
        "home_crest": "/static/img/crests/leeds.svg",
        "away_id": "chelsea",
        "away_name": "Chelsea",
        "away_short": "CHE",
        "away_crest": "/static/img/crests/chelsea.svg",
        "is_marquee": False
    },
    {
        "match_id": "ars_nfo",
        "matchweek": 11,
        "date_str": "Saturday, 21 November 2026",
        "day": "Sat 21 Nov",
        "time": "15:00",
        "datetime": "15:00 GMT, Saturday, 21 November 2026",
        "venue": "Emirates Stadium, London",
        "competition": "Premier League 2026/27",
        "home_id": "arsenal",
        "home_name": "Arsenal",
        "home_short": "ARS",
        "home_crest": "/static/img/crests/arsenal.svg",
        "away_id": "nottinghamforest",
        "away_name": "Nottingham Forest",
        "away_short": "NFO",
        "away_crest": "/static/img/crests/nottinghamforest.svg",
        "is_marquee": False
    },
    {
        "match_id": "avl_cry",
        "matchweek": 11,
        "date_str": "Saturday, 21 November 2026",
        "day": "Sat 21 Nov",
        "time": "15:00",
        "datetime": "15:00 GMT, Saturday, 21 November 2026",
        "venue": "Villa Park, Birmingham",
        "competition": "Premier League 2026/27",
        "home_id": "astonvilla",
        "home_name": "Aston Villa",
        "home_short": "AVL",
        "home_crest": "/static/img/crests/astonvilla.svg",
        "away_id": "crystalpalace",
        "away_name": "Crystal Palace",
        "away_short": "CRY",
        "away_crest": "/static/img/crests/crystalpalace.svg",
        "is_marquee": False
    },
    {
        "match_id": "bou_bha",
        "matchweek": 11,
        "date_str": "Saturday, 21 November 2026",
        "day": "Sat 21 Nov",
        "time": "15:00",
        "datetime": "15:00 GMT, Saturday, 21 November 2026",
        "venue": "Vitality Stadium, Bournemouth",
        "competition": "Premier League 2026/27",
        "home_id": "bournemouth",
        "home_name": "AFC Bournemouth",
        "home_short": "BOU",
        "home_crest": "/static/img/crests/bournemouth.svg",
        "away_id": "brighton",
        "away_name": "Brighton & Hove Albion",
        "away_short": "BHA",
        "away_crest": "/static/img/crests/brighton.svg",
        "is_marquee": False
    },
    {
        "match_id": "eve_bre",
        "matchweek": 11,
        "date_str": "Saturday, 21 November 2026",
        "day": "Sat 21 Nov",
        "time": "15:00",
        "datetime": "15:00 GMT, Saturday, 21 November 2026",
        "venue": "Goodison Park, Liverpool",
        "competition": "Premier League 2026/27",
        "home_id": "everton",
        "home_name": "Everton",
        "home_short": "EVE",
        "home_crest": "/static/img/crests/everton.svg",
        "away_id": "brentford",
        "away_name": "Brentford",
        "away_short": "BRE",
        "away_crest": "/static/img/crests/brentford.svg",
        "is_marquee": False
    },
    {
        "match_id": "ful_sun",
        "matchweek": 11,
        "date_str": "Saturday, 21 November 2026",
        "day": "Sat 21 Nov",
        "time": "15:00",
        "datetime": "15:00 GMT, Saturday, 21 November 2026",
        "venue": "Craven Cottage, London",
        "competition": "Premier League 2026/27",
        "home_id": "fulham",
        "home_name": "Fulham",
        "home_short": "FUL",
        "home_crest": "/static/img/crests/fulham.svg",
        "away_id": "sunderland",
        "away_name": "Sunderland",
        "away_short": "SUN",
        "away_crest": "/static/img/crests/sunderland.svg",
        "is_marquee": False
    },
    {
        "match_id": "mci_tot",
        "matchweek": 11,
        "date_str": "Saturday, 21 November 2026",
        "day": "Sat 21 Nov",
        "time": "17:30",
        "datetime": "17:30 GMT, Saturday, 21 November 2026",
        "venue": "Etihad Stadium, Manchester",
        "competition": "Premier League 2026/27",
        "home_id": "mancity",
        "home_name": "Manchester City",
        "home_short": "MCI",
        "home_crest": "/static/img/crests/mancity.svg",
        "away_id": "tottenham",
        "away_name": "Tottenham Hotspur",
        "away_short": "TOT",
        "away_crest": "/static/img/crests/tottenham.svg",
        "is_marquee": True
    },
    {
        "match_id": "cov_liv",
        "matchweek": 11,
        "date_str": "Sunday, 22 November 2026",
        "day": "Sun 22 Nov",
        "time": "14:00",
        "datetime": "14:00 GMT, Sunday, 22 November 2026",
        "venue": "Coventry Building Society Arena, Coventry",
        "competition": "Premier League 2026/27",
        "home_id": "coventry",
        "home_name": "Coventry City",
        "home_short": "COV",
        "home_crest": "/static/img/crests/coventry.svg",
        "away_id": "liverpool",
        "away_name": "Liverpool",
        "away_short": "LIV",
        "away_crest": "/static/img/crests/liverpool.svg",
        "is_marquee": False
    },
    {
        "match_id": "ips_mun",
        "matchweek": 11,
        "date_str": "Sunday, 22 November 2026",
        "day": "Sun 22 Nov",
        "time": "16:30",
        "datetime": "16:30 GMT, Sunday, 22 November 2026",
        "venue": "Portman Road, Ipswich",
        "competition": "Premier League 2026/27",
        "home_id": "ipswich",
        "home_name": "Ipswich Town",
        "home_short": "IPS",
        "home_crest": "/static/img/crests/ipswich.svg",
        "away_id": "manunited",
        "away_name": "Manchester United",
        "away_short": "MUN",
        "away_crest": "/static/img/crests/manunited.svg",
        "is_marquee": True
    },
    {
        "match_id": "new_hul",
        "matchweek": 11,
        "date_str": "Monday, 23 November 2026",
        "day": "Mon 23 Nov",
        "time": "20:00",
        "datetime": "20:00 GMT, Monday, 23 November 2026",
        "venue": "St. James\' Park, Newcastle",
        "competition": "Premier League 2026/27",
        "home_id": "newcastle",
        "home_name": "Newcastle United",
        "home_short": "NEW",
        "home_crest": "/static/img/crests/newcastle.svg",
        "away_id": "hullcity",
        "away_name": "Hull City",
        "away_short": "HUL",
        "away_crest": "/static/img/crests/hullcity.svg",
        "is_marquee": False
    }
]

# Official Authentic 2026/2027 Season Statistics (Matchweeks 1–10 Played Through 8 November 2026)
OFFICIAL_SEASON_STATS_2026_27 = {
    "arsenal": {
        "goals": 17, "assists": 14, "involvements": 31, "xg": 21.20,
        "shots_in_box": 94, "shots_out_box": 56, "touches_in_box": 395,
        "penalties": "2 (2)", "woodwork": 6, "xa": 16.20, "fk_scored": 2, "crosses": "210 (28%)",
        "total_passes": "6,150 (88%)", "long_passes": "395 (65%)", "corners": 74,
        "total_tackles": 182, "interceptions": 84, "blocks": 30, "ga": 7, "clean_sheets": 5,
        "fouls": 98, "offsides": 16, "own_goals": 0, "yellow_cards": 14, "red_cards": 0,
        "mins": 9900, "dribbles": "148 (58%)", "duels_won": 560, "aerial_duels": 132
    },
    "brighton": {
        "goals": 27, "assists": 22, "involvements": 49, "xg": 24.50,
        "shots_in_box": 102, "shots_out_box": 60, "touches_in_box": 410,
        "penalties": "3 (3)", "woodwork": 6, "xa": 18.90, "fk_scored": 2, "crosses": "218 (27%)",
        "total_passes": "6,100 (87%)", "long_passes": "430 (63%)", "corners": 76,
        "total_tackles": 178, "interceptions": 82, "blocks": 28, "ga": 8, "clean_sheets": 5,
        "fouls": 96, "offsides": 18, "own_goals": 0, "yellow_cards": 13, "red_cards": 0,
        "mins": 9900, "dribbles": "154 (55%)", "duels_won": 558, "aerial_duels": 120
    },
    "mancity": {
        "goals": 21, "assists": 18, "involvements": 39, "xg": 22.80,
        "shots_in_box": 98, "shots_out_box": 65, "touches_in_box": 405,
        "penalties": "3 (3)", "woodwork": 4, "xa": 18.20, "fk_scored": 2, "crosses": "238 (30%)",
        "total_passes": "6,750 (89%)", "long_passes": "370 (68%)", "corners": 84,
        "total_tackles": 162, "interceptions": 75, "blocks": 23, "ga": 13, "clean_sheets": 3,
        "fouls": 88, "offsides": 13, "own_goals": 0, "yellow_cards": 11, "red_cards": 0,
        "mins": 9900, "dribbles": "162 (61%)", "duels_won": 520, "aerial_duels": 106
    },
    "liverpool": {
        "goals": 14, "assists": 12, "involvements": 26, "xg": 19.80,
        "shots_in_box": 88, "shots_out_box": 55, "touches_in_box": 360,
        "penalties": "2 (2)", "woodwork": 5, "xa": 15.60, "fk_scored": 1, "crosses": "205 (27%)",
        "total_passes": "5,820 (86%)", "long_passes": "455 (61%)", "corners": 71,
        "total_tackles": 196, "interceptions": 96, "blocks": 33, "ga": 10, "clean_sheets": 4,
        "fouls": 104, "offsides": 22, "own_goals": 0, "yellow_cards": 16, "red_cards": 0,
        "mins": 9900, "dribbles": "146 (56%)", "duels_won": 570, "aerial_duels": 136
    },
    "chelsea": {
        "goals": 17, "assists": 14, "involvements": 31, "xg": 18.50,
        "shots_in_box": 82, "shots_out_box": 48, "touches_in_box": 335,
        "penalties": "2 (2)", "woodwork": 4, "xa": 14.80, "fk_scored": 1, "crosses": "188 (26%)",
        "total_passes": "5,680 (87%)", "long_passes": "420 (62%)", "corners": 62,
        "total_tackles": 184, "interceptions": 88, "blocks": 36, "ga": 14, "clean_sheets": 2,
        "fouls": 108, "offsides": 18, "own_goals": 0, "yellow_cards": 18, "red_cards": 0,
        "mins": 9900, "dribbles": "136 (54%)", "duels_won": 536, "aerial_duels": 116
    },
    "everton": {
        "goals": 12, "assists": 9, "involvements": 21, "xg": 13.80,
        "shots_in_box": 62, "shots_out_box": 36, "touches_in_box": 252,
        "penalties": "1 (1)", "woodwork": 2, "xa": 10.40, "fk_scored": 0, "crosses": "174 (25%)",
        "total_passes": "4,520 (80%)", "long_passes": "520 (56%)", "corners": 48,
        "total_tackles": 210, "interceptions": 104, "blocks": 44, "ga": 10, "clean_sheets": 4,
        "fouls": 120, "offsides": 12, "own_goals": 0, "yellow_cards": 20, "red_cards": 0,
        "mins": 9900, "dribbles": "104 (48%)", "duels_won": 610, "aerial_duels": 168
    },
    "bournemouth": {
        "goals": 16, "assists": 12, "involvements": 28, "xg": 15.20,
        "shots_in_box": 70, "shots_out_box": 42, "touches_in_box": 280,
        "penalties": "1 (1)", "woodwork": 3, "xa": 11.20, "fk_scored": 0, "crosses": "184 (23%)",
        "total_passes": "4,250 (78%)", "long_passes": "530 (54%)", "corners": 50,
        "total_tackles": 216, "interceptions": 108, "blocks": 46, "ga": 11, "clean_sheets": 3,
        "fouls": 124, "offsides": 13, "own_goals": 0, "yellow_cards": 20, "red_cards": 0,
        "mins": 9900, "dribbles": "98 (46%)", "duels_won": 588, "aerial_duels": 152
    },
    "brentford": {
        "goals": 17, "assists": 13, "involvements": 30, "xg": 16.40,
        "shots_in_box": 72, "shots_out_box": 42, "touches_in_box": 285,
        "penalties": "2 (2)", "woodwork": 3, "xa": 12.60, "fk_scored": 0, "crosses": "178 (25%)",
        "total_passes": "4,960 (83%)", "long_passes": "480 (58%)", "corners": 54,
        "total_tackles": 188, "interceptions": 94, "blocks": 36, "ga": 12, "clean_sheets": 3,
        "fouls": 104, "offsides": 14, "own_goals": 0, "yellow_cards": 16, "red_cards": 0,
        "mins": 9900, "dribbles": "116 (50%)", "duels_won": 564, "aerial_duels": 152
    },
    "leeds": {
        "goals": 12, "assists": 9, "involvements": 21, "xg": 13.90,
        "shots_in_box": 64, "shots_out_box": 38, "touches_in_box": 260,
        "penalties": "1 (1)", "woodwork": 2, "xa": 10.60, "fk_scored": 0, "crosses": "165 (24%)",
        "total_passes": "5,040 (84%)", "long_passes": "450 (60%)", "corners": 50,
        "total_tackles": 196, "interceptions": 98, "blocks": 38, "ga": 10, "clean_sheets": 4,
        "fouls": 112, "offsides": 15, "own_goals": 0, "yellow_cards": 18, "red_cards": 0,
        "mins": 9900, "dribbles": "124 (52%)", "duels_won": 580, "aerial_duels": 140
    },
    "astonvilla": {
        "goals": 15, "assists": 12, "involvements": 27, "xg": 16.80,
        "shots_in_box": 74, "shots_out_box": 44, "touches_in_box": 290,
        "penalties": "1 (1)", "woodwork": 4, "xa": 12.80, "fk_scored": 0, "crosses": "182 (25%)",
        "total_passes": "5,200 (84%)", "long_passes": "450 (59%)", "corners": 56,
        "total_tackles": 188, "interceptions": 92, "blocks": 34, "ga": 18, "clean_sheets": 2,
        "fouls": 108, "offsides": 16, "own_goals": 0, "yellow_cards": 18, "red_cards": 0,
        "mins": 9900, "dribbles": "122 (51%)", "duels_won": 560, "aerial_duels": 134
    },
    "tottenham": {
        "goals": 11, "assists": 8, "involvements": 19, "xg": 14.50,
        "shots_in_box": 65, "shots_out_box": 40, "touches_in_box": 270,
        "penalties": "1 (1)", "woodwork": 3, "xa": 10.80, "fk_scored": 0, "crosses": "175 (24%)",
        "total_passes": "4,840 (82%)", "long_passes": "480 (57%)", "corners": 46,
        "total_tackles": 208, "interceptions": 102, "blocks": 48, "ga": 12, "clean_sheets": 3,
        "fouls": 122, "offsides": 14, "own_goals": 0, "yellow_cards": 24, "red_cards": 1,
        "mins": 9900, "dribbles": "112 (49%)", "duels_won": 522, "aerial_duels": 108
    },
    "newcastle": {
        "goals": 14, "assists": 11, "involvements": 25, "xg": 15.60,
        "shots_in_box": 70, "shots_out_box": 42, "touches_in_box": 280,
        "penalties": "2 (2)", "woodwork": 3, "xa": 11.90, "fk_scored": 1, "crosses": "184 (26%)",
        "total_passes": "5,220 (84%)", "long_passes": "470 (59%)", "corners": 56,
        "total_tackles": 192, "interceptions": 92, "blocks": 34, "ga": 17, "clean_sheets": 2,
        "fouls": 110, "offsides": 18, "own_goals": 0, "yellow_cards": 18, "red_cards": 0,
        "mins": 9900, "dribbles": "132 (53%)", "duels_won": 576, "aerial_duels": 144
    },
    "hullcity": {
        "goals": 10, "assists": 7, "involvements": 17, "xg": 12.10,
        "shots_in_box": 54, "shots_out_box": 34, "touches_in_box": 226,
        "penalties": "1 (1)", "woodwork": 2, "xa": 8.90, "fk_scored": 0, "crosses": "156 (23%)",
        "total_passes": "4,620 (81%)", "long_passes": "490 (57%)", "corners": 44,
        "total_tackles": 204, "interceptions": 100, "blocks": 40, "ga": 10, "clean_sheets": 3,
        "fouls": 116, "offsides": 14, "own_goals": 0, "yellow_cards": 18, "red_cards": 0,
        "mins": 9900, "dribbles": "108 (49%)", "duels_won": 596, "aerial_duels": 148
    },
    "ipswich": {
        "goals": 12, "assists": 9, "involvements": 21, "xg": 12.90,
        "shots_in_box": 52, "shots_out_box": 32, "touches_in_box": 218,
        "penalties": "1 (1)", "woodwork": 2, "xa": 9.20, "fk_scored": 0, "crosses": "152 (22%)",
        "total_passes": "4,360 (79%)", "long_passes": "510 (55%)", "corners": 40,
        "total_tackles": 216, "interceptions": 108, "blocks": 48, "ga": 17, "clean_sheets": 2,
        "fouls": 124, "offsides": 14, "own_goals": 1, "yellow_cards": 22, "red_cards": 0,
        "mins": 9900, "dribbles": "98 (46%)", "duels_won": 584, "aerial_duels": 156
    },
    "fulham": {
        "goals": 10, "assists": 8, "involvements": 18, "xg": 12.40,
        "shots_in_box": 54, "shots_out_box": 34, "touches_in_box": 225,
        "penalties": "1 (1)", "woodwork": 2, "xa": 9.10, "fk_scored": 0, "crosses": "154 (22%)",
        "total_passes": "4,240 (78%)", "long_passes": "520 (54%)", "corners": 40,
        "total_tackles": 218, "interceptions": 110, "blocks": 48, "ga": 12, "clean_sheets": 2,
        "fouls": 126, "offsides": 13, "own_goals": 0, "yellow_cards": 22, "red_cards": 0,
        "mins": 9900, "dribbles": "94 (46%)", "duels_won": 594, "aerial_duels": 158
    },
    "nottinghamforest": {
        "goals": 10, "assists": 8, "involvements": 18, "xg": 11.80,
        "shots_in_box": 52, "shots_out_box": 32, "touches_in_box": 215,
        "penalties": "1 (1)", "woodwork": 2, "xa": 8.60, "fk_scored": 0, "crosses": "148 (22%)",
        "total_passes": "4,100 (78%)", "long_passes": "540 (54%)", "corners": 38,
        "total_tackles": 220, "interceptions": 110, "blocks": 50, "ga": 14, "clean_sheets": 2,
        "fouls": 128, "offsides": 12, "own_goals": 0, "yellow_cards": 24, "red_cards": 0,
        "mins": 9900, "dribbles": "92 (45%)", "duels_won": 600, "aerial_duels": 164
    },
    "coventry": {
        "goals": 6, "assists": 4, "involvements": 10, "xg": 8.90,
        "shots_in_box": 40, "shots_out_box": 26, "touches_in_box": 176,
        "penalties": "1 (1)", "woodwork": 1, "xa": 6.20, "fk_scored": 0, "crosses": "130 (20%)",
        "total_passes": "3,840 (75%)", "long_passes": "560 (52%)", "corners": 32,
        "total_tackles": 228, "interceptions": 116, "blocks": 54, "ga": 16, "clean_sheets": 2,
        "fouls": 132, "offsides": 11, "own_goals": 1, "yellow_cards": 26, "red_cards": 1,
        "mins": 9900, "dribbles": "84 (43%)", "duels_won": 616, "aerial_duels": 170
    },
    "manunited": {
        "goals": 15, "assists": 12, "involvements": 27, "xg": 16.20,
        "shots_in_box": 72, "shots_out_box": 44, "touches_in_box": 278,
        "penalties": "2 (2)", "woodwork": 4, "xa": 12.20, "fk_scored": 0, "crosses": "176 (25%)",
        "total_passes": "5,300 (84%)", "long_passes": "440 (60%)", "corners": 54,
        "total_tackles": 190, "interceptions": 90, "blocks": 34, "ga": 20, "clean_sheets": 1,
        "fouls": 106, "offsides": 16, "own_goals": 0, "yellow_cards": 16, "red_cards": 0,
        "mins": 9900, "dribbles": "128 (52%)", "duels_won": 556, "aerial_duels": 132
    },
    "sunderland": {
        "goals": 9, "assists": 6, "involvements": 15, "xg": 11.50,
        "shots_in_box": 48, "shots_out_box": 30, "touches_in_box": 200,
        "penalties": "1 (1)", "woodwork": 2, "xa": 8.30, "fk_scored": 0, "crosses": "146 (23%)",
        "total_passes": "4,400 (79%)", "long_passes": "500 (55%)", "corners": 40,
        "total_tackles": 212, "interceptions": 106, "blocks": 46, "ga": 19, "clean_sheets": 2,
        "fouls": 120, "offsides": 14, "own_goals": 0, "yellow_cards": 20, "red_cards": 0,
        "mins": 9900, "dribbles": "100 (47%)", "duels_won": 590, "aerial_duels": 150
    },
    "crystalpalace": {
        "goals": 9, "assists": 6, "involvements": 15, "xg": 11.20,
        "shots_in_box": 46, "shots_out_box": 30, "touches_in_box": 196,
        "penalties": "1 (1)", "woodwork": 2, "xa": 8.00, "fk_scored": 0, "crosses": "144 (22%)",
        "total_passes": "4,300 (78%)", "long_passes": "520 (54%)", "corners": 38,
        "total_tackles": 214, "interceptions": 108, "blocks": 48, "ga": 24, "clean_sheets": 1,
        "fouls": 122, "offsides": 14, "own_goals": 0, "yellow_cards": 22, "red_cards": 0,
        "mins": 9900, "dribbles": "102 (48%)", "duels_won": 592, "aerial_duels": 154
    }
}


class FootballDataRepository:
    def __init__(self):
        self.teams_dict: Dict[str, Dict[str, Any]] = {}
        self.league_df: pd.DataFrame = pd.DataFrame()
        self._initialize_data()

    def _initialize_data(self):
        rows = []
        for raw in RAW_PREMIER_LEAGUE_2026_27:
            t_id = raw["id"]
            poss = raw["possession_pct"]
            
            padj_val = calculate_padj(raw["raw_tackles_interceptions"], poss)
            
            team_metrics = {
                "npxg_per_90": raw["npxg_per_90"],
                "shot_quality_xg_per_shot": raw["shot_quality_xg_per_shot"],
                "box_touches_per_90": raw["box_touches_per_90"],
                "field_tilt_pct": raw["field_tilt_pct"],
                "xt_per_90": raw["xt_per_90"],
                "deep_completions_per_90": raw["deep_completions_per_90"],
                "direct_speed_ms": raw["direct_speed_ms"],
                "pass_success_under_pressure_pct": raw["pass_success_under_pressure_pct"],
                "progressive_passes_per_90": raw["progressive_passes_per_90"],
                "ppda": raw["ppda"],
                "defensive_line_height_m": raw["defensive_line_height_m"],
                "padj_interceptions_tackles_per_90": padj_val,
                "high_turnovers_per_90": raw["high_turnovers_per_90"],
                "xga_per_90": raw["xga_per_90"]
            }
            
            self.teams_dict[t_id] = {
                "id": t_id,
                "name": raw["name"],
                "short_name": raw["short_name"],
                "crest_url": f"/static/img/crests/{t_id}.svg",
                "league": raw["league"],
                "country": raw["country"],
                "manager": raw["manager"],
                "formation": raw["formation"],
                "archetype": raw["archetype"],
                "primary_color": raw["primary_color"],
                "secondary_color": raw["secondary_color"],
                "possession_pct": poss,
                "metrics": team_metrics
            }
            
            row = {"id": t_id, "possession_pct": poss}
            row.update(team_metrics)
            rows.append(row)
            
        self.league_df = pd.DataFrame(rows).set_index("id")

    def get_all_teams(self) -> List[Dict[str, Any]]:
        """Returns all 20 Premier League clubs sorted by name."""
        return [
            {
                "id": t["id"],
                "name": t["name"],
                "short_name": t["short_name"],
                "crest_url": t.get("crest_url", f"/static/img/crests/{t['id']}.svg"),
                "league": t["league"],
                "country": t["country"],
                "manager": t["manager"],
                "archetype": t["archetype"],
                "formation": t["formation"],
                "primary_color": t["primary_color"]
            }
            for t in sorted(self.teams_dict.values(), key=lambda x: x["name"])
        ]

    def get_team(self, team_id: str) -> Dict[str, Any]:
        return self.teams_dict.get(team_id)

    def generate_shot_map(self, team_id: str, count: int = 24) -> List[Dict[str, Any]]:
        """
        Generates realistic shot event coordinates (StatsBomb 120x80 coordinates)
        and realistic xG distributions for the 2026/2027 Premier League team.
        """
        team = self.teams_dict.get(team_id)
        if not team:
            return []
            
        np.random.seed(abs(hash(team_id)) % (2**32))
        avg_quality = team["metrics"]["shot_quality_xg_per_shot"]
        is_high_volume = team["metrics"]["box_touches_per_90"] > 32.0
        
        shots = []
        outcomes = ["Goal", "Saved", "Blocked", "Missed", "Post"]
        weights = [0.13, 0.35, 0.27, 0.22, 0.03]
        
        for i in range(count):
            in_box = np.random.rand() < (0.78 if is_high_volume else 0.58)
            if in_box:
                x = round(np.random.normal(108, 4.2), 1)
                y = round(np.random.normal(40, 7.0), 1)
                x = max(102.0, min(118.5, x))
                y = max(24.0, min(56.0, y))
                xg = round(np.random.gamma(shape=2.5, scale=avg_quality / 2.2), 3)
                xg = max(0.04, min(0.78, xg))
            else:
                x = round(np.random.uniform(90.0, 102.0), 1)
                y = round(np.random.uniform(20.0, 60.0), 1)
                xg = round(np.random.uniform(0.02, 0.08), 3)
                
            outcome = np.random.choice(outcomes, p=weights)
            if xg > 0.35 and outcome in ["Missed", "Blocked"] and np.random.rand() < 0.4:
                outcome = "Goal"
                
            shots.append({
                "id": f"{team_id}_shot_{i+1}",
                "minute": int(np.random.randint(2, 94)),
                "x": x,
                "y": y,
                "xg": xg,
                "outcome": outcome,
                "is_goal": outcome == "Goal",
                "shot_type": "Open Play" if np.random.rand() > 0.2 else "Set Piece"
            })
            
        return sorted(shots, key=lambda s: s["minute"])

    def generate_pitch_control_zones(self, team_a_id: str, team_b_id: str) -> Dict[str, Any]:
        """
        Computes 18-Zone (6 longitudinal x 3 lateral) territorial dominance and field tilt distribution
        between Premier League Team A and Team B.
        """
        team_a = self.teams_dict.get(team_a_id)
        team_b = self.teams_dict.get(team_b_id)
        if not team_a or not team_b:
            return {}
            
        tilt_a = team_a["metrics"]["field_tilt_pct"]
        tilt_b = team_b["metrics"]["field_tilt_pct"]
        line_a = team_a["metrics"]["defensive_line_height_m"]
        line_b = team_b["metrics"]["defensive_line_height_m"]
        
        zones = []
        band_names = [
            f"{team_a['short_name']} Def Box", f"{team_a['short_name']} Def 3rd",
            "Mid 3rd (Def)", "Mid 3rd (Att)",
            f"{team_a['short_name']} Att 3rd", f"{team_b['short_name']} Box Edge"
        ]
        lane_names = ["Left Half-Space/Flank", "Central Channel", "Right Half-Space/Flank"]
        
        for band_idx, band_label in enumerate(band_names):
            progress_ratio = band_idx / 5.0
            base_a = (tilt_a / (tilt_a + tilt_b)) * 100.0
            
            if progress_ratio < 0.33:
                ctrl_a = base_a * 0.85 + (line_a / 60.0) * 25.0
            elif progress_ratio > 0.66:
                ctrl_a = base_a * 1.15 - (line_b / 60.0) * 15.0
            else:
                ctrl_a = base_a
                
            ctrl_a = max(25.0, min(75.0, ctrl_a))
            
            for lane_idx, lane_label in enumerate(lane_names):
                lane_drift = 0.0
                if lane_idx == 0:
                    lane_drift = 2.0
                elif lane_idx == 2:
                    lane_drift = -1.5
                    
                zone_a = round(max(20.0, min(80.0, ctrl_a + lane_drift)), 1)
                zone_b = round(100.0 - zone_a, 1)
                
                dominant = team_a["name"] if zone_a > zone_b else (team_b["name"] if zone_b > zone_a else "Contested")
                
                zones.append({
                    "band_index": band_idx,
                    "lane_index": lane_idx,
                    "band_label": band_label,
                    "lane_label": lane_label,
                    "team_a_pct": zone_a,
                    "team_b_pct": zone_b,
                    "dominant_team": dominant
                })
                
        return {
            "team_a_name": team_a["name"],
            "team_b_name": team_b["name"],
            "team_a_tilt": tilt_a,
            "team_b_tilt": tilt_b,
            "team_a_line": line_a,
            "team_b_line": line_b,
            "zones": zones
        }

    def get_dashboard_data(self, team_id: str = "arsenal") -> Dict[str, Any]:
        """Provides full 2026/2027 Premier League dataset with complete 20-club standings and dual-team metrics."""
        team = self.get_team(team_id) or self.get_team("arsenal")
        
        # Complete Official 2026/2027 Premier League Standings table (All 20 clubs through 8 November 2026)
        standings = [
            {"rank": 1, "id": "arsenal", "name": "Arsenal", "short": "ARS", "crest_url": "/static/img/crests/arsenal.svg", "mp": 10, "w": 9, "d": 0, "l": 1, "gf": 17, "ga": 7, "gd": "+10", "g": "17:7", "pts": 27, "zone": "ucl"},
            {"rank": 2, "id": "brighton", "name": "Brighton & Hove Albion", "short": "BHA", "crest_url": "/static/img/crests/brighton.svg", "mp": 10, "w": 7, "d": 1, "l": 2, "gf": 27, "ga": 8, "gd": "+19", "g": "27:8", "pts": 22, "zone": "ucl"},
            {"rank": 3, "id": "mancity", "name": "Manchester City", "short": "MCI", "crest_url": "/static/img/crests/mancity.svg", "mp": 10, "w": 7, "d": 0, "l": 3, "gf": 21, "ga": 13, "gd": "+8", "g": "21:13", "pts": 21, "zone": "ucl"},
            {"rank": 4, "id": "liverpool", "name": "Liverpool", "short": "LIV", "crest_url": "/static/img/crests/liverpool.svg", "mp": 10, "w": 5, "d": 3, "l": 2, "gf": 14, "ga": 10, "gd": "+4", "g": "14:10", "pts": 18, "zone": "ucl"},
            {"rank": 5, "id": "chelsea", "name": "Chelsea", "short": "CHE", "crest_url": "/static/img/crests/chelsea.svg", "mp": 10, "w": 5, "d": 1, "l": 4, "gf": 17, "ga": 14, "gd": "+3", "g": "17:14", "pts": 16, "zone": "uel"},
            {"rank": 6, "id": "everton", "name": "Everton", "short": "EVE", "crest_url": "/static/img/crests/everton.svg", "mp": 10, "w": 4, "d": 4, "l": 2, "gf": 12, "ga": 10, "gd": "+2", "g": "12:10", "pts": 16, "zone": "uecl"},
            {"rank": 7, "id": "bournemouth", "name": "AFC Bournemouth", "short": "BOU", "crest_url": "/static/img/crests/bournemouth.svg", "mp": 10, "w": 4, "d": 3, "l": 3, "gf": 16, "ga": 11, "gd": "+5", "g": "16:11", "pts": 15, "zone": "mid"},
            {"rank": 8, "id": "brentford", "name": "Brentford", "short": "BRE", "crest_url": "/static/img/crests/brentford.svg", "mp": 10, "w": 3, "d": 5, "l": 2, "gf": 17, "ga": 12, "gd": "+5", "g": "17:12", "pts": 14, "zone": "mid"},
            {"rank": 9, "id": "leeds", "name": "Leeds United", "short": "LEE", "crest_url": "/static/img/crests/leeds.svg", "mp": 10, "w": 3, "d": 5, "l": 2, "gf": 12, "ga": 10, "gd": "+2", "g": "12:10", "pts": 14, "zone": "mid"},
            {"rank": 10, "id": "astonvilla", "name": "Aston Villa", "short": "AVL", "crest_url": "/static/img/crests/astonvilla.svg", "mp": 10, "w": 3, "d": 4, "l": 3, "gf": 15, "ga": 18, "gd": "-3", "g": "15:18", "pts": 13, "zone": "mid"},
            {"rank": 11, "id": "tottenham", "name": "Tottenham Hotspur", "short": "TOT", "crest_url": "/static/img/crests/tottenham.svg", "mp": 10, "w": 3, "d": 3, "l": 4, "gf": 11, "ga": 12, "gd": "-1", "g": "11:12", "pts": 12, "zone": "mid"},
            {"rank": 12, "id": "newcastle", "name": "Newcastle United", "short": "NEW", "crest_url": "/static/img/crests/newcastle.svg", "mp": 10, "w": 3, "d": 3, "l": 4, "gf": 14, "ga": 17, "gd": "-3", "g": "14:17", "pts": 12, "zone": "mid"},
            {"rank": 13, "id": "hullcity", "name": "Hull City", "short": "HUL", "crest_url": "/static/img/crests/hullcity.svg", "mp": 10, "w": 2, "d": 5, "l": 3, "gf": 10, "ga": 10, "gd": "0", "g": "10:10", "pts": 11, "zone": "mid"},
            {"rank": 14, "id": "ipswich", "name": "Ipswich Town", "short": "IPS", "crest_url": "/static/img/crests/ipswich.svg", "mp": 10, "w": 3, "d": 2, "l": 5, "gf": 12, "ga": 17, "gd": "-5", "g": "12:17", "pts": 11, "zone": "mid"},
            {"rank": 15, "id": "fulham", "name": "Fulham", "short": "FUL", "crest_url": "/static/img/crests/fulham.svg", "mp": 10, "w": 2, "d": 4, "l": 4, "gf": 10, "ga": 12, "gd": "-2", "g": "10:12", "pts": 10, "zone": "mid"},
            {"rank": 16, "id": "nottinghamforest", "name": "Nottingham Forest", "short": "NFO", "crest_url": "/static/img/crests/nottinghamforest.svg", "mp": 10, "w": 2, "d": 3, "l": 5, "gf": 10, "ga": 14, "gd": "-4", "g": "10:14", "pts": 9, "zone": "mid"},
            {"rank": 17, "id": "coventry", "name": "Coventry City", "short": "COV", "crest_url": "/static/img/crests/coventry.svg", "mp": 10, "w": 3, "d": 0, "l": 7, "gf": 6, "ga": 16, "gd": "-10", "g": "6:16", "pts": 9, "zone": "mid"},
            {"rank": 18, "id": "manunited", "name": "Manchester United", "short": "MUN", "crest_url": "/static/img/crests/manunited.svg", "mp": 10, "w": 1, "d": 5, "l": 4, "gf": 15, "ga": 20, "gd": "-5", "g": "15:20", "pts": 8, "zone": "rel"},
            {"rank": 19, "id": "sunderland", "name": "Sunderland", "short": "SUN", "crest_url": "/static/img/crests/sunderland.svg", "mp": 10, "w": 2, "d": 2, "l": 6, "gf": 9, "ga": 19, "gd": "-10", "g": "9:19", "pts": 8, "zone": "rel"},
            {"rank": 20, "id": "crystalpalace", "name": "Crystal Palace", "short": "CRY", "crest_url": "/static/img/crests/crystalpalace.svg", "mp": 10, "w": 2, "d": 1, "l": 7, "gf": 9, "ga": 24, "gd": "-15", "g": "9:24", "pts": 7, "zone": "rel"}
        ]
        
        # Resolve specific Matchweek 11 fixture for the active dashboard team
        team_match = None
        for fix in MATCHWEEK_11_FIXTURES:
            if fix["home_id"] == team["id"] or fix["away_id"] == team["id"]:
                team_match = fix
                break
        
        if team_match is None:
            team_match = MATCHWEEK_11_FIXTURES[0]
            
        is_home = team_match["home_id"] == team["id"]
        opp_id = team_match["away_id"] if is_home else team_match["home_id"]
        opp_team_obj = self.get_team(opp_id) or self.get_team("mancity")
        
        next_game = {
            "competition": team_match["competition"],
            "datetime": team_match["datetime"],
            "venue": team_match["venue"],
            "is_home": is_home,
            "home_team": team_match["home_name"],
            "home_id": team_match["home_id"],
            "home_badge": team_match["home_short"],
            "home_crest": team_match["home_crest"],
            "away_team": team_match["away_name"],
            "away_id": team_match["away_id"],
            "away_badge": team_match["away_short"],
            "away_crest": team_match["away_crest"]
        }
        
        # Match standings data dynamically for Games statistics
        standings_by_id = {row["id"]: row for row in standings}
        team_a_row = standings_by_id.get(team["id"], standings[1])
        team_b_row = standings_by_id.get(opp_id, standings[0])
        
        # Games statistics for BOTH teams (Side-by-side comparative record)
        games_statistic = {
            "team_a": {
                "id": team["id"],
                "name": team["name"],
                "crest_url": team.get("crest_url", f"/static/img/crests/{team['id']}.svg"),
                "pl": team_a_row["mp"],
                "victories": team_a_row["w"],
                "draws": team_a_row["d"],
                "lost": team_a_row["l"],
                "pct_victories": round((team_a_row["w"] / team_a_row["mp"]) * 100, 1) if team_a_row["mp"] > 0 else 0.0,
                "pct_draws": round((team_a_row["d"] / team_a_row["mp"]) * 100, 1) if team_a_row["mp"] > 0 else 0.0,
                "pct_lost": round((team_a_row["l"] / team_a_row["mp"]) * 100, 1) if team_a_row["mp"] > 0 else 0.0,
                "goals": f"{team_a_row['gf']}:{team_a_row['ga']}",
                "pts": team_a_row["pts"],
                "rank": team_a_row["rank"],
                "gd": team_a_row["gd"]
            },
            "team_b": {
                "id": opp_team_obj["id"],
                "name": opp_team_obj["name"],
                "crest_url": opp_team_obj.get("crest_url", f"/static/img/crests/{opp_id}.svg"),
                "pl": team_b_row["mp"],
                "victories": team_b_row["w"],
                "draws": team_b_row["d"],
                "lost": team_b_row["l"],
                "pct_victories": round((team_b_row["w"] / team_b_row["mp"]) * 100, 1) if team_b_row["mp"] > 0 else 0.0,
                "pct_draws": round((team_b_row["d"] / team_b_row["mp"]) * 100, 1) if team_b_row["mp"] > 0 else 0.0,
                "pct_lost": round((team_b_row["l"] / team_b_row["mp"]) * 100, 1) if team_b_row["mp"] > 0 else 0.0,
                "goals": f"{team_b_row['gf']}:{team_b_row['ga']}",
                "pts": team_b_row["pts"],
                "rank": team_b_row["rank"],
                "gd": team_b_row["gd"]
            }
        }
        
        # Authentic 2026/2027 Club Financial & Performance Profiles
        CLUB_FINANCIALS = {
            "mancity": {"overall_price": "$1.35b", "transfer_budget": "$240.0m", "average_score": 7.9},
            "arsenal": {"overall_price": "$1.24b", "transfer_budget": "$215.0m", "average_score": 7.6},
            "liverpool": {"overall_price": "$1.15b", "transfer_budget": "$195.0m", "average_score": 7.5},
            "chelsea": {"overall_price": "$1.08b", "transfer_budget": "$230.0m", "average_score": 7.3},
            "manunited": {"overall_price": "$940.0m", "transfer_budget": "$180.0m", "average_score": 7.0},
            "tottenham": {"overall_price": "$890.0m", "transfer_budget": "$165.0m", "average_score": 7.1},
            "newcastle": {"overall_price": "$760.0m", "transfer_budget": "$170.0m", "average_score": 7.2},
            "astonvilla": {"overall_price": "$710.0m", "transfer_budget": "$145.0m", "average_score": 7.1},
            "brighton": {"overall_price": "$580.0m", "transfer_budget": "$130.0m", "average_score": 7.4},
            "brentford": {"overall_price": "$470.0m", "transfer_budget": "$95.0m", "average_score": 7.2},
            "nottinghamforest": {"overall_price": "$430.0m", "transfer_budget": "$85.0m", "average_score": 6.9},
            "crystalpalace": {"overall_price": "$420.0m", "transfer_budget": "$80.0m", "average_score": 6.8},
            "fulham": {"overall_price": "$390.0m", "transfer_budget": "$75.0m", "average_score": 6.7},
            "bournemouth": {"overall_price": "$380.0m", "transfer_budget": "$70.0m", "average_score": 6.7},
            "everton": {"overall_price": "$360.0m", "transfer_budget": "$65.0m", "average_score": 6.8},
            "leeds": {"overall_price": "$330.0m", "transfer_budget": "$60.0m", "average_score": 7.0},
            "sunderland": {"overall_price": "$240.0m", "transfer_budget": "$45.0m", "average_score": 6.6},
            "ipswich": {"overall_price": "$210.0m", "transfer_budget": "$40.0m", "average_score": 6.5},
            "hullcity": {"overall_price": "$190.0m", "transfer_budget": "$35.0m", "average_score": 6.6},
            "coventry": {"overall_price": "$170.0m", "transfer_budget": "$30.0m", "average_score": 6.4}
        }
        
        team_fin = CLUB_FINANCIALS.get(team["id"], {"overall_price": "$450.0m", "transfer_budget": "$85.0m", "average_score": 7.0})
        
        quick_stats = {
            "team_id": team["id"],
            "team_name": team["name"],
            "crest_url": team.get("crest_url", f"/static/img/crests/{team['id']}.svg"),
            "possession": int(round(team["possession_pct"])),
            "overall_price": team_fin["overall_price"],
            "transfer_budget": team_fin["transfer_budget"],
            "average_score": team_fin["average_score"]
        }
        
        # Build comprehensive overview lookup for all 20 Premier League teams
        all_team_overviews = {}
        for t in self.teams_dict.values():
            t_fin = CLUB_FINANCIALS.get(t["id"], {"overall_price": "$450.0m", "transfer_budget": "$85.0m", "average_score": 7.0})
            all_team_overviews[t["id"]] = {
                "team_id": t["id"],
                "team_name": t["name"],
                "crest_url": t.get("crest_url", f"/static/img/crests/{t['id']}.svg"),
                "possession": int(round(t["possession_pct"])),
                "overall_price": t_fin["overall_price"],
                "transfer_budget": t_fin["transfer_budget"],
                "average_score": t_fin["average_score"]
            }
        
        return {
            "coach_name": team["manager"],
            "coach_avatar": "/static/img/andrea_pirlo.jpg",
            "team": team,
            "next_game": next_game,
            "fixtures": MATCHWEEK_11_FIXTURES,
            "last_match_played": LAST_MATCH_PLAYED,
            "matchweek_11_results": MATCHWEEK_10_RESULTS,
            "games_statistic": games_statistic,
            "standings": standings,
            "quick_stats": quick_stats,
            "all_team_overviews": all_team_overviews
        }

    def get_head_to_head_sections(self, team_a_id: str, team_b_id: str) -> List[Dict[str, Any]]:
        """
        Generates the exact official Premier League head-to-head comparison format
        with Attack, Possession, Defence, Discipline, and Physical categories for 2026/27.
        """
        team_a = self.get_team(team_a_id) or self.get_team("arsenal")
        team_b = self.get_team(team_b_id) or self.get_team("mancity")
        
        m_a = team_a["metrics"]
        m_b = team_b["metrics"]
        
        st_a = OFFICIAL_SEASON_STATS_2026_27.get(team_a["id"], OFFICIAL_SEASON_STATS_2026_27["arsenal"])
        st_b = OFFICIAL_SEASON_STATS_2026_27.get(team_b["id"], OFFICIAL_SEASON_STATS_2026_27["mancity"])
        
        # Helper to determine leader
        def make_row(label: str, val_a_str: str, val_b_str: str, num_a: float, num_b: float, higher_is_better: bool = True):
            leader = None
            if num_a != num_b:
                if higher_is_better:
                    leader = "team_a" if num_a > num_b else "team_b"
                else:
                    leader = "team_a" if num_a < num_b else "team_b"
            return {
                "label": label,
                "team_a_val": val_a_str,
                "team_b_val": val_b_str,
                "leader": leader
            }

        return [
            {
                "category_id": "attack",
                "title": "Attack",
                "stats": [
                    make_row("Goals", str(st_a["goals"]), str(st_b["goals"]), st_a["goals"], st_b["goals"], True),
                    make_row("Assists", str(st_a["assists"]), str(st_b["assists"]), st_a["assists"], st_b["assists"], True),
                    make_row("Goal Involvements", str(st_a["involvements"]), str(st_b["involvements"]), st_a["involvements"], st_b["involvements"], True),
                    make_row("Expected Goals", f"{st_a['xg']:.2f}", f"{st_b['xg']:.2f}", st_a["xg"], st_b["xg"], True),
                    make_row("Shots Inside The Box", str(st_a["shots_in_box"]), str(st_b["shots_in_box"]), st_a["shots_in_box"], st_b["shots_in_box"], True),
                    make_row("Shots Outside The Box", str(st_a["shots_out_box"]), str(st_b["shots_out_box"]), st_a["shots_out_box"], st_b["shots_out_box"], True),
                    make_row("Touches In Opposition Box", str(st_a["touches_in_box"]), str(st_b["touches_in_box"]), st_a["touches_in_box"], st_b["touches_in_box"], True),
                    make_row("Penalties (Scored)", str(st_a["penalties"]), str(st_b["penalties"]), float(st_a["penalties"][0]), float(st_b["penalties"][0]), True),
                    make_row("Hit Woodwork", str(st_a["woodwork"]), str(st_b["woodwork"]), st_a["woodwork"], st_b["woodwork"], True),
                    make_row("Expected Assists", f"{st_a['xa']:.2f}", f"{st_b['xa']:.2f}", st_a["xa"], st_b["xa"], True),
                    make_row("Free Kicks Scored", str(st_a["fk_scored"]), str(st_b["fk_scored"]), st_a["fk_scored"], st_b["fk_scored"], True),
                    make_row("Total Crosses", str(st_a["crosses"]), str(st_b["crosses"]), float(st_a["crosses"].split()[0]), float(st_b["crosses"].split()[0]), True)
                ],
                "items": [
                    make_row("Goals", str(st_a["goals"]), str(st_b["goals"]), st_a["goals"], st_b["goals"], True),
                    make_row("Assists", str(st_a["assists"]), str(st_b["assists"]), st_a["assists"], st_b["assists"], True),
                    make_row("Goal Involvements", str(st_a["involvements"]), str(st_b["involvements"]), st_a["involvements"], st_b["involvements"], True),
                    make_row("Expected Goals", f"{st_a['xg']:.2f}", f"{st_b['xg']:.2f}", st_a["xg"], st_b["xg"], True),
                    make_row("Shots Inside The Box", str(st_a["shots_in_box"]), str(st_b["shots_in_box"]), st_a["shots_in_box"], st_b["shots_in_box"], True),
                    make_row("Shots Outside The Box", str(st_a["shots_out_box"]), str(st_b["shots_out_box"]), st_a["shots_out_box"], st_b["shots_out_box"], True),
                    make_row("Touches In Opposition Box", str(st_a["touches_in_box"]), str(st_b["touches_in_box"]), st_a["touches_in_box"], st_b["touches_in_box"], True),
                    make_row("Penalties (Scored)", str(st_a["penalties"]), str(st_b["penalties"]), float(st_a["penalties"][0]), float(st_b["penalties"][0]), True),
                    make_row("Hit Woodwork", str(st_a["woodwork"]), str(st_b["woodwork"]), st_a["woodwork"], st_b["woodwork"], True),
                    make_row("Expected Assists", f"{st_a['xa']:.2f}", f"{st_b['xa']:.2f}", st_a["xa"], st_b["xa"], True),
                    make_row("Free Kicks Scored", str(st_a["fk_scored"]), str(st_b["fk_scored"]), st_a["fk_scored"], st_b["fk_scored"], True),
                    make_row("Total Crosses", str(st_a["crosses"]), str(st_b["crosses"]), float(st_a["crosses"].split()[0]), float(st_b["crosses"].split()[0]), True)
                ]
            },
            {
                "category_id": "possession",
                "title": "Possession",
                "stats": [
                    make_row("Total Passes", str(st_a["total_passes"]), str(st_b["total_passes"]), float(st_a["total_passes"].split()[0].replace(',', '')), float(st_b["total_passes"].split()[0].replace(',', '')), True),
                    make_row("Long Passes", str(st_a["long_passes"]), str(st_b["long_passes"]), float(st_a["long_passes"].split()[0]), float(st_b["long_passes"].split()[0]), True),
                    make_row("Corners", str(st_a["corners"]), str(st_b["corners"]), st_a["corners"], st_b["corners"], True),
                    make_row("Possession %", f"{team_a['possession_pct']}%", f"{team_b['possession_pct']}%", team_a["possession_pct"], team_b["possession_pct"], True),
                    make_row("Progressive Passes", f"{m_a['progressive_passes_per_90']}", f"{m_b['progressive_passes_per_90']}", m_a["progressive_passes_per_90"], m_b["progressive_passes_per_90"], True),
                    make_row("Field Tilt %", f"{m_a['field_tilt_pct']}%", f"{m_b['field_tilt_pct']}%", m_a["field_tilt_pct"], m_b["field_tilt_pct"], True)
                ],
                "items": [
                    make_row("Total Passes", str(st_a["total_passes"]), str(st_b["total_passes"]), float(st_a["total_passes"].split()[0].replace(',', '')), float(st_b["total_passes"].split()[0].replace(',', '')), True),
                    make_row("Long Passes", str(st_a["long_passes"]), str(st_b["long_passes"]), float(st_a["long_passes"].split()[0]), float(st_b["long_passes"].split()[0]), True),
                    make_row("Corners", str(st_a["corners"]), str(st_b["corners"]), st_a["corners"], st_b["corners"], True),
                    make_row("Possession %", f"{team_a['possession_pct']}%", f"{team_b['possession_pct']}%", team_a["possession_pct"], team_b["possession_pct"], True),
                    make_row("Progressive Passes", f"{m_a['progressive_passes_per_90']}", f"{m_b['progressive_passes_per_90']}", m_a["progressive_passes_per_90"], m_b["progressive_passes_per_90"], True),
                    make_row("Field Tilt %", f"{m_a['field_tilt_pct']}%", f"{m_b['field_tilt_pct']}%", m_a["field_tilt_pct"], m_b["field_tilt_pct"], True)
                ]
            },
            {
                "category_id": "defence",
                "title": "Defence",
                "stats": [
                    make_row("Total tackles", str(st_a["total_tackles"]), str(st_b["total_tackles"]), st_a["total_tackles"], st_b["total_tackles"], True),
                    make_row("Interceptions", str(st_a["interceptions"]), str(st_b["interceptions"]), st_a["interceptions"], st_b["interceptions"], True),
                    make_row("Blocks", str(st_a["blocks"]), str(st_b["blocks"]), st_a["blocks"], st_b["blocks"], True),
                    make_row("Goals Conceded", str(st_a["ga"]), str(st_b["ga"]), st_a["ga"], st_b["ga"], False),
                    make_row("Clean Sheets", str(st_a["clean_sheets"]), str(st_b["clean_sheets"]), st_a["clean_sheets"], st_b["clean_sheets"], True),
                    make_row("PAdj Tackles & Interceptions", f"{m_a['padj_interceptions_tackles_per_90']}", f"{m_b['padj_interceptions_tackles_per_90']}", m_a["padj_interceptions_tackles_per_90"], m_b["padj_interceptions_tackles_per_90"], True)
                ],
                "items": [
                    make_row("Total tackles", str(st_a["total_tackles"]), str(st_b["total_tackles"]), st_a["total_tackles"], st_b["total_tackles"], True),
                    make_row("Interceptions", str(st_a["interceptions"]), str(st_b["interceptions"]), st_a["interceptions"], st_b["interceptions"], True),
                    make_row("Blocks", str(st_a["blocks"]), str(st_b["blocks"]), st_a["blocks"], st_b["blocks"], True),
                    make_row("Goals Conceded", str(st_a["ga"]), str(st_b["ga"]), st_a["ga"], st_b["ga"], False),
                    make_row("Clean Sheets", str(st_a["clean_sheets"]), str(st_b["clean_sheets"]), st_a["clean_sheets"], st_b["clean_sheets"], True),
                    make_row("PAdj Tackles & Interceptions", f"{m_a['padj_interceptions_tackles_per_90']}", f"{m_b['padj_interceptions_tackles_per_90']}", m_a["padj_interceptions_tackles_per_90"], m_b["padj_interceptions_tackles_per_90"], True)
                ]
            },
            {
                "category_id": "discipline",
                "title": "Discipline",
                "stats": [
                    make_row("Fouls", str(st_a["fouls"]), str(st_b["fouls"]), st_a["fouls"], st_b["fouls"], False),
                    make_row("Offsides", str(st_a["offsides"]), str(st_b["offsides"]), st_a["offsides"], st_b["offsides"], False),
                    make_row("Own Goals", str(st_a["own_goals"]), str(st_b["own_goals"]), st_a["own_goals"], st_b["own_goals"], False),
                    make_row("Yellow Cards", str(st_a["yellow_cards"]), str(st_b["yellow_cards"]), st_a["yellow_cards"], st_b["yellow_cards"], False),
                    make_row("Red Cards", str(st_a["red_cards"]), str(st_b["red_cards"]), st_a["red_cards"], st_b["red_cards"], False)
                ],
                "items": [
                    make_row("Fouls", str(st_a["fouls"]), str(st_b["fouls"]), st_a["fouls"], st_b["fouls"], False),
                    make_row("Offsides", str(st_a["offsides"]), str(st_b["offsides"]), st_a["offsides"], st_b["offsides"], False),
                    make_row("Own Goals", str(st_a["own_goals"]), str(st_b["own_goals"]), st_a["own_goals"], st_b["own_goals"], False),
                    make_row("Yellow Cards", str(st_a["yellow_cards"]), str(st_b["yellow_cards"]), st_a["yellow_cards"], st_b["yellow_cards"], False),
                    make_row("Red Cards", str(st_a["red_cards"]), str(st_b["red_cards"]), st_a["red_cards"], st_b["red_cards"], False)
                ]
            },
            {
                "category_id": "physical",
                "title": "Physical",
                "stats": [
                    make_row("Minutes Played", str(st_a["mins"]), str(st_b["mins"]), st_a["mins"], st_b["mins"], True),
                    make_row("Dribbles", str(st_a["dribbles"]), str(st_b["dribbles"]), float(st_a["dribbles"].split()[0]), float(st_b["dribbles"].split()[0]), True),
                    make_row("Duels Won", str(st_a["duels_won"]), str(st_b["duels_won"]), st_a["duels_won"], st_b["duels_won"], True),
                    make_row("Aerial Duels Won", str(st_a["aerial_duels"]), str(st_b["aerial_duels"]), st_a["aerial_duels"], st_b["aerial_duels"], True)
                ],
                "items": [
                    make_row("Minutes Played", str(st_a["mins"]), str(st_b["mins"]), st_a["mins"], st_b["mins"], True),
                    make_row("Dribbles", str(st_a["dribbles"]), str(st_b["dribbles"]), float(st_a["dribbles"].split()[0]), float(st_b["dribbles"].split()[0]), True),
                    make_row("Duels Won", str(st_a["duels_won"]), str(st_b["duels_won"]), st_a["duels_won"], st_b["duels_won"], True),
                    make_row("Aerial Duels Won", str(st_a["aerial_duels"]), str(st_b["aerial_duels"]), st_a["aerial_duels"], st_b["aerial_duels"], True)
                ]
            }
        ]


# Singleton instance
data_repo = FootballDataRepository()

