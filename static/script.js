console.log("script loaded");

//page switching
function showPage(pageId) {

    const pages = document.querySelectorAll(".page");

    pages.forEach(page => {
        page.classList.add("hidden");
    });

    const activePage = document.getElementById(pageId);

    if (activePage) {
        activePage.classList.remove("hidden");
    }
}

//darkmode
function toggleDarkMode() {
    document.body.classList.toggle("dark");

    if (document.body.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

window.onload = function () {

    console.log("DOM ready");

    // theme load
    const theme = localStorage.getItem("theme");

    if (theme === "dark") {
        document.body.classList.add("dark");
    }

    // default page
    showPage("dashboard");
};