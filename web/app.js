const state = {
  file: null,
  sourceUrl: null,
  transcript: "",
  words: [],
  metrics: null,
  firstWord: null,
  lastWord: null,
  ledger: [],
};

const elements = {
  audioInput: document.querySelector("#audio-input"),
  dropTarget: document.querySelector("#drop-target"),
  sourceStatus: document.querySelector("#source-status"),
  sourceDetail: document.querySelector("#source-detail"),
  sourcePlayerWrap: document.querySelector("#source-player-wrap"),
  sourcePlayer: document.querySelector("#source-player"),
  transcribe: document.querySelector("#transcribe-button"),
  runtime: document.querySelector("#runtime-status"),
  transcriptEmpty: document.querySelector("#transcript-empty"),
  wordStream: document.querySelector("#word-stream"),
  metrics: document.querySelector("#metrics-status"),
  selectionBar: document.querySelector("#selection-bar"),
  selectionCopy: document.querySelector("#selection-copy"),
  clearSelection: document.querySelector("#clear-selection"),
  ledgerForm: document.querySelector("#ledger-form"),
  rowType: document.querySelector("#row-type"),
  rowNote: document.querySelector("#row-note"),
  createRow: document.querySelector("#create-row"),
  ledgerEmpty: document.querySelector("#ledger-empty"),
  ledgerList: document.querySelector("#ledger-list"),
  ledgerCount: document.querySelector("#ledger-count"),
  exportButton: document.querySelector("#export-button"),
  proofModel: document.querySelector("#proof-model"),
  proofNetwork: document.querySelector("#proof-network"),
  template: document.querySelector("#ledger-row-template"),
};

function formatTime(seconds) {
  const value = Number(seconds || 0);
  const minutes = Math.floor(value / 60);
  const remainder = (value % 60).toFixed(1).padStart(4, "0");
  return `${minutes}:${remainder}`;
}

function byteLabel(bytes) {
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function selectionRange() {
  if (state.firstWord === null || state.lastWord === null) return null;
  return [Math.min(state.firstWord, state.lastWord), Math.max(state.firstWord, state.lastWord)];
}

function updateSelectionUi() {
  const range = selectionRange();
  elements.selectionBar.hidden = !range;
  elements.createRow.disabled = !range;
  if (!range) return;
  const [start, end] = range;
  const words = state.words.slice(start, end + 1);
  elements.selectionCopy.textContent = `${formatTime(words[0].start)} to ${formatTime(words.at(-1).end)} selected`;
}

function renderWords() {
  const range = selectionRange();
  elements.wordStream.replaceChildren();
  state.words.forEach((word, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "word";
    button.textContent = word.text;
    button.title = `${formatTime(word.start)} to ${formatTime(word.end)}`;
    if (range && index >= range[0] && index <= range[1]) button.classList.add("selected");
    button.addEventListener("click", () => selectWord(index));
    elements.wordStream.append(button);
  });
  elements.transcriptEmpty.hidden = state.words.length > 0;
  updateSelectionUi();
}

function cueSource(seconds) {
  if (!state.file) return;
  elements.sourcePlayer.currentTime = Number(seconds || 0);
  elements.sourcePlayer.focus({ preventScroll: true });
}

function selectWord(index) {
  if (state.firstWord === null || state.lastWord !== null) {
    state.firstWord = index;
    state.lastWord = null;
  } else {
    state.lastWord = index;
  }
  cueSource(state.words[index].start);
  renderWords();
}

function clearSelection() {
  state.firstWord = null;
  state.lastWord = null;
  renderWords();
}

function renderLedger() {
  elements.ledgerList.replaceChildren();
  state.ledger.forEach((row) => {
    const fragment = elements.template.content.cloneNode(true);
    const item = fragment.querySelector(".ledger-row");
    fragment.querySelector(".row-kind").textContent = row.type;
    const timeButton = fragment.querySelector(".row-time");
    timeButton.textContent = `Cue ${formatTime(row.start)}`;
    timeButton.title = `Cue the local source at ${formatTime(row.start)}`;
    timeButton.addEventListener("click", () => cueSource(row.start));
    fragment.querySelector(".row-quote").textContent = `“${row.quote}”`;
    const noteInput = fragment.querySelector(".row-note-input");
    noteInput.value = row.note;
    noteInput.addEventListener("input", () => { row.note = noteInput.value; });
    fragment.querySelector(".delete-row").addEventListener("click", () => {
      state.ledger = state.ledger.filter((candidate) => candidate.id !== row.id);
      renderLedger();
    });
    item.dataset.rowId = row.id;
    elements.ledgerList.append(fragment);
  });
  const count = state.ledger.length;
  elements.ledgerCount.textContent = `${count} ${count === 1 ? "row" : "rows"}`;
  elements.ledgerEmpty.hidden = count > 0;
  elements.exportButton.disabled = count === 0;
}

async function readFileAsBase64(file) {
  const buffer = await file.arrayBuffer();
  const bytes = new Uint8Array(buffer);
  let binary = "";
  for (let index = 0; index < bytes.length; index += 1) binary += String.fromCharCode(bytes[index]);
  return btoa(binary);
}

function setFile(file) {
  if (state.sourceUrl) URL.revokeObjectURL(state.sourceUrl);
  state.file = file;
  state.sourceUrl = file ? URL.createObjectURL(file) : null;
  state.transcript = "";
  state.words = [];
  state.metrics = null;
  state.ledger = [];
  clearSelection();
  renderLedger();
  if (!file) {
    elements.sourceStatus.textContent = "No audio loaded";
    elements.sourceDetail.textContent = "No source selected.";
    elements.transcribe.disabled = true;
    elements.sourcePlayer.removeAttribute("src");
    elements.sourcePlayerWrap.hidden = true;
    return;
  }
  elements.sourcePlayer.src = state.sourceUrl;
  elements.sourcePlayerWrap.hidden = false;
  if (file.size > 8 * 1024 * 1024) {
    elements.sourceStatus.textContent = "Use a shorter WAV";
    elements.sourceDetail.textContent = `${file.name} is ${byteLabel(file.size)}. This proof accepts WAVs up to 8 MB.`;
    elements.transcribe.disabled = true;
    return;
  }
  elements.sourceStatus.textContent = "Ready locally";
  elements.sourceDetail.textContent = `${file.name} · ${byteLabel(file.size)} · removed after transcription`;
  elements.transcribe.disabled = false;
}

async function transcribe() {
  if (!state.file) return;
  elements.transcribe.disabled = true;
  elements.transcribe.textContent = "Listening locally...";
  elements.metrics.textContent = "Model working";
  try {
    const response = await fetch("/api/transcribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sourceName: state.file.name, audioBase64: await readFileAsBase64(state.file) }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "The local model could not finish this WAV.");
    state.transcript = payload.transcript;
    state.words = payload.words;
    state.metrics = payload.metrics;
    elements.metrics.textContent = `${(payload.metrics.elapsedMs / 1000).toFixed(2)} s · ${payload.words.length} moments`;
    elements.proofModel.textContent = payload.metrics.model.replace("mlx-community/", "");
    elements.proofNetwork.textContent = payload.metrics.offlineModelCache ? "Offline cached model" : "Model cache available";
    clearSelection();
    renderWords();
  } catch (error) {
    elements.metrics.textContent = error.message;
  } finally {
    elements.transcribe.textContent = "Transcribe locally";
    elements.transcribe.disabled = !state.file;
  }
}

function createLedgerRow(event) {
  event.preventDefault();
  const range = selectionRange();
  if (!range) return;
  const [startIndex, endIndex] = range;
  const words = state.words.slice(startIndex, endIndex + 1);
  const quote = words.map((word) => word.text).join(" ");
  state.ledger.push({
    id: crypto.randomUUID(),
    type: elements.rowType.value,
    note: elements.rowNote.value.trim() || "Review this source moment.",
    quote,
    start: words[0].start,
    end: words.at(-1).end,
  });
  elements.rowNote.value = "";
  clearSelection();
  renderLedger();
}

function exportLedger() {
  const payload = {
    exportedAt: new Date().toISOString(),
    sourceName: state.file?.name || "voice-note.wav",
    transcript: state.transcript,
    metrics: state.metrics,
    ledger: state.ledger,
    localOnly: true,
  };
  const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = "arm-voice-ledger.json";
  link.click();
  URL.revokeObjectURL(url);
}

async function checkRuntime() {
  try {
    const response = await fetch("/api/health");
    const payload = await response.json();
    elements.runtime.textContent = payload.offlineModelCache ? "Offline model cache ready" : "Local model ready";
    elements.proofNetwork.textContent = payload.offlineModelCache ? "Offline cached model" : "Local model cache";
    elements.proofModel.textContent = payload.model.replace("mlx-community/", "");
  } catch {
    elements.runtime.textContent = "Local server unavailable";
    elements.proofNetwork.textContent = "Server unavailable";
  }
}

elements.audioInput.addEventListener("change", (event) => setFile(event.target.files?.[0] || null));
elements.dropTarget.addEventListener("dragover", (event) => event.preventDefault());
elements.dropTarget.addEventListener("drop", (event) => {
  event.preventDefault();
  setFile(event.dataTransfer.files?.[0] || null);
});
elements.transcribe.addEventListener("click", transcribe);
elements.clearSelection.addEventListener("click", clearSelection);
elements.ledgerForm.addEventListener("submit", createLedgerRow);
elements.exportButton.addEventListener("click", exportLedger);
checkRuntime();
