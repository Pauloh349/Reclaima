// FAQ Toggle Functionality
const faqItems = document.querySelectorAll(".faq-item");

faqItems.forEach((item) => {
  const question = item.querySelector(".faq-question");
  const answer = item.querySelector(".faq-answer");
  const toggle = item.querySelector(".faq-toggle");

  question.addEventListener("click", () => {
    // Close all other FAQ items
    faqItems.forEach((otherItem) => {
      if (otherItem !== item) {
        otherItem.classList.remove("active");
        otherItem.querySelector(".faq-answer").classList.remove("active");
      }
    });

    // Toggle current item
    item.classList.toggle("active");
    answer.classList.toggle("active");
  });
});

// Mobile Menu Toggle
const mobileMenu = document.querySelector(".mobile-menu");
const navUl = document.querySelector("nav ul");

mobileMenu.addEventListener("click", () => {
  navUl.style.display = navUl.style.display === "flex" ? "none" : "flex";
});

// CTA Button Functionality
const ctaButtons = document.querySelectorAll(".cta-button");
const secondaryButtons = document.querySelectorAll(".secondary-button");

ctaButtons.forEach((button) => {
  button.addEventListener("click", function () {
    const buttonText = this.textContent.trim();

    if (buttonText.includes("Lost Item")) {
      // In a real app, this would navigate to the lost items page
      window.location.href = "lost-items.html";
    } else if (buttonText.includes("Get Started")) {
      // Scroll to the overview section
      document
        .querySelector(".overview")
        .scrollIntoView({ behavior: "smooth" });
    } else if (buttonText.includes("Success Stories")) {
      // In a real app, this would navigate to success stories
      alert("Navigating to success stories page");
    } else if (buttonText.includes("Report")) {
      // In a real app, this would open a report modal
      alert("Opening report form");
    }
  });
});

secondaryButtons.forEach((button) => {
  button.addEventListener("click", function () {
    const buttonText = this.textContent.trim();

    if (buttonText.includes("Found Item")) {
      // In a real app, this would navigate to the found items page
      window.location.href = "found-items.html";
    } else if (buttonText.includes("Lost Items")) {
      window.location.href = "lost-items.html";
    } else if (buttonText.includes("Success Stories")) {
      alert("Navigating to success stories page");
    } else if (buttonText.includes("Report")) {
      alert("Opening found item report form");
    }
  });
});

// Animate process steps on scroll
function animateOnScroll() {
  const processSteps = document.querySelectorAll(".process-step");
  const stepDetails = document.querySelectorAll(".step-detail");
  const guidelineCards = document.querySelectorAll(".guideline-card");

  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  // Set initial state for animation
  processSteps.forEach((step) => {
    step.style.opacity = "0";
    step.style.transform = "translateY(20px)";
    step.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    observer.observe(step);
  });

  stepDetails.forEach((detail, index) => {
    detail.style.opacity = "0";
    detail.style.transform = "translateY(30px)";
    detail.style.transition = `opacity 0.5s ease ${
      index * 0.2
    }s, transform 0.5s ease ${index * 0.2}s`;
    observer.observe(detail);
  });

  guidelineCards.forEach((card, index) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";
    card.style.transition = `opacity 0.5s ease ${
      index * 0.1
    }s, transform 0.5s ease ${index * 0.1}s`;
    observer.observe(card);
  });
}

// Initialize animations when page loads
document.addEventListener("DOMContentLoaded", animateOnScroll);
