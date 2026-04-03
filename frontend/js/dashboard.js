/**
 * FemBridge – dashboard.js
 * Loads dashboard stats, applied jobs, resume score, and recommendations
 */

document.addEventListener("DOMContentLoaded", async () => {
  const user = requireAuth();
  if (!user) return;

  // Set greeting
  const greetEl = document.getElementById("dash-greeting");
  if (greetEl) greetEl.textContent = `Welcome back, ${user.name.split(" ")[0]}! 🌸`;

  // Load all dashboard sections in parallel
  await Promise.all([
    loadDashboardStats(),
    loadAppliedJobs(),
    loadResumeScore(),
    loadRecommendations(),
  ]);

  // Resume upload handler
  const resumeInput = document.getElementById("resume-upload");
  if (resumeInput) {
    resumeInput.addEventListener("change", handleResumeUpload);
  }
});

async function loadDashboardStats() {
  const data = await apiFetch("/dashboard");
  if (!data.success) return;

  setEl("stat-applied",  data.applied_count);
  setEl("stat-score",    data.resume_score + "%");
  setEl("stat-jobs",     data.total_jobs);
}

async function loadAppliedJobs() {
  showLoading("applied-jobs-list", "Loading your applications...");
  const data = await apiFetch("/my-applications");

  if (!data.success || !data.applications?.length) {
    showEmpty("applied-jobs-list", "📋", "No applications yet. Start applying!");
    return;
  }

  const container = document.getElementById("applied-jobs-list");
  container.innerHTML = data.applications.map(app => `
    <div class="job-card fade-in" style="margin-bottom:0.8rem;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem;">
        <div>
          <div class="job-title">${app.title}</div>
          <div class="job-company">🏢 ${app.company}</div>
        </div>
        <span class="badge-type" style="background:${statusColor(app.status)}20;color:${statusColor(app.status)};border-color:${statusColor(app.status)}50;">
          ${statusIcon(app.status)} ${app.status}
        </span>
      </div>
      <div class="job-meta" style="margin-top:0.5rem;">
        <span>📍 ${app.location}</span>
        <span>💰 ${app.salary}</span>
        <span>${app.type}</span>
      </div>
    </div>
  `).join("");
}

async function loadResumeScore() {
  const data = await apiFetch("/resume/score");
  if (!data.success) return;

  const score = data.score || 0;
  setEl("resume-score-display", score + "/100");

  // Animate the score ring
  const ring = document.getElementById("score-ring");
  if (ring) {
    ring.style.background = `conic-gradient(var(--pink-deep) ${score * 3.6}deg, var(--pink-light) 0deg)`;
  }

  const suggestionsEl = document.getElementById("resume-suggestions");
  if (suggestionsEl && data.suggestions?.length) {
    suggestionsEl.innerHTML = data.suggestions.map(s =>
      `<li style="margin-bottom:0.4rem;font-size:0.88rem;color:var(--gray-700);">💡 ${s}</li>`
    ).join("");
  } else if (suggestionsEl) {
    suggestionsEl.innerHTML = `<li style="color:var(--gray-500);font-size:0.88rem;">Upload your resume to get personalized tips.</li>`;
  }
}

async function loadRecommendations() {
  showLoading("recommendations-list", "Our AI is finding your best matches...");
  const data = await apiFetch("/recommend");

  if (!data.success || !data.recommendations?.length) {
    showEmpty("recommendations-list", "🤖", data.message || "Update your skills in your profile to get AI recommendations!");
    return;
  }

  const container = document.getElementById("recommendations-list");
  container.innerHTML = data.recommendations.map(job => buildJobCard(job, true, true)).join("");
}

async function handleResumeUpload(e) {
  const file = e.target.files[0];
  if (!file) return;

  const uploadStatus = document.getElementById("upload-status");
  if (uploadStatus) uploadStatus.textContent = "⏳ Analyzing your resume...";

  const formData = new FormData();
  formData.append("resume", file);

  try {
    const res = await fetch("http://localhost:5000/resume", {
      method: "POST",
      credentials: "include",
      body: formData,
    });
    const data = await res.json();

    if (data.success) {
      showToast(`Resume analyzed! Score: ${data.score}/100`, "success");
      if (uploadStatus) uploadStatus.textContent = `✅ Uploaded! Score: ${data.score}/100`;
      await loadResumeScore();
      await loadDashboardStats();
    } else {
      showToast(data.message || "Upload failed.", "error");
      if (uploadStatus) uploadStatus.textContent = "❌ Upload failed.";
    }
  } catch {
    showToast("Upload error. Please try again.", "error");
  }
}

/* ── Helpers ─────────────────────────────────────────────────────────────── */
function setEl(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function statusColor(status) {
  return { Pending: "#f59e0b", Reviewed: "#3b82f6", Shortlisted: "#22c55e", Rejected: "#ef4444" }[status] || "#9e9e9e";
}

function statusIcon(status) {
  return { Pending: "⏳", Reviewed: "👀", Shortlisted: "⭐", Rejected: "❌" }[status] || "•";
}