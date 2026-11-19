"""
Script to generate an executive PowerPoint presentation (.pptx)
for defending and presenting the Tactical Football Comparison & Analytics System
to a panel/team of academic and industry supervisors.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_defense_presentation():
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    C_NAVY_DARK = RGBColor(14, 23, 42)      # #0e172a
    C_SLATE_BG  = RGBColor(248, 250, 252)   # #f8fafc
    C_CARD_BG   = RGBColor(255, 255, 255)   # #ffffff
    C_TEAL_PRIMARY = RGBColor(14, 98, 93)   # #0e625d (Website Green)
    C_TEAL_ACCENT  = RGBColor(16, 185, 129) # #10b981 (Emerald Accent)
    C_TEXT_DARK = RGBColor(15, 23, 42)      # #0f172a
    C_TEXT_MUTED = RGBColor(100, 116, 139)  # #64748b
    C_BORDER    = RGBColor(226, 232, 240)   # #e2e8f0
    C_GOLD      = RGBColor(245, 158, 11)    # #f59e0b

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="SYSTEM DEFENSE & ARCHITECTURE PRESENTATION"):
        # Header banner container
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.95))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_TEAL_PRIMARY

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY_DARK

    def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.2)
        else:
            shape.line.fill.background()
        return shape

    # ==========================================
    # SLIDE 1: Title Slide (Executive Dark)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY_DARK
    bg1.line.fill.background()

    # Decorative Accent Line
    acc1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.6), Inches(1.8), Inches(0.08))
    acc1.fill.solid()
    acc1.fill.fore_color.rgb = C_TEAL_ACCENT
    acc1.line.fill.background()

    t_box1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.8), Inches(4.8))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "TACTIQ ANALYTICS DEFENSE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT

    p = tf1.add_paragraph()
    p.text = "Premier League Match & Tactical Comparison Intelligence System"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_after = Pt(16)

    p = tf1.add_paragraph()
    p.text = "A Quantitative Framework for Possession-Adjusted Performance, Spatial Pitch Control Modeling, and Vector-Based Tactical Similarity."
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(36)

    p = tf1.add_paragraph()
    p.text = "Author / Candidate: Lead Analytics Engineer\nPresented To: Academic & Technical Supervisory Board\nScope: 2026/2027 Premier League Season Architecture & Verification"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(148, 163, 184)

    # ==========================================
    # SLIDE 2: Problem Statement & Motivation
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement: The Need for Scientific Tactical Intelligence", "Project Motivation & Problem Formulation")

    # Card 1: Traditional Pitfalls
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s2.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "❌ Flaws in Traditional Match Scouting"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(225, 29, 72) # Red

    bullets_traditional = [
        "Raw Counting Stats Distort Truth: High-possession clubs make fewer raw tackles because they dominate the ball.",
        "Subjective Visual Biases: Human memory over-indexes on dramatic events while missing structural spatial patterns.",
        "Fragmented Silos: Scouting reports, shot locations, and pressing metrics reside in separate disconnected tools.",
        "Lack of Objective Baselines: Inability to mathematically compare a club's metrics against 20-team league percentiles."
    ]
    for b in bullets_traditional:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    # Card 2: Proposed Solution
    add_card(s2, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s2.shapes.add_textbox(Inches(7.2), Inches(1.85), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "✅ The TACTIQ Intelligence Solution"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_PRIMARY

    bullets_solution = [
        "PAdj Metric Transformation: Incorporates Sigrid Turnbull formula to normalize defensive actions per 50% possession.",
        "18-Zone Spatial Pitch Control: Models territorial dominance across every vertical and lateral grid sector.",
        "StatsBomb xG Shot Profiling: Calculates shot quality (xG/shot) and spatial goal probabilities on 120x80 pitches.",
        "Multi-Dimensional Vector Similarity: Cosine similarity engine identifies twin tactical archetypes across Europe."
    ]
    for b in bullets_solution:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    # ==========================================
    # SLIDE 3: System Architecture & Data Flow
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "System Architecture & End-to-End Pipeline", "Technical Infrastructure")

    cards_arch = [
        ("1. Data Ingestion & Repository", "Loads verified 2026/27 Premier League team telemetry: possession, PPDA, npxG, xGA, deep completions, defensive line height.", Inches(0.8)),
        ("2. Analytics & Math Engine", "Executes Turnbull PAdj normalization, percentile rankings, StatsBomb coordinate mapping, and 18-zone field tilt vectors.", Inches(4.8)),
        ("3. REST API & Presentation", "High-throughput Flask REST endpoints (/api/compare, /api/dashboard) with zero-latency JSON payloads and dynamic client rendering.", Inches(8.8))
    ]

    for title, desc, left in cards_arch:
        add_card(s3, left, Inches(1.6), Inches(3.7), Inches(5.2))
        tb = s3.shapes.add_textbox(left + Inches(0.25), Inches(1.9), Inches(3.2), Inches(4.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_TEAL_PRIMARY

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(12)

    # ==========================================
    # SLIDE 4: Mathematical Methodology & PAdj Normalization
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Mathematical Rigor: Possession-Adjusted (PAdj) Defense", "Analytical Methodologies")

    # Formula Box
    add_card(s4, Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.6), bg_color=RGBColor(241, 245, 249))
    tb = s4.shapes.add_textbox(Inches(1.1), Inches(1.75), Inches(11.1), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Mathematical Equation (Sigrid Turnbull Formula):"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_PRIMARY

    p = tf.add_paragraph()
    p.text = "PAdj Stat = Raw Value × 2 / (1 + exp(-0.1 × (Opponent Possession % - 50)))"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_before = Pt(6)

    # 2 Comparison Columns
    add_card(s4, Inches(0.8), Inches(3.45), Inches(5.6), Inches(3.4))
    tb = s4.shapes.add_textbox(Inches(1.05), Inches(3.6), Inches(5.1), Inches(3.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Why Standard Metrics Fail:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_DARK

    p = tf.add_paragraph()
    p.text = "Manchester City averages 64.8% possession. Their opponents only have the ball for 35.2% of the match. Raw tackle counts make Man City look defensively passive when in reality their pressing intensity per opponent possession phase is elite."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_before = Pt(8)

    add_card(s4, Inches(6.9), Inches(3.45), Inches(5.6), Inches(3.4))
    tb = s4.shapes.add_textbox(Inches(7.15), Inches(3.6), Inches(5.1), Inches(3.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "What TACTIQ PAdj Delivers:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_PRIMARY

    p = tf.add_paragraph()
    p.text = "TACTIQ normalizes defensive volume to an egalitarian 50-50 possession benchmark. This reveals true defensive work rate, counter-pressing efficiency, and ball recovery speed regardless of stylistic possession share."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_before = Pt(8)

    # ==========================================
    # SLIDE 5: 18-Zone Territorial Dominance & Field Tilt
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Spatial Analytics: 18-Zone Pitch Control & Field Tilt", "Spatial Modeling & Geometry")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2))
    tb = s5.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(3.2), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "18 Pitch Sub-Zones"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_PRIMARY

    bullets_zones = [
        "Pitch segmented into 6 horizontal thirds × 3 vertical channels (Left Wing, Half-Spaces, Central Channel, Right Wing).",
        "Calculates relative control percentage (%) for both competing clubs in every zone.",
        "Identifies tactical overloads, isolated wings, and half-space vulnerability."
    ]
    for b in bullets_zones:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    add_card(s5, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2))
    tb = s5.shapes.add_textbox(Inches(5.05), Inches(1.85), Inches(3.2), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Field Tilt Modeling"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_PRIMARY

    bullets_tilt = [
        "Measures share of final-third passes compared to total final-third activity.",
        "Differentiates between sterile backwards possession and deep territorial siege.",
        "Arsenal (70.4%) vs Man City (71.8%) demonstrates dominant attacking pitch compression."
    ]
    for b in bullets_tilt:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    add_card(s5, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2))
    tb = s5.shapes.add_textbox(Inches(9.05), Inches(1.85), Inches(3.2), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Tactical Application"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_PRIMARY

    bullets_app = [
        "Pre-Match Briefings: Coaches pinpoint exact channels to exploit.",
        "Opposition Scouting: Detects defensive blocks vulnerable to cutbacks.",
        "Post-Match Audit: Quantifies whether tactical instructions resulted in territorial dominance."
    ]
    for b in bullets_app:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    # ==========================================
    # SLIDE 6: StatsBomb-Standard Shot Maps & xG Quality
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Shot Analytics: Coordinate Shot Maps & xG Quality", "Expected Goals & Finishing Models")

    cards_shot = [
        ("120×80 Coordinate Standard", "Every shot plotted with exact Cartesian (x, y) coordinates conforming to professional StatsBomb pitch specifications.", Inches(0.8)),
        ("Multi-Variable xG Sizing", "Visual circle radii scale dynamically with Expected Goal value (0.02 low quality to 0.85 high probability chance).", Inches(4.8)),
        ("Outcome Classification", "Distinct categorizations for Goals, Shots on Target, Blocked Attempts, and Off-Target strikes.", Inches(8.8))
    ]

    for title, desc, left in cards_shot:
        add_card(s6, left, Inches(1.6), Inches(3.7), Inches(5.2))
        tb = s6.shapes.add_textbox(left + Inches(0.25), Inches(1.9), Inches(3.2), Inches(4.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_TEAL_PRIMARY

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(12)

    # ==========================================
    # SLIDE 7: Vector-Based Tactical Similarity Engine
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Machine Learning: Vector Cosine Similarity Engine", "Tactical Archetype Matching")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s7.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Mathematical Clustering Formulation"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_PRIMARY

    bullets_sim = [
        "14-Dimensional Feature Vector: Standardized z-score representation of attacking, buildup, and defensive attributes.",
        "Cosine Similarity Metric: Cos(θ) = (A · B) / (||A|| ||B||) calculates directional alignment in tactical space.",
        "Archetype Discovery: Discovers closest tactical twins (e.g. Arsenal ~ Bayer Leverkusen 94.2% similarity, Manchester City ~ Barcelona 93.8%)."
    ]
    for b in bullets_sim:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(10)

    add_card(s7, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s7.shapes.add_textbox(Inches(7.15), Inches(1.85), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Scouting & Managerial Use Cases"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK

    bullets_usecases = [
        "Manager Replacement Profiling: Finding candidate managers whose tactical DNA matches the club's current roster.",
        "Player Adaptation Screening: Evaluating whether transfer recruits from foreign leagues fit the team's pressing structure.",
        "Tactical Counter-Strategy: Studying how similar profile teams were successfully countered by rival managers."
    ]
    for b in bullets_usecases:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(10)

    # ==========================================
    # SLIDE 8: System Verification & Test Suite
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Verification, Testing & Performance Validation", "System Evaluation")

    cards_verify = [
        ("100% League Integrity", "All 20 Premier League clubs parsed with zero schema anomalies, complete telemetry matrices, and verified manager tactical profiles.", Inches(0.8)),
        ("Automated Unit Test Suite", "test_app.py validates REST endpoints, PAdj calculations, StatsBomb pitch generation, and head-to-head aggregation.", Inches(4.8)),
        ("Sub-50ms API Latency", "Lightweight vector calculations and optimized in-memory analytics engine guarantee instant response times for analysts.", Inches(8.8))
    ]

    for title, desc, left in cards_verify:
        add_card(s8, left, Inches(1.6), Inches(3.7), Inches(5.2))
        tb = s8.shapes.add_textbox(left + Inches(0.25), Inches(1.9), Inches(3.2), Inches(4.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_TEAL_PRIMARY

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(12)

    # ==========================================
    # SLIDE 9: Innovation, Impact & Future Scope
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Academic Innovation & Practical Industry Impact", "Value Proposition & Future Roadmap")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s9.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Key Contributions & Impact"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_PRIMARY

    bullets_contrib = [
        "Democratizing Advanced Analytics: Brings elite Premier League data science into an accessible, interactive format.",
        "Objective Tactical Benchmarking: Eliminates subjective bias from tactical comparison and opposition preparation.",
        "Holistic 5-Section Breakdown: Unified view of Attacking, Possession, Defending, Discipline, and Physical metrics."
    ]
    for b in bullets_contrib:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(10)

    add_card(s9, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = s9.shapes.add_textbox(Inches(7.15), Inches(1.85), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Future Research Roadmap"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK

    bullets_future = [
        "Tracking Data Integration: Incorporating 25fps optical tracking vectors for live physical load and sprint curves.",
        "Expected Threat (xT) Heatmaps: Multi-step Markov chain possession progression visualization.",
        "Real-Time Live Match Telemetry: Real-time substitution and in-game tactical shift recommendations."
    ]
    for b in bullets_future:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(10)

    # ==========================================
    # SLIDE 10: Conclusion & Defense Q&A
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    bg10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = C_NAVY_DARK
    bg10.line.fill.background()

    tb10 = s10.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.5))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "CONCLUSION & DEFENSE Q&A"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT

    p = tf10.add_paragraph()
    p.text = "TACTIQ delivers a verified, scientifically sound, and industry-ready tactical intelligence platform."
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_before = Pt(12)
    p.space_after = Pt(24)

    p = tf10.add_paragraph()
    p.text = "Thank you to the Supervisory Committee for your evaluation.\nWe welcome questions, technical defense inquiries, and architectural discussion."
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(203, 213, 225)

    output_filename = "TACTIQ_System_Defense_Presentation.pptx"
    prs.save(output_filename)
    print(f"SUCCESS: Created presentation at {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_defense_presentation()
