// Sample found items data
const foundItems = [
  {
    id: 1,
    title: "iPhone 12 Pro - Space Gray",
    category: "electronics",
    categoryName: "Electronics",
    location: "Downtown Coffee Shop",
    date: "2023-10-15",
    description:
      "Found on a table near the window. Black case with floral pattern. Screen has a small crack on top left corner.",
    status: "unclaimed",
    icon: "fas fa-mobile-alt",
    finder: "Coffee Shop Staff",
  },
  {
    id: 2,
    title: "Car Keys with BMW Keychain",
    category: "keys",
    categoryName: "Keys & Access",
    location: "Central Parking Garage, Level 3",
    date: "2023-10-18",
    description:
      "Set of car keys found near elevator. Silver BMW keychain with 4 keys total, including a small mailbox key.",
    status: "unclaimed",
    icon: "fas fa-key",
    finder: "Parking Attendant",
  },
  {
    id: 3,
    title: "Leather Wallet - Brown",
    category: "wallets",
    categoryName: "Wallets & Purses",
    location: "City Park, Near Fountain",
    date: "2023-10-20",
    description:
      "Brown leather wallet containing ID, credit cards, and some cash. Photo of a family in the ID window.",
    status: "claimed",
    icon: "fas fa-wallet",
    finder: "Park Visitor",
  },
  {
    id: 4,
    title: "Wireless Headphones - Sony WH-1000XM4",
    category: "electronics",
    categoryName: "Electronics",
    location: "Public Bus Route 42",
    date: "2023-10-22",
    description:
      "Sony noise-cancelling headphones in black case. Case has small scratch on front. Found on seat near back.",
    status: "unclaimed",
    icon: "fas fa-headphones",
    finder: "Bus Driver",
  },
  {
    id: 5,
    title: "Silver Bracelet with Heart Charm",
    category: "jewelry",
    categoryName: "Jewelry & Accessories",
    location: "Shopping Mall, Food Court",
    date: "2023-10-10",
    description:
      "Delicate silver bracelet with small heart charm. Clasp appears to be broken.",
    status: "unclaimed",
    icon: "fas fa-gem",
    finder: "Mall Security",
  },
  {
    id: 6,
    title: "Passport & Travel Documents",
    category: "documents",
    categoryName: "Documents",
    location: "Airport Terminal B, Security Check",
    date: "2023-10-05",
    description:
      "Blue passport with several visa stamps. Includes boarding passes and currency exchange receipts.",
    status: "claimed",
    icon: "fas fa-passport",
    finder: "TSA Officer",
  },
  {
    id: 7,
    title: "Laptop Bag - Black Targus",
    category: "bags",
    categoryName: "Bags & Luggage",
    location: "Train Station, Waiting Area",
    date: "2023-10-25",
    description:
      "Black Targus laptop backpack. Contains laptop charger, notebooks, and water bottle in side pocket.",
    status: "unclaimed",
    icon: "fas fa-briefcase",
    finder: "Station Staff",
  },
  {
    id: 8,
    title: "Men's Watch - Fossil",
    category: "jewelry",
    categoryName: "Jewelry & Accessories",
    location: "Gym Locker Room",
    date: "2023-10-17",
    description:
      "Brown leather strap Fossil watch with silver face. Band is worn with initials engraved on clasp.",
    status: "unclaimed",
    icon: "fas fa-clock",
    finder: "Gym Member",
  },
];

// DOM Elements
const foundItemsGrid = document.getElementById("foundItemsGrid");
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

// Set found date default to today
document.getElementById("foundDate").value = today;

// Initialize items display
function displayItems(items) {
  foundItemsGrid.innerHTML = "";

  if (items.length === 0) {
    foundItemsGrid.innerHTML = `
                    <div class="no-items">
                        <i class="fas fa-search"></i>
                        <h3>No Found Items Match Your Search</h3>
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
                        <div class="item-status ${
                          item.status === "claimed"
                            ? "status-claimed"
                            : "status-unclaimed"
                        }">
                            ${
                              item.status === "claimed"
                                ? "Claimed"
                                : "Unclaimed"
                            }
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
                            <div><i class="fas fa-user"></i> ${
                              item.finder
                            }</div>
                        </div>
                        <p class="item-description">${item.description}</p>
                        <div class="item-actions">
                            <a href="#" class="item-btn view-btn">View Details</a>
                            ${
                              item.status === "claimed"
                                ? '<button class="item-btn" style="background-color: var(--success); color: white;" disabled>Already Claimed</button>'
                                : '<button class="item-btn claim-btn">I Think This Is Mine</button>'
                            }
                        </div>
                    </div>
                `;

    foundItemsGrid.appendChild(itemCard);
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
  let filtered = foundItems.filter((item) => {
    // Search term filter
    if (
      searchTerm &&
      !item.title.toLowerCase().includes(searchTerm) &&
      !item.description.toLowerCase().includes(searchTerm) &&
      !item.location.toLowerCase().includes(searchTerm) &&
      !item.finder.toLowerCase().includes(searchTerm)
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
    const itemStatus = item.status === "claimed" ? "claimed" : "unclaimed";
    if (selectedStatus.length > 0 && !selectedStatus.includes(itemStatus)) {
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
  document.getElementById("foundDate").value = today;
  document.getElementById("safeStorage").checked = false;
}

// Initialize page
function initPage() {
  displayItems(foundItems);

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
    const foundDate = document.getElementById("foundDate").value;
    const foundLocation = document.getElementById("foundLocation").value;
    const itemDescription = document.getElementById("itemDescription").value;
    const finderName = document.getElementById("finderName").value;
    const contactEmail = document.getElementById("contactEmail").value;
    const safeStorage = document.getElementById("safeStorage").checked;

    if (
      !itemName ||
      !itemCategory ||
      !foundDate ||
      !foundLocation ||
      !itemDescription ||
      !finderName ||
      !contactEmail ||
      !safeStorage
    ) {
      alert(
        "Please fill in all required fields and agree to store the item safely."
      );
      return;
    }

    // In a real app, you would submit this data to a server
    alert(
      "Thank you for reporting the found item! We'll help connect you with the owner if they come forward."
    );
    closeModal();

    // Add the new item to the list (in a real app, this would come from the server)
    const newItem = {
      id: foundItems.length + 1,
      title: itemName,
      category: itemCategory,
      categoryName:
        itemCategory.charAt(0).toUpperCase() + itemCategory.slice(1),
      location: foundLocation,
      date: foundDate,
      description: itemDescription,
      status: "unclaimed",
      icon: getIconForCategory(itemCategory),
      finder: finderName,
    };

    foundItems.unshift(newItem);
    applyFilters();
  });

  // File upload interaction
  const fileUpload = document.getElementById("fileUpload");
  fileUpload.addEventListener("click", function () {
    alert("In a real application, this would open a file picker dialog.");
  });

  // Mobile menu toggle
  document.querySelector(".mobile-menu").addEventListener("click", function () {
    document.querySelector("nav ul").style.display =
      document.querySelector("nav ul").style.display === "flex"
        ? "none"
        : "flex";
  });

  // Pagination
  document.querySelectorAll(".page-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      document
        .querySelectorAll(".page-btn")
        .forEach((b) => b.classList.remove("active"));
      this.classList.add("active");

      // In a real app, this would load the corresponding page of results
      if (!this.querySelector("i")) {
        alert(`Loading page ${this.textContent}...`);
      }
    });
  });
}

// Helper function to get icon for category
function getIconForCategory(category) {
  switch (category) {
    case "electronics":
      return "fas fa-mobile-alt";
    case "keys":
      return "fas fa-key";
    case "wallets":
      return "fas fa-wallet";
    case "documents":
      return "fas fa-passport";
    case "jewelry":
      return "fas fa-gem";
    case "clothing":
      return "fas fa-tshirt";
    case "bags":
      return "fas fa-briefcase";
    default:
      return "fas fa-question-circle";
  }
}

// Initialize the page when DOM is loaded
document.addEventListener("DOMContentLoaded", initPage);
