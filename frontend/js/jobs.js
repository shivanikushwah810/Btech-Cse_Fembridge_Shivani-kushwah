/**
 * FemBridge – jobs.js
 * Job listing, search/filter, and apply functionality
 */

document.addEventListener("DOMContentLoaded", async () => {
  await loadJobs();

  // Filter listeners
  document.getElementById("search-input")?.addEventListener("input", debounce(loadJobs, 400));
  document.getElementById("type-filter")?.addEventListener("change", loadJobs);
  document.getElementById("location-filter")?.addEventListener("change", loadJobs);

  // Pre-fill location filter from user profile
  const user = getUser();
  const locFilter = document.getElementById("location-filter");
  if (user?.location && locFilter) {
    // Add user's city as an option if not already present
    const cityVal = user.location.trim();
    let found = false;
    for (const opt of locFilter.options) {
      if (opt.value.toLowerCase() === cityVal.toLowerCase()) { found = true; break; }
    }
    if (!found && cityVal) {
      const opt = new Option(cityVal, cityVal);
      locFilter.appendChild(opt);
    }
  }
});

async function loadJobs() {
  const search   = document.getElementById("search-input")?.value || "";
  const type     = document.getElementById("type-filter")?.value || "";
  const location = document.getElementById("location-filter")?.value || "";

  showLoading("jobs-container", "Finding the best jobs for you...");

  const params = new URLSearchParams();
  if (search)   params.set("search", search);
  if (type)     params.set("type", type);
  if (location) params.set("location", location);

  const data = await apiFetch(`/jobs?${params.toString()}`);
  const container = document.getElementById("jobs-container");

  if (!data.success || !data.jobs?.length) {
    showEmpty("jobs-container", "🔍", "No jobs found. Try adjusting your filters.");
    return;
  }

  // Update count
  const countEl = document.getElementById("job-count");
  if (countEl) countEl.textContent = `${data.jobs.length} jobs found`;

  container.innerHTML = data.jobs.map(job => buildJobCard(job)).join("");
}

// Simple debounce utility
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}