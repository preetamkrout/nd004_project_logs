#! /usr/bin/env python3


# Project to get the logs from DB with SQL
# Answers following questions:
# 1. What are the most popular three articles of all time?
# 2. Who are the most popular article authors of all time?
# 3. On which days did more than 1% of requests lead to errors?

import psycopg2


def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Unable to connect to DB")


def print_output(out_list, count_unit=" views", quotes=""):
    for out_obj in out_list:
        print("{quotes}{out_obj[0]}{quotes} -- "
              "{out_obj[1]}{count_unit}".format(out_obj=out_obj,
                                                 count_unit=count_unit,
                                                 quotes=quotes))


def print_popular_articles(cursor):
    query = "select a.title, a.article_views " \
            "from popular_articles as a limit 3;"
    cursor.execute(query)

    most_popular_articles = cursor.fetchall()
    print("Most popular three articles of all time:")
    print_output(most_popular_articles, " views", "\"")


def print_popular_authors(cursor):
    query = "select b.name, sum(a.article_views) as author_views " \
            "from popular_articles as a, authors as b " \
            "where a.author = b.id group by b.name order by author_views desc;"
    cursor.execute(query)

    most_popular_authors = cursor.fetchall()
    print("\nMost popular article authors of all time:")
    print_output(most_popular_authors)


def print_high_errors(cursor):
    query = "select " \
            "trim(regexp_replace(to_char(er.req_date, 'Month DD, YYYY')," \
            " '\s+', ' ', 'g')), " \
            "round(((round(er.reqs, 2)/round(all_view.reqs, 2))*100), 2) " \
            "as err_pers " \
            "from error_log as er, all_log as all_view " \
            "where er.req_date = all_view.req_date and round(((round(" \
            "er.reqs, 2)/round(all_view.reqs, 2))*100), 2) > round(1, 2);"
    cursor.execute(query)

    error_days = cursor.fetchall()
    print("\nWhich days did more than 1% of requests lead to errors?")
    print_output(error_days, "% errors")


def execute_report():
    db, cursor = connect()
    print_popular_articles(cursor)
    print_popular_authors(cursor)
    print_high_errors(cursor)
    db.close()

execute_report()
