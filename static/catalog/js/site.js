const watchDialog = document.querySelector("#watch-dialog");
const watchMessage = document.querySelector("#watch-dialog-message");

document.querySelectorAll("[data-watch-title]").forEach((button) => {
    button.addEventListener("click", () => {
        watchMessage.textContent = `A reprodução de "${button.dataset.watchTitle}" estará disponível em uma próxima versão do projeto.`;
        watchDialog.showModal();
    });
});

document.querySelectorAll("[data-close-dialog]").forEach((button) => {
    button.addEventListener("click", () => watchDialog.close());
});
