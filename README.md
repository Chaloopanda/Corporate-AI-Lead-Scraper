<div align="center">
  <h1>🚀 Corporate AI Lead Scraper (Niche Discovery Engine)</h1>
  <p><i>Automated intelligence gathering for AI research and engineering internships.</i></p>

  <p>
    <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img alt="Flask" src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
    <img alt="Pandas" src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  </p>
</div>

---

## 🌟 Overview

The **Corporate AI Lead Scraper** is a specialized web application built for researchers and students looking to break into the AI industry. Instead of relying on static lists, this tool operates as a **Niche Discovery Engine**. It scours the web in real-time to uncover hidden, remote-friendly AI startups and corporate labs, analyzes their team profiles, and extracts actionable contact information.

If you are hunting for opportunities in **Computer Vision**, **Edge AI**, or **Trustworthy AI**, this tool automatically scores and tiers potential leads based on your specific skills!

## ✨ Key Features

- 🕵️‍♂️ **Dynamic Niche Discovery**: Leverages DuckDuckGo search programmatically to hunt down obscure, early-stage startup team pages based on highly targeted queries.
- 🧠 **Smart Skill Matching**: Heuristically scans researcher profiles and recent publications for niche technical keywords (e.g., Vision Transformers, GANs, Tensor Networks).
- 🎓 **Internship Targeting**: Automatically boosts the score of leads whose pages explicitly mention "intern", "undergraduate", or "student" roles.
- ⚡ **Real-Time Web UI**: A stunning, dark-mode glassmorphic Flask frontend. Results are streamed live using **Server-Sent Events (SSE)** so you never have to wait for a loading screen.
- 📊 **Instant Markdown Export**: One-click export of your tiered leads into a beautifully formatted Markdown table.

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask, Requests, BeautifulSoup4, DuckDuckGo-Search
- **Data Processing**: Pandas
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), JavaScript (SSE integration)

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Chaloopanda/Corporate-AI-Lead-Scraper.git
   cd Corporate-AI-Lead-Scraper
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask Server:**
   ```bash
   python app.py
   ```

4. **Launch the Application:**
   Open your browser and navigate to [http://localhost:5000](http://localhost:5000)

## 💡 How it Works

1. **Discovery**: The backend queries search engines for niche permutations (e.g. `"edge AI" startup "careers"`).
2. **Extraction**: It visits the discovered URLs and extracts names, corporate affiliations, and emails (smartly bypassing common `[at]` obfuscations).
3. **Scoring Engine**: 
   - +1 for matching Technical Keywords
   - +1 for Corporate Labs/Startups
   - +1 for Remote/Distributed indicators
   - +1 for Internship mentions
4. **Categorization**: Leads scoring 3 or higher are flagged as **Tier 1 (Hot Match)**.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Chaloopanda/Corporate-AI-Lead-Scraper/issues).
