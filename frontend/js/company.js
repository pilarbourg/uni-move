
/* -------------------------------------------------------
   GET URL PARAMS
------------------------------------------------------- */
function getParams() {
  const p = new URLSearchParams(window.location.search);
  return {
    id: p.get("id"),
    from: p.get("from"),
    to: p.get("to"),
    date: p.get("date"),
    small: Number(p.get("small")),
    medium: Number(p.get("medium")),
    large: Number(p.get("large")),
    type: p.get("type")
  };
}

/* -------------------------------------------------------
   RENDER STARS
------------------------------------------------------- */
function renderStars(n) {
  let s = "";
  const full = Math.floor(n);
  const half = n % 1 >= 0.5;

  for (let i = 0; i < full; i++) s += "★";
  if (half) s += "☆";
  return s;
}

/* -------------------------------------------------------
   PACKAGE BREAKDOWN
------------------------------------------------------- */
function renderPackageBreakdown(pack) {
  const container = document.getElementById("packageBreakdownList");
  container.innerHTML = "";

  const desc = {
    small: "up to 25 kg",
    medium: "25–50 kg",
    large: "over 50 kg"
  };

  Object.entries(pack).forEach(([t, c]) => {
    if (c > 0) {
      container.innerHTML += `
        <div class="package-item">
          <span>📦 ${t} (x${c})</span>
          <span>${desc[t]}</span>
        </div>`;
    }
  });
}

/* -------------------------------------------------------
   LOAD COMPANY
------------------------------------------------------- */
async function loadCompany() {
  const params = getParams();

  const res = await fetch("http://127.0.0.1:8080/get_moving_companies");
  const companies = await res.json();
  const c = companies.find(x => x.id == params.id);

  if (!c) return alert("Company not found");

  document.getElementById("companyName").textContent = c.name;
  document.getElementById("companyCIF").textContent = c.cif;
  document.getElementById("companyBaseFee").textContent = c.base_fee + " €";
  document.getElementById("companyCity").textContent = c.location;
  document.getElementById("companyTime").textContent = c.estimated_time_days + " days";
  document.getElementById("companyWeight").textContent = c.max_weight_kg + " kg";
  document.getElementById("companyRating").textContent = c.rating;
  document.getElementById("companyRatingStars").innerHTML = renderStars(c.rating);

  // Prices
  document.getElementById("priceSmall").textContent = c.price_small_package + " €";
  document.getElementById("priceMedium").textContent = c.price_medium_package + " €";
  document.getElementById("priceLarge").textContent = c.price_large_package + " €";
  document.getElementById("priceSolo").textContent = c.price_solo_traslado + " €";
  document.getElementById("priceMudanza").textContent = c.price_mudanza + " €";
  document.getElementById("priceMudanzaCompleta").textContent = c.price_mudanza_completa + " €";

  // Contact
  document.getElementById("companyPhone").textContent = c.phone ?? "Not available";
  document.getElementById("companyEmail").textContent = c.email ?? "Not available";
  const km_price = c.km_price ? c.km_price + " €" : "Not available";
  // Reviews
  const reviews = c.reviews ?? [];
  document.getElementById("reviewsList").innerHTML = reviews.length === 0 ?
      "<p>No reviews yet.</p>" :
      reviews.map(r => `
        <div class="review-card">
          <div class="review-stars">${renderStars(r.stars)}</div>
          <div class="review-author">${r.author}</div>
          <div class="review-preview">${r.text}</div>
        </div>`).join("");

  // Load images separated
  await loadCompanyImages(c.id);

  // Package breakdown
  renderPackageBreakdown({
    small: params.small,
    medium: params.medium,
    large: params.large
  });
}

/* -------------------------------------------------------
   LOAD IMAGES
------------------------------------------------------- */
async function loadCompanyImages(id) {
  const res = await fetch(`http://127.0.0.1:8080/get_company_images?id=${id}`);
  const imgs = await res.json();

  const gallery = document.getElementById("companyImages");

  if (!imgs || imgs.length === 0) {
    gallery.innerHTML = "<p>No images available.</p>";
    return;
  }

  gallery.innerHTML = imgs.map(img =>
    `<img src="${img.image_url}" class="company-img">`
  ).join("");
}

/* -------------------------------------------------------
   LOAD PRICE ESTIMATE
------------------------------------------------------- */
async function loadEstimateCard() {
  const { from, to, small, medium, large, type } = getParams();

  document.getElementById("estimateRoute").textContent = `${from} → ${to}`;
  document.getElementById("estimatePackages").textContent = small + medium + large;
  document.getElementById("estimateType").textContent = type;

  const res = await fetch(`http://127.0.0.1:8080/calc_distance?from=${from}&to=${to}`);
  const data = await res.json();

  if (!data.distance_km) {
    document.getElementById("estimateDistance").textContent = "N/A";
    return;
  }

  const distance = data.distance_km;
  document.getElementById("estimateDistance").textContent = `${distance} km`;
  const totalCostKm= data.distance_km * km_price;
  const totalCostPackages = (small * price_small_package) +
                            (medium * price_medium_package) +
                            (large * price_large_package);
  const totalCost = totalCostKm + totalCostPackages + base_fee;
    document.getElementById("estimateTotalCost").textContent = totalCost.toFixed(2) + " €"; 

}

/* -------------------------------------------------------
   SEND MESSAGE
------------------------------------------------------- */
function sendMessage() {
  const msg = document.getElementById("contactMessage").value.trim();
  if (!msg) return alert("Please write a message.");
  alert("Message sent ✔");
}

/* -------------------------------------------------------
   INIT PAGE (MAIN)
------------------------------------------------------- */
async function initPage() {
  try {
    const params = getParams();
    await loadCompany(params.id);
    await loadEstimateCard();
  } catch (e) {
    console.error(e);
  } finally {
    document.getElementById("loader").style.display = "none";
    document.getElementById("pageContent").style.display = "block";
  }
}

document.addEventListener("DOMContentLoaded", initPage);
