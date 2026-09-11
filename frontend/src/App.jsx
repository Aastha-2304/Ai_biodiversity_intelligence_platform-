import React, { useState, useEffect } from 'react';
import NavigationSidebar from './components/layout/NavigationSidebar';
import AppHeader from './components/layout/AppHeader';
import DashboardView from './components/dashboard/DashboardView';
import BiodiversityView from './components/biodiversity/BiodiversityView';
import AssessmentFormView from './components/assessment/AssessmentFormView';
import AIScientistWorkspace from './components/scientist/AIScientistWorkspace';
import RecommendationsView from './components/recommendations/RecommendationsView';
import KnowledgeSourcesView from './components/sources/KnowledgeSourcesView';
import HistoryView from './components/history/HistoryView';
import StreamlitPortalView from './components/streamlit/StreamlitPortalView';
import EnvironmentalBackground from './components/common/EnvironmentalBackground';
import { sendChatMessage, fetchSessionDetails, resetCaseFile } from './api/client';

const INITIAL_WELCOME = {
  role: 'system',
  timestamp: 'SESSION INITIALIZED',
  text: `### 🌿 Darukaa.Earth — AI Biodiversity & Environmental Intelligence
Welcome to the unified environmental intelligence console. The system combines deterministic biophysical modeling with biome-gated RAG vector retrieval to formulate rigorous, evidence-gated ecological restoration pathways.

**Active Operational Modules:**
- **📊 Dashboard**: Immediate environmental health score, key metric cards, and ecological threshold comparisons.
- **🧬 Biodiversity Analysis**: 5-axis ecological equilibrium radar and calibrated 5-year recovery projections.
- **📝 Environmental Assessment**: Standardized telemetry entry across Edaphic, Climatic, Vegetative, and Anthropic domains.
- **🔬 AI Scientist**: 3-pane research workspace for interactive hypothesis testing and multi-turn inquiry.
- **🎯 Action Prescriptions**: Ranked field protocols with exact spatial arrangements and critical pitfalls.
- **📚 Scientific Sources**: Peer-reviewed citations from FAO, IPCC, Science, PNAS, Nature, and Ramsar.`,
  recommendations: [],
  retrieved_evidence: [],
  causal_hops: []
};

export default function App() {
  const [sessionId, setSessionId] = useState(() => 'sess_' + Math.random().toString(36).substring(2, 9));
  const [activeTab, setActiveTab] = useState('dashboard');
  const [messages, setMessages] = useState([INITIAL_WELCOME]);
  const [caseFile, setCaseFile] = useState({
    case_id: sessionId,
    profile: {
      ecosystem_type: 'forest',
      land_use: 'Fragmented temperate mixed forest',
      vegetation_cover: 24.0,
      fragmentation_index: 'severe',
      deforestation_rate: 'high',
      rainfall_mm: 850.0,
      soc_percent: 0.8
    },
    provenance: {},
    contradictions: []
  });
  const [ruleMetrics, setRuleMetrics] = useState({
    ecosystem_type: 'forest',
    system_health_index: 38,
    primary_limiting_factors: [
      'Severe forest canopy fragmentation and patch isolation distance',
      'Anthropogenic canopy deforestation and arrested natural regeneration'
    ],
    identified_risks: [
      {
        variable: 'Forest Fragmentation & Edge Desiccation',
        severity: 'Critical',
        mechanism: 'Canopy perforation allows advective winds to elevate vapor-pressure deficit (VPD) up to 200m into interior forest fragments.'
      },
      {
        variable: 'Hydraulic Xylem Cavitation',
        severity: 'Critical',
        mechanism: 'Climax canopy trees experience excessive negative xylem tension, driving edge tree mortality up to 65% above core baselines.'
      }
    ]
  });
  const [recommendations, setRecommendations] = useState([
    {
      id: 'REC-01',
      name: 'Structural Forest Biodiversity Corridors & Canopy Stepping Bridges',
      action_summary: 'Establish a 50–100m wide native multi-tier corridor reconnecting fragmented forest patches with fast-growing pioneer buffer shelterbelts.',
      scientific_reasoning: 'Re-establishes aerodynamic microclimatic humidity buffers, dropping vapor pressure deficit by 45% and eliminating physical movement barriers for interior avian taxa.',
      time_horizon: 'Medium Term (3–5 Years)',
      confidence: { score: 0.94, label: 'Very High Confidence' },
      expected_impacts: [
        { metric: 'Canopy Connectivity', change: '↑ +55%' },
        { metric: 'Edge Cavitation Mortality', change: '↓ -60%' },
        { metric: 'Interior Bird Dispersal', change: '↑ Restored' }
      ],
      implementation_protocol: {
        phase_1: 'Survey high-priority pinch points; plant fast-growing pioneer species at 2.5m spacing along exposed edges.',
        phase_2: 'Interplant native climax canopy trees and shade-tolerant understory shrubs to establish 3-tier stratification.',
        phase_3: 'Monitor canopy closure, control aggressive invasive lianas, and verify avian flyway re-establishment.'
      },
      critical_pitfalls: 'Do not plant single-species monoculture rows; mixed native frameworks with mycorrhizal inoculation are essential to resist fungal pathogens.',
      evidence_citations: ['SCIENCE-FOREST-FRAGMENTATION-2020', 'FAO-SOFO-FORESTS-2022']
    },
    {
      id: 'REC-02',
      name: 'Assisted Natural Regeneration (ANR) & Invasive Liana Suppression',
      action_summary: 'Selective manual liberation thinning of invasive choking vines combined with direct-seeding of heavy-seeded climax framework trees.',
      scientific_reasoning: 'Removes light competition and structural strangulation, allowing dormant soil seed-banks and pioneer saplings to ascend into the mid-story canopy.',
      time_horizon: 'Short Term (1–2 Years)',
      confidence: { score: 0.88, label: 'High Confidence' },
      expected_impacts: [
        { metric: 'Sapling Recruitment', change: '↑ +75%' },
        { metric: 'Natural Seedling Survival', change: '↑ +40%' }
      ],
      implementation_protocol: {
        phase_1: 'Cut invasive liana stems at ground level; avoid chemical herbicides that contaminate subsoil mycelium.',
        phase_2: 'Erect perches to attract frugivorous birds, accelerating natural ornithochoric seed rain across gaps.',
        phase_3: 'Establish perimeter mulch rings around emerging climax seedlings to retain capillary topsoil moisture.'
      },
      critical_pitfalls: 'Avoid widespread clear-cutting of undergrowth; preserve all emerging native woody seedlings during weeding.',
      evidence_citations: ['FAO-SOFO-FORESTS-2022', 'PNAS-LANDSCAPE-CONNECTIVITY-2019']
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [notification, setNotification] = useState(null);

  // Sync with backend on session load or mount
  useEffect(() => {
    fetchSessionDetails(sessionId)
      .then((data) => {
        if (data.case_file && Object.keys(data.case_file.profile || {}).length > 0) {
          setCaseFile(data.case_file);
        }
        if (data.rule_metrics && Object.keys(data.rule_metrics).length > 0) {
          setRuleMetrics(data.rule_metrics);
        }
        if (data.recommendations && data.recommendations.length > 0) {
          setRecommendations(data.recommendations);
        }
        if (data.messages && data.messages.length > 0) {
           setMessages([INITIAL_WELCOME, ...data.messages.map(m => ({
               role: m.role,
               text: m.text,
               timestamp: m.time || m.created_at || 'Previous',
               recommendations: m.recommendations || []
           }))]);
        } else {
           setMessages([INITIAL_WELCOME]);
        }
      })
      .catch((err) => {
        console.error('Failed to load session:', err);
      });
  }, [sessionId]);

  const showNotification = (msg, type = 'success') => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 4000);
  };

  const handleSendMessage = async (userText, structuredInput = null) => {
    const userMsg = {
      role: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      text: userText || (structuredInput ? `Telemetry Input:\n\`\`\`json\n${JSON.stringify(structuredInput, null, 2)}\n\`\`\`` : '')
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await sendChatMessage(userText, structuredInput, sessionId);

      const systemMsg = {
        role: 'system',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        text: response.reply_markdown,
        recommendations: response.recommendations || [],
        retrieved_evidence: response.retrieved_evidence || [],
        causal_hops: response.causal_hops || [],
        clarifying_question: response.clarifying_question || null,
        stages: response.stages || null
      };

      setMessages((prev) => [...prev, systemMsg]);

      if (response.recommendations && response.recommendations.length > 0) {
        setRecommendations(response.recommendations);
      }

      if (response.case_file_profile) {
        setCaseFile((prev) => ({
          ...prev,
          profile: response.case_file_profile,
          running_assessment: response.running_assessment
        }));
      }

      if (response.rule_metrics) {
        setRuleMetrics(response.rule_metrics);
      }

      showNotification('Environmental telemetry successfully analyzed by diagnostic pipeline.');
    } catch (err) {
      const errorMsg = {
        role: 'system',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        text: `### ⚠️ Biophysical Pipeline Diagnostic Alert\n\n${err.message || 'Unable to complete environmental analysis. Please check telemetry inputs.'}`,
        recommendations: []
      };
      setMessages((prev) => [...prev, errorMsg]);
      showNotification('Telemetry validation alert occurred.', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetSession = async () => {
    setIsLoading(true);
    try {
      await resetCaseFile(sessionId);
      setMessages([INITIAL_WELCOME]);
      showNotification('Environmental session reset to baseline.');
    } catch {
      showNotification('Local session cleared.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleApplyPreset = (text, payload) => {
    handleSendMessage(text, payload);
    setActiveTab('dashboard');
  };

  const handleTelemetrySubmit = (summaryText, payload) => {
    handleSendMessage(summaryText, payload);
    setActiveTab('dashboard');
  };

  const handleSwitchSession = (newSessionId) => {
    setSessionId(newSessionId);
    showNotification(`Switched to session ${newSessionId}`);
    setActiveTab('dashboard');
  };

  const currentEco = (caseFile.profile?.ecosystem_type || ruleMetrics?.ecosystem_type || 'agricultural').toLowerCase();
  const currentHealth = ruleMetrics?.system_health_index || 48;

  return (
    <div className="platform-shell">
      <EnvironmentalBackground />
      {/* Persistent Left Navigation Sidebar */}
      <NavigationSidebar
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        sessionId={sessionId}
        healthScore={currentHealth}
        ecosystemType={currentEco}
      />

      {/* Main Workspace Body */}
      <div className="platform-main">
        {/* Top App Header with Presets & Telemetry Badge */}
        <AppHeader
          ecosystemType={currentEco}
          onSelectPreset={handleApplyPreset}
          onResetSession={handleResetSession}
          onOpenAssessment={() => setActiveTab('assessment')}
          onOpenStreamlit={() => setActiveTab('streamlit')}
          isProcessing={isLoading}
        />

        {/* Global Floating Notification */}
        {notification && (
          <div className={`global-toast-banner ${notification.type}`}>
            <span className="toast-icon">{notification.type === 'error' ? '⚠️' : '✅'}</span>
            <span>{notification.msg}</span>
          </div>
        )}

        {/* Primary View Router */}
        <div className="platform-content-viewport">
          {activeTab === 'dashboard' && (
            <DashboardView
              caseFile={caseFile}
              ruleMetrics={ruleMetrics}
              recommendations={recommendations}
              onNavigateTab={setActiveTab}
            />
          )}

          {activeTab === 'biodiversity' && (
            <BiodiversityView
              caseFile={caseFile}
              ruleMetrics={ruleMetrics}
              onNavigateTab={setActiveTab}
            />
          )}

          {activeTab === 'assessment' && (
            <AssessmentFormView
              onSubmitTelemetry={handleTelemetrySubmit}
              isProcessing={isLoading}
            />
          )}

          {activeTab === 'scientist' && (
            <AIScientistWorkspace
              messages={messages}
              onSendMessage={handleSendMessage}
              caseFile={caseFile}
              ruleMetrics={ruleMetrics}
              isLoading={isLoading}
            />
          )}

          {activeTab === 'recommendations' && (
            <RecommendationsView
              recommendations={recommendations}
              onNavigateTab={setActiveTab}
            />
          )}

          {activeTab === 'sources' && (
            <KnowledgeSourcesView />
          )}

          {activeTab === 'history' && (
            <HistoryView
              messages={messages}
              caseFile={caseFile}
              onNavigateTab={setActiveTab}
              sessionId={sessionId}
              onSwitchSession={handleSwitchSession}
            />
          )}

          {activeTab === 'streamlit' && (
            <StreamlitPortalView />
          )}
        </div>
      </div>
    </div>
  );
}
