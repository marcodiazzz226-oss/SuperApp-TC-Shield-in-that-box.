from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

class ScanRequest(BaseModel):
    legal_text: str

def analyze_tc(text):
    # Core logic to find "Red Flags" in legal documents
    flags = {
        "Data Sharing": ["share your data", "third parties", "partners", "sell", "advertising"],
        "Hidden Fees": ["subscription", "auto-renew", "billing", "charges", "non-refundable"],
        "Rights Waivers": ["irrevocable", "ownership", "waive", "termination", "no liability"],
        "Privacy Risks": ["track", "cookies", "location", "personal information", "monitor"]
    }
    
    found_flags = []
    text_lower = text.lower()
    
    for category, keywords in flags.items():
        for word in keywords:
            if word in text_lower:
                found_flags.append(category)
                break # Move to next category once a flag is found
    
    return found_flags if found_flags else ["No major red flags detected."]

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>SUPER APP // T&C SHIELD</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { background: #0f172a; color: #f8fafc; font-family: sans-serif; padding: 20px; margin: 0; }
                .container { max-width: 600px; margin: 40px auto; background: #1e293b; padding: 30px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5); }
                h1 { color: #38bdf8; text-align: center; font-size: 24px; margin-bottom: 10px; }
                p { text-align: center; color: #94a3b8; font-size: 14px; }
                textarea { width: 100%; height: 250px; background: #0f172a; color: #e2e8f0; border: 1px solid #334155; padding: 15px; border-radius: 12px; font-size: 14px; outline: none; transition: border 0.3s; }
                textarea:focus { border-color: #38bdf8; }
                button { width: 100%; padding: 15px; margin-top: 15px; background: #38bdf8; color: #0f172a; border: none; font-weight: bold; border-radius: 12px; cursor: pointer; font-size: 16px; transition: opacity 0.2s; }
                button:hover { opacity: 0.9; }
                #results { margin-top: 25px; padding: 20px; background: #334155; border-radius: 12px; display: none; border-left: 4px solid #38bdf8; }
                .flag { color: #fb7185; font-weight: bold; margin: 10px 0; display: flex; align-items: center; }
                .safe { color: #4ade80; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>T&C Shield</h1>
                <p>Grade 10 STEM Project: Scans legal text for hidden risks.</p>
                <textarea id="input" placeholder="Paste the Terms and Conditions here..."></textarea>
                <button onclick="scan()">START ANALYSIS</button>
                <div id="results">
                    <h3 style="margin-top:0">Scan Report:</h3>
                    <div id="flagList"></div>
                </div>
            </div>
            <script>
                async function scan() {
                    const text = document.getElementById('input').value;
                    if(!text.trim()) return alert("Please paste some text first.");
                    
                    const btn = document.querySelector('button');
                    btn.innerText = "SCANNING...";
                    
                    try {
                        const res = await fetch('/scan', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({legal_text: text})
                        });
                        const data = await res.json();
                        
                        const rDiv = document.getElementById('results');
                        const fList = document.getElementById('flagList');
                        rDiv.style.display = 'block';
                        
                        if(data.flags[0].includes("No major")) {
                            fList.innerHTML = `<p class="safe">✅ ${data.flags[0]}</p>`;
                        } else {
                            fList.innerHTML = data.flags.map(f => `<p class="flag">⚠️ ${f} Detected</p>`).join('');
                        }
                    } catch (e) {
                        alert("Error connecting to server.");
                    } finally {
                        btn.innerText = "START ANALYSIS";
                    }
                }
            </script>
        </body>
    </html>
    """

@app.post("/scan")
async def scan_tc(req: ScanRequest):
    results = analyze_tc(req.legal_text)
    return {"flags": results}
