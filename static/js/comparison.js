/**
 * CoachPro Tactical Comparison & Intelligence Engine
 * Handles:
 * - Realtime REST API synchronization
 * - Chart.js Multi-Dimensional Radar Charts with CoachPro aesthetic
 * - SVG 18-Zone Territory & Field Tilt Visualizer
 * - Dynamic Shot Map on a StatsBomb-proportioned Pitch
 * - Percentile Net Delta Analytics Table
 * - Tactical Similarity Twin Matchers
 */

let currentComparisonData = null;
let radarChartInstance = null;
let currentPitchTab = 'territory'; // 'territory' or 'shots'

document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

function initApp() {
    const teamASelect = document.getElementById('selectTeamA');
    const teamBSelect = document.getElementById('selectTeamB');
    const swapBtn = document.getElementById('btnSwapTeams');

    if (teamASelect && teamBSelect) {
        teamASelect.addEventListener('change', () => {
            if (teamASelect.value === teamBSelect.value) {
                alert("Please select two distinct teams for tactical comparison.");
                return;
            }
            loadComparison(teamASelect.value, teamBSelect.value);
        });

        teamBSelect.addEventListener('change', () => {
            if (teamASelect.value === teamBSelect.value) {
                alert("Please select two distinct teams for tactical comparison.");
                return;
            }
            loadComparison(teamASelect.value, teamBSelect.value);
        });
    }

    if (swapBtn) {
        swapBtn.addEventListener('click', () => {
            const temp = teamASelect.value;
            teamASelect.value = teamBSelect.value;
            teamBSelect.value = temp;
            loadComparison(teamASelect.value, teamBSelect.value);
        });
    }

    // Category filter buttons
    const catButtons = document.querySelectorAll('.cat-filter-btn');
    catButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            catButtons.forEach(b => {
                b.classList.remove('active');
                b.style.background = '#f4f8f7';
                b.style.color = '#678682';
            });
            
            btn.classList.add('active');
            btn.style.background = 'var(--cp-dark-teal)';
            btn.style.color = '#ffffff';
            
            const cat = btn.getAttribute('data-category');
            filterMetricsTable(cat);
        });
    });

    // Pitch tabs (Territory vs Shots)
    const territoryTabBtn = document.getElementById('tabTerritoryBtn');
    const shotsTabBtn = document.getElementById('tabShotsBtn');
    if (territoryTabBtn && shotsTabBtn) {
        territoryTabBtn.addEventListener('click', () => {
            currentPitchTab = 'territory';
            territoryTabBtn.style.background = 'var(--cp-dark-teal)';
            territoryTabBtn.style.color = '#ffffff';
            shotsTabBtn.style.background = 'transparent';
            shotsTabBtn.style.color = '#678682';
            renderPitchView();
        });

        shotsTabBtn.addEventListener('click', () => {
            currentPitchTab = 'shots';
            shotsTabBtn.style.background = 'var(--cp-dark-teal)';
            shotsTabBtn.style.color = '#ffffff';
            territoryTabBtn.style.background = 'transparent';
            territoryTabBtn.style.color = '#678682';
            renderPitchView();
        });
    }

    // Initial load from URL or elements
    const urlParams = new URLSearchParams(window.location.search);
    const initialA = urlParams.get('teamA') || (teamASelect ? teamASelect.value : 'juventus');
    const initialB = urlParams.get('teamB') || (teamBSelect ? teamBSelect.value : 'mancity');

    if (teamASelect) teamASelect.value = initialA;
    if (teamBSelect) teamBSelect.value = initialB;

    loadComparison(initialA, initialB);
}

async function loadComparison(teamAId, teamBId) {
    try {
        const response = await fetch(`/api/compare?team_a=${encodeURIComponent(teamAId)}&team_b=${encodeURIComponent(teamBId)}`);
        const data = await response.json();

        if (data.status !== 'success') {
            console.error("API error", data);
            return;
        }

        currentComparisonData = data;
        updateUIHeaders(data.team_a, data.team_b);
        renderH2HSections(data.head_to_head_sections);
        renderRadarChart(data);
        renderMetricsTable(data.comparison_table);
        renderPitchView();
        renderSimilarityPanels(data.similarity, data.team_a, data.team_b);

        // Update URL query parameters cleanly without reload
        const newUrl = `${window.location.pathname}?teamA=${teamAId}&teamB=${teamBId}`;
        window.history.replaceState({ path: newUrl }, '', newUrl);

    } catch (err) {
        console.error("Failed to load tactical comparison:", err);
    }
}

function renderH2HSections(sections) {
    const container = document.getElementById('h2hSectionsContainer');
    if (!container || !sections) return;

    let html = '';
    sections.forEach(sec => {
        html += `
        <div class="h2h-section-card" id="${sec.category_id}-section">
            <div class="h2h-section-header" onclick="toggleH2HSection(this)">
                <h3 class="h2h-section-title">${sec.title}</h3>
                <div class="h2h-chevron-pill">
                    <i class="fa-solid fa-chevron-down"></i>
                </div>
            </div>

            <div class="h2h-section-body">
                ${(sec.stats || sec.items || []).map(item => `
                    <div class="h2h-stat-row">
                        <!-- Team A Value + Indicator -->
                        <div class="h2h-team-val-box left">
                            ${item.leader === 'team_a' ? '<div class="h2h-leader-bar team-a"></div>' : ''}
                            <span class="h2h-stat-val">${item.team_a_val}</span>
                        </div>

                        <!-- Center Stat Label -->
                        <div class="h2h-stat-label">
                            ${item.label}
                        </div>

                        <!-- Team B Value + Indicator -->
                        <div class="h2h-team-val-box right">
                            <span class="h2h-stat-val">${item.team_b_val}</span>
                            ${item.leader === 'team_b' ? '<div class="h2h-leader-bar team-b"></div>' : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
        `;
    });

    container.innerHTML = html;
}

function updateUIHeaders(teamA, teamB) {
    const aNameEls = document.querySelectorAll('.team-a-name');
    const bNameEls = document.querySelectorAll('.team-b-name');
    aNameEls.forEach(el => el.textContent = teamA.name);
    bNameEls.forEach(el => el.textContent = teamB.name);

    const aShortEls = document.querySelectorAll('.team-a-short');
    const bShortEls = document.querySelectorAll('.team-b-short');
    aShortEls.forEach(el => el.textContent = teamA.short_name || teamA.name);
    bShortEls.forEach(el => el.textContent = teamB.short_name || teamB.name);

    const aManagerEls = document.querySelectorAll('.team-a-manager');
    const bManagerEls = document.querySelectorAll('.team-b-manager');
    aManagerEls.forEach(el => el.textContent = teamA.manager);
    bManagerEls.forEach(el => el.textContent = teamB.manager);

    const aFormationEls = document.querySelectorAll('.team-a-formation');
    const bFormationEls = document.querySelectorAll('.team-b-formation');
    aFormationEls.forEach(el => el.textContent = teamA.formation);
    bFormationEls.forEach(el => el.textContent = teamB.formation);

    const aArchetypeEls = document.querySelectorAll('.team-a-archetype');
    const bArchetypeEls = document.querySelectorAll('.team-b-archetype');
    aArchetypeEls.forEach(el => el.textContent = teamA.archetype);
    bArchetypeEls.forEach(el => el.textContent = teamB.archetype);

    const aPossEls = document.querySelectorAll('.team-a-poss');
    const bPossEls = document.querySelectorAll('.team-b-poss');
    aPossEls.forEach(el => el.textContent = `${teamA.possession_pct}% Avg Possession`);
    bPossEls.forEach(el => el.textContent = `${teamB.possession_pct}% Avg Possession`);

    const aCrestEls = document.querySelectorAll('.team-a-crest');
    const bCrestEls = document.querySelectorAll('.team-b-crest');
    aCrestEls.forEach(el => {
        el.src = teamA.crest_url || `/static/img/crests/${teamA.id}.svg`;
        el.alt = teamA.name;
    });
    bCrestEls.forEach(el => {
        el.src = teamB.crest_url || `/static/img/crests/${teamB.id}.svg`;
        el.alt = teamB.name;
    });
}

function renderRadarChart(data) {
    const ctx = document.getElementById('radarChart') || document.getElementById('tacticalRadarChart');
    if (!ctx) return;

    const radarMetricKeys = [
        "npxg_per_90",
        "box_touches_per_90",
        "field_tilt_pct",
        "xt_per_90",
        "deep_completions_per_90",
        "pass_success_under_pressure_pct",
        "padj_interceptions_tackles_per_90",
        "high_turnovers_per_90"
    ];

    const labels = [];
    const teamAValues = [];
    const teamBValues = [];

    radarMetricKeys.forEach(k => {
        const item = data.comparison_table.find(m => m.key === k);
        if (item) {
            labels.push(item.name.replace(/ \/ 90|\(.*?\)/g, '').trim());
            teamAValues.push(item.pct_a);
            teamBValues.push(item.pct_b);
        }
    });

    if (radarChartInstance) {
        radarChartInstance.destroy();
    }

    radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: data.team_a.name,
                    data: teamAValues,
                    backgroundColor: 'rgba(14, 98, 92, 0.25)',
                    borderColor: '#0e625d',
                    borderWidth: 2.5,
                    pointBackgroundColor: '#0e625d',
                    pointBorderColor: '#ffffff',
                    pointHoverRadius: 6,
                    pointRadius: 4
                },
                {
                    label: data.team_b.name,
                    data: teamBValues,
                    backgroundColor: 'rgba(244, 63, 127, 0.22)',
                    borderColor: '#f43f7f',
                    borderWidth: 2.5,
                    pointBackgroundColor: '#f43f7f',
                    pointBorderColor: '#ffffff',
                    pointHoverRadius: 6,
                    pointRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: 'rgba(0, 0, 0, 0.08)' },
                    grid: { color: 'rgba(0, 0, 0, 0.06)' },
                    pointLabels: {
                        color: '#11322f',
                        font: { family: 'Plus Jakarta Sans', size: 9.5, weight: '700' }
                    },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: { display: false, stepSize: 25 }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#11322f',
                        font: { family: 'Outfit', size: 11, weight: '700' },
                        boxWidth: 10,
                        padding: 10
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 50, 47, 0.95)',
                    titleColor: '#7ce0d6',
                    bodyColor: '#ffffff',
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            return ` ${context.dataset.label}: ${context.raw}th Percentile`;
                        }
                    }
                }
            }
        }
    });
}

function renderMetricsTable(comparisonList) {
    const tbody = document.getElementById('metricsTableBody');
    if (!tbody) return;

    tbody.innerHTML = '';

    comparisonList.forEach(m => {
        const tr = document.createElement('tr');
        tr.className = 'metric-row';
        tr.setAttribute('data-category', m.category);

        const deltaSign = m.delta > 0 ? `+${m.delta}` : `${m.delta}`;
        const isAdvA = m.advantage === currentComparisonData.team_a.name;
        const isAdvB = m.advantage === currentComparisonData.team_b.name;
        const advClass = isAdvA 
            ? 'background: #e2f4f1; color: var(--cp-dark-teal); font-weight: 700;'
            : (isAdvB ? 'background: #ffe3ed; color: #f43f7f; font-weight: 700;' : 'background: #f1f5f9; color: #64748b;');

        tr.innerHTML = `
            <td class="text-start py-3">
                <div class="fw-bold" style="color: var(--cp-text-main); font-size: 13px;">${m.name}</div>
                <div class="text-muted" style="font-size: 11px;">${m.description}</div>
            </td>
            <td>
                <span class="badge" style="background: #f4f8f7; color: #678682; font-weight: 600;">${m.category}</span>
            </td>
            <td class="text-center">
                <span class="fw-bold" style="color: var(--cp-dark-teal); font-size: 13px;">${m.val_a} ${m.unit}</span>
            </td>
            <td>
                <div class="d-flex align-items-center justify-content-center gap-2">
                    <span class="text-muted" style="font-size: 11px;">${m.pct_a}%</span>
                    <div style="width: 50px; height: 6px; background: #e2edea; border-radius: 999px; overflow: hidden;">
                        <div style="width: ${m.pct_a}%; height: 100%; background: var(--cp-dark-teal);"></div>
                    </div>
                </div>
            </td>
            <td class="text-center">
                <span class="fw-bold" style="color: #f43f7f; font-size: 13px;">${m.val_b} ${m.unit}</span>
            </td>
            <td>
                <div class="d-flex align-items-center justify-content-center gap-2">
                    <span class="text-muted" style="font-size: 11px;">${m.pct_b}%</span>
                    <div style="width: 50px; height: 6px; background: #ffe6ee; border-radius: 999px; overflow: hidden;">
                        <div style="width: ${m.pct_b}%; height: 100%; background: #f43f7f;"></div>
                    </div>
                </div>
            </td>
            <td>
                <span class="badge rounded-pill px-3 py-1.5" style="${advClass}">
                    ${m.advantage} (${deltaSign})
                </span>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filterMetricsTable(category) {
    const rows = document.querySelectorAll('.metric-row');
    rows.forEach(r => {
        if (category === 'ALL' || category === 'All' || r.getAttribute('data-category') === category) {
            r.style.display = '';
        } else {
            r.style.display = 'none';
        }
    });
}

function renderPitchView() {
    const container = document.getElementById('pitchVisualizerWrapper') || document.getElementById('pitchVisualizerContainer');
    if (!container || !currentComparisonData) return;

    if (currentPitchTab === 'territory') {
        renderTerritoryGrid(container);
    } else {
        renderShotMap(container);
    }
}

function renderTerritoryGrid(container) {
    const ptData = currentComparisonData.pitch_control;
    const zones = ptData.zones || [];
    const teamA = currentComparisonData.team_a;
    const teamB = currentComparisonData.team_b;

    let svgHtml = `
    <div style="position: relative; width: 100%; height: 100%; background: #07433e; padding: 12px; border-radius: 18px; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="d-flex justify-content-between align-items-center text-white" style="font-size: 11px; font-weight: 700;">
            <span style="color: #7ce0d6;">${teamA.name} (Line: ${teamA.metrics.defensive_line_height_m}m)</span>
            <span style="color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 0.1em;">Attacking Direction &rarr;</span>
            <span style="color: #ff9cb7;">${teamB.name} (Line: ${teamB.metrics.defensive_line_height_m}m)</span>
        </div>

        <svg viewBox="0 0 600 340" style="width: 100%; height: calc(100% - 30px); border-radius: 12px;">
            <rect x="10" y="10" width="580" height="320" fill="#0d5d54" stroke="rgba(255,255,255,0.4)" stroke-width="2" rx="8" />
            <line x1="300" y1="10" x2="300" y2="330" stroke="rgba(255,255,255,0.4)" stroke-width="2" />
            <circle cx="300" cy="170" r="45" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2" />
            <rect x="10" y="70" width="85" height="200" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2" />
            <rect x="505" y="70" width="85" height="200" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2" />
    `;

    const colWidth = 580 / 6;
    const rowHeight = 320 / 3;

    zones.forEach(z => {
        const x = 10 + z.band_index * colWidth;
        const y = 10 + z.lane_index * rowHeight;
        const aPct = z.team_a_pct;
        const bPct = z.team_b_pct;
        
        let fillColor = 'rgba(14, 98, 92, 0.3)';
        if (aPct > 55) {
            const alpha = 0.25 + ((aPct - 50) / 50) * 0.55;
            fillColor = `rgba(14, 98, 92, ${alpha.toFixed(2)})`;
        } else if (bPct > 55) {
            const alpha = 0.25 + ((bPct - 50) / 50) * 0.55;
            fillColor = `rgba(244, 63, 127, ${alpha.toFixed(2)})`;
        }

        svgHtml += `
            <g class="zone-cell">
                <rect x="${x + 2}" y="${y + 2}" width="${colWidth - 4}" height="${rowHeight - 4}" 
                      rx="6" fill="${fillColor}" stroke="rgba(255,255,255,0.12)" stroke-width="1">
                    <title>${z.band_label} | ${z.lane_label}&#10;${teamA.name}: ${aPct}%&#10;${teamB.name}: ${bPct}%</title>
                </rect>
                <text x="${x + colWidth / 2}" y="${y + rowHeight / 2 - 2}" 
                      fill="#ffffff" font-size="12" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" text-anchor="middle">
                    ${aPct}%
                </text>
                <text x="${x + colWidth / 2}" y="${y + rowHeight / 2 + 14}" 
                      fill="rgba(255,255,255,0.7)" font-size="10" font-family="'Plus Jakarta Sans', sans-serif" text-anchor="middle">
                    ${bPct}%
                </text>
            </g>
        `;
    });

    svgHtml += `
        </svg>
    </div>
    `;

    container.innerHTML = svgHtml;
}

function renderShotMap(container) {
    const teamA = currentComparisonData.team_a;
    const teamB = currentComparisonData.team_b;
    const shotsA = currentComparisonData.shot_maps.team_a;
    const shotsB = currentComparisonData.shot_maps.team_b;

    let svgHtml = `
    <div style="position: relative; width: 100%; height: 100%; background: #07433e; padding: 12px; border-radius: 18px; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="d-flex justify-content-between align-items-center text-white" style="font-size: 11px; font-weight: 700;">
            <span style="color: #7ce0d6;">${teamA.name} Shots (Attacking Right &rarr;)</span>
            <div class="d-flex gap-3">
                <span><i class="fa-solid fa-circle text-warning me-1"></i> Goal</span>
                <span><i class="fa-solid fa-circle text-info me-1"></i> Saved</span>
                <span><i class="fa-solid fa-circle text-secondary me-1"></i> Miss/Block</span>
            </div>
            <span style="color: #ff9cb7;">(&larr; Attacking Left) ${teamB.name} Shots</span>
        </div>

        <svg viewBox="0 0 600 340" style="width: 100%; height: calc(100% - 30px); border-radius: 12px;">
            <rect x="10" y="10" width="580" height="320" fill="#0d5d54" stroke="rgba(255,255,255,0.4)" stroke-width="2" rx="8" />
            <line x1="300" y1="10" x2="300" y2="330" stroke="rgba(255,255,255,0.4)" stroke-width="2" />
            <circle cx="300" cy="170" r="45" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2" />
            <rect x="10" y="70" width="85" height="200" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2" />
            <rect x="505" y="70" width="85" height="200" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2" />
    `;

    shotsA.forEach(s => {
        const svgX = 300 + ((s.x - 60) / 60) * 285;
        const svgY = 10 + (s.y / 80) * 320;
        const radius = Math.max(4, Math.min(16, s.xg * 22));
        const color = s.is_goal ? '#f59e0b' : (s.outcome === 'Saved' ? '#14b8a6' : 'rgba(255, 255, 255, 0.5)');
        
        svgHtml += `
            <circle cx="${svgX.toFixed(1)}" cy="${svgY.toFixed(1)}" r="${radius.toFixed(1)}" 
                    fill="${color}" stroke="#ffffff" stroke-width="1.2" opacity="0.9">
                <title>${teamA.name}&#10;Minute: ${s.minute}'&#10;xG: ${s.xg}&#10;Outcome: ${s.outcome}</title>
            </circle>
        `;
    });

    shotsB.forEach(s => {
        const svgX = 300 - ((s.x - 60) / 60) * 285;
        const svgY = 10 + (s.y / 80) * 320;
        const radius = Math.max(4, Math.min(16, s.xg * 22));
        const color = s.is_goal ? '#f59e0b' : (s.outcome === 'Saved' ? '#f43f7f' : 'rgba(255, 255, 255, 0.5)');
        
        svgHtml += `
            <circle cx="${svgX.toFixed(1)}" cy="${svgY.toFixed(1)}" r="${radius.toFixed(1)}" 
                    fill="${color}" stroke="#ffffff" stroke-width="1.2" opacity="0.9">
                <title>${teamB.name}&#10;Minute: ${s.minute}'&#10;xG: ${s.xg}&#10;Outcome: ${s.outcome}</title>
            </circle>
        `;
    });

    svgHtml += `
        </svg>
    </div>
    `;

    container.innerHTML = svgHtml;
}

function renderSimilarityPanels(similarityData, teamA, teamB) {
    const containerA = document.getElementById('similarTwinsA') || document.getElementById('similarTeamsA');
    const containerB = document.getElementById('similarTwinsB') || document.getElementById('similarTeamsB');

    if (containerA && similarityData.team_a) {
        containerA.innerHTML = similarityData.team_a.map(sim => `
            <div class="d-flex align-items-center justify-content-between p-2.5 rounded-3 mb-1.5" style="background: #f4f8f7; border: 1px solid rgba(0,0,0,0.03);">
                <div class="d-flex align-items-center gap-2.5">
                    <span class="badge rounded-circle p-2" style="background: #e2f4f1; color: var(--cp-dark-teal); font-weight: 800; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center;">
                        ${sim.composite_score}%
                    </span>
                    <div>
                        <div class="fw-bold" style="font-size: 13px; color: var(--cp-text-main);">${sim.team_name}</div>
                        <div class="text-muted" style="font-size: 11px;">${sim.league} &bull; ${sim.tactical_archetype}</div>
                    </div>
                </div>
                <button onclick="switchTeam('A', '${sim.team_id}')" class="btn btn-sm rounded-pill fw-bold" style="background: var(--cp-dark-teal); color: #fff; font-size: 11px;">
                    Compare
                </button>
            </div>
        `).join('');
    }

    if (containerB && similarityData.team_b) {
        containerB.innerHTML = similarityData.team_b.map(sim => `
            <div class="d-flex align-items-center justify-content-between p-2.5 rounded-3 mb-1.5" style="background: #f4f8f7; border: 1px solid rgba(0,0,0,0.03);">
                <div class="d-flex align-items-center gap-2.5">
                    <span class="badge rounded-circle p-2" style="background: #ffe3ed; color: #f43f7f; font-weight: 800; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center;">
                        ${sim.composite_score}%
                    </span>
                    <div>
                        <div class="fw-bold" style="font-size: 13px; color: var(--cp-text-main);">${sim.team_name}</div>
                        <div class="text-muted" style="font-size: 11px;">${sim.league} &bull; ${sim.tactical_archetype}</div>
                    </div>
                </div>
                <button onclick="switchTeam('B', '${sim.team_id}')" class="btn btn-sm rounded-pill fw-bold" style="background: #f43f7f; color: #fff; font-size: 11px;">
                    Compare
                </button>
            </div>
        `).join('');
    }
}

window.switchTeam = function(slot, newTeamId) {
    const selectA = document.getElementById('selectTeamA');
    const selectB = document.getElementById('selectTeamB');
    if (slot === 'A' && selectA) selectA.value = newTeamId;
    if (slot === 'B' && selectB) selectB.value = newTeamId;
    if (selectA && selectB) loadComparison(selectA.value, selectB.value);
};
