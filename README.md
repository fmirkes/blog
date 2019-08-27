# fmirkes/blog
This repo contains all files to generate my blog [fmirkes.github.io](https://fmirkes.github.io).

The site itself, and the atom feed are templated with Jinja2. Articles are saved as markdown under ```articles/{date} - {title}.md```.

The script ```generate_blog.py``` puts everything together and outputs the website to the folder ```fmirkes.github.io/```.

Everything is pretty much tailored to my needs, but it should be easily adaptable (just some links and titles are hardcoded).
