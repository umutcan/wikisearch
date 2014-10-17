wikisearch
==========

A search tool for indexed (Elasticsearch) local dump of Wikipedia


## Requirements 

Requirements are given in requirements.txt. You can easily install with ``pip``:

        pip install -r requirements.txt
        
## Using tool

This tool connects to a local Elasticsearch instance. It runs prefix query and retrives  titles of reletad pages.
Pages are sorted based ``_score`` field. 
 
A basic example for searching articles related to word "istanbul":

        python search.py -s istanbul
        
Default index name is "wiki" and type name is "pages". You can change this by providing related options:

        python search.py -s istanbul -i test_index -t test_pages
        

You can us ``-page`` and ``-limit`` options in order to browse the results. They have also short cut: ``-p`` and ``-t``
There will be thousands of pages in most of the searches. So, pagination sounds like a good idea. 

        python search.py -s istanbul -p 2 -l 50