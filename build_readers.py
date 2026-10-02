from pathlib import Path
import json,html,base64,re,subprocess,shutil,hashlib
P=Path(__file__).resolve().parent; E=html.escape
specs={
'predator-prey':('predator-prey-simulation/simulation.ipynb','Saved implementation and outputs. This is a synthetic spatial density model; models have not been rerun. The linked report contains the narrative and derivations.'),
'airport-security':('airport-security-simulation/analysis.ipynb','Saved team course notebook and simulation outputs, not observed airport data. Models have not been rerun. See the linked report for assumptions and recommendations.'),
'bayesian-housing':('BA Real Estate/bayesian_regression_real_estate_BA_code.ipynb','Saved course analysis; models have not been rerun. PSIS-LOO warnings for influential observations limit the strength of the model ranking.'),
'social-networks':('male-loneliness-epidemic-simulation/CS166_final_codebook.ipynb','All outcomes are simulations under specified assumptions, not measured effects in a population. Models have not been rerun.'),
'multilevel-scores':('Discrete and multi-level models.ipynb','Saved course analysis; models have not been rerun. Reading correction: 1500 × sigmoid(mu) is the logit-normal median, not its arithmetic mean. Interpret the original “effective mean” labels accordingly.'),
'movie-preferences':('multimodal-movie-preference-modeling/analysis.ipynb','This is the sanitized, output-free public notebook. The revised fold-local evaluation has not been rerun; historical classifier scores are not validated performance estimates.')}
style='body{max-width:1000px;margin:auto;padding:28px;font:18px/1.65 system-ui;color:#172b33}h1,h2{font-family:Georgia}a{color:#087d89}img{max-width:100%;height:auto;display:block;margin:25px auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px;max-height:450px;overflow:auto;background:#f2f5f6;padding:16px}details{margin:12px 0;border:1px solid #dbe3e6;padding:12px}summary{cursor:pointer}.note{background:#edf5f6;padding:20px;border-left:4px solid #087d89}table{display:block;overflow:auto;border-collapse:collapse}td,th{padding:8px;border-bottom:1px solid #ddd}'
for slug,(src,note) in specs.items():
 d=P/slug;a=d/'figures';a.mkdir(exist_ok=True);n=json.loads((P.parent/src).read_text());parts=[]
 inline_count=0
 for i,c in enumerate(n['cells']):
  s=''.join(c['source'])
  if c['cell_type']=='markdown':
   for name,values in c.get('attachments',{}).items():
    for mime,value in values.items():
     if mime in ['image/png','image/jpeg']:
      fn=f'attachment-{i}-{hashlib.sha256(name.encode()).hexdigest()[:8]}.'+('png' if mime.endswith('png') else 'jpg');(a/fn).write_bytes(base64.b64decode(''.join(value)));s=s.replace('attachment:'+name,'figures/'+fn)
   def extract(m):
    fn=f'inline-{i}.png';(a/fn).write_bytes(base64.b64decode(m[1]));return 'figures/'+fn
   s=re.sub(r'data:image/png;base64,([A-Za-z0-9+/=\s]+)(?=["\)])',extract,s)
   parts.append(subprocess.run(['pandoc','-f','markdown','-t','html','--mathml'],input=s,text=True,capture_output=True,check=True).stdout)
  else:
   parts.append(f'<details><summary>Show code · cell {i+1}</summary><pre><code>{E(s)}</code></pre></details>')
   for j,o in enumerate(c.get('outputs',[])):
    data=o.get('data',{})
    if 'image/png' in data:
     fn=f'cell-{i}-{j}.png';(a/fn).write_bytes(base64.b64decode(''.join(data['image/png'])));parts.append(f'<img src="figures/{fn}" alt="Saved figure from cell {i+1}" loading="lazy">')
    else:
     txt=''.join(o.get('text',data.get('text/plain',[])))
     if txt:
      if len(txt)>12000:txt=txt[:12000]+'\n[Long output truncated in this preview; see original notebook.]'
      parts.append(f'<details><summary>Saved output · cell {i+1}</summary><pre>{E(txt)}</pre></details>')
 if slug in ['predator-prey','social-networks']:
  media='predator-prey' if slug=='predator-prey' else 'social-network'
  caption='Local bunny and fox densities over simulation time.' if slug=='predator-prey' else 'Illustrative friendship network: color shows ideological drift, and edges show ties.'
  parts.insert(0,f'<figure><video controls loop muted playsinline preload="none" poster="../assets/videos/{media}-poster.png" style="width:100%;height:auto"><source src="../assets/videos/{media}.mp4" type="video/mp4"></video><figcaption>{caption} Synthetic simulation; use controls to play or pause.</figcaption></figure>')
 title=slug.replace('-',' ').title()
 (d/'analysis.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · Full analysis</title><style>{style}</style></head><body><a href="./">← Project overview</a><h1>{title}: full analysis</h1><aside class="note">{E(note)}</aside>'+''.join(parts)+'</body></html>')
 print(slug,len(parts),'reader sections')
for name in ['metadata-pca.png','poster-pca.png']:
 shutil.copyfile(P.parent/'multimodal-movie-preference-modeling/assets'/name,P/'movie-preferences/figures'/name)
