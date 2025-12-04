// LOAD HEADER HTML INTO PAGE
document.addEventListener("DOMContentLoaded", async () => {
  const placeholder = document.getElementById("header-placeholder");
  if (!placeholder) return;

  // Load header.html
 const res = await fetch("/frontend/components/header.html");
  const html = await res.text();
  placeholder.innerHTML = html;

  // After inserting the header, activate logic:
  initHeaderLogic();
});

function initHeaderLogic() {
  const username = localStorage.getItem("username");
  const userNameEl = document.getElementById("user-name");
  const logoutBtn = document.getElementById("logout");

  const universities = document.getElementById("universitiesLink");
  const degrees = document.getElementById("degreesLink");
  const apartments = document.getElementById("apartmentsLink");
  const moving_companies=document.getElementById("movingLink");
  const health = document.getElementById("healthLink");
  const clinicalmaps = document.getElementById("clinicalmapsLink");
  const study = document.getElementById("studyLink");

  const loggedIn = Boolean(username);

  // DISPLAY USERNAME IF LOGGED
  if (loggedIn) {
    userNameEl.textContent = username;
    userNameEl.style.display = "inline";
    logoutBtn.style.display = "inline";

    // PAGE NAVIGATION ALLOWED
    universities.href = "/frontend/pages/universidades.html";
degrees.href = "/frontend/pages/searchByDegree.html";
apartments.href = "/frontend/pages/mapaapartamentos.html";
moving_companies.herf="/frontend/pages/moving_companies_lsit.html"
health.href = "/frontend/pages/biomedical.html";
clinicalmaps.href = "/frontend/pages/mapclinics.html";
study.href = "/frontend/pages/studentLife.html";

  } 
  else {
    // GUEST MODE
    userNameEl.style.display = "none";
    logoutBtn.style.display = "none";
universities.href = "/frontend/pages/login.html";
degrees.href = "/frontend/pages/login.html";
apartments.href = "/frontend/pages/login.html";
health.href = "/frontend/pages/login.html";
clinicalmaps.href = "/frontend/pages/login.html";
study.href = "/frontend/pages/login.html";
moving_companies.herf= "/frontend/pages/login.html";

  }

  // USER PROFILE BUTTON
  userNameEl.onclick = () => window.location.href = "/pages/profile.html";

  // LOGOUT HANDLER
  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("username");
    alert("You have successfully logged out.");
    window.location.reload();
  });
}
