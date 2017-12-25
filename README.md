# Udacity Logs Analysis Project

Logs Analysis and reporting project for Full Stack nanodegree

## Getting Started

Create following views in the **news** db

```sql
-- View for popular articles in descending articles
create view popular_articles as
select articles.author, articles.slug, articles.title, count(*) as article_views
    from log, articles
    where articles.slug = substring(log.path, position(articles.slug in log.path), char_length(articles.slug))
    group by articles.author, articles.slug, articles.title
    order by article_views desc;

-- View for all error logs on any date (used in 3rd report query)
create view error_log as
select status, time::timestamp::date as req_date, count(*) as reqs
    from log
    where status like '4%' or status like '5%'
    group by status, req_date;

-- View for all logs (including errors) on any date (used in 3rd report query)
create view all_log as
select log.time::timestamp::date as req_date, count(*) as reqs
    from log
    group by req_date;

```

Once all the views are created. You can run the reporting program and see the results:
```
$ python reporting.py
```

## Authors

**Preetam Kajal Rout** - *Initial work* - [Github](https://github.com/preetamkrout)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details