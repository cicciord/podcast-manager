"use strict;";

// the search implemented is case insensitive
// to make the search case sensitive remove toLowerCase function
document.querySelector(".search-tab").addEventListener("input", (e) => {
  e.preventDefault();
  const value = e.target.value.toLowerCase();
  const podcastsEl = document.querySelectorAll("[data-podcast]");
  podcastsEl.forEach((podcastEl) => {
    const podcastTitle = podcastEl
      .querySelector("[data-podcast-title]")
      .innerHTML.toLowerCase();
    const podcastDes = podcastEl
      .querySelector("[data-podcast-description]")
      .innerHTML.toLowerCase();

    podcastEl.classList.remove("d-none");
    if (!value) {
      return;
    }
    if (!(podcastTitle.includes(value) || podcastDes.includes(value))) {
      podcastEl.classList.add("d-none");
    }
  });
});
