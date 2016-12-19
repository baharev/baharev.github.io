#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import namedtuple
from glob import glob
from os import mkdir
from os.path import basename, splitext
from shutil import copy, rmtree, copytree
from string import Formatter

from markdown import markdown

OUT_DIR = '/tmp/output/'
IN_DIR = '/tmp/input/'


def main():
    clean(OUT_DIR)
    tales_by_lang = get_tales_by_lang()
    write_index_links(tales_by_lang) # Warning: writes into the input directory!
    #
    site_template = get_as_str(IN_DIR + 'site.html')
    # menu pages: index, authors, contact; translations: Märchen, Autoren, ...
    menu_pages, lang_menutitles = get_menu_content(IN_DIR + 'menu.txt')
    for lang, menu_titles in lang_menutitles.items():
        write_site(lang, site_template, menu_pages, menu_titles, tales_by_lang[lang])

#-------------------------------------------------------------------------------

Tale = namedtuple('Tale', 'src  lang  title  ascii')

def get_tales_by_lang():
    sources = sorted(f for f in glob(IN_DIR + 'tales/''*_??.md'))
    #print('Tale source files with path:', sources)
    fnames = [get_filename_wo_extension(src) for src in sources]
    #print('Tale file names:', fnames)
    # fname: '002_de' -> lang: 'de'
    languages = [fname.split('_')[1] for fname in fnames]
    #print('Languages:', languages)
    titles = [get_tale_title(src) for src in sources]
    #print('Tale titles:', titles)
    ascii_name = [fname+'_'+to_ascii(title) for fname, title in zip(fnames, titles)]
    #print('Tale ASCII filenames:', ascii_name)
    # Group tales by language
    tales_by_lang = {lang: [] for lang in languages}
    for t in zip(sources, languages, titles, ascii_name):
        tale = Tale(*t)
        tales_by_lang[tale.lang].append(tale)
    return tales_by_lang  

def get_filename_wo_extension(filepath):
    return splitext(basename(filepath))[0]

def get_tale_title(filepath):
    first_line = get_first_line(filepath)
    return first_line.split(' ', 1)[1].strip() # chop off leading '# ' 

def to_ascii(string):
    table = str.maketrans('áéíóöőúüűä ', 'aeiooouuua_')
    return string.lower().replace('ß', 'ss').translate(table)

#-------------------------------------------------------------------------------

def write_index_links(tales_by_lang):
    link = get_as_str(IN_DIR + 'link_templates/tale_link.html')
    for lang, tales in tales_by_lang.items():
        fname = IN_DIR + 'index/index_' + lang + '.md'
        content = [get_first_line(fname)] # Save the page heading
        content.extend(link.format(page=tale.ascii+'.html', title=tale.title)
                       for tale in tales)
        content.append('\n')
        write(fname, '\n'.join(content))  

def write_site(lang, site_template, menu_pages, menu_titles, tales):
    print('Language:', lang)
    mkdir(OUT_DIR + lang)
    menu_links = menu_links_html(menu_pages, menu_titles)
    write_pages(site_template, lang, menu_links, menu_pages, menu_titles)
    write_tales(site_template, lang, menu_links, tales)
    copy(IN_DIR + 'style.css', OUT_DIR + lang + '/')
    copy(IN_DIR + 'images/icon.ico', OUT_DIR + lang + '/')
    copytree(IN_DIR + 'js/', OUT_DIR + lang + '/js/')
    copytree(IN_DIR + 'images/', OUT_DIR + lang + '/images/')
    print('---------------------------------------------------------------')

def write_tales(site_template, lang, menu_links, tales):
    for tale in tales:
        print('Tale:', tale.ascii)
        content = md_to_html(get_as_str(tale.src))
        page_html = site_template.format(title=tale.title, page_content=content, 
                                         menu_links=menu_links)
        write(OUT_DIR + lang + '/' + tale.ascii + '.html', page_html)

def write_pages(site_template, lang, menu_links, menu_pages, menu_titles):
    for page, title in zip(menu_pages, menu_titles):
        print('Page:', page)
        content = md_to_html(get_as_str(IN_DIR+page+'/'+page+'_'+lang+'.md'))
        page_html = site_template.format(title=title, page_content=content, 
                                         menu_links=menu_links)
        write(OUT_DIR + lang + '/' + page + '.html', page_html)

def menu_links_html(menu_pages, menu_titles):
    templ = get_as_str(IN_DIR + 'link_templates/menu_link.html')
    links = [templ.format(page=p, title=t) for p, t in zip(menu_pages, menu_titles)]
    return '\n'.join(links)

def get_menu_content(filename):
    lines = get_lines(filename)
    # The first line gives the pages in the menu: index, authors, contact, ... 
    menu_pages = lines[0].split('\t')[1:]  # [1:] to discard '' due to leading tab
    # The next lines give the titles: contact is Contact in English, etc.
    lang_titles = {} # 'en': ['Tales', 'Authors', 'Contact']
    for line in lines[1:]:
        lang, titles = line.split('\t', 1)
        lang_titles[lang] = titles.split('\t')
    print('Pages in menu:', ', '.join(menu_pages))
    print('Translations: ', lang_titles)
    return menu_pages, lang_titles

def get_arguments(template):
    # tup: (literal_text, argument_name, format_spec, conversion)
    arguments = set(tup[1] for tup in Formatter().parse(template) if tup[1])
    return sorted(arguments)    

#-------------------------------------------------------------------------------

def md_to_html(md_text):
    return markdown(md_text, output_format='html5', 
                    extensions=['markdown.extensions.attr_list'])

def write(filepath, content):
    check_bom(content, filepath)
    with open(filepath, 'w') as f:
        f.write(content)

def get_first_line(filepath):
    with open(filepath, 'r') as f:
        first_line = next(f)
        check_bom(first_line, filepath)
        return first_line

def get_lines(filepath):
    return get_as_str(filepath).splitlines()    

def get_as_str(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        check_bom(content, filepath)
        return content

def check_bom(str_to_check, msg):
    assert '\uFEFF' not in str_to_check, 'BOM found: ' + msg

def clean(directory):
    rmtree(directory, ignore_errors=True)
    mkdir(directory)

if __name__ == '__main__':
    main()
