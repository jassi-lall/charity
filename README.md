# Charity alerter
Scrape charity data from https://givingmatters.civicore.com/ and give an alert when any new organisation is added.

# Crawl delay
The script can run very fast but is intentionally slowed down with a random crawl delay of 1-2 seconds per page scanned (total 110 pages) to avoid blocking of the IP making requests. It is intended to be run in the background automatically. The crawl delay can be easily adjusted if required.
