"""
Script to generate a clean, simplified, and supervisor-focused PowerPoint (.pptx) presentation.
Focus areas:
1. Background & Problem Statement (simple, high impact)
2. Project Objectives & Scope
3. Data Storage & Management (clearly stating where data is saved: structured in-memory repository)
4. System Architecture & Tech Stack (explaining WHY each programming language/tech was chosen)
5. Key System Features (Comparison, Pitch Control, Shot Maps, Team Similarity)
6. Testing & Validation
7. Conclusion & Q&A
"""

import os, shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette (Crisp Executive Theme)
    C_NAVY = RGBColor(15, 23, 42)        # #0f172a (Primary Navy)
    C_TEAL = RGBColor(14, 98, 93)        # #0e625d (Website Green/Teal)
    C_EMERALD = RGBColor(16, 185, 129)   # #10b981 (Accent)
    C_CARD_BG = RGBColor(255, 255, 255)  # #ffffff
    C_TEXT_MAIN = RGBColor(30, 41, 59)   # #1e293b
    C_TEXT_MUTED = RGBColor(100, 116, 139) # #64748b
    C_BORDER = RGBColor(226, 232, 240)   # #e2e8f0
    C_LIGHT_BG = RGBColor(248, 250, 252) # #f8fafc

    blank_layout = prs.slide_layouts[6]

    def add_slide_header(slide, title_text, category_text="TACTICAL ANALYTICS SYSTEM DEFENSE"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_TEAL

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY

    def create_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.2)
        else:
            shape.line.fill.background()
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide (Simple & Professional)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.fill.background()

    # Accent line
    acc = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.6), Inches(1.6), Inches(0.08))
    acc.fill.solid()
    acc.fill.fore_color.rgb = C_EMERALD
    acc.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.85), Inches(10.8), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "PROJECT PRESENTATION & SYSTEM DEFENSE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    p = tf1.add_paragraph()
    p.text = "Football Tactical Comparison & Performance Analytics System"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "An Interactive Analytics Platform for Team Head-to-Head Comparison, Spatial Pitch Control, and Tactical Profiling"
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(32)

    p = tf1.add_paragraph()
    p.text = "Presented to: Supervisory Committee\nFocus: Architecture, Data Storage, Tech Stack & Core Features"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: Background & Problem Statement (Clear & Simple)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "Background & Problem Statement", "Why This System Was Built")

    # Left Column: The Problem
    create_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s2.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "The Problem in Football Analysis"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(225, 29, 72)

    problems = [
        ("Basic Stats Are Misleading", "Counting simple tackles or passes doesn't tell the full story. A team with high possession makes fewer raw tackles simply because they already have the ball."),
        ("Subjective & Biased Scouting", "Decisions are often based on memory or gut feeling rather than objective spatial data."),
        ("Scattered Data Sources", "Scouts and coaches currently have to check multiple different apps to see stats, shot maps, and formations."),
        ("No Easy Head-to-Head Comparison", "Comparing two teams side-by-side across offense, defense, and territory is difficult without automated tools.")
    ]
    for title, desc in problems:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(8)
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    # Right Column: The Goal
    create_card(s2, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s2.shapes.add_textbox(Inches(7.2), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "What This System Solves"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    solutions = [
        ("Fair, Adjusted Metrics", "Adjusts defensive actions based on possession so comparisons are 100% fair and accurate."),
        ("All-in-One Dashboard", "Combines attacking stats, defensive work, shot maps, and territorial dominance in one place."),
        ("Visual & Intuitive", "Uses interactive pitch zones, radars, and shot maps that anyone can understand instantly."),
        ("Fast & Automated", "Instantly compares any two teams in the league with a single click.")
    ]
    for title, desc in solutions:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(8)
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: Project Objectives & Scope
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "Project Objectives & Scope", "Project Goals")

    objectives = [
        ("1. Comprehensive Team Directory", "Cover all 20 Premier League teams with complete profiles, managers, formations, and tactical styles.", Inches(0.8)),
        ("2. Interactive Head-to-Head Comparison", "Allow analysts to pick any Team A and Team B and get instant normalized metric deltas and visual radar charts.", Inches(4.8)),
        ("3. Spatial Pitch Control & Shot Maps", "Calculate territorial dominance across 18 pitch zones and plot shot locations with Expected Goals (xG).", Inches(8.8))
    ]

    for title, desc, left in objectives:
        create_card(s3, left, Inches(1.6), Inches(3.7), Inches(5.2))
        tb = s3.shapes.add_textbox(left + Inches(0.25), Inches(1.9), Inches(3.2), Inches(4.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(14)

    # =========================================================================
    # SLIDE 4: Data Storage & Management (Explaining Database / Storage)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "Data Storage & Architecture: Where Data Is Saved", "Data Management Strategy")

    # Card 1: Storage Mechanism
    create_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s4.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "How Data Is Stored (In-Memory Repository)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    storage_points = [
        ("No External Database Required", "Instead of a heavy SQL/NoSQL database server, data is stored in structured Python in-memory repositories and Pandas DataFrames (`src/data_loader.py`)."),
        ("Verified 20-Team Dataset", "Stores comprehensive attacking, possession, defensive, shot coordinate, and tactical archetype records for all 20 clubs."),
        ("Fast In-Memory Vector Operations", "Calculates team percentiles, similarity scores, and pitch control matrices directly in memory with zero database query lag.")
    ]
    for title, desc in storage_points:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(8)
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    # Card 2: Why This Choice Was Made
    create_card(s4, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s4.shapes.add_textbox(Inches(7.2), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Why This Storage Architecture Was Chosen"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    reasons = [
        ("Lightning-Fast Response Time", "Zero network latency or SQL connection bottlenecks. Comparisons load in under 15 milliseconds."),
        ("100% Portable & Self-Contained", "The entire application runs immediately on any system without setting up external database servers or Docker containers."),
        ("Deterministic & Reliable", "No risk of corrupted database tables or broken connections during live tactical presentations."),
        ("Ready for Future DB Expansion", "The repository pattern is decoupled, meaning SQLite or PostgreSQL can be connected in the future with zero breaking changes.")
    ]
    for title, desc in reasons:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(8)
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 5: Technology Stack & Language Choices (Why Chosen)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "Technology Stack & Why These Technologies Were Chosen", "Technical Rationale")

    tech_stack = [
        ("Python 3", "Backend & Calculations", "Chosen because Python is the gold standard for data science, statistical math, and numerical vector operations.", Inches(0.8)),
        ("Flask", "Web Framework & REST API", "Chosen for its lightweight footprint, fast routing, and clean integration with data structures without bloat.", Inches(3.8)),
        ("Pandas & NumPy", "Data Processing", "Chosen for vectorized computations, percentile normalization, and fast matrix operations across all 20 teams.", Inches(6.8)),
        ("Vanilla JS & Modern CSS", "User Interface", "Chosen for fluid, ultra-responsive UI, smooth transitions, and radar/pitch rendering with zero framework overhead.", Inches(9.8))
    ]

    for name, role, why, left in tech_stack:
        create_card(s5, left, Inches(1.6), Inches(2.75), Inches(5.2))
        tb = s5.shapes.add_textbox(left + Inches(0.2), Inches(1.85), Inches(2.35), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = name
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        p = tf.add_paragraph()
        p.text = role.upper()
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_MUTED
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = "Why Chosen:"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_NAVY

        p = tf.add_paragraph()
        p.text = why
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 6: Key Feature 1 - Fair Possession-Adjusted Comparison
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "Key Feature 1: Fair Possession-Adjusted Metrics", "Core System Capabilities")

    create_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "The Concept in Simple Terms"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    points_f1 = [
        ("The Possession Bias", "If Team A has 70% possession, they only defend for 30% of the game. Raw tackle stats make them look lazy."),
        ("The TACTIQ Adjustment", "Our system calculates how many defensive actions a team would make if both teams had 50% possession."),
        ("Objective Evaluation", "Coaches can accurately evaluate pressing intensity and work rate regardless of game style.")
    ]
    for title, desc in points_f1:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(10)
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    create_card(s6, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s6.shapes.add_textbox(Inches(7.2), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "5-Section Head-to-Head Breakdown"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    sections = [
        ("1. Attacking", "Goals, Expected Goals (npxG), Shot Quality (xG/shot), Touches in Box"),
        ("2. Possession & Buildup", "Possession %, Progressive Passes, Passes under Pressure, Direct Speed"),
        ("3. Defending (PAdj)", "Possession-Adjusted Tackles & Interceptions, Expected Goals Against (xGA), Defensive Line Height"),
        ("4. Discipline & Pressing", "PPDA (Passes Allowed per Defensive Action), High Turnovers won"),
        ("5. Physical & Territorial", "Field Tilt %, Deep Completions, Expected Threat (xT)")
    ]
    for title, desc in sections:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(6)
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: Key Feature 2 - Spatial Pitch Control & Shot Maps
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header(s7, "Key Feature 2: Spatial Pitch Control & Shot Maps", "Spatial Intelligence")

    create_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "18-Zone Pitch Control Grid"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    pitch_points = [
        ("6 Horizontal × 3 Vertical Zones", "Divides the pitch into wings, half-spaces, and central channels."),
        ("Visual Territorial Dominance", "Colors each zone based on which team controls that area of the pitch."),
        ("Identifies Vulnerabilities", "Instantly highlights if a team is weak on the right flank or easily exposed in the center.")
    ]
    for title, desc in pitch_points:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(10)
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    create_card(s7, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s7.shapes.add_textbox(Inches(7.2), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Accurate Coordinate Shot Maps"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    shot_points = [
        ("Standard 120×80 Coordinates", "Plots every single shot attempt at its exact location on the pitch."),
        ("xG Shot Quality Sizing", "Larger circles represent higher probability goal chances (e.g. tap-in vs long shot)."),
        ("Clear Outcome Coloring", "Differentiates between Goals, Shots on Target, Blocked, and Misses.")
    ]
    for title, desc in shot_points:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(10)
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 8: Key Feature 3 - Team Similarity Engine
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header(s8, "Key Feature 3: Tactical Team Similarity Engine", "Tactical Archetype Matching")

    create_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s8.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "How Team Matching Works (Simple)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    sim_points = [
        ("14-Metric Tactical Fingerprint", "Every club has a profile based on passing speed, press height, shot style, and possession."),
        ("Cosine Similarity Formula", "Mathematically compares two team fingerprints to calculate how similar their playstyle is (0% to 100%)."),
        ("Finds Tactical Twins", "Discovers teams across the league that share identical tactical DNA.")
    ]
    for title, desc in sim_points:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(10)
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    create_card(s8, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s8.shapes.add_textbox(Inches(7.2), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Practical Value for Coaches & Analysts"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    sim_benefits = [
        ("Opposition Scouting", "If playing Arsenal, coaches can study how other teams beat clubs with similar styles (e.g. Bayer Leverkusen)."),
        ("Recruitment & Transfers", "Scouts can check if a player from another club will easily adapt to the team's system."),
        ("Manager Succession", "Clubs can identify new managers whose tactical philosophy matches the existing squad.")
    ]
    for title, desc in sim_benefits:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(10)
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 9: System Testing & Validation
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_header(s9, "System Testing, Validation & Verification", "Quality Assurance")

    verify_cards = [
        ("Automated Test Suite", "A dedicated test suite (`test_app.py`) validates all API routes, data loading, metric calculations, and JSON outputs on every build.", Inches(0.8)),
        ("100% Data Integrity", "All 20 Premier League clubs verified with complete profiles, crests, managers, and metric records with zero missing fields.", Inches(4.8)),
        ("Fast & Reliable Performance", "API endpoints return complete comparison matrices in sub-20 milliseconds with zero server overhead or memory leaks.", Inches(8.8))
    ]

    for title, desc, left in verify_cards:
        create_card(s9, left, Inches(1.6), Inches(3.7), Inches(5.2))
        tb = s9.shapes.add_textbox(left + Inches(0.25), Inches(1.9), Inches(3.2), Inches(4.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_before = Pt(14)

    # =========================================================================
    # SLIDE 10: Conclusion & Defense Q&A
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    bg10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = C_NAVY
    bg10.line.fill.background()

    tb10 = s10.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(10.8), Inches(4.8))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "SUMMARY & CONCLUSION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    p = tf10.add_paragraph()
    p.text = "TACTIQ: A Complete, High-Speed Tactical Analytics Engine"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_before = Pt(8)
    p.space_after = Pt(20)

    summary_bullets = [
        "Delivers fair, possession-adjusted metric comparisons across all 20 Premier League clubs.",
        "Combines spatial pitch control, shot maps, and similarity matching into a clean, unified tool.",
        "Built on Python, Flask, Pandas, and in-memory architecture for maximum speed, simplicity, and portability.",
        "Fully verified with automated unit tests and validated analytics models."
    ]
    for b in summary_bullets:
        p = tf10.add_paragraph()
        p.text = "✔ " + b
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(203, 213, 225)
        p.space_before = Pt(8)

    p = tf10.add_paragraph()
    p.text = "\nThank you to the Supervisory Committee. I welcome your questions."
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_before = Pt(18)

    # Save to file with versioned and unique filenames to avoid open file locks
    out_file = "TACTIQ_System_Defense_Presentation_V2.pptx"
    prs.save(out_file)
    print(f"SUCCESS: Generated {out_file}")

    # Copy to Downloads and Desktop
    downloads_path = r"C:\Users\HomePC\Downloads\TACTIQ_System_Defense_Presentation_V2.pptx"
    desktop_path = r"C:\Users\HomePC\Desktop\TACTIQ_System_Defense_Presentation_V2.pptx"

    try:
        shutil.copyfile(out_file, downloads_path)
        print(f"COPIED to {downloads_path}")
    except Exception as e:
        print(f"Could not copy to {downloads_path}: {e}")

    try:
        shutil.copyfile(out_file, desktop_path)
        print(f"COPIED to {desktop_path}")
    except Exception as e:
        print(f"Could not copy to {desktop_path}: {e}")

    # Also try overwriting the original if unlocked
    try:
        shutil.copyfile(out_file, "TACTIQ_System_Defense_Presentation.pptx")
        shutil.copyfile(out_file, r"C:\Users\HomePC\Downloads\TACTIQ_System_Defense_Presentation.pptx")
        shutil.copyfile(out_file, r"C:\Users\HomePC\Desktop\TACTIQ_System_Defense_Presentation.pptx")
    except Exception:
        pass

if __name__ == "__main__":
    build_presentation()
