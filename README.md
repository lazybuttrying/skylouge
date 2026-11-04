# ✈️ SKYLOGUE | Scale Aircraft & Military Aviation Wiki Database

A modern, high-performance static wiki and database for diecast aircraft collectors, scale aviation modelers, and military aviation enthusiasts. Built for high SEO visibility, global English-speaking audiences, and seamless **Google AdSense** monetization.

---

## 🌟 Key Features

1. **Collector-Grade Wiki Templates:**
   - **InfoBox Specifications:** Brand, Scale, Aircraft Type, Real Registration/Tail Code, Military Squadron/Unit, Historical Ace Pilot, Tooling Lineage (OEM Foundry), and Diecast Material.
   - **Historical Context:** Squadrons, combat sorties, and airframe history.
   - **Tooling & Mold Analysis:** Deep analysis of mold origins (e.g. WLTK vs Herpa shared tooling), tampo printing fidelity, and gear detail.
   - **Macro Walkaround Photography:** Integrated high-resolution photo galleries.
2. **Google AdSense Ready:**
   - Fully compliant structure with mandatory legal pages (`/about.html`, `/privacy-policy.html`, `/terms.html`, `/contact.html`).
   - Integrated `ads.txt` and `sitemap.xml`.
   - Dedicated high-CTR responsive ad slots (Top leaderboard, in-article, and sidebar rectangle).
3. **Automated CI/CD with GitHub Actions:**
   - Push any new model markdown to the `main` branch, and GitHub Actions automatically builds and deploys to **GitHub Pages** within seconds.
   - Blazing fast build time (< 5 seconds) with zero complex npm dependencies.

---

## 📁 Project Structure

```text
skylogue/
├── .github/
│   └── workflows/
│       └── deploy.yml           # Automated GitHub Pages CI/CD workflow
├── assets/
│   └── images/                  # High-resolution model photography
│       ├── spitfire-mkvb-raf-303-sqn/
│       ├── tu160-blackjack-rf94105/
│       ├── il76td-90vd-volga-dnepr-ra76503/
│       └── p40b-flying-tigers-white-47/
├── content/
│   └── models/                  # Markdown files for each model entry
│       ├── spitfire-mkvb-raf-303-sqn.md
│       ├── tu160-blackjack-rf94105.md
│       ├── il76td-90vd-volga-dnepr-ra76503.md
│       └── p40b-flying-tigers-white-47.md
├── dist/                        # Built production static site
├── build.py                     # Python static site generator
└── README.md
```

---

## 🚀 How to Add a New Model

1. Create a new markdown file in `content/models/your-model-slug.md` with the following frontmatter:

```yaml
---
title: "Model Name - Operator (Tail Code)"
slug: "your-model-slug"
brand: "Gemini Jets / JC Wings / Hobby Master"
scale: "1:72 / 1:200 / 1:400"
category: "Military Fighters / Heavy Transports / Commercial Airliners"
era: "World War II / Cold War / Modern"
aircraft: "Boeing B-52H Stratofortress"
operator: "USAF 2nd Bomb Wing"
tail_code: "LA 60-0001"
mold_origin: "Herpa / Inflight200 Tooling"
release_year: "2024"
material: "Diecast Metal"
featured_image: "assets/images/your-model-slug/photo_1.jpg"
images:
  - "assets/images/your-model-slug/photo_1.jpg"
  - "assets/images/your-model-slug/photo_2.jpg"
---

## Real Aircraft History
[History of the airframe, squadron operations, and combat record...]

## Diecast Model & Mold Analysis
[Review of tampo printing, mold lineage, cockpit canopy, and accuracy...]
```

2. Place model photos in `assets/images/your-model-slug/`.
3. Commit and push:
```bash
git add .
git commit -m "Add new model: your-model-slug"
git push origin main
```
GitHub Actions will build and update the live wiki automatically!

---

## 💰 How to Connect Google AdSense

1. Open `build.py` and replace `ca-pub-XXXXXXXXXXXXXXXX` with your approved **AdSense Publisher ID**.
2. Open `dist/ads.txt` (or update in `build.py`) and replace `pub-XXXXXXXXXXXXXXXX` with your publisher ID:
```text
google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
```
3. Submit `https://your-username.github.io/skylogue` in the **Google AdSense Sites** dashboard.

---

## 🛠 Local Build

To rebuild the site locally at any time:
```bash
python3 build.py
```
Open `dist/index.html` in any browser to preview!
