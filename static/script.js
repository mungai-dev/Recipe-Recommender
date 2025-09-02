// Optional: Add smooth scroll on form submit
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("recipeForm");
  form.addEventListener("submit", () => {
    setTimeout(() => {
      document.querySelector(".recipes").scrollIntoView({ behavior: "smooth" });
    }, 300);
  });
});
