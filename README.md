# Activity - Word Search

A browser-based word search activity built with vanilla HTML, CSS, and JavaScript.

## How to Run on PC

This is a static web application — no installation or build step required.

### Option 1: Open Directly in a Browser (Quickest)

1. Clone or download this repository:
   ```bash
   git clone <repo-url>
   cd activity-word-search-starter
   ```
2. Double-click `index.html` to open it in your default browser,
   **or** drag and drop `index.html` onto any open browser window.

> **Note:** Some browser security policies block JavaScript when opening files directly with `file://`. If the search button does nothing, use Option 2 instead.

---

### Option 2: Use a Local Development Server (Recommended)

Running through a local server avoids browser security restrictions and better mirrors a real web environment.

#### With VS Code + Live Server (easiest)

1. Install [Visual Studio Code](https://code.visualstudio.com/).
2. Install the **Live Server** extension (by Ritwick Dey) from the Extensions panel (`Ctrl+Shift+X`).
3. Open the project folder in VS Code (`File → Open Folder`).
4. Right-click `index.html` in the Explorer and choose **"Open with Live Server"**.
5. The app opens automatically at `http://127.0.0.1:5500`.

#### With Python (no extra install needed on most systems)

```bash
# Python 3
python -m http.server 8080

# Then open your browser to:
# http://localhost:8080
```

#### With Node.js `npx serve`

```bash
npx serve .
# Then open the URL shown in the terminal
```

---

## Project Structure

```
activity-word-search-starter/
├── index.html        # Main page
├── assets/
│   ├── main.js       # JavaScript (complete the TODOs here)
│   └── style.css     # Styles
└── README.md
```

## Activity Instructions

Open `assets/main.js` and complete the `TODO` comments to make the word search work:

1. **TODO 1** – Select the page elements with `querySelector`.
2. **TODO 2** – Write an `if` statement to check whether the user's input appears in the quote.
3. **TODO 3** – Display a success or failure message in `#search-results`.

Stretch goals (case-insensitivity, match highlighting, word count, etc.) are listed at the bottom of `main.js`.
