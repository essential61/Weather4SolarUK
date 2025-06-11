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

#### Location-specific code

#### Repo Permissions
In order for the scripts to update the repo with the latest weather forecast, the GITHUB_TOKEN requires write permission on the repository.
![permissions](githubaction.png)


#### Raw file for download
To individually download any generated files, you can select the 'raw' URL for the file.
#### crontab accuracy
Scheduling when the github actions run is specified using a crontab-style syntax. Times are specified in UTC. Note that the actual runtime for the action can differ from the specified time by a few minutes.




