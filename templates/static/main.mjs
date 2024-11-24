document.addEventListener("DOMContentLoaded", () => {
	const buttons = document.querySelectorAll(".controls a");

	buttons.forEach((button) => {
		button.addEventListener("mouseover", () => {
			button.style.boxShadow = "0px 6px 12px rgba(255, 255, 255, 0.5)";
		});

		button.addEventListener("mouseout", () => {
			button.style.boxShadow = "0px 4px 8px rgba(0, 0, 0, 0.4)";
		});
	});
});
