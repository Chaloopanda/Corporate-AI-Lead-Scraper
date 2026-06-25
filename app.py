import json
from flask import Flask, render_template, request, Response
from lead_scraper import analyze_profile
from duckduckgo_search import DDGS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scrape', methods=['POST'])
def scrape():
    def generate():
        # Searching for niche AI startup opportunities dynamically
        queries = [
            '"computer vision" startup "team" "remote"',
            '"edge AI" startup "careers"',
            '"trustworthy AI" boutique startup'
        ]
        
        discovered_urls = set()
        
        # Yield status to frontend
        yield f"data: {json.dumps({'status_msg': 'Discovering niche startups...'})}\n\n"
        
        try:
            ddgs = DDGS()
            for query in queries:
                results = ddgs.text(query, max_results=5)
                for r in results:
                    discovered_urls.add(r['href'])
        except Exception as e:
            print(f"Search error: {e}")
            
        urls = list(discovered_urls)
        
        if not urls:
             yield f"data: {json.dumps({'status_msg': 'Failed to discover URLs.'})}\n\n"
             return

        yield f"data: {json.dumps({'status_msg': f'Found {len(urls)} niche opportunities. Scraping...'})}\n\n"

        for url in urls:
            url = url.strip()
            if url:
                # Call the scraping function from our module
                result = analyze_profile(url)
                # Yield JSON for this specific result
                yield f"data: {json.dumps(result)}\n\n"
                
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=False, port=5000)
