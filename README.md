# Corporate AI Lead Scraper (Niche Discovery Engine)

A robust, web-based intelligence gathering tool designed to hunt down niche AI startups and extract research/engineering internship opportunities.

## Features
- **Dynamic Niche Discovery**: Uses DuckDuckGo search to actively discover obscure startups based on highly targeted queries (e.g., Computer Vision, Edge AI, Trustworthy AI).
- **Targeted Lead Scraping**: Automatically extracts names, affiliations, and emails (with obfuscation handling).
- **Internship & Keyword Matching**: Evaluates pages for internship/student keywords and technical terms (ViT, GANs, Tensor Networks) to score leads.
- **Real-Time Web UI**: A beautiful, dark-mode Flask web application that streams discovery and scraping results live via Server-Sent Events (SSE).
- **Markdown Export**: Instantly export your sorted, high-priority leads to a clean Markdown table.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Chaloopanda/Corporate-AI-Lead-Scraper.git
cd Corporate-AI-Lead-Scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`.
