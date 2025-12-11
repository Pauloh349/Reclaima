document.addEventListener("DOMContentLoaded", function () {
  // Story detail modal functionality
  const modal = document.getElementById("storyModal");
  const closeModal = document.getElementById("closeModal");
  const storyCards = document.querySelectorAll(".story-card, .view-full-story");

  // Fetch and display full story
  async function loadStoryDetail(storyId) {
    try {
      const response = await fetch(`/api/stories/${storyId}/`);
      const story = await response.json();

      // Populate modal with story data
      document.getElementById("modalStoryTitle").textContent = story.title;
      document.getElementById("modalAuthor").textContent = story.author_name;
      document.getElementById("modalDate").textContent = new Date(
        story.created_at
      ).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
      document.getElementById("modalCategory").textContent =
        story.category_display;
      document.getElementById(
        "modalContent"
      ).innerHTML = `<p>${story.content}</p>`;

      // Set image if available
      const modalImage = document.getElementById("modalImage");
      if (story.image_url) {
        modalImage.src = story.image_url;
        modalImage.style.display = "block";
      } else {
        modalImage.style.display = "none";
      }

      // Show modal
      modal.style.display = "block";
      document.body.style.overflow = "hidden";
    } catch (error) {
      console.error("Error loading story:", error);
      alert("Failed to load story details. Please try again.");
    }
  }

  // Event listeners for story cards
  storyCards.forEach((card) => {
    card.addEventListener("click", function (e) {
      const storyId = this.getAttribute("data-story-id");
      if (storyId) {
        loadStoryDetail(storyId);
      }
    });
  });

  // Close modal
  closeModal.addEventListener("click", function () {
    modal.style.display = "none";
    document.body.style.overflow = "auto";
  });

  // Close modal when clicking outside
  window.addEventListener("click", function (e) {
    if (e.target === modal) {
      modal.style.display = "none";
      document.body.style.overflow = "auto";
    }
  });

  // File upload preview
  const fileInput = document.getElementById("image");
  const uploadPreview = document.querySelector(".upload-preview");

  if (fileInput && uploadPreview) {
    fileInput.addEventListener("change", function (e) {
      if (this.files && this.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
          uploadPreview.innerHTML = `
                        <img src="${e.target.result}" style="max-width: 200px; max-height: 150px; border-radius: 8px; margin-bottom: 1rem;">
                        <p>${fileInput.files[0].name}</p>
                        <p style="font-size: 0.9rem; color: var(--gray)">
                            Click to change photo
                        </p>
                    `;
        };

        reader.readAsDataURL(this.files[0]);
      }
    });
  }

  // Form validation
  const storyForm = document.querySelector(".share-form");
  if (storyForm) {
    storyForm.addEventListener("submit", function (e) {
      const requiredFields = this.querySelectorAll("[required]");
      let isValid = true;

      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          isValid = false;
          field.style.borderColor = "#dc3545";
        } else {
          field.style.borderColor = "";
        }
      });

      if (!isValid) {
        e.preventDefault();
        alert("Please fill in all required fields.");
      }
    });
  }

  // Smooth scroll for share story link
  const shareLink = document.querySelector('a[href="#share-story"]');
  if (shareLink) {
    shareLink.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
        });
      }
    });
  }
});
