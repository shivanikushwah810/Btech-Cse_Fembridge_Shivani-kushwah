/**
 * FemBridge – main.js
 * Shared utilities: API calls, toast notifications, auth helpers, navbar
 */

const API = "http://localhost:5000";

/* ── Toast Notification ──────────────────────────────────────────────────── */
function showToast(message, type = "info") {
  const existing = document.getElementById("toast-el");
  if (existing) existing.remove();

  const icons = { success: "✅", error: "❌", info: "ℹ️", warning: "⚠️" };
  const toast = document.createElement("div");
  toast.id = "toast-el";
  toast.className = `toast-custom ${type}`;
  toast.innerHTML = `<span>${icons[type] || "ℹ️"}</span><span>${message}</span>`;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = "slideIn 0.3s ease reverse";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

/* ── API Helper ──────────────────────────────────────────────────────────── */
async function apiFetch(endpoint, options = {}) {
  try {
    const res = await fetch(API + endpoint, {
      credentials: "include",
      headers: { "Content-Type": "application/json", ...options.headers },
      ...options,
    });
    return await res.json();
  } catch (err) {
    console.error("API Error:", err);
    return { success: false, message: "Server connection failed. Is the backend running?" };
  }
}

/* ── Auth Helpers ────────────────────────────────────────────────────────── */
function getUser() {
  try {
    return JSON.parse(localStorage.getItem("fembridge_user") || "null");
  } catch {
    return null;
  }
}

function setUser(user) {
  localStorage.setItem("fembridge_user", JSON.stringify(user));
}

function clearUser() {
  localStorage.removeItem("fembridge_user");
}

function requireAuth(redirectTo = "login.html") {
  const user = getUser();
  if (!user) {
    showToast("Please login to continue.", "warning");
    setTimeout(() => (window.location.href = redirectTo), 1200);
    return null;
  }
  return user;
}

/* ── Navbar Setup ────────────────────────────────────────────────────────── */
function setupNavbar() {
  const user = getUser();
  const navAuth = document.getElementById("nav-auth");
  const navUser = document.getElementById("nav-user");
  const navName = document.getElementById("nav-username");

  if (!navAuth || !navUser) return;

  if (user) {
    navAuth.style.display = "none";
    navUser.style.display = "flex";
    if (navName) navName.textContent = user.name.split(" ")[0];
  } else {
    navAuth.style.display = "flex";
    navUser.style.display = "none";
  }
}

async function handleLogout() {
  await apiFetch("/logout", { method: "POST" });
  clearUser();
  showToast("Logged out successfully.", "success");
  setTimeout(() => (window.location.href = "index.html"), 800);
}

/* ── Loading Helpers ─────────────────────────────────────────────────────── */
function showLoading(containerId, message = "Loading...") {
  const el = document.getElementById(containerId);
  if (el) {
    el.innerHTML = `
      <div class="page-loading">
        <div class="spinner"></div>
        <span>${message}</span>
      </div>`;
  }
}

function showEmpty(containerId, icon = "💼", message = "Nothing here yet.") {
  const el = document.getElementById(containerId);
  if (el) {
    el.innerHTML = `
      <div class="empty-state fade-in">
        <div class="empty-icon">${icon}</div>
        <p>${message}</p>
      </div>`;
  }
}

/* ── Job Card Builder ────────────────────────────────────────────────────── */
function buildJobCard(job, showApply = true, showScore = false) {
  const isRemote = job.location?.toLowerCase() === "remote";
  const scoreBadge = showScore && job.match_score != null
    ? `<span class="match-score-badge">🤖 ${job.match_score}% match</span>`
    : "";

  const matchedSkills = showScore && job.matched_skills?.length
    ? `<p style="font-size:0.78rem;color:var(--gray-500);margin-top:0.4rem;">
         Skills matched: <strong>${job.matched_skills.join(", ")}</strong>
       </p>`
    : "";

  const applyBtn = showApply
    ? `<button class="btn-primary-pink" onclick="applyJob(${job.id})" style="margin-top:1rem;width:100%">
         Apply Now →
       </button>`
    : "";

  return `
    <div class="job-card fade-in" style="margin-bottom:1rem;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem;">
        <div>
          <div class="job-title">${job.title}</div>
          <div class="job-company">🏢 ${job.company}</div>
        </div>
        <div style="display:flex;gap:0.4rem;flex-wrap:wrap;">
          ${scoreBadge}
          <span class="badge-type">${job.type}</span>
          ${isRemote ? '<span class="badge-remote">🌐 Remote</span>' : ""}
        </div>
      </div>
      <div class="job-meta" style="margin-top:0.7rem;">
        <span>📍 ${job.location}</span>
        <span>💰 ${job.salary}</span>
      </div>
      ${matchedSkills}
      ${job.description
        ? `<p style="font-size:0.85rem;color:var(--gray-500);margin-top:0.5rem;line-height:1.5;">
             ${job.description.split(" ").slice(0, 18).join(" ")}...
           </p>`
        : ""}
      ${applyBtn}
    </div>`;
}

/* ── Apply Job ───────────────────────────────────────────────────────────── */
async function applyJob(jobId) {
  const user = getUser();
  if (!user) {
    showToast("Please login to apply for jobs.", "warning");
    setTimeout(() => (window.location.href = "login.html"), 1200);
    return;
  }

  const data = await apiFetch("/apply", {
    method: "POST",
    body: JSON.stringify({ job_id: jobId }),
  });

  showToast(data.message, data.success ? "success" : "error");
}

/* ── Init ────────────────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  setupNavbar();

  // Logout button listener
  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) logoutBtn.addEventListener("click", handleLogout);
});