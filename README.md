*scraping.py* is for Twitter scraping
*volume_analysis.py* uses *2013-2021.csv* data set
*correlation_analysis.py* uses *cc.csv*, *gw.csv*, *gt.csv* and *f4f.csv* data sets

data have been collected with the following queries:
* 2013-2021.csv, query: ``` '"climate change" min_retweets:100 until:2021-12-31 since: 2013-01-01 lang:en' ```
* cc.csv, query: ``` '"climate change" OR (#climatechange)  -"greta thunberg" -(#gretathunberg) -"fridays for future" -(#fridaysforfuture) min_retweets:100 until:2019-12-31 since:2018-09-01 lang:en' ```
* gw.csv, query: ``` '"global warming" OR (#globalwarming) -"greta thunberg" -(#gretathunberg) -"fridays for future" -(#fridaysforfuture) min_retweets:100 until:2019-12-31 since: 2018-09-01 lang:en' ```
* gt.csv, query: ``` '"greta thunberg" OR (#gretathunberg) -"climate change" -(#climatechange) -"global warming" -(#globalwarming) min_retweets:100 until:2019-12-31 since:2018-09-01 lang:en' ```
* f4f.csv, query: ``` '"fridays for future" OR (#fridaysforfuture) -"climate change" -"global warming" -(#climatechange) -(#globalwarming) min_retweets:100 until:2019-12-31 since:2018-09-01 lang:en' ```
