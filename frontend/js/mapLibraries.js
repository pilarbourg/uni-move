const map = L.map("librariesMap").setView([40.4168, -3.7038], 12);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);

const blueIcon = new L.Icon({
  iconUrl: "../assets/images/marker-icon-2x-blue.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

let allLibraries = [];
let allMarkers = [];
let selectedMarker = null;
const libraryList = document.getElementById("library-list");

function clearMarkers() {
  allMarkers.forEach((marker) => map.removeLayer(marker));
  allMarkers = [];
  if (selectedMarker) {
    map.removeLayer(selectedMarker);
    selectedMarker = null;
  }
}

function fitMapToMarkers() {
  if (allMarkers.length === 0) {
    map.setView([40.4168, -3.7038], 10);
    return;
  }
  const bounds = L.latLngBounds(allMarkers.map((m) => m.getLatLng()));
  map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14 });
}

async function fetchReviews(libraryId) {
  try {
    const response = await fetch(
      `http://localhost:8080/api/libraries/${libraryId}/reviews`
    );
    if (!response.ok) throw new Error("Failed to fetch reviews");

    const reviews = await response.json();
    return reviews;
  } catch (err) {
    console.error("Error fetching reviews:", err);
    return [];
  }
}

function showLibrary(lib) {
  const lat = parseFloat(lib.latitude);
  const lng = parseFloat(lib.longitude);
  if (isNaN(lat) || isNaN(lng)) return;

  map.setView([lat, lng], 16, { animate: true });

  const marker = allMarkers.find((m) => {
    const mLatLng = m.getLatLng();
    return mLatLng.lat === lat && mLatLng.lng === lng;
  });

  if (marker) {
    marker.openPopup();
  }
}

async function showAllLibraries() {
  clearMarkers();
  libraryList.innerHTML = "";

  for (const lib of allLibraries) {
    const lat = parseFloat(lib.latitude);
    const lng = parseFloat(lib.longitude);
    if (isNaN(lat) || isNaN(lng)) continue;

    const marker = L.marker([lat, lng], { icon: blueIcon }).addTo(map);
    allMarkers.push(marker);

    const reviews = await fetchReviews(lib.id);
    let ratingText = "No reviews yet";
    let commentsHTML = "";

    if (reviews.length > 0) {
      const sum = reviews.reduce((acc, r) => acc + r.rating, 0);
      const avg = sum / reviews.length;
      ratingText = `${avg.toFixed(1)} ⭐ (${reviews.length} review${
        reviews.length > 1 ? "s" : ""
      })`;

      commentsHTML = `
        <div class="reviews-list">
          ${reviews
            .map(
              (r) => `
            <div class="review-item-display">
              <p class="review-rating-display">⭐ ${r.rating}</p>
              ${
                r.comment
                  ? `<p class="review-comment-display">“${r.comment}”</p>`
                  : ""
              }
              <p class="review-date">${new Date(
                r.created_at
              ).toLocaleDateString()}</p>
            </div>
          `
            )
            .join("")}
        </div>
      `;
    }

    marker.bindPopup(
      `<b>${lib.name}</b><br>${lib.street || ""}<br>⭐ ${ratingText}`
    );

    const li = document.createElement("li");
    li.className = "library-card";

    li.innerHTML = `
      <h4>${lib.name}</h4>
      <p><i>${lib.street || ""}, ${lib.postal_code || ""}</i></p>
      <p><strong>Services:</strong> ${lib.services || "Not available"}</p>
      <p><strong>Description:</strong> ${
        lib.description || "No description"
      }</p>
      <p><strong>Average Rating:</strong> ${ratingText}</p>
      ${
        reviews.length > 0
          ? `
            <button class="toggle-reviews-btn">View Reviews (${
              reviews.length
            }) ▼</button>
            <div class="reviews-list" style="display:none;">
              ${reviews
                .map(
                  (r) => `
                    <div class="review-item-display">
                      <p class="review-rating-display">⭐ ${r.rating}</p>
                      ${
                        r.comment
                          ? `<p class="review-comment-display">“${r.comment}”</p>`
                          : ""
                      }
                      <p class="review-date">${new Date(
                        r.created_at
                      ).toLocaleDateString()}</p>
                    </div>
                  `
                )
                .join("")}
            </div>
          `
          : "<p>No reviews yet</p>"
      }
      <button class="leave-review-btn">Leave a Review</button>
      <div class="review-form" style="display:none; margin-top:8px;">
      <div>
        <label for="rating" class="review-label">Your Rating:</label>
        <select id="rating" class="review-rating">
          <option value="1">⭐ 1</option>
          <option value="2">⭐⭐ 2</option>
          <option value="3" selected>⭐⭐⭐ 3</option>
          <option value="4">⭐⭐⭐⭐ 4</option>
          <option value="5">⭐⭐⭐⭐⭐ 5</option>
        </select>
        </div>

        <div>
        <label for="comment" class="review-label">Your Comment (optional):</label>
        <textarea
          id="comment"
          class="review-comment"
          placeholder="Share your thoughts about this library..."
          rows="5"
        ></textarea>
        </div>
        
        <button class="submit-review-btn">Submit</button>
      </div>
    `;

    libraryList.appendChild(li);

    li.addEventListener("click", () => showLibrary(lib));
    li.addEventListener("mouseenter", () => (li.style.cursor = "pointer"));

    const leaveBtn = li.querySelector(".leave-review-btn");
    const formDiv = li.querySelector(".review-form");
    leaveBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      formDiv.style.display =
        formDiv.style.display === "none" ? "block" : "none";
    });

    const submitBtn = li.querySelector(".submit-review-btn");

    submitBtn.addEventListener("click", async (e) => {
      e.stopPropagation();
      try {
        const rating = parseInt(li.querySelector(".review-rating").value);
        const commentInput = li.querySelector(".review-comment");
        const comment = commentInput ? commentInput.value.trim() : "";
        const userId = 1;
    
        await submitReview(lib.id, userId, rating, comment);
    
        const updatedReviews = await fetchReviews(lib.id);
    
        let reviewsDiv = li.querySelector(".reviews-list");
        const avgRatingP = Array.from(li.querySelectorAll("p")).find(p =>
          p.textContent.trim().startsWith("Average Rating:")
        );
        if (!reviewsDiv) {
          reviewsDiv = document.createElement("div");
          reviewsDiv.className = "reviews-list";
          avgRatingP.parentElement.insertAdjacentElement("afterend", reviewsDiv);
        }

        reviewsDiv.innerHTML = updatedReviews
          .map(
            r => `
            <div class="review-item-display">
              <p class="review-rating-display">⭐ ${r.rating}</p>
              ${r.comment ? `<p class="review-comment-display">“${r.comment}”</p>` : ""}
              <p class="review-date">${new Date(r.created_at).toLocaleDateString()}</p>
            </div>
          `
          ).join("");
        reviewsDiv.style.display = "block";
    
        const avg = updatedReviews.reduce((sum,r)=>sum+r.rating,0)/updatedReviews.length;
        avgRatingP.textContent = `Average Rating: ${avg.toFixed(1)} ⭐ (${updatedReviews.length} review${updatedReviews.length>1?'s':''})`;
    
        formDiv.style.display = "none";
        commentInput.value = "";
    
      } catch(err) {
        console.error("Error submitting review:", err);
        alert("Something went wrong while submitting your review. Please try again.");
      }
    });

    const toggleReviewsBtn = li.querySelector(".toggle-reviews-btn");
    if (toggleReviewsBtn) {
      const reviewsDiv = li.querySelector(".reviews-list");
      toggleReviewsBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const isHidden = reviewsDiv.style.display === "none";
        reviewsDiv.style.display = isHidden ? "block" : "none";
        toggleReviewsBtn.textContent = isHidden
          ? `Hide Reviews ▲`
          : `View Reviews ▼`;
      });
    }
  }

  fitMapToMarkers();
}

async function submitReview(libraryId, userId, rating, comment) {
  try {
    const res = await fetch(
      `http://localhost:8080/api/libraries/${libraryId}/reviews`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, rating, comment }),
      }
    );

    if (res.ok) {
      console.log("Review added successfully!");
    } else {
      let errorMsg = "";
      try {
        const text = await res.text();
        errorMsg = text || `Status ${res.status}`;
      } catch {
        errorMsg = `Status ${res.status} and no readable body`;
      }
      console.error("Error submitting review:", errorMsg);
    }
  } catch (err) {
    console.error("Network or fetch error:", err);
  }
}

async function fetchLibraries() {
  try {
    const res = await fetch("http://localhost:8080/api/libraries");
    if (!res.ok) throw new Error("Failed to fetch libraries");
    allLibraries = await res.json();
    showAllLibraries();
    setTimeout(() => map.invalidateSize(), 500);
  } catch (err) {
    console.error("Error fetching libraries:", err);
  }
}

document.addEventListener("DOMContentLoaded", fetchLibraries);
