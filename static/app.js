"use strict;";

const searchTab = document.querySelector(".search-tab");
const podcastsEl = document.querySelectorAll("[data-podcast]");

searchTab.addEventListener("input", (e) => {
  const value = e.target.value;
  podcastsEl.forEach((podcastEl) => {
    const podcastTitle = podcastEl.querySelector(
      "[data-podcast-title]"
    ).innerHTML;
    const podcastDes = podcastEl.querySelector(
      "[data-podcast-description]"
    ).innerHTML;

    podcastEl.classList.remove("d-none");
    if (!value) {
      return;
    }
    if (!(podcastTitle.includes(value) || podcastDes.includes(value))) {
      podcastEl.classList.add("d-none");
    }
  });
});
