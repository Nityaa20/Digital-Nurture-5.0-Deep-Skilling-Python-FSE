// app.js - Hands On 9 (accessibility part)
// Written simple, no fancy stuff, just plain JS

// ---- Hamburger menu toggle (task 131 - aria-expanded) ----
var menuBtn = document.getElementById("menuBtn");
var mainNav = document.getElementById("mainNav").querySelector("ul");

menuBtn.addEventListener("click", function () {
  var isOpen = mainNav.classList.contains("show");

  if (isOpen) {
    mainNav.classList.remove("show");
    menuBtn.setAttribute("aria-expanded", "false");
  } else {
    mainNav.classList.add("show");
    menuBtn.setAttribute("aria-expanded", "true");
  }
});


// ---- Search box filtering (task 130 - aria-live announce results) ----
var searchBox = document.getElementById("search-courses");
var courseCards = document.querySelectorAll(".course-card");
var resultCount = document.getElementById("resultCount");

searchBox.addEventListener("input", function () {
  var typed = searchBox.value.toLowerCase();
  var visibleCount = 0;

  courseCards.forEach(function (card) {
    var courseName = card.querySelector("h3").textContent.toLowerCase();

    if (courseName.indexOf(typed) !== -1) {
      card.style.display = "block";
      visibleCount++;
    } else {
      card.style.display = "none";
    }
  });

  // this text will be read out by screen reader automatically because of aria-live
  resultCount.textContent = visibleCount + " courses found";
});


// ---- Click and Keyboard access on course cards (task 129) ----
var selectedDiv = document.getElementById("selected-course");

function showCourseInfo(card) {
  var name = card.querySelector("h3").textContent;
  var credits = card.querySelector("span").textContent;
  selectedDiv.textContent = "Selected: " + name + " (" + credits + ")";
}

courseCards.forEach(function (card) {
  // normal mouse click
  card.addEventListener("click", function () {
    showCourseInfo(card);
  });

  // keyboard users - pressing Enter should do the same thing as click
  card.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      showCourseInfo(card);
    }
  });
});


// ---- Explore button just scrolls down to courses section ----
var exploreBtn = document.getElementById("exploreBtn");
exploreBtn.addEventListener("click", function () {
  document.getElementById("courses").scrollIntoView({ behavior: "smooth" });
});


// ---- Profile form submit ----
var profileForm = document.getElementById("profileForm");
profileForm.addEventListener("submit", function (e) {
  e.preventDefault();
  alert("Profile saved (this is just a demo, not sent anywhere)");
});
