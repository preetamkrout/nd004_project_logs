# Project to get the logs from DB with SQL
# Answers following questions:
# 1. What are the most popular three articles of all time?
# 2. Who are the most popular article authors of all time?
# 3. On which days did more than 1% of requests lead to errors?

import psycopg2

db = psycopg2.connect("dbname=news")

c = db.cursor()
c.execute("select a.title, a.article_views "
          "from popular_articles as a limit 3;")
most_popular_articles = c.fetchall()
print("Most popular three articles of all time:")
for popular_article in most_popular_articles:
    print("\"{article[0]}\" -- "
          "{article[1]} views".format(article=popular_article))

c.execute("select b.name, sum(a.article_views) as author_views"
          " from popular_articles as a, authors as b"
          " where a.author = b.id group by b.name order by author_views desc;")
most_popular_authors = c.fetchall()
print("\nMost popular article authors of all time:")
for popular_author in most_popular_authors:
    print("{author[0]} -- {author[1]} views".format(author=popular_author))

c.execute("select "
          "trim(regexp_replace(to_char(er.req_date, 'Month DD, YYYY'),"
          " '\s+', ' ', 'g')), "
          "round(((round(er.reqs, 2)/round(all_view.reqs, 2))*100), 2)"
          " as err_pers "
          "from error_log as er, all_log as all_view "
          "where er.req_date = all_view.req_date "
          "and "
          "round(((round(er.reqs, 2)/round(all_view.reqs, 2))*100), 2)"
          " > round(1, 2);")
error_days = c.fetchall()
print("\nWhich days did more than 1% of requests lead to errors?")
for err_day in error_days:
    print("{err_day[0]} -- {err_day[1]}% errors".format(err_day=err_day))
db.close()
