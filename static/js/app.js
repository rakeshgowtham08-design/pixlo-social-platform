document.addEventListener("DOMContentLoaded", () => {
  const imageInput = document.getElementById("id_image");
  const imageName = document.getElementById("image-name");
  if (imageInput && imageName) {
    imageInput.addEventListener("change", () => {
      imageName.textContent = imageInput.files.length ? imageInput.files[0].name : "JPG, PNG or WEBP";
    });
  }
  document.querySelectorAll(".flash").forEach((message) => {
    window.setTimeout(() => {
      message.classList.add("flash-hide");
      window.setTimeout(() => message.remove(), 350);
    }, 4200);
  });
  document.querySelectorAll("img").forEach((img) => {
    img.addEventListener("error", () => img.classList.add("image-error"), { once: true });
  });
});
