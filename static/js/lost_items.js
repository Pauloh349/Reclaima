      // DOM Elements
      const lostItemsGrid = document.getElementById("lostItemsGrid");
      const searchInput = document.getElementById("searchInput");
      const categoryCheckboxes = document.querySelectorAll(
        'input[type="checkbox"][id^="cat-"]'
      );
      const locationFilter = document.getElementById("locationFilter");
      const dateFrom = document.getElementById("dateFrom");
      const dateTo = document.getElementById("dateTo");
      const statusCheckboxes = document.querySelectorAll(
        'input[type="checkbox"][id^="status-"]'
      );
      const applyFiltersBtn = document.getElementById("applyFilters");
      const resetFiltersBtn = document.getElementById("resetFilters");
      const sortBy = document.getElementById("sortBy");
      const itemsShown = document.getElementById("itemsShown");
      const itemsTotal = document.getElementById("itemsTotal");
      const reportModal = document.getElementById("reportModal");
      const reportItemBtn = document.getElementById("reportItemBtn");
      const openReportModalBtn = document.getElementById("openReportModal");
      const closeModalBtn = document.getElementById("closeModal");
      const cancelReportBtn = document.getElementById("cancelReport");
      const submitReportBtn = document.getElementById("submitReport");
      const reportForm = document.getElementById("reportForm");

      // Set default dates for filters
      const today = new Date().toISOString().split("T")[0];
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      const thirtyDaysAgoStr = thirtyDaysAgo.toISOString().split("T")[0];

      dateFrom.value = thirtyDaysAgoStr;
      dateTo.value = today;

      // Set lost date default to today
      document.getElementById("lostDate").value = today;

      // Initialize items display
      function displayItems(items) {
        lostItemsGrid.innerHTML = "";

        if (items.length === 0) {
          lostItemsGrid.innerHTML = `
                    <div class="no-items">
                        <i class="fas fa-search"></i>
                        <h3>No Lost Items Found</h3>
                        <p>Try adjusting your filters or search terms</p>
                    </div>
                `;
          itemsShown.textContent = "0";
          return;
        }

        items.forEach((item) => {
          const itemCard = document.createElement("div");
          itemCard.className = "item-card";
          itemCard.innerHTML = `
                    <div class="item-image">
                        <div class="item-placeholder">
                            <i class="${item.icon}"></i>
                        </div>
                        <div class="item-category">
                            <i class="${item.icon}"></i>
                            <span>${item.categoryName}</span>
                        </div>
                    </div>
                    <div class="item-details">
                        <h3 class="item-title">${item.title}</h3>
                        <div class="item-meta">
                            <div><i class="fas fa-map-marker-alt"></i> ${
                              item.location
                            }</div>
                            <div><i class="fas fa-calendar-alt"></i> ${formatDate(
                              item.date
                            )}</div>
                        </div>
                        <p class="item-description">${item.description}</p>
                        <div class="item-actions">
                            <a href="#" class="item-btn view-btn">View Details</a>
                            ${
                              item.claimed
                                ? '<button class="item-btn" style="background-color: var(--success); color: white;" disabled>Claimed</button>'
                                : '<button class="item-btn claim-btn">I Think This Is Mine</button>'
                            }
                        </div>
                    </div>
                `;

          lostItemsGrid.appendChild(itemCard);
        });

        itemsShown.textContent = items.length.toString();
      }

      // Format date for display
      function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
          year: "numeric",
        });
      }

      // Filter items based on current filter values
      function filterItems() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedCategories = Array.from(categoryCheckboxes)
          .filter((cb) => cb.checked)
          .map((cb) => cb.id.replace("cat-", ""));

        const selectedLocation = locationFilter.value;
        const dateFromVal = dateFrom.value ? new Date(dateFrom.value) : null;
        const dateToVal = dateTo.value ? new Date(dateTo.value) : null;

        const selectedStatus = Array.from(statusCheckboxes)
          .filter((cb) => cb.checked)
          .map((cb) => cb.id.replace("status-", ""));

        // Filter items
        let filtered = lostItems.filter((item) => {
          // Search term filter
          if (
            searchTerm &&
            !item.title.toLowerCase().includes(searchTerm) &&
            !item.description.toLowerCase().includes(searchTerm) &&
            !item.location.toLowerCase().includes(searchTerm)
          ) {
            return false;
          }

          // Category filter
          if (
            selectedCategories.length > 0 &&
            !selectedCategories.includes(item.category)
          ) {
            return false;
          }

          // Location filter
          if (
            selectedLocation !== "all" &&
            !item.location.toLowerCase().includes(selectedLocation)
          ) {
            return false;
          }

          // Date filter
          const itemDate = new Date(item.date);
          if (dateFromVal && itemDate < dateFromVal) return false;
          if (dateToVal && itemDate > dateToVal) return false;

          // Status filter
          const itemStatus = item.claimed ? "claimed" : "unclaimed";
          if (
            selectedStatus.length > 0 &&
            !selectedStatus.includes(itemStatus)
          ) {
            return false;
          }

          return true;
        });

        // Sort items
        const sortValue = sortBy.value;
        filtered.sort((a, b) => {
          if (sortValue === "recent") {
            return new Date(b.date) - new Date(a.date);
          } else if (sortValue === "oldest") {
            return new Date(a.date) - new Date(b.date);
          } else if (sortValue === "location") {
            return a.location.localeCompare(b.location);
          } else if (sortValue === "category") {
            return a.categoryName.localeCompare(b.categoryName);
          }
          return 0;
        });

        return filtered;
      }

      // Apply filters and update display
      function applyFilters() {
        const filteredItems = filterItems();
        displayItems(filteredItems);
      }

      // Reset all filters
      function resetFilters() {
        searchInput.value = "";

        categoryCheckboxes.forEach((cb) => {
          if (
            cb.id === "cat-electronics" ||
            cb.id === "cat-keys" ||
            cb.id === "cat-wallets"
          ) {
            cb.checked = true;
          } else {
            cb.checked = false;
          }
        });

        locationFilter.value = "all";

        dateFrom.value = thirtyDaysAgoStr;
        dateTo.value = today;

        statusCheckboxes.forEach((cb) => {
          cb.checked = cb.id === "status-unclaimed";
        });

        sortBy.value = "recent";

        applyFilters();
      }

      // Modal functions
      function openModal() {
        reportModal.style.display = "flex";
        document.body.style.overflow = "hidden";
      }

      function closeModal() {
        reportModal.style.display = "none";
        document.body.style.overflow = "auto";
        reportForm.reset();
        document.getElementById("lostDate").value = today;
      }

      // Initialize page
      function initPage() {
        itemsTotal.textContent = lostItems.length.toString();
        displayItems(lostItems);

        // Add event listeners
        applyFiltersBtn.addEventListener("click", applyFilters);
        resetFiltersBtn.addEventListener("click", resetFilters);
        searchInput.addEventListener("input", applyFilters);
        sortBy.addEventListener("change", applyFilters);

        // Modal event listeners
        reportItemBtn.addEventListener("click", openModal);
        openReportModalBtn.addEventListener("click", openModal);
        closeModalBtn.addEventListener("click", closeModal);
        cancelReportBtn.addEventListener("click", closeModal);

        // Close modal when clicking outside
        reportModal.addEventListener("click", function (e) {
          if (e.target === reportModal) {
            closeModal();
          }
        });

        // Submit report
        submitReportBtn.addEventListener("click", function (e) {
          e.preventDefault();

          // Basic form validation
          const itemName = document.getElementById("itemName").value;
          const itemCategory = document.getElementById("itemCategory").value;
          const lostDate = document.getElementById("lostDate").value;
          const lostLocation = document.getElementById("lostLocation").value;
          const itemDescription =
            document.getElementById("itemDescription").value;
          const contactEmail = document.getElementById("contactEmail").value;

          if (
            !itemName ||
            !itemCategory ||
            !lostDate ||
            !lostLocation ||
            !itemDescription ||
            !contactEmail
          ) {
            alert("Please fill in all required fields.");
            return;
          }

          // In a real app, you would submit this data to a server
          alert(
            "Thank you for reporting your lost item. We'll notify you if someone finds it!"
          );
          closeModal();
        });

        // File upload interaction
        const fileUpload = document.getElementById("fileUpload");
        fileUpload.addEventListener("click", function () {
          alert("In a real application, this would open a file picker dialog.");
        });
      }

      // Initialize the page when DOM is loaded
      document.addEventListener("DOMContentLoaded", initPage);