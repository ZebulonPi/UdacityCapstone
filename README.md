# Project Title
### Data Engineering Capstone Project

#### Project Summary
For this project my goal is to perform ETL (extraction, transformation, and loading)
of data from a variety of given sources into a backend (Redshift) database, creating a
data model that allows for analysis of immigration data, with various additional metadata
sources acting as dimensions to enrich the immigration facts.

The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up

### Step 1: Scope the Project and Gather Data

#### Scope 
The overall scope of the project involves examining the given data sources, determining the best
transformations for that data, applying those, then loading it into a backend set of tables in
Amazon Redshift. With the loaded data, along with a representative data model for analysts to work
off of, this will act as an analytics platform to perform research around immigration into the
United States, answering questions such as:

1) what are the top areas/countries that are immigrating to the United States?
2) what types of vias are they immigrating with?
3) what are the top destinations for immigrants coming to the United States?
4) do certain immigrant nationalities prefer certain regions in the United States?
5) are there certain criteria (similar temperature, etc.) driving immigration patterns?

By building our this platform, all these questions, and more, can be researched.

#### Describe and Gather Data 
The datasets for this project consist of the following:

##### I94 Immigration Data
This data comes from the [I-94 Visitor Arrivals Program](https://travel.trade.gov/research/reports/i94/historical/2016.html), run by the National Travel and Tourism Office (NTTO). From their website:
"The National Travel and Tourism Office (NTTO) works cooperatively with the U.S. Department of Homeland Security (DHS)/U.S. Customs and Border Protection (CBP) to release I-94 Visitor Arrivals Program data, providing a comprehensive count of all visitors (overseas all travel modes plus Mexico air and sea) entering the United States."

This dataset will act as our main fact data. For this EDA (exploratory data analysis), we will be
only looking at April of 2016.

#### World Temperature Data
This dataset came from Kaggle, which in turn has sourced it from the Berkeley Earth project. You can read more about it [here](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data).

From Berkeley Earth's site: "The Berkeley Earth averaging process generates a variety of Output data including a set of gridded temperature fields, regional averages, and bias-corrected station data. Source data consists of the raw temperature reports that form the foundation of our averaging system. Source observations are provided as originally reported and will contain many quality control and redundancy issues. Intermediate data is constructed from the source data by merging redundant records, identifying a variety of quality control problems, and creating monthly averages from daily reports when necessary."

#### U.S. City Demographic Data
This data comes from OpenSoft. You can read more about it [here](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/).

From OpenSoft's site: "This dataset contains information about the demographics of all US cities and census-designated places with a population greater or equal to 65,000. 

This data comes from the US Census Bureau's 2015 American Community Survey."

#### Airport Code Table
This is a simple table of airport codes and corresponding cities, sourced from datahub.io. It comes from [here](https://datahub.io/core/airport-codes#data). 

From their website: "'airport-codes.csv' contains the list of all airport codes, the attributes are identified in datapackage description. Some of the columns contain attributes identifying airport locations, other codes (IATA, local if exist) that are relevant to identification of an airport.

Original source url is http://ourairports.com/data/airports.csv (stored in archive/data.csv)"

#### SAS Label Descriptions

By utilizing this text file, we can come up with a number of dimensions surrounding the
different codes present in the I94 dataset. By building these out, we save the analyst
(or, further down the analytics pipeline, a business user reading a report) from having to
look up given codes for country of citizenship, etc.

As we can source multiple dimensions from the single text file, we'll build a function to
read a given set of rows, and process them into a dataset. Utilizing this function, we can now 
build out additional dimensions surrounding country, port of entry, travel mode, U.S. states, and visa type.


### Step 2: Explore and Assess the Data

#### Explore the Data 
Identify data quality issues, like missing values, duplicate data, etc.

##### I94 Immigration Data
Dataframe count and info gives as the overall layout of the dataset, as well as the number of
records in total (3,096,313), as well as non-null counts for each of the given fields. Many of the
'important' fields (from a research perspective) as full populated, like immigrant citizenship and
residency, but others, like occupancy, are predominantly empty, limiting its usefulness in analytics.

We can also see that there are a number of codes in this dataset, for items like country of citizenship, 
that we should create dimension tables around. This will make it much easier for analysts to both analyze
and report on these features.

##### I94 Immigration Data - Countries
This dimension will contain all the country codes from the I94 data,
as well as their corresponding country descriptions.

##### I94 Immigration Data - Ports
This dimension will contain all the port codes from the I94 data,
as well as their corresponding port descriptions.

##### I94 Immigration Data - Travel Mode
This dimension will contain all the mode of travel code from the 
I94 data, as well as their corresponding mode descriptions.

##### I94 Immigration Data - U.S. States
This dimension will contain all the state codes from the I94 data,
as well as their corresponding state descriptions.

##### I94 Immigration Data - Visa Type
This dimension will contain all the visa codes from the I94 data,
as well as their corresponding visa descriptions.

##### Global Temperature Data
Dataframe count and info gives as the overall layout of the dataset, as well as the number of
records in total (8,599,212), as well as non-null counts for each of the given fields. Many of the
'important' fields (from a research perspective) as full populated, like city and country, while others are into the 95% range for population.

For our needs, this dataset is far too vast, from a temporal perspective, for what we're trying to analyze. Even taking into account things like temperature trending over time driving immigration, the fact that the data goes back to the mid-1700s makes the set too unweildly for fast analytics. While we could argue almost any date, limiting the data to the 1970s forwards shrinks it by quite a bit (XXX record,only XX% of the original size), but also give 50+ of trending data.

#### U.S. City Demographic Data
Looking at this demographic data, we can see that almost all of the fields in the set are populated. 

#### Airport Code Table
Looking at this set, we can see that the majority of the airport fields are populated. We can
also see that this file contains international airports as well, while the immigration data only
looks at US ports on ingress. Based on this, we will want to subset this dataset to include only
US airports before loading it into Redshift.

#### Cleaning Steps
In order to make the data as usuable as possible, as well as reduce the data footprint 
(giving us both speed of query as well as storage cost savings), we'll want to remove the
columns that won't be adding much value to our future analytics.


### Step 3: Define the Data Model

#### 3.1 Conceptual Data Model
insert pic here
For this model, I chose a star schema, with our I94 immigration data as our fact, and the other
related data sets as our dimensions

#### 3.2 Mapping Out Data Pipelines
For our pipelines, I currently have Python doing the heavy lifting of ingesting the data
from the different data sets we have, including the 'sas7bdat' files. Given the sheer amount of
records we have (3+ million for one month of immigration data alone), I would typically be
leveraging Spark to ingest, as we've done in previous projects, but there was an unavoidable
bug with Spark in the Jupyter environment that Support was unable to mitigate, forcing me to
use straight Pandas instead.

### Step 4: Run Pipelines to Model the Data

#### 4.1 Create the data model
Build the data pipelines to create the data model.

#### 4.2 Data Quality Checks
Explain the data quality checks you'll perform to ensure the pipeline ran as expected. These could include:
 * Integrity constraints on the relational database (e.g., unique key, data type, etc.)
 * Unit tests for the scripts to ensure they are doing the right thing
 * Source/Count checks to ensure completeness
 
Run Quality Checks

#### 4.3 Data dictionary 
Create a data dictionary for your data model. For each field, provide a brief description of what the data is and where it came from. You can include the data dictionary in the notebook or in a separate file.

#### Step 5: Complete Project Write Up
* Clearly state the rationale for the choice of tools and technologies for the project.
* Propose how often the data should be updated and why.
* Write a description of how you would approach the problem differently under the following scenarios:
 * The data was increased by 100x.
 * The data populates a dashboard that must be updated on a daily basis by 7am every day.
 * The database needed to be accessed by 100+ people.
 
From a scalability standpoint, Redshift / Spark / Pandas was the way to go for this project. The
ability to scale both the processing technology (Spark), as well as the backend database tectnology
(Redshift), meant that we would always have the ability to scale out, in terms of nodes, as well as
up, by leveraging the power of AWS to add additional compute power if necessary.

Because a lot of these datasets are time-based, and are not updated daily, I wouldn't suggest that
the ETL process be run on a scheduled basis. Rather, I would run an update when a given dataset
was updated at the source (i.e., a new month/year of immigration data is released, etc.). This would
both ensure that the data the analysts are working with is the most current available, as well as 
saving the business money by not having Spark clusters spun up needlessly.

If the data was increased 100x, or if 100+ people need to access the data, we are in the clear with
utilizing Redshift as our backend platform. Redshift's ability to scale means that we can store
petabytes of information, and handle almost unlimited user connections, without having to change
technologies, or indeed introduce any downtime. The ability to spin up additional nodes means
we can scale up, or down, as the business demands.

For the other listed scenario, where there is a dashboard that must be updated on a daily basis 
by 7am every day, I would suggest utilizing a job scheduling technology like Airflow. Any aggregation
or additional transformation jobs that needed to be run to populate the semantic layer that the
dashboard runs against could easily be handled by Airflow, running on an EC2 instance and reading
and writing from/to Redshift. This would also save the business on data egress charges.