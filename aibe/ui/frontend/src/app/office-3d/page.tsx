"use client";

import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import { ALL_AGENTS, TIERS } from "@/lib/agents-data";
import { api } from "@/lib/api";
import { useAgentStore } from "@/stores/agent-store";
import { useMeetingStore } from "@/stores/meeting-store";
import { useWsStore } from "@/stores/ws-store";
import { ZOOM_MAX, ZOOM_MIN } from "@/pixelagents/constants";
import { EditorState } from "@/pixelagents/office/editor/editorState";
import { OfficeState } from "@/pixelagents/office/engine/officeState";
import { OfficeCanvas } from "@/pixelagents/office/components/OfficeCanvas";
import { loadPixelAgentsAssets } from "@/pixelagents/assetLoader";
import { EditorToolbar } from "@/pixelagents/office/editor/EditorToolbar";
import { useEditorActions } from "@/pixelagents/hooks/useEditorActions";

type ChatMessage = {
  id: string;
  role: "operator" | "agent" | "system";
  author: string;
  text: string;
  timestamp: string;
};

const editorState = new EditorState();

export default function Office2DDepthPage() {
  const agents = useAgentStore((s) => s.agents);
  const refreshAgents = useAgentStore((s) => s.refreshAgents);
  const meetings = useMeetingStore((s) => s.meetings);
  const refreshMeetings = useMeetingStore((s) => s.refreshMeetings);
  const connected = useWsStore((s) => s.connected);
  const connectWs = useWsStore((s) => s.connect);
  const agentStatuses = useWsStore((s) => s.agentStatuses);
  const officeRef = useRef<HTMLDivElement | null>(null);
  const officeStateRef = useRef<OfficeState | null>(null);
  const templatesReadyRef = useRef(false);
  const [selectedAgentId, setSelectedAgentId] = useState(ALL_AGENTS[0]?.id ?? "oracle");
  const [meetingTopic, setMeetingTopic] = useState("Daily Tactical Sync");
  const [chatInput, setChatInput] = useState("");
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [sending, setSending] = useState(false);
  const [, setRenderTick] = useState(0);
  const [chatLog, setChatLog] = useState<ChatMessage[]>([
    {
      id: crypto.randomUUID(),
      role: "system",
      author: "System",
      text: "Pixel office online. Selecione um agente para conversar ou convocar reunião.",
      timestamp: new Date().toISOString(),
    },
  ]);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [loadedAssets, setLoadedAssets] = useState<any>(null);

  const backendById = useMemo(() => new Map(agents.map((agent) => [agent.agent_id, agent])), [agents]);
  const numericIdByAgentId = useMemo(
    () => new Map(ALL_AGENTS.map((agent, index) => [agent.id, index + 1])),
    [],
  );
  const agentIdByNumericId = useMemo(
    () => new Map(ALL_AGENTS.map((agent, index) => [index + 1, agent.id])),
    [],
  );
  const selectedAgent = useMemo(
    () => ALL_AGENTS.find((agent) => agent.id === selectedAgentId) || ALL_AGENTS[0],
    [selectedAgentId],
  );

  const activeMeetingParticipants = useMemo(() => {
    const set = new Set<string>();
    for (const meeting of meetings) {
      if (meeting.status === "in_progress" || meeting.status === "active" || meeting.status === "scheduled") {
        for (const participant of meeting.participants) {
          set.add(participant);
        }
      }
    }
    return set;
  }, [meetings]);

  const sceneAgents = useMemo(
    () =>
      ALL_AGENTS.map((agent) => {
        const live = backendById.get(agent.id);
        const status = agentStatuses[agent.id] || live?.status || "offline";
        const isActive = status === "running" || status === "ready" || status === "active";
        const tier = TIERS.find((item) => item.id === agent.tier);
        return {
          id: agent.id,
          name: agent.name,
          role: agent.role,
          tierColor: tier?.color || "#8B5CF6",
          status,
          isActive,
          inMeeting: activeMeetingParticipants.has(agent.id),
          tasks: live?.tasks_completed ?? 0,
          errors: live?.error_count ?? 0,
        };
      }),
    [activeMeetingParticipants, agentStatuses, backendById],
  );

  const activeCount = sceneAgents.filter((agent) => agent.isActive).length;
  const meetingCount = sceneAgents.filter((agent) => agent.inMeeting).length;

  const getOfficeState = () => {
    if (!officeStateRef.current) {
      officeStateRef.current = new OfficeState();
    }
    return officeStateRef.current;
  };

  const editor = useEditorActions(getOfficeState, editorState);

  useEffect(() => {
    if (!templatesReadyRef.current) {
      loadPixelAgentsAssets().then((res) => {
        if (res?.layout && officeStateRef.current) {
          officeStateRef.current.rebuildFromLayout(res.layout);
        }
        if (res?.loadedAssets) {
          setLoadedAssets(res.loadedAssets);
        }
        templatesReadyRef.current = true;
        // Force a re-render to ensure layout is drawn
        setRenderTick(t => t + 1);
      });
    }
  }, []);

  useEffect(() => {
    connectWs();
    void refreshAgents();
    void refreshMeetings();
    const refreshTimer = setInterval(() => {
      void refreshAgents();
      void refreshMeetings();
    }, 20_000);
    return () => clearInterval(refreshTimer);
  }, [connectWs, refreshAgents, refreshMeetings]);

  useEffect(() => {
    const os = getOfficeState();
    const targetIds = new Set<number>();
    for (const [agentId, numericId] of numericIdByAgentId) {
      targetIds.add(numericId);
      if (!os.characters.has(numericId)) {
        const meta = ALL_AGENTS.find((agent) => agent.id === agentId);
        
        let dept = "executive";
        if (meta?.tierName === "AI / ML") dept = "ml";
        else if (meta?.tierName) dept = meta.tierName.toLowerCase();

        // Assign a random seat from that department
        // Assuming there are max 4 seats per department (0 to 3)
        // officeState will fall back to any free seat if this specific one is taken
        const randomSeatIdx = Math.floor(Math.random() * 4);
        const preferredSeat = `seat-${dept}-${randomSeatIdx}`;

        os.addAgent(numericId, undefined, undefined, preferredSeat, true, meta?.name);
      }
    }
    for (const numericId of Array.from(os.characters.keys())) {
      if (numericId > 0 && !targetIds.has(numericId)) {
        os.removeAgent(numericId);
      }
    }
  }, [numericIdByAgentId]);

  useEffect(() => {
    const os = getOfficeState();
    for (const agent of sceneAgents) {
      const numericId = numericIdByAgentId.get(agent.id);
      if (!numericId) continue;
      os.setAgentActive(numericId, agent.isActive);
      os.setAgentTool(numericId, agent.inMeeting ? "Meeting" : agent.isActive ? "Working" : null);
      
      if (agent.inMeeting) {
        const currentSeat = os.characters.get(numericId)?.seatId;
        if (!currentSeat || !currentSeat.startsWith("seat-meeting")) {
          let meetingSeat = null;
          for (const [uid, seat] of os.seats) {
            if (uid.startsWith("seat-meeting") && !seat.assigned) {
              meetingSeat = uid;
              break;
            }
          }
          if (meetingSeat) {
            os.reassignSeat(numericId, meetingSeat);
          }
        }
      } else {
        const currentSeat = os.characters.get(numericId)?.seatId;
        if (currentSeat && currentSeat.startsWith("seat-meeting")) {
           let dept = "executive";
           const meta = ALL_AGENTS.find((a) => a.id === agent.id);
           if (meta?.tierName === "AI / ML") dept = "ml";
           else if (meta?.tierName) dept = meta.tierName.toLowerCase();
           
           let newSeat = null;
           for (const [uid, seat] of os.seats) {
             if (uid.startsWith(`seat-${dept}`) && !seat.assigned) {
               newSeat = uid;
               break;
             }
           }
           if (newSeat) {
             os.reassignSeat(numericId, newSeat);
           }
        }
      }

      if (agent.status === "waiting") {
        os.showWaitingBubble(numericId);
      }
      if (agent.status !== "waiting") {
        os.clearPermissionBubble(numericId);
      }
    }
  }, [numericIdByAgentId, sceneAgents]);

  useEffect(() => {
    const selectedNumericId = numericIdByAgentId.get(selectedAgentId);
    if (!selectedNumericId) return;
    const os = getOfficeState();
    os.selectedAgentId = selectedNumericId;
    os.cameraFollowId = selectedNumericId;
  }, [numericIdByAgentId, selectedAgentId]);

  useEffect(() => {
    const timer = setInterval(() => setRenderTick((value) => value + 1), 150);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const onChange = () => setIsFullscreen(Boolean(document.fullscreenElement));
    document.addEventListener("fullscreenchange", onChange);
    return () => document.removeEventListener("fullscreenchange", onChange);
  }, []);

  async function toggleFullscreen() {
    if (!officeRef.current) return;
    if (!document.fullscreenElement) {
      await officeRef.current.requestFullscreen();
      return;
    }
    await document.exitFullscreen();
  }

  async function handleConveneMeeting() {
    const topic = meetingTopic.trim();
    if (!topic || !selectedAgent) return;
    setSending(true);
    try {
      const participants = Array.from(new Set([selectedAgent.id, "oracle", "minerva"]));
      await api.meetings.create({
        topic,
        participants,
        meeting_type: "strategy",
        max_rounds: 8,
      });
      setChatLog((prev) => [
        {
          id: crypto.randomUUID(),
          role: "system",
          author: "System",
          text: `Meeting "${topic}" initiated with ${participants.join(", ")}.`,
          timestamp: new Date().toISOString(),
        },
        ...prev,
      ]);
      await refreshMeetings();
      setMeetingTopic("");
    } finally {
      setSending(false);
    }
  }

  async function handleSendChat() {
    const text = chatInput.trim();
    if (!text || !selectedAgent) return;
    setSending(true);
    setChatLog((prev) => [
      {
        id: crypto.randomUUID(),
        role: "operator",
        author: "You",
        text,
        timestamp: new Date().toISOString(),
      },
      ...prev,
    ]);
    setChatInput("");
    try {
      await api.tasks.submit({
        target_agent: selectedAgent.id,
        title: `Operator message: ${text.slice(0, 64)}`,
        description: text,
        priority: 2,
      });
      setChatLog((prev) => [
        {
          id: crypto.randomUUID(),
          role: "agent",
          author: selectedAgent.name,
          text: "Message received. Working on it now.",
          timestamp: new Date().toISOString(),
        },
        ...prev,
      ]);
    } catch {
      setChatLog((prev) => [
        {
          id: crypto.randomUUID(),
          role: "system",
          author: "System",
          text: "Failed to deliver message to backend.",
          timestamp: new Date().toISOString(),
        },
        ...prev,
      ]);
    } finally {
      setSending(false);
    }
  }

  return (
    <main className="h-[calc(100vh-24px)] px-2 pb-2 pt-1 md:px-4">
      <div
        ref={officeRef}
        className="relative flex h-full min-h-0 flex-col overflow-hidden rounded-md border-2 border-[#4f4f4f] bg-[#1a1a1a]"
      >
        <header className="relative z-20 flex flex-wrap items-center justify-between gap-2 border-b-2 border-[#4f4f4f] bg-[#111111] px-3 py-2 text-[#f5f5f5]">
          <div className="flex items-center gap-2">
            <span className="rounded border border-[#5e5e5e] bg-[#1b1b1b] px-2 py-1 text-[11px] uppercase tracking-[0.14em]">
              Pixel Agents Office
            </span>
            <span className="text-xs text-[#c4c4c4]">2D + depth + live agents</span>
          </div>
          <div className="flex flex-wrap items-center gap-1.5 text-[11px]">
            <button
              type="button"
              onClick={editor.handleToggleEditMode}
              className={`rounded border px-2 py-1 ${editor.isEditMode ? "border-amber-500/70 bg-amber-500/20 text-amber-200" : "border-[#5e5e5e] bg-[#212121] hover:bg-[#2c2c2c]"}`}
            >
              {editor.isEditMode ? "Exit Edit" : "Edit Layout"}
            </button>
            <span className="rounded border border-[#5e5e5e] bg-[#212121] px-2 py-1">Agents: {sceneAgents.length}</span>
            <span className="rounded border border-[#5e5e5e] bg-[#212121] px-2 py-1">Active: {activeCount}</span>
            <span className="rounded border border-[#5e5e5e] bg-[#212121] px-2 py-1">In meeting: {meetingCount}</span>
            <span
              className={`rounded border px-2 py-1 ${
                connected ? "border-emerald-500/70 bg-emerald-500/20 text-emerald-200" : "border-amber-500/70 bg-amber-500/20 text-amber-200"
              }`}
            >
              WS: {connected ? "online" : "offline"}
            </span>
            <button
              type="button"
              onClick={() => editor.handleZoomChange(Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, editor.zoom - 1)))}
              className="rounded border border-[#5e5e5e] bg-[#212121] px-2 py-1 hover:bg-[#2c2c2c]"
            >
              -
            </button>
            <span className="rounded border border-[#5e5e5e] bg-[#212121] px-2 py-1">{editor.zoom}x</span>
            <button
              type="button"
              onClick={() => editor.handleZoomChange(Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, editor.zoom + 1)))}
              className="rounded border border-[#5e5e5e] bg-[#212121] px-2 py-1 hover:bg-[#2c2c2c]"
            >
              +
            </button>
            <button
              type="button"
              onClick={toggleFullscreen}
              className="rounded border border-[#5e5e5e] bg-[#212121] px-2 py-1 hover:bg-[#2c2c2c]"
            >
              {isFullscreen ? "Exit Fullscreen" : "Fullscreen"}
            </button>
            <Link href="/" className="rounded border border-[#5e5e5e] bg-[#212121] px-2 py-1 hover:bg-[#2c2c2c]">
              Back
            </Link>
          </div>
        </header>

        <section className="grid min-h-0 flex-1 grid-cols-1 xl:grid-cols-[1fr_340px]">
          <div className="relative min-h-0 bg-[#181818]">
            <OfficeCanvas
              officeState={getOfficeState()}
              onClick={(numericId) => {
                const mappedAgentId = agentIdByNumericId.get(numericId);
                if (mappedAgentId) {
                  setSelectedAgentId(mappedAgentId);
                }
              }}
              isEditMode={editor.isEditMode}
              editorState={editorState}
              onEditorTileAction={editor.handleEditorTileAction}
              onEditorEraseAction={editor.handleEditorEraseAction}
              onEditorSelectionChange={editor.handleEditorSelectionChange}
              onDeleteSelected={editor.handleDeleteSelected}
              onRotateSelected={editor.handleRotateSelected}
              onDragMove={editor.handleDragMove}
              editorTick={editor.editorTick}
              zoom={editor.zoom}
              onZoomChange={editor.handleZoomChange}
              panRef={editor.panRef}
            />
            {editor.isEditMode && loadedAssets && (
              <div className="absolute bottom-4 left-1/2 -translate-x-1/2 rounded-lg bg-[#1a1a1a]/90 p-2 shadow-xl backdrop-blur-sm border border-[#333]">
                <div className="mb-2 flex items-center justify-between border-b border-[#333] pb-2 px-2">
                  <span className="text-xs font-semibold text-[#ccc] uppercase tracking-wider">Layout Editor</span>
                  <div className="flex gap-2">
                    <button
                      onClick={() => {
                        const json = JSON.stringify(getOfficeState().layout, null, 2);
                        const blob = new Blob([json], { type: "application/json" });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement("a");
                        a.href = url;
                        a.download = "office-layout.json";
                        a.click();
                        URL.revokeObjectURL(url);
                      }}
                      className="rounded bg-[#2a2a2a] px-2 py-1 text-xs text-[#ccc] hover:bg-[#3a3a3a] border border-[#444]"
                    >
                      Export Layout
                    </button>
                    <button
                      onClick={() => {
                        getOfficeState().resizeMap(getOfficeState().cols + 5, getOfficeState().rows + 5);
                        setRenderTick(t => t + 1);
                      }}
                      className="rounded bg-[#2a2a2a] px-2 py-1 text-xs text-[#ccc] hover:bg-[#3a3a3a] border border-[#444]"
                    >
                      Expand Map
                    </button>
                  </div>
                </div>
                <EditorToolbar
                  activeTool={editorState.activeTool}
                  selectedTileType={editorState.selectedTileType}
                  selectedFurnitureType={editorState.selectedFurnitureType}
                  selectedFurnitureUid={editorState.selectedFurnitureUid}
                  selectedFurnitureColor={
                    editorState.selectedFurnitureUid
                      ? (getOfficeState().layout.furniture.find((f) => f.uid === editorState.selectedFurnitureUid)?.color ?? null)
                      : null
                  }
                  floorColor={editorState.floorColor}
                  wallColor={editorState.wallColor}
                  selectedWallSet={editorState.selectedWallSet}
                  onToolChange={editor.handleToolChange}
                  onTileTypeChange={editor.handleTileTypeChange}
                  onFloorColorChange={editor.handleFloorColorChange}
                  onWallColorChange={editor.handleWallColorChange}
                  onWallSetChange={editor.handleWallSetChange}
                  onSelectedFurnitureColorChange={editor.handleSelectedFurnitureColorChange}
                  onFurnitureTypeChange={editor.handleFurnitureTypeChange}
                  loadedAssets={loadedAssets}
                />
              </div>
            )}
          </div>

          <aside className="min-h-0 border-l-2 border-[#4f4f4f] bg-[#121212] p-2">
            <div className="flex h-full min-h-0 flex-col gap-2">
              <div className="rounded border border-[#4f4f4f] bg-[#1b1b1b] p-2 text-xs">
                <p className="text-[10px] uppercase tracking-[0.14em] text-[#a9a9a9]">Focused Agent</p>
                <p className="mt-1 text-sm font-semibold text-white">{selectedAgent?.name}</p>
                <p className="text-[#b2b2b2]">{selectedAgent?.role}</p>
              </div>

              <div className="rounded border border-[#4f4f4f] bg-[#1b1b1b] p-2 text-xs">
                <p className="text-[10px] uppercase tracking-[0.14em] text-[#a9a9a9]">Agent Roster</p>
                <div className="mt-2 max-h-32 space-y-1 overflow-y-auto pr-1">
                  {sceneAgents.map((agent) => (
                    <button
                      key={agent.id}
                      type="button"
                      onClick={() => setSelectedAgentId(agent.id)}
                      className={`flex w-full items-center justify-between rounded border px-2 py-1 text-left ${
                        selectedAgentId === agent.id
                          ? "border-cyber-cyan bg-cyber-cyan/15 text-white"
                          : "border-[#4f4f4f] bg-[#222] text-[#cfcfcf] hover:bg-[#2b2b2b]"
                      }`}
                    >
                      <span className="truncate">{agent.name}</span>
                      <span
                        className={`ml-2 h-2.5 w-2.5 rounded-full ${
                          agent.inMeeting ? "bg-cyan-300" : agent.isActive ? "bg-emerald-400" : "bg-amber-400"
                        }`}
                        style={{ boxShadow: `0 0 8px ${agent.tierColor}` }}
                      />
                    </button>
                  ))}
                </div>
              </div>

              <div className="rounded border border-[#4f4f4f] bg-[#1b1b1b] p-2 text-xs">
                <p className="text-[10px] uppercase tracking-[0.14em] text-[#a9a9a9]">Convene Meeting</p>
                <input
                  value={meetingTopic}
                  onChange={(event) => setMeetingTopic(event.target.value)}
                  placeholder="Meeting topic"
                  className="mt-2 w-full rounded border border-[#4f4f4f] bg-[#262626] px-2 py-1.5 text-xs text-white outline-none"
                />
                <button
                  type="button"
                  disabled={sending}
                  onClick={handleConveneMeeting}
                  className="mt-2 w-full rounded border border-[#4f4f4f] bg-[#2c2150] px-2 py-1.5 text-xs text-[#d9d5ff] hover:bg-[#3c2b67] disabled:opacity-60"
                >
                  Start Meeting
                </button>
              </div>

              <div className="rounded border border-[#4f4f4f] bg-[#1b1b1b] p-2 text-xs">
                <p className="text-[10px] uppercase tracking-[0.14em] text-[#a9a9a9]">Chat</p>
                <textarea
                  value={chatInput}
                  onChange={(event) => setChatInput(event.target.value)}
                  placeholder={`Message ${selectedAgent?.name}`}
                  className="mt-2 h-16 w-full resize-none rounded border border-[#4f4f4f] bg-[#262626] px-2 py-1.5 text-xs text-white outline-none"
                />
                <button
                  type="button"
                  disabled={sending}
                  onClick={handleSendChat}
                  className="mt-2 w-full rounded border border-[#4f4f4f] bg-[#1f3950] px-2 py-1.5 text-xs text-[#b7deff] hover:bg-[#285274] disabled:opacity-60"
                >
                  Send to Agent
                </button>
              </div>

              <div className="min-h-0 flex-1 overflow-hidden rounded border border-[#4f4f4f] bg-[#1b1b1b] p-2">
                <p className="text-[10px] uppercase tracking-[0.14em] text-[#a9a9a9]">Operation Log</p>
                <div className="mt-2 h-[calc(100%-18px)] space-y-1 overflow-y-auto pr-1">
                  {chatLog.map((message) => (
                    <article key={message.id} className="rounded border border-[#3f3f3f] bg-[#232323] p-1.5 text-[11px] text-[#cdcdcd]">
                      <div className="mb-1 flex items-center justify-between">
                        <p
                          className={`font-semibold ${
                            message.role === "operator"
                              ? "text-cyan-300"
                              : message.role === "agent"
                                ? "text-emerald-300"
                                : "text-amber-300"
                          }`}
                        >
                          {message.author}
                        </p>
                        <p className="text-[10px] text-[#8f8f8f]">{new Date(message.timestamp).toLocaleTimeString()}</p>
                      </div>
                      <p>{message.text}</p>
                    </article>
                  ))}
                </div>
              </div>
            </div>
          </aside>
        </section>
      </div>
    </main>
  );
}



