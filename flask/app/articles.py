from flask import render_template
from templates import *

def get_author_data(author: str):
    import json

    with open("/blog/data/authors.json") as f:
        data = json.load(f)
        if author in data:
            return data[author]
        else:
            return None

def render_author_big(author: str):
    data = get_author_data(author)
    return render_template(
        f"authors/author_big.html",
        portrait_file= data['portrait-file'],
        portrait_alt= data['portrait-alt'],
        link= data['link'],
        name= data['display_name'],
        github= data['github']
    )

def render_author_small(author: str):
    data = get_author_data(author)
    return render_template(
        f"authors/author_small.html",
        portrait_file= data['portrait-file'],
        portrait_alt= data['portrait-alt'],
        link= data['link'],
        name= data['nickname']
    )

def render_article_date(metadata):
    import time

    return "" if metadata['date'] is None else time.strftime("%b %d, %Y", metadata['date'])

def render_article_preview(metadata):
    authors = ''.join([ render_author_small(a) for a in metadata['authors'] ])
    return render_template(
        "articles/preview.html",
        title = metadata['title'],
        subtitle = metadata['subtitle'],
        authors = authors,
        date = render_article_date(metadata),
        other_lang = 'en' in metadata,
        page = f"./articles/{metadata['page']}",
    )

def __parse_article_date(date: str):
    import time
    time_format = "%Y-%m-%d"

    try:
        if date is None or date == "":
            return None
        else:
            return time.strptime(date, time_format)
    except:
        return None

def __parse_article_metadata(article, data):
    data['page'] = article
    data['date'] = __parse_article_date(data['date'])
    if 'content-type' not in data:
        data['content-type'] = 'html'
    if 'hidden' not in data:
        data['hidden'] = False

    return data

def get_article_metadata(article: str):
    import json
    with open("/blog/data/articles.json") as f:
        data = json.load(f)
        if article in data:
            return __parse_article_metadata(article, data[article])
        else:
            return None

def get_articles_metadata():
    import json
    with open("/blog/data/articles.json") as f:
        data = json.load(f)
        return [ __parse_article_metadata(article, data) for article, data in data.items() ]

def render_article(article: str, skip_hidden = True, lang = None):
    import time

    metadata = get_article_metadata(article)
    main_lang = lang is None or lang == 'it' or 'en' not in metadata   
    other_lang = None if 'en' not in metadata else ('en' if main_lang else 'it')

    if skip_hidden and metadata['hidden']:
        return None

    authors = ''.join([ render_author_big(a) for a in metadata['authors'] ])
    header = render_template(
        "articles/header.html",
        title = metadata['title'] if main_lang else metadata['en']['title'],
        subtitle = metadata['subtitle'] if main_lang else metadata['en']['subtitle'],
        authors = authors,
        other_lang = other_lang,
        date = render_article_date(metadata),
    )
    
    page = None
    content = metadata['content'] if main_lang else metadata['en']['content'] 
    contenttype = metadata['content-type'] if main_lang else metadata['en']['content-type']
    if contenttype == 'html':
        page = render_template(
            f"root/{content}",
            header = header
        )
    elif contenttype == 'markdown':
        import markdown
        from md_extensions import TailwindExtension

        with open(f"/blog/{content}", 'r') as f:
            page = markdown.markdown(
                f.read(),
                extensions=['extra', TailwindExtension()]
            )

        page = render_template(
            "articles/markdown_skeleton.html",
            header = header,
            markdown = page
        )

    if page is None:
        return None
    
    return {
        'article' : page,
        'metadata': metadata
    }

def render_articles_previews():
    import time

    metadata = get_articles_metadata()
    metadata = sorted(
        filter(lambda elem: not elem['hidden'], metadata),
        key= lambda elem: elem['date'] if elem['date'] is not None else time.gmtime(0),
        reverse= True
    )

    return [ render_article_preview(md) for md in metadata ]