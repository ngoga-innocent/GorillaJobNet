function scrollLeft() {
  const container = document.getElementById("carousel");
  container.scrollBy({ left: -container.clientWidth, behavior: "smooth" });
}

function scrollRight() {
  const container = document.getElementById("carousel");
  container.scrollBy({ left: container.clientWidth, behavior: "smooth" });
}
