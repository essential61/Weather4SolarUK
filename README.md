# Weather4SolarUK
This repo hosts a pair of python scripts (using the beautiful soup library) to scrape place-specific, weather forecast information from the UK met office website.

As the owner of a Solar installation, I am specifically interested in how likely it is to be sunny or overcast for the following day as well as correlate historical weather forecasts against photo-voltaic energy produced.

Each script is run as GitHub action using time of day as the trigger.

The first script runs once a day and fetches the forecast for the following day.

The second script runs hourly during daylight to fetch the forecast for the next hour to record the most recent update.

The output of both scripts is a SQL batch file to populate rows of a table as described below.

    CREATE TABLE public.forecasts (
	 starttime timestamptz NOT NULL,
     sky text NULL,```
     CONSTRAINT forecasts_pk PRIMARY KEY (starttime)
    );

###### Location-specific code

###### Repo Permissions

![permissions](githubaction.png)


###### Raw file for download

###### crontab accuracy




