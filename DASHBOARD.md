# MemeTide Web Dashboard

Beautiful, interactive web interface for MemeTide API.

---

## Features

✅ **Real-time scanning** - Scan memecoins with live updates  
✅ **Interactive UI** - Clean, modern design  
✅ **Dark mode** - Toggle between light/dark themes  
✅ **Export to JSON** - Save scan results locally  
✅ **Scan history** - Browse last 10 scans (localStorage)  
✅ **Sample tweets** - See top 3 tweets per token  
✅ **On-chain display** - Price, liquidity, market cap visualized  
✅ **Confidence badges** - High/Medium/Low with color coding  
✅ **Responsive** - Works on desktop, tablet, mobile  
✅ **Zero setup** - Just open browser  
✅ **Theme persistence** - Remembers your dark mode preference  

---

## Access

**Local:** http://localhost:8000/  
**Production:** https://your-domain.com/

---

## Screenshots

### Main Dashboard
- Gradient purple background (or dark blue-gray in dark mode)
- Clean card-based layout
- Form with 4 input fields (min mentions, top N, data source, on-chain toggle)
- Three action buttons:
  - 🚀 "Scan" - Run new scan
  - 💾 "Export" - Download results as JSON
  - 📜 "History" - View past scans
- Theme toggle button (🌙/☀️) in header

### Scan Results
- Scan metadata (ID, duration, mentions, tokens found)
- Token cards with:
  - Confidence badge (colored: green=high, yellow=medium, red=low)
  - Score out of 100
  - Stats grid (mentions, sentiment, risk)
  - On-chain metrics section (price, market cap, liquidity, age)
  - Sample tweets section (top 3 by engagement)

### Scan History
- List of last 10 scans
- Each entry shows: scan ID, timestamp, token count, mentions
- Click to reload results

### Features
- Loading spinner during scan
- Error messages with red banner
- Export button downloads JSON file
- Hover effects on cards
- Animated wave emoji in header
- Dark mode with smooth transition
- Theme preference saved to localStorage
- Links to API docs and GitHub

---

## Usage

1. **Open Dashboard**
   ```bash
   # Start server
   cd ~/memetide
   ./start_server.sh
   
   # Open browser
   open http://localhost:8000
   ```

2. **Configure Scan**
   - **Min Mentions:** Minimum mentions to consider (default: 3)
   - **Top N Results:** How many tokens to show (default: 10)
   - **Data Source:** Mock (fast) or Real Twitter (slow)
   - **On-Chain Metrics:** Enable to fetch price/liquidity

3. **Run Scan**
   - Click "Start Scan"
   - Wait ~1-2 seconds
   - View results

4. **Interpret Results**
   - 🔥 **High confidence** (70-100): Strong signal, act now
   - ⚠️ **Medium confidence** (40-69): Promising, monitor
   - ❌ **Low confidence** (0-39): Weak signal, avoid

5. **Export & History**
   - Click "Export" to download JSON
   - Click "History" to view past scans
   - Theme toggle in top-right corner

---

## Customization

### Change Colors

Edit `static/index.html`:

```css
/* Purple gradient (default) */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Blue gradient */
background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);

/* Green gradient */
background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
```

### Change API Endpoint

For production deployment:

```javascript
// Change this line in index.html
const API_BASE = 'https://your-api.railway.app';
```

Or leave as `window.location.origin` to auto-detect.

---

## Deployment

Dashboard is automatically deployed with API server.

**Railway/Render:** Just push to GitHub, dashboard is included.

**Custom Domain:**
- Main site: https://memetide.com/
- API docs: https://memetide.com/docs
- Dashboard: https://memetide.com/ (auto-redirects)

---

## Tech Stack

- **Vanilla JavaScript** - No framework needed
- **CSS3** - Gradients, animations, responsive grid
- **Fetch API** - Async HTTP requests
- **FastAPI Static Files** - Served by backend

---

## Browser Support

✅ Chrome 90+  
✅ Firefox 88+  
✅ Safari 14+  
✅ Edge 90+  

---

## Performance

- **Initial load:** <100ms (single HTML file)
- **Scan request:** 0.5-2s (depends on on-chain fetch)
- **File size:** ~28KB (uncompressed, self-contained)
- **Local storage:** <50KB (scan history)

---

## Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- High contrast colors
- Mobile-friendly

---

## Future Enhancements

**v1.1:** ✅ DONE
- [x] Dark mode toggle
- [x] Export results to JSON
- [x] Scan history (localStorage)
- [x] Sample tweets display

**v1.2:**
- [ ] Chart visualization (price history)
- [ ] Real-time WebSocket updates
- [ ] Save favorite tokens
- [ ] Compare multiple scans

**v2.0:**
- [ ] User authentication
- [ ] Cloud-saved scan history
- [ ] Alert notifications
- [ ] Custom watchlists
- [ ] Advanced filters

---

## Troubleshooting

**Dashboard not loading?**
- Ensure `static/` directory exists
- Check FastAPI mounted static files: `app.mount("/static", ...)`
- Verify file path: `static/index.html`

**API calls failing?**
- Check CORS settings in `api_server.py`
- Ensure API is running: `curl http://localhost:8000/health`
- Open browser console (F12) for errors

**Styling broken?**
- CSS is inline in HTML file
- No external dependencies
- Check browser console for errors

---

**Built for OKX.AI Genesis Hackathon 2026** 🚀
