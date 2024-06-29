# spotify_data_engineering
This repository contains an end-to-end data engineering project using AWS Cloud and PySpark, from Spotify data information. The project involves extracting Spotify data using APIs, transforming the data with PySpark, storing it in AWS S3, and performing data analysis. The project involves extracting, transforming, and loading Spotify data to build a data pipeline. Key components include:

- Data Extraction: Retrieving Spotify data using APIs.
- Data Transformation: Processing data with PySpark.
- Data Storage: Storing transformed data in AWS S3.
- Data Analysis: Analyzing data using PySpark.

### Technologies Used
- AWS Cloud: S3, IAM
- PySpark
- Python

### Project Structure
- data_extraction/: Scripts for extracting data from Spotify APIs.
- data_transformation/: PySpark scripts for transforming data.
- data_storage/: Configurations for storing data in AWS S3.
- data_analysis/: Notebooks and scripts for analyzing the data.

### Getting Started
To get started with this project, follow the instructions below:

- Clone this repository.
- Set up AWS credentials and configure S3 buckets.
- Install required Python packages.
- Run the data extraction scripts.
- Execute the data transformation pipeline using PySpark.
- Analyze the transformed data using this README.

### Data Used
I'm using data placed on kaggle, created by Tony Gordon Jr. [Spotify Dataset 2023](https://www.kaggle.com/datasets/tonygordonjr/spotify-dataset-2023)

1. albums
2. artists
3. tracks

### Architecture Diagram

<p align='center'><img src="img/architecture.png"></p>

### Data Engineering Process

1. `CREATE IAM USER`: On the first step we will create a new user via root account, then login via new IAM user for security measures. [Click here](https://www.youtube.com/watch?v=ubrE4xq9_9c) on how to setup IAM user. Then attaching necessary `direct policies` for this project, that's include S3, Glue, Athena & QuickSight access. And before setting up the account, do review the account before its creation, refer image below.

<p align="center"><img src=img/s3-access.png></p>
<p align="center"><img src=img/glue-access.png></p>
<p align="center"><img src=img/athena-access.png></p>
<p align="center"><img src=img/quicksight-access.png></p>
<p align="center"><img src=img/review-IAM.png></p>

Once complete, you can signing via IAM account that you just created, which the system will request Account ID number, Username and password. For first time log in, the system will auto asking to change the password accordingly.

2. `CREATE S3 BUCKET`: Go to S3, and create a bucket. As for this project I've named my bucket as `my-spotify-de-project` you can named it whatever you want, do noted each bucket is unique and remembers its purpose.

Then, you can start to create two new folder `staging` and `datawarehouse`.

<p align="center"><img src=img/create-folder.png></p>
<p align="center"><img src=img/create-folder-02.png></p>

3. `DOWNLOAD THE DATASET`: Before we begin processing, we must acquired dataset. Usually the data we will fetch from `DynamoDB` or `Database Instance`. But for this project since we outsource the dataset, we will upload it manually.

Get the Dataset [HERE](https://www.kaggle.com/datasets/tonygordonjr/spotify-dataset-2023)

4. `UPLOAD THE DATASET`: For this project, I've upload it inside `staging/` that just created earlier, and selected three files out of five files inside the dataset we retrieve earlier, I've upload Artist, Albums & Tracks. 

<p align="center"><img src=img/upload-success.png></p>

5. `ETL JOB WITH AWS GLUE`: Now the tricky and charges apply. In this section, you should beware that this tools have charges. Below is the snippet on the `AWS GLUE: ETL Jobs` which I named it as DE-Spotify-ETL

<p align="center"><img src=img/glue-architecture.png></p>

Next, you based on the glue architecture you can follow on creating new jobs. 
- Source: Select the Amazon S3 bucket. in this case, we have three items; artist.csv, tracks.csv & albums.csv so we will insert three s3 buckets.

<p align="center"><img src=img/ETL-pt-1.png></p>

<p align="center"><img src=img/ETL-pt-2.png></p>

- Transform: We gonna join the relevant items as per images.

<p align="center"><img src=img/ETL-pt-3.png></p>

<p align="center"><img src=img/ETL-pt-4.png></p>

Next, remove redundancy using `drop fields`

<p align="center"><img src=img/ETL-pt-5.png></p>

- Destination Target: There are variety destination target you can choose, I chose S3 bucket that we just created earlier inside `datawarehouse` folder as my destination target. I use `parquet` as for the format and `snappy` ensuring the file is `lightweight` 

<p align="center"><img src=img/ETL-pt-6.png></p>

<p align="center"><img src=img/ETL-pt-7.png></p>

- Creating new IAM role: We need to create new role from root account, allowing us to run the ETL jobs. Go to `root account` then go to `IAM` then click roles at the left navigation pane.

<p align="center"><img src=img/IAM-role-glue.png></p>

This role will allowing `s3fullaccess` 

<p align="center"><img src=img/IAM-role-glue-02.png></p>

- `Component for ETL Job Details`: before you can save the ETL job, you need pre-configure the settings beforehand. Here is my settings for this project, the red line indicates the key elements you need to focus when creating job, yellow highlight are settings that suits for this small project.

<p align="center"><img src=img/glue-job-details.png></p>

- `RUN THE JOB!!`: once everything have been configure, you can the ETL accordingly and visit the `Job run monitoring` to view the running status.

<p align="center"><img src=img/run-job.png></p>

This process might take a while, you might need coffee break here. It tooks  minutes to complete running the ETL jobs.

<p align="center"><img src=img/job-duration.png></p>

<p align="center"><img src=img/ETL-job-successful.png></p>

6. `CRAWLING WITH AWS GLUE`: This process will create catalog and database (db). Now, let's revisit the AWS GLUE and go to `crawlers` under `Data Catalog` and hit `Create Crawler`. 

<p align="center"><img src=img/create-crawler.png></p>

- `Set crawler properties`: I've named it as `ndl_`

<p align="center"><img src=img/crawler-01.png></p>

- `Choose data sources and classifiers`: Choosing the S3 location the files we just transformed earlier ../datawarehouse

<p align="center"><img src=img/crawler-02.png></p>

- `Configure security settings`: I'm choosing I'm role created earlier

<p align="center"><img src=img/crawler-03.png></p>

- `Set output and scheduling`: We need to create new Target database, now, open new tab and go to the AWS Glue and choose `database` under Data Catalog, `add database`. I've named it as `spotify`.

<p align="center"><img src=img/database-01.png></p>

<p align="center"><img src=img/database-02.png></p>

<p align="center"><img src=img/crawler-04.png></p>

- `Review and create`: once crawler is finished setting up you can create the crawler

<p align="center"><img src=img/crawler-05.png></p>

<p align="center"><img src=img/run-crawler.png></p>

6. `QUERYING WITH ATHENA`: In this section we gonna query data through AWS Athena. At the Amazon Athena, you can go `Query Editor`, this tools is using `SQL` language. Then, in this query we need to adjust few settings. First you need to create new S3 bucket to insert the output querying location.

<p align="center"><img src=img/athena-s3.png></p>

<p align="center"><img src=img/athena-01.png></p>

<p align="center"><img src=img/athena-02.png></p>

<p align="center"><img src=img/athena-03.png></p>

7. `DATA VISUALIZATION WITH QUICKSIGHT`: This tool will help you to create proper data visualization similar `powerBI` or `Tableau`. Now go to QUICKSIGHT. If this is your first time trying to access the `QUICKSIGHT` you need to login via your root account and create an account for `QUICKSIGHT`, Please be noted that tool have charges apply (quite expensive)

<p align="center"><img src=img/quicksight.png></p>
















source:

- [Tutorial by Date with Data](https://www.youtube.com/watch?v=yIc5a7C8aHs)
















References:
-  [Spotify playlist data engineering by Date with Data](https://www.youtube.com/watch?v=yIc5a7C8aHs)
-  [Creating IAM user](https://www.youtube.com/watch?v=ubrE4xq9_9c)
