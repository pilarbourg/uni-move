
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
async function loadReviews(companyId) {
  try {
    const res = await fetch(`http://127.0.0.1:8080/fetch_company_reviews?id=${companyId}`);
    const reviews = await res.json();

    renderReviews(reviews);

  } catch (err) {
    console.error("Error loading reviews:", err);
  }
}
function renderReviews(reviews) {
  const container = document.getElementById("reviewsList");

  if (!reviews.length) {
    container.innerHTML = `<p>No reviews yet.</p>`;
    return;
  }

  container.innerHTML = reviews
    .map(r => {
    const user_name = localStorage.getItem("user_email");
      return `
        <div class="review-card">

          <div class="review-header">


            <div class="review-meta">
              <strong class="review-user">${user_name?? "Anonymous"}</strong>
              <span class="review-date">${r.review_date ?? ""}</span>
            </div>

            <div class="review-rating">
               ${renderStars(r.rating)}
            </div>

          </div>

          <p class="review-text">${r.comment}</p>

        </div>
      `;
    })
    .join("");
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

  // 🔥 GUARDAR COMPAÑÍA GLOBALMENTE
  window.currentCompany = c;

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

  await loadCompanyImages(c.id);

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
  `<img src="${img.image}" alt="Company image">`
).join("");

}

/* -------------------------------------------------------
   LOAD PRICE ESTIMATE
------------------------------------------------------- */
async function loadEstimateCard() {
  const { from, to, small, medium, large, type } = getParams();
  const c = window.currentCompany; // ⭐ Recuperamos la compañía

  if (!c) return;

  document.getElementById("estimateRoute").textContent = `${from} → ${to}`;
  document.getElementById("estimatePackages").textContent = small + medium + large;
  document.getElementById("estimateType").textContent = type;

  const res = await fetch(
    `http://127.0.0.1:8080/calc_distance?from=${from}&to=${to}`
  );
  const data = await res.json();

  if (!data.distance_km) {
    document.getElementById("estimateDistance").textContent = "N/A";
    return;
  }
  
  const distance = data.distance_km;
  document.getElementById("estimateDistance").textContent = `${distance} km`;

  const kmPrice = c.km_price ?? 0;
  const baseFee = c.base_fee ?? 0;

  const priceSmall = c.price_small_package ?? 0;
  const priceMedium = c.price_medium_package ?? 0;
  const priceLarge = c.price_large_package ?? 0;

  const PACKAGE_WEIGHTS = {
  small: 12.5,
  medium: 20,
  large: 35
};

  const costPackages =
      small * priceSmall +
      medium * priceMedium +
      large * priceLarge;

  const totalWeight =
      small  * PACKAGE_WEIGHTS.small +
      medium * PACKAGE_WEIGHTS.medium +
      large  * PACKAGE_WEIGHTS.large;
  const MAX_WEIGHT_PER_MOVE =c.max_weight_kg;
  const movesNeeded = Math.ceil(totalWeight / MAX_WEIGHT_PER_MOVE);
  console.log("small:", small);
console.log("medium:", medium);
console.log("large:", large);

console.log("weights:", PACKAGE_WEIGHTS);
console.log("MAX_WEIGHT_PER_MOVE:", MAX_WEIGHT_PER_MOVE);

console.log("totalWeight:", totalWeight);
document.getElementById("neededMoves").textContent= `${movesNeeded} moves`;
  const costDistance = kmPrice * distance;
  const partialCost = baseFee + costPackages + costDistance ;
  const extraCost = calculateExpressFee(getParams().date, partialCost);
  const finalPrice=extraCost.finalPrice*movesNeeded;
  console.log(movesNeeded);
 console.log(finalPrice);
  document.getElementById("estimateTotalCost")
    .textContent = finalPrice.toFixed(2) + " €";
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

function calculateExpressFee(moveDate, basePrice) {
  const today = new Date();
  const target = new Date(moveDate);
  const daysLeft = daysBetween(today, target);

  let extra = 0;

  if (daysLeft < 14) {
    // Mudanza express → recargo fuerte
    extra = basePrice * 0.5; 
  } else if (daysLeft < 30) {
    // Menos de un mes → recargo moderado
    extra = basePrice * 0.25;   // +10% (ejemplo)
  } else {
    // Más de un mes → sin recargo
    extra = 0;
  }

  const finalPrice = basePrice + extra;

  return {
    daysLeft,
    extra,
    finalPrice
  };
}
function daysBetween(date1, date2) {
  const diff = date2.getTime() - date1.getTime();
  return Math.ceil(diff / (1000 * 60 * 60 * 24)); // días

}
document.addEventListener("DOMContentLoaded", async () => {
  const params = new URLSearchParams(window.location.search);
  const companyId = params.get("id");

  console.log("Loading reviews for company", companyId);

  await loadReviews(companyId);
});

document.addEventListener("DOMContentLoaded", () => {
  console.log("JS loaded, DOM ready ✅");

 // Elements
const reviewModal = document.getElementById("reviewModal");
const openReviewBtn = document.getElementById("openReviewBtn");
const closeReviewBtn = document.getElementById("closeReviewBtn");

// When clicking "Write a Review"
openReviewBtn.addEventListener("click", () => {
  console.log("Opening review modal...");
  reviewModal.style.display = "flex";
});

// Close modal
closeReviewBtn.addEventListener("click", () => {
  reviewModal.style.display = "none";
});

// Close modal when clicking outside the box
window.addEventListener("click", (e) => {
  if (e.target === reviewModal) reviewModal.style.display = "none";
});
});


document.getElementById("sendReviewBtn").onclick = async function () {
  const params = new URLSearchParams(window.location.search);
  const company_id = params.get("id");

  let user_id = localStorage.getItem("user_id");

  if (!user_id) {
    alert("You must be logged in to write a review.");
    return;
  }

  const rating = Number(document.getElementById("reviewRating").value);
  const comment = document.getElementById("reviewComment").value.trim();
  const date = document.getElementById("reviewDate").value;
  const service_type = document.getElementById("reviewType").value;

  const payload = { company_id, user_id, rating, comment, date, service_type };
  console.log("Sending review payload:", payload);

  try {
    const res = await fetch("http://127.0.0.1:8080/submit_company_review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      console.error("Error from backend:", data);
      alert("Error submitting review.");
      return;
    }

    alert("Review submitted successfully!");
    reviewModal.style.display = "none";

  } catch (error) {
    console.error("Fetch error:", error);
    alert("Network or CORS error");
  }
};


