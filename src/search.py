__author__ = 'umutcan'
import logging
import sys

try:
    import argparse
    from elasticsearch import Elasticsearch, exceptions
except ImportError, e:
    logging.error("Module missing: %r" % e)
    sys.exit(1)


def search(keyword, index, doc_type, page, limit):
    keyword_lcase = keyword.lower()
    body = {
        "query": {
            "filtered": {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "prefix": {
                                    "revision.text": {"value": keyword_lcase}
                                }
                            },
                            {
                                "prefix": {
                                    "revision.contributor.username": {"value": keyword_lcase, "boost": 2.0}
                                }
                            }
                        ]
                    }
                },
                "filter": {
                    "bool": {
                        "must": [
                            {
                                "terms": {
                                    "_type": [
                                        "pages"
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }
    }
    try:
        es = Elasticsearch(
            hosts="localhost"
        )
        from_ = (page - 1) * limit
        result = es.search(
            index=index,
            doc_type=doc_type,
            body=body,
            size=limit,
            from_=from_
        )

        # print "%s result found."
        print "==%s-%s of %s Results ==" % (str(from_), str(from_ + limit), result["hits"]["total"])

        for page in result["hits"]["hits"]:
            print unicode(page["_source"]["title"])
    except exceptions.ElasticsearchException, e:
        logging.error(e)


if __name__ == '__main__':
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', default='pages', help="Document type for search. Optional. Default is pages")
    parser.add_argument('-i', '--index', default='wiki', help="Index for search. Optional. Default is wiki")
    parser.add_argument('-p', '--page', type=int, default=1, help="Page number. Optional. Default is 1")
    parser.add_argument('-l', '--limit', type=int, default=20, help="Item limit for a page. Optional. Default is 20")
    parser.add_argument('-k', '--keyword', help="keyword for search. It is mandatory")
    args = parser.parse_args()

    if args.keyword is None:
        parser.print_help()
    else:
        keyword = args.keyword
        index = args.index
        doc_type = args.type
        page = args.page
        limit = args.limit
        search(keyword, index, doc_type, page, limit)
