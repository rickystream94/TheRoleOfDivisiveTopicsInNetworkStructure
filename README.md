# M.Sc. Thesis Project: The Role of Divisive Topics in Network Structure
This repository hosts all the supplementary material for my M.Sc. Thesis Project, completed at the Technical University of Denmark (DTU), Copenhagen.
All the material included in the repository is meant to represent the Appendix of the official final report.

Folder and contents:
- **Notebooks**: It contains all the Jupyter Notebeooks I used for development purposes. They include all the source code I wrote to carry out my analysis and produce the plots. The notebooks are numerically sorted in ascending order to reflect the chronological order of creation;
- **Pictures**: a set of folders, each one corresponding to different sets of notebooks, where all the output plots have been saved;
- **lib/GetOldTweets-python**: contains the library used to crawl old tweets and the wrapper script I maintained to customize the features and create an ad-hoc solution that nicely suited my case;
- **scripts**: A set of standalone scripts written in Python/Julia/Bash for miscellaneous/isolated tasks.

Inside **lib/GetOldTweets-python**, two important files deserve further attention:
- `twitter_object_dictionaries.json`: a JSON file indicating the Twitter API Platform objects (e.g. [Tweet Object](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object)) attributes I considered when downloading tweets. All the missing fields were not relevant for my analysis hence they have been filtered out before saving the tweets;
- `get_old_tweets.py`: mixes functionalities offered by the GetOldTweets library and the Twitter API Platform to crawl old tweets, retrieve their full information and save them in JSON format. It includes a simple text pre-processing step that strips out URLs from the tweets. The script creates a log file to report the progress.


### Report Abstract
> Ideological polarization on social media reflects a crucial issue of contemporary societies. Several studies within social sciences and psychology tried to investigate the root causes and formulated theories to describe this phenomenon. Information retrieval through social media platforms like Twitter has the means to hinder a democratic approach towards political debates. This aspect fosters the creation of echo chambers that enhance the spreading and reinforcement of polarized opinions among ideologically similar individuals. The aim of this study was to find a scientific way to measure the impact of controversial topics on Twitter users' behavior from a temporal perspective. By relying on third-party software and the Twitter Developer API, I  collected a set of raw tweets from Twitter related to political controversies that took place between September 2013 and December 2016. Each controversy was related to a set of hashtags conventionally adopted by the users to express their political affiliation. A large network of Twitter users, mutually interacting in the same time window, along with the collection of tweets designated the subject of the study. I revealed evidence of a positive bonding effect on Twitter users mutually communicating as part of the global conversations represented by such controversial hashtags. This reflected into an increase of the mutual interaction consistency in both the short and long term, fostered by the online controversies. I further discovered that the mutual interactions network obeyed the laws of a precise topological structure which highlighted the presence of community clusters growing around the most influential users. The obtained results hinted the existence of the echo chamber phenomenon. The role of the community hubs and the high in-community communication suggests a clear resemblance of a realistic political debate between opposing groups. Further investigation within NLP suggested that predicting tweets' political leaning is a viable task.