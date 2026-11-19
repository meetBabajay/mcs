"""
Football Team Performance Comparison System
Main Flask Application & Analytics REST API
"""

import os
from flask import Flask, render_template, request, jsonify
from src.data_loader import data_repo
from src.metrics import compare_teams_metrics, METRIC_DEFINITIONS
from src.similarity import TeamSimilarityEngine

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates")
)

# Initialize similarity engine with league baseline
similarity_engine = TeamSimilarityEngine(data_repo.league_df, data_repo.teams_dict)


@app.route("/")
def index():
    """Renders the Premier League Match & Tactical Comparison Command Center."""
    teams = data_repo.get_all_teams()
    team_id = request.args.get("team", "arsenal")
    if team_id not in data_repo.teams_dict:
        team_id = "arsenal"
        
    dashboard_data = data_repo.get_dashboard_data(team_id)
    
    return render_template(
        "index.html",
        teams=teams,
        selected_team_id=team_id,
        data=dashboard_data,
        metrics_meta=METRIC_DEFINITIONS
    )


@app.route("/api/dashboard")
def api_dashboard():
    """API endpoint for live dashboard data updates."""
    team_id = request.args.get("team", "arsenal")
    if team_id not in data_repo.teams_dict:
        team_id = "arsenal"
    dashboard_data = data_repo.get_dashboard_data(team_id)
    return jsonify({
        "status": "success",
        "data": dashboard_data
    })




@app.route("/compare")
def compare_view():
    """Renders the comprehensive interactive analytics comparison suite."""
    teams = data_repo.get_all_teams()
    team_a_id = request.args.get("teamA", "arsenal")
    team_b_id = request.args.get("teamB", "mancity")
    
    if team_a_id not in data_repo.teams_dict:
        team_a_id = "arsenal"
    if team_b_id not in data_repo.teams_dict:
        team_b_id = "mancity"
        
    team_a = data_repo.get_team(team_a_id)
    team_b = data_repo.get_team(team_b_id)
    h2h_sections = data_repo.get_head_to_head_sections(team_a_id, team_b_id)
        
    return render_template(
        "compare.html",
        teams=teams,
        selected_a=team_a_id,
        selected_b=team_b_id,
        team_a=team_a,
        team_b=team_b,
        h2h_sections=h2h_sections
    )


@app.route("/api/teams")
def api_teams():
    """Returns directory of teams."""
    return jsonify({
        "status": "success",
        "teams": data_repo.get_all_teams()
    })


@app.route("/api/compare")
def api_compare():
    """
    Main comparison endpoint returning:
    - Team details
    - Head-to-head sections (Attack, Possession, Defence, Discipline, Physical)
    - Normalized metric percentiles and deltas
    - Radar chart dimensions
    - 18-zone territorial dominance & field tilt
    - Shot map coordinates (StatsBomb pitch layout)
    - Similarity recommendations
    """
    team_a_id = request.args.get("team_a", "arsenal")
    team_b_id = request.args.get("team_b", "mancity")
    
    team_a = data_repo.get_team(team_a_id)
    team_b = data_repo.get_team(team_b_id)
    
    if not team_a or not team_b:
        return jsonify({"status": "error", "message": "Invalid team identifier provided."}), 400
        
    # Official Premier League Head-to-Head sections (Attack, Possession, Defence, Discipline, Physical)
    head_to_head_sections = data_repo.get_head_to_head_sections(team_a_id, team_b_id)

    # Metric comparison & normalization
    comparison_table = compare_teams_metrics(team_a, team_b, data_repo.league_df)
    
    # Categorized metrics for radar and section breakdowns
    categories = {"Attacking": [], "Possession": [], "Defending": []}
    for item in comparison_table:
        cat = item["category"]
        if cat in categories:
            categories[cat].append(item)
            
    # Pitch control 18 zones
    pitch_control = data_repo.generate_pitch_control_zones(team_a_id, team_b_id)
    
    # Shot maps
    shots_a = data_repo.generate_shot_map(team_a_id, count=22)
    shots_b = data_repo.generate_shot_map(team_b_id, count=22)
    
    # Top 3 similar teams for both
    similar_a = similarity_engine.find_top_similar(team_a_id, top_k=3)
    similar_b = similarity_engine.find_top_similar(team_b_id, top_k=3)
    
    return jsonify({
        "status": "success",
        "team_a": team_a,
        "team_b": team_b,
        "head_to_head_sections": head_to_head_sections,
        "comparison_table": comparison_table,
        "categories": categories,
        "pitch_control": pitch_control,
        "shot_maps": {
            "team_a": shots_a,
            "team_b": shots_b
        },
        "similarity": {
            "team_a": similar_a,
            "team_b": similar_b
        }
    })



@app.route("/api/similarity/<team_id>")
def api_similarity(team_id):
    """Returns top similar teams for any single club."""
    if team_id not in data_repo.teams_dict:
        return jsonify({"status": "error", "message": "Team not found"}), 404
        
    similar = similarity_engine.find_top_similar(team_id, top_k=5)
    return jsonify({
        "status": "success",
        "team": data_repo.get_team(team_id),
        "similar_teams": similar
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Football Intelligence Server on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
