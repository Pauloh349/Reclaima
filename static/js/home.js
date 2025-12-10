
// Animate stats counter
function animateStats() {
  const stat1 = document.getElementById("stat1");
  const stat2 = document.getElementById("stat2");
  const stat3 = document.getElementById("stat3");

  const target1 = 15872;
  const target2 = 42590;
  const target3 = 89;

  let current1 = 0;
  let current2 = 0;
  let current3 = 0;

  const increment1 = target1 / 50;
  const increment2 = target2 / 50;
  const increment3 = target3 / 50;

  const timer = setInterval(() => {
    current1 += increment1;
    current2 += increment2;
    current3 += increment3;

    if (current1 >= target1) {
      stat1.textContent = target1.toLocaleString() + "+";
      stat2.textContent = target2.toLocaleString() + "+";
      stat3.textContent = target3 + "%";
      clearInterval(timer);
    } else {
      stat1.textContent = Math.floor(current1).toLocaleString();
      stat2.textContent = Math.floor(current2).toLocaleString();
      stat3.textContent = Math.floor(current3) + "%";
    }
  }, 30);
}

// Testimonial slider functionality
let currentTestimonial = 0;

function showTestimonial(index) {
  testimonials.forEach((testimonial) => testimonial.classList.remove("active"));
  testimonialDots.forEach((dot) => dot.classList.remove("active"));

  testimonials[index].classList.add("active");
  testimonialDots[index].classList.add("active");
  currentTestimonial = index;
}

// Initialize page
function initPage() {
  displayFeaturedItems();

  // Animate stats when page loads
  setTimeout(animateStats, 500);

  // Set up testimonial slider
  testimonialDots.forEach((dot, index) => {
    dot.addEventListener("click", () => showTestimonial(index));
  });

  // Auto-rotate testimonials
  setInterval(() => {
    currentTestimonial = (currentTestimonial + 1) % testimonials.length;
    showTestimonial(currentTestimonial);
  }, 5000);

  // Search option toggle
  searchOptions.forEach((option) => {
    option.addEventListener("click", function () {
      searchOptions.forEach((opt) => opt.classList.remove("active"));
      this.classList.add("active");

      // Update search placeholder based on selection
      if (this.id === "searchLost") {
        searchInput.placeholder = "Describe what you lost...";
        searchButton.textContent = "Search Lost Items";
      } else {
        searchInput.placeholder = "Describe what you found...";
        searchButton.textContent = "Search Found Items";
      }
    });
  });

  // Search functionality
  searchButton.addEventListener("click", function () {
    const searchTerm = searchInput.value.trim();
    const isSearchingLost = document
      .getElementById("searchLost")
      .classList.contains("active");

    if (searchTerm) {
      if (isSearchingLost) {
        window.location.href = `lost-items.html?search=${encodeURIComponent(
          searchTerm
        )}`;
      } else {
        // In a real app, this would navigate to found items page
        alert(`Searching for found items matching: "${searchTerm}"`);
      }
    } else {
      if (isSearchingLost) {
        window.location.href = "lost-items.html";
      } else {
        // In a real app, this would navigate to found items page
        alert("Navigating to found items page");
      }
    }
  });

  // Mobile menu toggle
  mobileMenu.addEventListener("click", function () {
    navUl.style.display = navUl.style.display === "flex" ? "none" : "flex";
  });

  // CTA buttons
  document.querySelectorAll(".cta-button").forEach((button) => {
    if (!button.classList.contains("search-box")) {
      button.addEventListener("click", function () {
        // In a real app, this would open a report modal
        alert("Opening report item form");
      });
    }
  });

  // Secondary buttons
  document.querySelectorAll(".secondary-button").forEach((button) => {
    button.addEventListener("click", function () {
      // In a real app, this would navigate to appropriate page
      if (button.textContent.includes("Found")) {
        alert("Navigating to found items page");
      } else {
        window.location.href = "lost-items.html";
      }
    });
  });

  // Quick links
  document.querySelectorAll(".quick-link").forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const category = this.textContent.trim();
      window.location.href = `lost-items.html?category=${encodeURIComponent(
        category
      )}`;
    });
  });
}

// Initialize the page when DOM is loaded
document.addEventListener("DOMContentLoaded", initPage);
