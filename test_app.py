import sys
print("Python:", sys.executable)
try:
    import app
    teams = app.data_repo.get_all_teams()
    print(f"SUCCESS: Loaded {len(teams)} Premier League teams.")
    assert len(teams) == 20
    
    with app.app.test_client() as client:
        # 1. Test Index / Dashboard route
        res_idx = client.get("/")
        print("Index page status:", res_idx.status_code)
        assert res_idx.status_code == 200
        assert b"Premier League" in res_idx.data
        assert b"Arsenal" in res_idx.data
        assert b"Manchester City" in res_idx.data
        assert b"Next game" in res_idx.data
        assert b"Standings" in res_idx.data
        
        # 2. Test Dashboard API
        res_dash = client.get("/api/dashboard?team=arsenal")
        print("Dashboard API status:", res_dash.status_code)
        dash_json = res_dash.get_json()
        assert dash_json["status"] == "success"
        assert dash_json["data"]["team"]["name"] == "Arsenal"
        
        # 3. Test Compare route & API
        res_comp_page = client.get("/compare?teamA=arsenal&teamB=mancity")
        print("Compare page status:", res_comp_page.status_code)
        assert res_comp_page.status_code == 200
        
        res_comp_api = client.get("/api/compare?team_a=arsenal&team_b=mancity")
        print("Compare API status:", res_comp_api.status_code)
        json_data = res_comp_api.get_json()
        assert json_data["status"] == "success"
        assert len(json_data["comparison_table"]) == 14
        assert len(json_data["pitch_control"]["zones"]) == 18

        # 4. Test Head-to-Head sections with Chelsea vs Man City
        h2h_sections = app.data_repo.get_head_to_head_sections("chelsea", "mancity")
        attack_stats = {row["label"]: row for row in h2h_sections[0]["stats"]}
        print(f"Chelsea Goals: {attack_stats['Goals']['team_a_val']}, Man City Goals: {attack_stats['Goals']['team_b_val']}")
        assert attack_stats["Goals"]["team_a_val"] == "21"
        assert attack_stats["Goals"]["team_b_val"] == "22"
        print("All Premier League test assertions passed successfully!")
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)


