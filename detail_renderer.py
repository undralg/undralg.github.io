from pathlib import Path
from html import escape as E
import subprocess
from project_details import DETAILS

def render_markdown_detail(p, d, tags):
 source = (Path(__file__).parent / d['markdown_source']).read_text()
 title, subtitle, article = source.strip().split('\n\n', 2)
 title = title.removeprefix('# ')
 subtitle = subtitle.strip('*')
 article_html = subprocess.run(
  ['pandoc', '--from=markdown', '--to=html5', '--section-divs', '--wrap=none'],
  input=article, text=True, capture_output=True, check=True,
 ).stdout
 article_html = article_html.replace('id="abstract" class="level2"', 'id="abstract" class="level2 abstract"', 1)
 article_html = article_html.replace('<table>', '<div class="table-scroll"><table>').replace('</table>', '</table></div>')
 source_links = ''.join(f'<p><a href="{E(url)}">{E(label)}</a></p>' for label, url in d.get('source_links', []))
 return f'<section class="hero"><a class="back" href="../#projects">All projects</a><p class="eyebrow">{E(" / ".join(p["category"]))}</p><h1>{E(title)}</h1><p class="lead">{E(subtitle)}</p>{tags(p)}</section><article class="case-study">{article_html}<section class="source-section"><h2>Original report</h2>{source_links}</section></article>'

def render_detail(p,tags,deck=''):
 d=DETAILS[p['slug']]; slug=p['slug']
 if 'markdown_source' in d:
  return render_markdown_detail(p, d, tags)
 links=list(p['links'])
 if slug in ['bayesian-housing','social-networks','multilevel-scores','movie-preferences']:
  links.insert(0,('Read full analysis','analysis.html'))
 actions=''.join(f'<a class="button{(" secondary" if i else "")}" href="{E(u)}">{E(l)}</a>' for i,(l,u) in enumerate(links))
 body=f'<section class="hero"><a class="back" href="../#projects">All projects</a><p class="eyebrow">{E(p.get("company") or " / ".join(p["category"]))}</p><h1>{E(p["title"])}</h1><p class="lead">{E(p["question"])}</p><p class="role">{E(p["role"])}</p>{tags(p)}<div class="actions">{actions}</div></section><article class="case-study"><section class="abstract"><h2>Abstract</h2><p>{E(d["abstract"])}</p></section>'
 for i,(title,text) in enumerate(d['sections']):
  body+=f'<section><h2>{E(title)}</h2><p>{E(text)}</p></section>'
  if i==d.get('evidence_after',0):
   if 'video' in d:
    name,title,caption=d['video']
    body+=f'<figure class="simulation-video"><h3>{E(title)}</h3><video controls loop muted playsinline preload="none" poster="../assets/videos/{name}-poster.png" style="width:100%;height:auto"><source src="../assets/videos/{name}.mp4" type="video/mp4"><a href="../assets/videos/{name}.mp4">Download animation</a></video><figcaption>{E(caption)} Use the playback controls to pause or replay.</figcaption></figure>'
   if 'figure' in d:
    src,alt,caption=d['figure'];body+=f'<figure><img class="project-image" src="{E(src)}" alt="{E(alt)}" loading="lazy"><figcaption>{E(caption)}</figcaption></figure>'
   if 'bars' in d:
    title,rows=d['bars'];mx=max(v for _,v in rows)
    body+=f'<figure class="evidence"><h3>{E(title)}</h3>'
    for name,v in rows:
     body+=f'<div class="barrow"><div class="barlabel"><span>{E(name)}</span><strong>{format(v,d.get("bar_format",",.2f"))}</strong></div><div class="bar" style="width:{v/mx*100:.2f}%"></div></div>'
    body+='<figcaption>'+E(d.get('bar_note','Source: linked case report and model. Historical scenario estimates; bars start at zero.'))+'</figcaption></figure>'
   if 'rows' in d:
    body+='<div class="table-scroll"><table><thead><tr>'+''.join(f'<th scope="col">{E(t)}</th>' for t in d['headers'])+'</tr></thead><tbody>'
    body+=''.join('<tr>'+''.join(f'<td>{E(t)}</td>' for t in row)+'</tr>' for row in d['rows'])+'</tbody></table></div>'
    body+=f'<p class="role">{E(d.get("table_note","Source: original project materials linked below."))}</p>'
 if deck:body+=deck
 body+='<section class="source-section"><h2>'+('Sources and scope' if 'source_note' in d else 'Explore the work')+'</h2><p>'+E(d.get('source_note','The original materials retain the calculations, assumptions, and supporting discussion behind this overview.'))+'</p><div class="actions">'+actions+'</div>'
 for label,url in d.get('source_links',[]):
  body+=f'<p><a href="{E(url)}">{E(label)}</a></p>'
 if slug in ['bayesian-housing','social-networks','multilevel-scores','movie-preferences']:
  body+='<p class="role">The readable analysis preserves existing notebook content with code and long output collapsed. Models were not rerun for this presentation; interpretation notes appear at the top of each preview.</p>'
 body+='</section></article>'
 return body
