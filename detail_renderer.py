from pathlib import Path
from html import escape as E
from project_details import DETAILS

def render_detail(p,tags,deck=''):
 d=DETAILS[p['slug']]; slug=p['slug']
 links=list(p['links'])
 if slug in ['bayesian-housing','social-networks','multilevel-scores','movie-preferences']:
  links.insert(0,('Read full analysis','analysis.html'))
 actions=''.join(f'<a class="button{(" secondary" if i else "")}" href="{E(u)}">{E(l)}</a>' for i,(l,u) in enumerate(links))
 body=f'<section class="hero"><a class="back" href="../#projects">All projects</a><p class="eyebrow">{E(p.get("company") or " / ".join(p["category"]))}</p><h1>{E(p["title"])}</h1><p class="lead">{E(p["question"])}</p><p class="role">{E(p["role"])}</p>{tags(p)}<div class="actions">{actions}</div></section><article class="case-study"><section class="abstract"><h2>Abstract</h2><p>{E(d["abstract"])}</p></section>'
 for i,(title,text) in enumerate(d['sections']):
  body+=f'<section><h2>{E(title)}</h2><p>{E(text)}</p></section>'
  if i==0:
   if 'video' in d:
    name,title,caption=d['video']
    body+=f'<figure class="simulation-video"><h3>{E(title)}</h3><video controls loop muted playsinline preload="none" poster="../assets/videos/{name}-poster.png" style="width:100%;height:auto"><source src="../assets/videos/{name}.mp4" type="video/mp4"><a href="../assets/videos/{name}.mp4">Download animation</a></video><figcaption>{E(caption)} Use the playback controls to pause or replay.</figcaption></figure>'
   if 'figure' in d:
    src,alt,caption=d['figure'];body+=f'<figure><img class="project-image" src="{E(src)}" alt="{E(alt)}" loading="lazy"><figcaption>{E(caption)}</figcaption></figure>'
   if 'bars' in d:
    title,rows=d['bars'];mx=max(v for _,v in rows)
    body+=f'<figure class="evidence"><h3>{E(title)}</h3>'
    for name,v in rows:
     body+=f'<div class="barrow"><div class="barlabel"><span>{E(name)}</span><strong>{v:,.2f}</strong></div><div class="bar" style="width:{v/mx*100:.2f}%"></div></div>'
    body+='<figcaption>Source: linked case report and model. Historical scenario estimates; bars start at zero.</figcaption></figure>'
   if 'rows' in d:
    body+='<div class="table-scroll"><table><thead><tr>'+''.join(f'<th scope="col">{E(t)}</th>' for t in d['headers'])+'</tr></thead><tbody>'
    body+=''.join('<tr>'+''.join(f'<td>{E(t)}</td>' for t in row)+'</tr>' for row in d['rows'])+'</tbody></table></div>'
    body+=f'<p class="role">{E(d.get("table_note","Source: original project materials linked below."))}</p>'
 if deck:body+=deck
 body+='<section class="source-section"><h2>Explore the work</h2><p>The original materials retain the calculations, assumptions, and supporting discussion behind this overview.</p><div class="actions">'+actions+'</div>'
 if slug in ['bayesian-housing','social-networks','multilevel-scores','movie-preferences']:
  body+='<p class="role">The readable analysis preserves existing notebook content with code and long output collapsed. Models were not rerun for this presentation; interpretation notes appear at the top of each preview.</p>'
 body+='</section></article>'
 return body
