const WHITE_THEME = "white-theme"
const DARK_THEME = "dark-theme"

const theme_toggle = document.querySelector(".theme-toggle");

document.addEventListener("DOMContentLoaded", () => {
    const theme = localStorage.getItem("theme");
    const symbol = document.querySelector(".header-icon img, .login-icon img");
    if (theme) {
        (theme === WHITE_THEME)
            ? setWhiteTheme(symbol)
            : setDarkTheme(symbol);
    } else {
        localStorage.setItem("theme", DARK_THEME);
    }
})

theme_toggle.addEventListener("click", () => {
    const theme = document.body.classList.contains(WHITE_THEME);
    const symbol = document.querySelector(".header-icon img, .login-icon img");
    (!theme) ? setWhiteTheme(symbol) : setDarkTheme(symbol);
})

function setWhiteTheme(symbol) {
    document.body.classList.add(WHITE_THEME);
    localStorage.setItem('theme', WHITE_THEME);
    symbol.src = '/image/mobius-rumos.gif';
}

function setDarkTheme(symbol) {
    document.body.classList.remove(WHITE_THEME);
    localStorage.setItem('theme', DARK_THEME);
    symbol.src = '/image/mobius-nox.gif';
}