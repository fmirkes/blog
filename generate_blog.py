#!/usr/bin/env python3

import os
import markdown
import shutil

from datetime import datetime
from distutils import dir_util
from jinja2 import Environment, FileSystemLoader

output_dir = "fmirkes.github.io"

articles_dir = "articles"
favicon_dir = "favicon"
static_dir = "static"

templates_dir = "templates"

markdown_extensions = ['markdown.extensions.fenced_code', 'markdown.extensions.codehilite']

if __name__ == "__main__":
    jinja_env = Environment(loader=FileSystemLoader(templates_dir), keep_trailing_newline=True)

    if os.path.exists(output_dir):
        for dirpath, dirnames, filenames in os.walk(output_dir):
            for folder in dirnames:
                shutil.rmtree("{}/{}".format(dirpath, folder))
            
            for file in filenames:
                os.remove("{}/{}".format(dirpath, file))
    else:
        os.mkdir(output_dir)
    
    os.mkdir("{}/{}".format(output_dir, articles_dir))

    article_files = os.listdir(articles_dir)
    article_files.reverse()

    articles_all = {}
    for article in article_files:
        article_name_split = article.split("-", 1)
        
        article_date_str = article_name_split[0].strip()
        article_title = article_name_split[1].strip()[:-3]
        
        article_link = "{}/{}.html".format(articles_dir, article_date_str)

        article_file = open("{}/{}".format(articles_dir, article), "r")
        article_html = markdown.markdown(article_file.read(), extensions=markdown_extensions)
        article_file.close()

        article_date = datetime.strptime(article_date_str, "%Y%m%d")
        article_year = article_date.year

        article_list_entry = {
            "title": article_title,
            "link": article_link,
            "updated": article_date.isoformat(),
            "content": article_html
        }
        
        if article_year in articles_all:
            articles_all[article_year].append(article_list_entry)
        else:
            articles_all[article_year] = [article_list_entry]

        article_site_template = jinja_env.get_template("article.html.j2")
        article_site_html = article_site_template.render(
            title=article_title, article=article_html, show_back_button=True)

        article_file = open("{}/{}".format(output_dir, article_link), "w")
        article_file.writelines(article_site_html)
        article_file.close()

    index_template = jinja_env.get_template("index.html.j2")
    index_html = index_template.render(articles=articles_all)

    index_file = open("{}/index.html".format(output_dir), "w")
    index_file.writelines(index_html)
    index_file.close()

    atom_template = jinja_env.get_template("atom.xml.j2")
    atom_xml = atom_template.render(articles=articles_all)

    atom_file = open("{}/atom.xml".format(output_dir), "w")
    atom_file.writelines(atom_xml)
    atom_file.close()

    shutil.copytree(static_dir, "{}/{}".format(output_dir, static_dir))
    dir_util.copy_tree(favicon_dir, "{}/".format(output_dir))
