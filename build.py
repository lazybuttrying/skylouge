import os, re, json, datetime, html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content/models")
DIST_DIR = os.path.join(BASE_DIR, "dist")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

SITE_URL = "https://lazybuttrying.github.io/skylogue"
SITE_TITLE = "SKYLOGUE | Scale Aircraft & Military Aviation Database"
SITE_DESC = "The definitive collector's wiki & database for diecast aircraft, military aviation history, and scale mold analysis."

def parse_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read()
    
    frontmatter = {}
    body = raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()
            # simple yaml parse
            current_list_key = None
            for line in fm_text.splitlines():
                line = line.rstrip()
                if not line or line.startswith("#"): continue
                if line.startswith("  - ") and current_list_key:
                    val = line[4:].strip().strip('"').strip("'")
                    frontmatter[current_list_key].append(val)
                elif ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if val == "":
                        frontmatter[key] = []
                        current_list_key = key
                    else:
                        frontmatter[key] = val
                        current_list_key = None
    
    # Simple markdown to HTML
    body_html = ""
    for block in body.split("\n\n"):
        block = block.strip()
        if not block: continue
        if block.startswith("## "):
            body_html += f'<h2 class="text-2xl font-bold text-slate-100 mt-8 mb-4 border-b border-slate-700 pb-2 flex items-center gap-2"><span class="w-2 h-6 bg-sky-500 rounded-sm inline-block"></span>{html.escape(block[3:])}</h2>\n'
        elif block.startswith("### "):
            body_html += f'<h3 class="text-xl font-bold text-sky-400 mt-6 mb-3">{html.escape(block[4:])}</h3>\n'
        elif block.startswith("* ") or block.startswith("- "):
            items = block.splitlines()
            body_html += '<ul class="list-disc list-inside space-y-2 text-slate-300 my-4 pl-2 leading-relaxed">\n'
            for item in items:
                line_text = re.sub(r'^[\*\-]\s+', '', item)
                # bold
                line_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-slate-100 font-semibold">\1</strong>', line_text)
                # italic
                line_text = re.sub(r'\*(.*?)\*', r'<em class="text-sky-300">\1</em>', line_text)
                body_html += f'  <li>{line_text}</li>\n'
            body_html += '</ul>\n'
        elif re.match(r'^\d+\.\s', block):
            items = block.splitlines()
            body_html += '<ol class="list-decimal list-inside space-y-2 text-slate-300 my-4 pl-2 leading-relaxed">\n'
            for item in items:
                line_text = re.sub(r'^\d+\.\s+', '', item)
                line_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-slate-100 font-semibold">\1</strong>', line_text)
                line_text = re.sub(r'\*(.*?)\*', r'<em class="text-sky-300">\1</em>', line_text)
                body_html += f'  <li>{line_text}</li>\n'
            body_html += '</ol>\n'
        else:
            p_text = block.replace("\n", " ")
            p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-slate-100 font-semibold">\1</strong>', p_text)
            p_text = re.sub(r'\*(.*?)\*', r'<em class="text-sky-300">\1</em>', p_text)
            body_html += f'<p class="text-slate-300 leading-relaxed my-4 text-base">{p_text}</p>\n'
            
    return frontmatter, body_html

def get_header(current_page=""):
    return f"""
    <!-- Global Header -->
    <header class="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 text-slate-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <a href="{SITE_URL}/index.html" class="flex items-center gap-2 group">
            <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-sky-500 to-blue-600 flex items-center justify-center font-black text-white text-lg tracking-wider shadow-lg shadow-sky-500/20 group-hover:scale-105 transition-transform">
              S
            </div>
            <div>
              <span class="font-extrabold tracking-wider text-white text-lg block leading-none">SKYLOGUE</span>
              <span class="text-[10px] text-sky-400 tracking-widest font-mono uppercase block mt-0.5">Scale Aviation Wiki</span>
            </div>
          </a>
        </div>
        
        <nav class="hidden md:flex items-center gap-6 text-sm font-medium">
          <a href="{SITE_URL}/index.html" class="hover:text-sky-400 transition-colors py-1">Home</a>
          <a href="{SITE_URL}/models/index.html" class="hover:text-sky-400 transition-colors py-1">All Models</a>
          <a href="{SITE_URL}/about.html" class="hover:text-sky-400 transition-colors py-1">About Archive</a>
          <a href="{SITE_URL}/privacy-policy.html" class="hover:text-sky-400 transition-colors py-1">Privacy</a>
          <a href="{SITE_URL}/contact.html" class="hover:text-sky-400 transition-colors py-1">Contact</a>
        </nav>

        <div class="flex items-center gap-3">
          <div class="relative">
            <input type="text" id="quick-search" placeholder="Search registration, mold, aircraft..." class="bg-slate-800 text-xs text-slate-200 placeholder-slate-500 rounded-full pl-8 pr-4 py-1.5 border border-slate-700 focus:outline-none focus:border-sky-500 w-44 sm:w-60 transition-all">
            <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          </div>
        </div>
      </div>
    </header>
    """

def get_footer():
    year = datetime.datetime.now().year
    return f"""
    <!-- Global Footer -->
    <footer class="bg-slate-950 border-t border-slate-800 text-slate-400 text-xs mt-20 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div class="col-span-1 md:col-span-2">
            <div class="flex items-center gap-2 mb-3">
              <span class="w-6 h-6 rounded bg-sky-500 flex items-center justify-center font-black text-white text-xs">S</span>
              <span class="font-bold text-slate-200 tracking-wider">SKYLOGUE ARCHIVE</span>
            </div>
            <p class="text-slate-400 leading-relaxed max-w-sm mb-4">
              The premier scale diecast aircraft reference wiki and database. Dedicated to historical accuracy, detailed tooling lineage, and high-fidelity walkaround photography for collectors worldwide.
            </p>
            <p class="text-slate-500 text-[11px]">
              &copy; {year} Skylogue Archive. Content, photography and analysis protected under creative rights.
            </p>
          </div>
          <div>
            <h4 class="font-bold text-slate-200 text-sm mb-3">Database Navigation</h4>
            <ul class="space-y-2">
              <li><a href="{SITE_URL}/models/index.html" class="hover:text-sky-400 transition-colors">Complete Model Catalog</a></li>
              <li><a href="{SITE_URL}/models/index.html?scale=1:72" class="hover:text-sky-400 transition-colors">1:72 Military Fighters</a></li>
              <li><a href="{SITE_URL}/models/index.html?scale=1:200" class="hover:text-sky-400 transition-colors">1:200 Strategic & Airliners</a></li>
              <li><a href="{SITE_URL}/about.html" class="hover:text-sky-400 transition-colors">Editorial & Mold Lineage</a></li>
            </ul>
          </div>
          <div>
            <h4 class="font-bold text-slate-200 text-sm mb-3">Legal & Advertising</h4>
            <ul class="space-y-2">
              <li><a href="{SITE_URL}/privacy-policy.html" class="hover:text-sky-400 transition-colors">Privacy Policy</a></li>
              <li><a href="{SITE_URL}/terms.html" class="hover:text-sky-400 transition-colors">Terms of Service</a></li>
              <li><a href="{SITE_URL}/contact.html" class="hover:text-sky-400 transition-colors">Contact / Submissions</a></li>
              <li><a href="{SITE_URL}/ads.txt" class="hover:text-sky-400 transition-colors">ads.txt</a></li>
            </ul>
          </div>
        </div>
        <div class="border-t border-slate-900 pt-6 flex flex-col sm:flex-row items-center justify-between text-slate-500 text-[11px]">
          <p>Designed for global aviation enthusiasts, scale model historians, and serious diecast collectors.</p>
          <p class="mt-2 sm:mt-0">Hosted on GitHub Pages with automated GitHub Actions CI/CD.</p>
        </div>
      </div>
    </footer>
    """

def get_adsense_banner():
    return """
    <!-- Google AdSense - Top Responsive Banner Placeholder -->
    <div class="my-8 mx-auto max-w-5xl px-4 text-center">
      <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-4 min-h-[90px] flex flex-col items-center justify-center text-slate-600 text-xs">
        <span class="uppercase tracking-widest text-[10px] text-slate-500 mb-1">Advertisement</span>
        <!-- Paste your AdSense ad code below -->
        <!-- <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins> -->
        <span class="text-slate-600 font-mono text-[11px]">[ Google AdSense Banner Slot 728x90 / Responsive ]</span>
      </div>
    </div>
    """

def get_adsense_in_article():
    return """
    <!-- Google AdSense - In-Article Ad Slot -->
    <div class="my-8 bg-slate-900/60 border border-slate-800 rounded-xl p-4 min-h-[120px] flex flex-col items-center justify-center text-slate-600 text-xs">
      <span class="uppercase tracking-widest text-[10px] text-slate-500 mb-1">Sponsored Content</span>
      <!-- <ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX"></ins> -->
      <span class="text-slate-600 font-mono text-[11px]">[ Google AdSense In-Article Responsive Slot ]</span>
    </div>
    """

def build_site():
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "models"), exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "assets"), exist_ok=True)
    
    # Copy assets
    os.system(f"cp -r {ASSETS_DIR}/* {DIST_DIR}/assets/ 2>/dev/null || true")
    
    # Parse all models
    models_data = []
    for fname in sorted(os.listdir(CONTENT_DIR)):
        if fname.endswith(".md"):
            fpath = os.path.join(CONTENT_DIR, fname)
            fm, body_html = parse_markdown(fpath)
            models_data.append((fm, body_html))
            
    print(f"Parsed {len(models_data)} models.")
    
    # Common HTML Head
    def get_head(title, desc, image="", canonical=""):
        return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="canonical" href="{canonical or SITE_URL}">
  
  <!-- Open Graph -->
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical or SITE_URL}">
  <meta property="og:image" content="{image or (SITE_URL + '/assets/images/spitfire-mkvb-raf-303-sqn/photo_1.jpg')}">
  
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(desc)}">
  <meta name="twitter:image" content="{image or (SITE_URL + '/assets/images/spitfire-mkvb-raf-303-sqn/photo_1.jpg')}">
  
  <!-- Tailwind CSS via CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            slate: {{
              850: '#172033',
              950: '#0b0f19',
            }}
          }}
        }}
      }}
    }}
  </script>
  
  <!-- Google AdSense Auto Ads Tag Placeholder -->
  <!-- <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script> -->
  
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    body {{ font-family: 'Inter', sans-serif; }}
    code, pre {{ font-family: 'JetBrains Mono', monospace; }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col antialiased selection:bg-sky-500 selection:text-white">
"""

    # 1. Build Model Detail Pages
    for fm, body_html in models_data:
        slug = fm.get("slug", "model")
        title = fm.get("title", "Aviation Model")
        brand = fm.get("brand", "Unknown")
        scale = fm.get("scale", "1:72")
        aircraft = fm.get("aircraft", "")
        tail_code = fm.get("tail_code", "")
        serial = fm.get("serial_number", "")
        operator = fm.get("operator", "")
        unit = fm.get("unit", "")
        era = fm.get("era", "")
        category = fm.get("category", "")
        mold = fm.get("mold_origin", "")
        release_year = fm.get("release_year", "")
        material = fm.get("material", "Diecast Metal")
        pilot = fm.get("pilot", "")
        engine = fm.get("engine", "")
        armament = fm.get("armament", "")
        wingspan = fm.get("wingspan", "")
        length = fm.get("length", "")
        rating = fm.get("rating", "4.8")
        images = fm.get("images", [])
        
        main_img = images[0] if images else ""
        canonical_url = f"{SITE_URL}/models/{slug}.html"
        
        # Build gallery HTML
        gallery_html = ""
        for i, img in enumerate(images):
            gallery_html += f"""
            <a href="{SITE_URL}/{img}" target="_blank" class="block group overflow-hidden rounded-xl bg-slate-900 border border-slate-800 hover:border-sky-500 transition-all shadow-md">
              <img src="{SITE_URL}/{img}" alt="{html.escape(title)} - Shot {i+1}" class="w-full h-48 sm:h-56 object-cover object-center group-hover:scale-105 transition-transform duration-300">
              <div class="p-2.5 text-center text-[11px] text-slate-400 font-mono bg-slate-900/90 border-t border-slate-800/80">
                Walkaround Detail #{i+1}
              </div>
            </a>
            """
            
        page_html = get_head(f"{title} | {brand} {scale} Review & Specs", f"In-depth collector analysis, mold history, and historical background for {title} ({brand} {scale}).", SITE_URL + "/" + main_img, canonical_url)
        page_html += get_header()
        page_html += f"""
        <main class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
          <!-- Breadcrumb -->
          <nav class="flex items-center gap-2 text-xs text-slate-400 mb-6 font-mono">
            <a href="{SITE_URL}/index.html" class="hover:text-sky-400">Home</a>
            <span>/</span>
            <a href="{SITE_URL}/models/index.html" class="hover:text-sky-400">Database</a>
            <span>/</span>
            <span class="text-sky-400 font-semibold truncate">{html.escape(scale)}</span>
            <span>/</span>
            <span class="text-slate-200 truncate">{html.escape(title[:30])}...</span>
          </nav>
          
          {get_adsense_banner()}
          
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Main Content (8 cols) -->
            <div class="lg:col-span-8 space-y-6">
              <div>
                <div class="flex flex-wrap items-center gap-2 mb-3">
                  <span class="px-2.5 py-1 rounded-md text-xs font-bold bg-sky-500/20 text-sky-400 border border-sky-500/30">{html.escape(scale)} Scale</span>
                  <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/30">{html.escape(brand)}</span>
                  <span class="px-2.5 py-1 rounded-md text-xs font-medium bg-slate-800 text-slate-300">{html.escape(category)}</span>
                  <span class="px-2.5 py-1 rounded-md text-xs font-medium bg-slate-800 text-slate-400 font-mono">{html.escape(era)}</span>
                </div>
                <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight mb-3">
                  {html.escape(title)}
                </h1>
                <p class="text-slate-400 text-sm flex items-center gap-4">
                  <span>Author: <strong class="text-slate-200">Skylogue Curators</strong></span>
                  <span>•</span>
                  <span>Tooling Lineage: <strong class="text-sky-400 font-mono">{html.escape(mold)}</strong></span>
                </p>
              </div>

              <!-- Main Hero Image -->
              <div class="rounded-2xl overflow-hidden border border-slate-800 bg-slate-900 shadow-2xl relative group">
                <img src="{SITE_URL}/{main_img}" alt="{html.escape(title)}" class="w-full h-auto max-h-[520px] object-cover object-center group-hover:scale-[1.01] transition-transform duration-300">
                <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-slate-950/90 via-slate-950/40 to-transparent p-4 flex items-center justify-between text-xs text-slate-300">
                  <span class="font-mono text-sky-300 font-semibold">{html.escape(tail_code)} ({html.escape(serial)})</span>
                  <span class="bg-black/60 backdrop-blur px-2 py-1 rounded text-[11px] font-mono">Original Collector Photography</span>
                </div>
              </div>

              <!-- Article Content -->
              <div class="bg-slate-900/50 border border-slate-800/80 rounded-2xl p-6 sm:p-8 backdrop-blur-sm">
                {body_html}
                
                {get_adsense_in_article()}
                
                <!-- Walkaround Photo Gallery Section -->
                <h2 class="text-2xl font-bold text-slate-100 mt-12 mb-4 border-b border-slate-700 pb-2 flex items-center gap-2">
                  <span class="w-2 h-6 bg-sky-500 rounded-sm inline-block"></span>
                  Collector High-Res Walkaround Gallery
                </h2>
                <p class="text-slate-400 text-sm mb-6">
                  Detailed macro photography inspecting panel line depth, tampo registry, antenna installations, and landing gear struts.
                </p>
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                  {gallery_html}
                </div>
              </div>
            </div>

            <!-- Right Sidebar: InfoBox (4 cols) -->
            <div class="lg:col-span-4 space-y-6">
              <!-- InfoBox Card -->
              <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl sticky top-20">
                <div class="bg-gradient-to-r from-sky-600 to-blue-700 p-4 text-white">
                  <h3 class="font-extrabold text-lg tracking-wide uppercase font-mono">Model Specifications</h3>
                  <p class="text-sky-100 text-xs font-mono">{html.escape(brand)} • {html.escape(scale)}</p>
                </div>
                
                <div class="p-4 divide-y divide-slate-800 text-xs">
                  <div class="py-2.5 flex justify-between items-center">
                    <span class="text-slate-400 font-medium">Brand</span>
                    <span class="text-slate-100 font-semibold font-mono">{html.escape(brand)}</span>
                  </div>
                  <div class="py-2.5 flex justify-between items-center">
                    <span class="text-slate-400 font-medium">Scale</span>
                    <span class="text-sky-400 font-bold font-mono">{html.escape(scale)}</span>
                  </div>
                  <div class="py-2.5 flex justify-between items-center">
                    <span class="text-slate-400 font-medium">Aircraft Type</span>
                    <span class="text-slate-100 font-semibold">{html.escape(aircraft)}</span>
                  </div>
                  <div class="py-2.5 flex justify-between items-center">
                    <span class="text-slate-400 font-medium">Operator / Military</span>
                    <span class="text-slate-200 text-right max-w-[200px] font-medium">{html.escape(operator)}</span>
                  </div>
                  <div class="py-2.5 flex justify-between items-center">
                    <span class="text-slate-400 font-medium">Squadron / Unit</span>
                    <span class="text-slate-200 text-right max-w-[200px] font-mono">{html.escape(unit)}</span>
                  </div>
                  <div class="py-2.5 flex justify-between items-center">
                    <span class="text-slate-400 font-medium">Tail Code / Reg</span>
                    <span class="text-amber-400 font-bold font-mono">{html.escape(tail_code)}</span>
                  </div>
                  <div class="py-2.5 flex justify-between items-center">
                    <span class="text-slate-400 font-medium">Serial / c/n</span>
                    <span class="text-slate-200 font-mono">{html.escape(serial)}</span>
                  </div>
                  <div class="py-2.5 flex justify-between items-center">
                    <span class="text-slate-400 font-medium">Historical Pilot</span>
                    <span class="text-slate-200 text-right max-w-[200px]">{html.escape(pilot or 'Standard Crew')}</span>
                  </div>
                  <div class="py-2.5 flex justify-between items-center">
                    <span class="text-slate-400 font-medium">Diecast Material</span>
                    <span class="text-slate-200">{html.escape(material)}</span>
                  </div>
                  <div class="py-2.5 flex justify-between items-center">
                    <span class="text-slate-400 font-medium">Tooling / Mold Origin</span>
                    <span class="text-sky-400 font-mono font-semibold text-right max-w-[200px]">{html.escape(mold)}</span>
                  </div>
                  <div class="py-2.5 flex justify-between items-center">
                    <span class="text-slate-400 font-medium">Release Year</span>
                    <span class="text-slate-200 font-mono">{html.escape(release_year)}</span>
                  </div>
                  
                  <div class="pt-4">
                    <span class="block text-slate-400 font-semibold mb-2 uppercase tracking-wider text-[11px]">Real Aircraft Specs</span>
                    <div class="space-y-1.5 text-[11px] text-slate-300 font-mono bg-slate-950 p-3 rounded-lg border border-slate-800">
                      <div><span class="text-slate-500">Powerplant:</span> {html.escape(engine)}</div>
                      <div><span class="text-slate-500">Wingspan:</span> {html.escape(wingspan)}</div>
                      <div><span class="text-slate-500">Length:</span> {html.escape(length)}</div>
                      <div><span class="text-slate-500">Armament:</span> {html.escape(armament)}</div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Sidebar Ad Slot -->
              <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 text-center">
                <span class="text-[10px] text-slate-500 uppercase tracking-widest block mb-2">Sponsor</span>
                <div class="min-h-[250px] bg-slate-950 rounded-xl flex items-center justify-center text-slate-600 text-xs font-mono border border-slate-800/80">
                  [ Google AdSense 300x250 Medium Rectangle ]
                </div>
              </div>
            </div>
          </div>
        </main>
        """
        page_html += get_footer()
        page_html += "</body></html>"
        
        out_file = os.path.join(DIST_DIR, "models", f"{slug}.html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"Built {out_file}")

    # 2. Build Homepage (index.html)
    cards_html = ""
    for fm, _ in models_data:
        slug = fm.get("slug")
        title = fm.get("title")
        brand = fm.get("brand")
        scale = fm.get("scale")
        category = fm.get("category")
        era = fm.get("era")
        tail = fm.get("tail_code")
        main_img = fm.get("featured_image", "")
        mold = fm.get("mold_origin", "")
        
        cards_html += f"""
        <article class="bg-slate-900 border border-slate-800 hover:border-sky-500/80 rounded-2xl overflow-hidden shadow-lg hover:shadow-sky-500/10 transition-all duration-300 flex flex-col group">
          <div class="relative overflow-hidden aspect-[16/10] bg-slate-950">
            <img src="{SITE_URL}/{main_img}" alt="{html.escape(title)}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
            <div class="absolute top-3 left-3 flex gap-1.5">
              <span class="bg-sky-500 text-white font-extrabold text-[11px] px-2.5 py-0.5 rounded-md shadow-md">{html.escape(scale)}</span>
              <span class="bg-slate-900/90 backdrop-blur text-slate-200 font-semibold text-[11px] px-2 py-0.5 rounded-md border border-slate-700">{html.escape(brand)}</span>
            </div>
            <div class="absolute bottom-2.5 right-3 bg-black/70 backdrop-blur text-amber-400 font-mono text-[11px] px-2 py-0.5 rounded font-bold">
              {html.escape(tail)}
            </div>
          </div>
          
          <div class="p-5 flex-1 flex flex-col justify-between">
            <div>
              <div class="text-[11px] font-mono text-slate-400 uppercase tracking-wider mb-1.5 flex items-center justify-between">
                <span>{html.escape(category)}</span>
                <span class="text-slate-500">{html.escape(era.split()[0] if era else '')}</span>
              </div>
              <h3 class="font-bold text-slate-100 text-lg leading-snug group-hover:text-sky-400 transition-colors mb-2">
                <a href="{SITE_URL}/models/{slug}.html">{html.escape(title)}</a>
              </h3>
              <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-4">
                Tooling: <strong class="text-slate-300 font-mono">{html.escape(mold)}</strong>. Deep walkaround photography, panel line inspection, and historical combat provenance.
              </p>
            </div>
            
            <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-sky-400 font-semibold group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
                Explore Wiki Entry &rarr;
              </span>
              <span class="text-slate-500 font-mono text-[11px]">In Stock / Archive</span>
            </div>
          </div>
        </article>
        """

    index_html = get_head(SITE_TITLE, SITE_DESC)
    index_html += get_header()
    index_html += f"""
    <!-- Hero Section -->
    <section class="relative bg-gradient-to-b from-slate-900 to-slate-950 border-b border-slate-800 py-16 sm:py-24 overflow-hidden">
      <div class="absolute inset-0 bg-[radial-gradient(#38bdf8_1px,transparent_1px)] [background-size:24px_24px] opacity-10"></div>
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 text-xs font-mono font-medium mb-6">
          <span class="w-2 h-2 rounded-full bg-sky-400 animate-pulse"></span>
          Authentic Military Aviation & Diecast Database
        </div>
        <h1 class="text-4xl sm:text-6xl font-black text-white tracking-tight leading-tight max-w-4xl mx-auto mb-6">
          The Definitive Scale Aircraft & <span class="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-blue-500">Military Aviation Wiki</span>
        </h1>
        <p class="text-slate-300 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed mb-8">
          Detailed diecast mold analyses, OEM tooling lineage secrets, squadron histories, and museum-grade macro walkarounds for serious collectors worldwide.
        </p>
        
        <div class="flex flex-wrap items-center justify-center gap-4 text-xs font-mono">
          <a href="{SITE_URL}/models/index.html" class="px-6 py-3 rounded-xl bg-sky-500 hover:bg-sky-400 text-white font-bold transition-all shadow-lg shadow-sky-500/25">Browse Database</a>
          <a href="{SITE_URL}/about.html" class="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold border border-slate-700 transition-all">About Our Archive</a>
        </div>
      </div>
    </section>

    {get_adsense_banner()}

    <!-- Main Database Listing -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 w-full flex-1">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
        <div>
          <h2 class="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <span class="w-2.5 h-6 bg-sky-500 rounded-sm"></span>
            Featured Database Entries
          </h2>
          <p class="text-slate-400 text-xs mt-1">Recently documented airframes with verified tooling lineage and real-world combat provenance.</p>
        </div>
        
        <!-- Filter chips -->
        <div class="flex flex-wrap items-center gap-2 text-xs font-mono">
          <span class="px-3 py-1.5 rounded-lg bg-sky-500 text-white font-semibold">All Scales</span>
          <span class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white cursor-pointer">1:72 Military</span>
          <span class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white cursor-pointer">1:200 Heavies</span>
          <span class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white cursor-pointer">1:400 Commercial</span>
        </div>
      </div>

      <!-- Models Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8">
        {cards_html}
      </div>

      <!-- Database Stats Bar -->
      <div class="mt-16 bg-slate-900 border border-slate-800 rounded-2xl p-6 grid grid-cols-2 sm:grid-cols-4 gap-6 text-center">
        <div>
          <div class="text-3xl font-extrabold text-sky-400 font-mono">200+</div>
          <div class="text-xs text-slate-400 mt-1 uppercase tracking-wider">Models in Pipeline</div>
        </div>
        <div>
          <div class="text-3xl font-extrabold text-amber-400 font-mono">1:72 - 1:500</div>
          <div class="text-xs text-slate-400 mt-1 uppercase tracking-wider">Scales Covered</div>
        </div>
        <div>
          <div class="text-3xl font-extrabold text-emerald-400 font-mono">100%</div>
          <div class="text-xs text-slate-400 mt-1 uppercase tracking-wider">Original Macro Photos</div>
        </div>
        <div>
          <div class="text-3xl font-extrabold text-indigo-400 font-mono">Global</div>
          <div class="text-xs text-slate-400 mt-1 uppercase tracking-wider">Military & Civil Coverage</div>
        </div>
      </div>
    </main>
    """
    index_html += get_footer()
    index_html += "</body></html>"
    
    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    with open(os.path.join(DIST_DIR, "models/index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Built index.html and models/index.html")

    # 3. Build AdSense Required Pages: About, Privacy Policy, Terms, Contact
    # About
    about_html = get_head("About Skylogue Archive | Scale Aviation Wiki & Editorial Standards", "The history, collector credentials, and research methodology behind Skylogue Scale Aviation Archive.", canonical=f"{SITE_URL}/about.html")
    about_html += get_header()
    about_html += f"""
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex-1 text-slate-300">
      <div class="mb-8">
        <span class="text-sky-400 font-mono text-xs uppercase tracking-widest block mb-2">Editorial Methodology</span>
        <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">About Skylogue Archive</h1>
      </div>
      
      <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 text-sm leading-relaxed">
        <p>
          <strong>Skylogue Archive</strong> was founded by passionate scale aircraft historians and diecast collectors to bridge the gap between superficial catalog listings and authentic aeronautical analysis.
        </p>
        
        <h2 class="text-xl font-bold text-slate-100 pt-4 border-t border-slate-800">Our Core Pillars</h2>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800">
            <h3 class="font-bold text-sky-400 mb-1">Tooling & Mold Lineage</h3>
            <p class="text-xs text-slate-400">Investigating factory foundries, OEM relationships (such as WLTK and Herpa), and tooling evolutions over decades.</p>
          </div>
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800">
            <h3 class="font-bold text-amber-400 mb-1">Historical Accuracy</h3>
            <p class="text-xs text-slate-400">Verifying bureau numbers, tail registrations, ace pilot markings (like Jan Zumbach's Spitfire), and specific squadron deployments.</p>
          </div>
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800">
            <h3 class="font-bold text-emerald-400 mb-1">Authentic Photography</h3>
            <p class="text-xs text-slate-400">Every single model reviewed is personally inspected in our private studio with high-resolution macro walkaround shots.</p>
          </div>
        </div>
        
        <h2 class="text-xl font-bold text-slate-100 pt-4 border-t border-slate-800">Editorial Independence</h2>
        <p>
          We do not accept paid manufacturer placements to distort model ratings. Deficiencies in tampo alignment, tail fin geometry, or landing gear angle are documented truthfully for the global collector community.
        </p>
      </div>
    </main>
    """
    about_html += get_footer()
    about_html += "</body></html>"
    with open(os.path.join(DIST_DIR, "about.html"), "w", encoding="utf-8") as f:
        f.write(about_html)

    # Privacy Policy
    privacy_html = get_head("Privacy Policy | Skylogue Archive", "Privacy Policy and Cookie Disclosures compliant with GDPR, CCPA, and Google AdSense.", canonical=f"{SITE_URL}/privacy-policy.html")
    privacy_html += get_header()
    privacy_html += f"""
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex-1 text-slate-300">
      <div class="mb-8">
        <span class="text-sky-400 font-mono text-xs uppercase tracking-widest block mb-2">Legal Compliance</span>
        <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">Privacy Policy</h1>
        <p class="text-slate-400 text-xs mt-1">Last Updated: {datetime.datetime.now().strftime('%B %d, %Y')}</p>
      </div>
      
      <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 text-sm leading-relaxed">
        <p>At Skylogue Archive (accessible from {SITE_URL}), one of our main priorities is the privacy of our visitors. This Privacy Policy document outlines the types of information that is collected and recorded by Skylogue Archive and how we use it.</p>
        
        <h2 class="text-lg font-bold text-slate-100 pt-2">Log Files</h2>
        <p>Skylogue Archive follows a standard procedure of using log files. These files log visitors when they visit websites. The information collected by log files includes internet protocol (IP) addresses, browser type, Internet Service Provider (ISP), date and time stamp, referring/exit pages, and possibly the number of clicks. These are not linked to any information that is personally identifiable.</p>
        
        <h2 class="text-lg font-bold text-slate-100 pt-2">Cookies and Web Beacons</h2>
        <p>Like any other website, Skylogue Archive uses 'cookies'. These cookies are used to store information including visitors' preferences, and the pages on the website that the visitor accessed or visited. The information is used to optimize the users' experience by customizing our web page content based on visitors' browser type and/or other information.</p>
        
        <h2 class="text-lg font-bold text-slate-100 pt-2">Google DoubleClick DART Cookie</h2>
        <p>Google is one of a third-party vendor on our site. It also uses cookies, known as DART cookies, to serve ads to our site visitors based upon their visit to our site and other sites on the internet. However, visitors may choose to decline the use of DART cookies by visiting the Google ad and content network Privacy Policy at the following URL: <a href="https://policies.google.com/technologies/ads" target="_blank" class="text-sky-400 underline">https://policies.google.com/technologies/ads</a>.</p>
        
        <h2 class="text-lg font-bold text-slate-100 pt-2">Our Advertising Partners</h2>
        <p>Some of advertisers on our site may use cookies and web beacons. Our advertising partners include <strong>Google AdSense</strong>. Third-party ad servers or ad networks use technologies like cookies, JavaScript, or Web Beacons that are used in their respective advertisements and links that appear on Skylogue Archive, which are sent directly to users' browser.</p>
      </div>
    </main>
    """
    privacy_html += get_footer()
    privacy_html += "</body></html>"
    with open(os.path.join(DIST_DIR, "privacy-policy.html"), "w", encoding="utf-8") as f:
        f.write(privacy_html)

    # Terms of Service
    terms_html = get_head("Terms of Service | Skylogue Archive", "Terms of Service and Content Usage Agreement for Skylogue Archive.", canonical=f"{SITE_URL}/terms.html")
    terms_html += get_header()
    terms_html += f"""
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex-1 text-slate-300">
      <div class="mb-8">
        <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">Terms of Service</h1>
      </div>
      <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-4 text-sm leading-relaxed">
        <p>By accessing this website, you are agreeing to be bound by these website Terms and Conditions of Use, all applicable laws and regulations, and agree that you are responsible for compliance with any applicable local laws.</p>
        <p>All photography, mold analysis articles, and historical compilations are property of Skylogue Archive and may not be reproduced without explicit attribution and backlink.</p>
      </div>
    </main>
    """
    terms_html += get_footer()
    terms_html += "</body></html>"
    with open(os.path.join(DIST_DIR, "terms.html"), "w", encoding="utf-8") as f:
        f.write(terms_html)

    # Contact
    contact_html = get_head("Contact Skylogue Archive", "Inquiries, model review submissions, and corrections.", canonical=f"{SITE_URL}/contact.html")
    contact_html += get_header()
    contact_html += f"""
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex-1 text-slate-300">
      <div class="mb-8">
        <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">Contact & Model Submissions</h1>
        <p class="text-slate-400 text-sm mt-1">Have a rare diecast model you'd like our curators to document or a tooling correction to report?</p>
      </div>
      <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-4 text-sm leading-relaxed">
        <p>Email our archival desk directly at: <strong class="text-sky-400 font-mono">contact@skylogue.org</strong> (or via GitHub issues on our official repository).</p>
        <p>We welcome submissions of high-resolution photos, mold comparison insights, and historical serial verification from aviation enthusiasts worldwide.</p>
      </div>
    </main>
    """
    contact_html += get_footer()
    contact_html += "</body></html>"
    with open(os.path.join(DIST_DIR, "contact.html"), "w", encoding="utf-8") as f:
        f.write(contact_html)

    # 4. Generate robots.txt, sitemap.xml, ads.txt
    with open(os.path.join(DIST_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
        
    with open(os.path.join(DIST_DIR, "ads.txt"), "w", encoding="utf-8") as f:
        f.write("# Google AdSense ads.txt for Skylogue Archive\n# Replace ca-pub-XXXXXXXXXXXXXXXX with your AdSense Publisher ID upon approval\ngoogle.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0\n")

    # sitemap.xml
    now_iso = datetime.datetime.now().strftime('%Y-%m-%d')
    sitemap_entries = [
        f"<url><loc>{SITE_URL}/index.html</loc><lastmod>{now_iso}</lastmod><priority>1.0</priority></url>",
        f"<url><loc>{SITE_URL}/models/index.html</loc><lastmod>{now_iso}</lastmod><priority>0.9</priority></url>",
        f"<url><loc>{SITE_URL}/about.html</loc><lastmod>{now_iso}</lastmod><priority>0.7</priority></url>",
        f"<url><loc>{SITE_URL}/privacy-policy.html</loc><lastmod>{now_iso}</lastmod><priority>0.5</priority></url>",
        f"<url><loc>{SITE_URL}/contact.html</loc><lastmod>{now_iso}</lastmod><priority>0.5</priority></url>",
    ]
    for fm, _ in models_data:
        slug = fm.get("slug")
        sitemap_entries.append(f"<url><loc>{SITE_URL}/models/{slug}.html</loc><lastmod>{now_iso}</lastmod><priority>0.8</priority></url>")
        
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_entries)}
</urlset>"""
    with open(os.path.join(DIST_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
        
    print("Generated robots.txt, ads.txt, sitemap.xml successfully!")

if __name__ == "__main__":
    build_site()
