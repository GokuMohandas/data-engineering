# Data Engineering for Machine Learning

Learn data engineering fundamentals by constructing a modern data stack for analytics and machine learning applications. We'll also learn how to orchestrate our data workflows and programmatically execute tasks to prepare our high quality data for downstream consumers (analytics, ML, etc.)

<div align="left">
    <a target="_blank" href="https://madewithml.com"><img src="https://img.shields.io/badge/Subscribe-40K-brightgreen"></a>&nbsp;
    <a target="_blank" href="https://github.com/GokuMohandas/Made-With-ML"><img src="https://img.shields.io/github/stars/GokuMohandas/Made-With-ML.svg?style=social&label=Star"></a>&nbsp;
    <a target="_blank" href="https://www.linkedin.com/in/goku"><img src="https://img.shields.io/badge/style--5eba00.svg?label=LinkedIn&logo=linkedin&style=social"></a>&nbsp;
    <a target="_blank" href="https://twitter.com/GokuMohandas"><img src="https://img.shields.io/twitter/follow/GokuMohandas.svg?label=Follow&style=social"></a>
    <br>
</div>

<br>

👉 &nbsp;This repository contains the code that complements the [data stack](https://madewithml.com/courses/mlops/data-stack/) and [orchestration](https://madewithml.com/courses/mlops/orchestration/) lessons which is a part of the [MLOps course](https://github.com/GokuMohandas/mlops-course). If you haven't already, be sure to check out the lessons because all the concepts are covered extensively and tied to data engineering best practices for building the data stack for ML systems.

<div align="left">
<a target="_blank" href="https://madewithml.com/courses/mlops/data-stack/"><img src="https://img.shields.io/badge/📖 Read-lesson-9cf"></a>&nbsp;
<a href="https://github.com/GokuMohandas/data-engineering" role="button"><img src="https://img.shields.io/static/v1?label=&amp;message=View%20On%20GitHub&amp;color=586069&amp;logo=github&amp;labelColor=2f363d"></a>&nbsp;
</div>

<br>

## Data stack
- [Set up](#setup)
- [Extract via Airbyte](#extract-via-airbyte)
- [Load into BigQuery](#load-into-bigquery)
- [Transform via dbt-cloud](#transform-via-dbt-cloud)
- [Applications](#applications)

## Orchestration
- [Set up Airflow](#set-up-airflow)
- [Extract and load](#extract-and-load)
- [Validate via GE](#validate-via-ge)
- [Transform via dbt-core](#transform-via-dbt-core)

### Setup

At a high level, we're going to:

1. [**E**xtract and **L**oad](#extract_and_load) data from [sources](#sources) to [destinations](#destinations).
2. [**T**ransform](#transform) for downstream [applications](#applications).

This process is more commonly known as ELT, but there are variants such as ETL and reverse ETL, etc. They are all essentially the same underlying workflows but have slight differences in the order of data flow and where data is processed and stored.

<div class="ai-center-all">
    <img width="800" src="https://madewithml.com/static/images/mlops/data_stack/data.png" alt="data stack">
</div>

### Extract via airbyte

The first step in our data pipeline is to extract data from a source and load it into the appropriate destination. While we could construct custom scripts to do this manually or on a schedule, an ecosystem of data ingestion tools have already standardized the entire process. They all come equipped with connectors that allow for extraction, normalization, cleaning and loading between sources and destinations. And these pipelines can be scaled, monitored, etc. all with very little to no code.

<div class="ai-center-all">
    <img width="600" src="https://madewithml.com/static/images/mlops/data_stack/pipelines.png" alt="ingestion pipelines">
</div>

We're going to use the open-source tool [Airbyte](https://airbyte.com/) to create connections between our data sources and destinations. Let's set up Airbyte and define our data sources. As we progress in this lesson, we'll set up our destinations and create connections to extract and load data.

1. Ensure that we still have Docker installed from our [Docker lesson](https://madewithml.com/courses/mlops/docker) but if not, download it [here](https://www.docker.com/products/docker-desktop/). For Windows users, be sure to have these [configurations](https://docs.airbyte.com/deploying-airbyte/local-deployment/#deploy-on-windows) enabled.
2. In a parent directory, outside our project directory for the MLOps course, execute the following commands to load the Airbyte repository locally and launch the service.
```bash
git clone https://github.com/airbytehq/airbyte.git
cd airbyte
docker-compose up
```
3. After a few minutes, visit [http://localhost:8000/](http://localhost:8000/) to view the launched Airbyte service.

#### Sources

We'll start our ELT process by defining the data source in Airbyte:

1. On our [Airbyte UI](http://localhost:8000/), click on `Sources` on the left menu. Then click the `+ New source` button on the top right corner.
2. Click on the `Source type` dropdown and choose `File`. This will open a view to define our file data source.
```yaml
Name: Projects
URL: https://raw.githubusercontent.com/GokuMohandas/Made-With-ML/main/datasets/projects.csv
File Format: csv
Storage Provider: HTTPS: Public Web
Dataset Name: projects
```
3. Click the `Set up source` button and our data source will be tested and saved.
4. Repeat steps 1-3 for our tags data source as well:
```yaml
Name: Tags
URL: https://raw.githubusercontent.com/GokuMohandas/Made-With-ML/main/datasets/tags.csv
File Format: csv
Storage Provider: HTTPS: Public Web
Dataset Name: tags
```

<div class="ai-center-all">
    <img width="1000" src="https://madewithml.com/static/images/mlops/data_stack/sources.png" alt="data sources">
</div>

### Load into BigQuery

Once we know the source we want to extract data from, we need to decide the destination to load it. The choice depends on what our downstream applications want to be able to do with the data. And it's also common to store data in one location (ex. data lake) and move it somewhere else (ex. data warehouse) for specific processing.

#### Set up Google BigQuery

Our destination will be a [data warehouse](#data-warehouse) since we'll want to use the data for downstream analytical and machine learning applications. We're going to use [Google BigQuery](https://cloud.google.com/bigquery) which is free under Google Cloud's [free tier](https://cloud.google.com/bigquery/pricing#free-tier) for up to 10 GB storage and 1TB of queries (which is significantly more than we'll ever need for our purpose).

1. Log into your [Google account](https://accounts.google.com/signin){:target="_blank} and then head over to [Google CLoud](https://cloud.google.com/). If you haven't already used Google Cloud's free trial, you'll have to sign up. It's free and you won't be autocharged unless you manually upgrade your account. Once the trial ends, we'll still have the free tier which is more than plenty for us.
2. Go to the [Google BigQuery page](https://console.cloud.google.com/bigquery){:target="_blank} and click on the `Go to console` button.
3. We can create a new project by following these [instructions](https://cloud.google.com/resource-manager/docs/creating-managing-projects#console) which will lead us to the [create project page](https://console.cloud.google.com/projectcreate).
```yaml
Project name: made-with-ml  # Google will append a unique ID to the end of it
Location: No organization
```
4. Once the project has been created, refresh the page and we should see it (along with few other default projects from Google).

```bash
# Google BigQuery projects
├── made-with-ml-XXXXXX   👈 our project
├── bigquery-publicdata
├── imjasonh-storage
└── nyc-tlc
```

#### Define BigQuery destination in Airbyte

Next, we need to establish the connection between Airbyte and BigQuery so that we can load the extracted data to the destination. In order to authenticate our access to BigQuery with Airbyte, we'll need to create a service account and generate a secret key. This is basically creating an identity with certain access that we can use for verification. Follow these [instructions](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-console) to create a service and generate the key file (JSON). Note down the location of this file because we'll be using it throughout this lesson. For example ours is `/Users/goku/Downloads/made-with-ml-XXXXXX-XXXXXXXXXXXX.json`.

1. On our [Airbyte UI](http://localhost:8000/), click on `Destinations` on the left menu. Then click the `+ New destination` button on the top right corner.
2. Click on the `Destination type` dropdown and choose `BigQuery`. This will open a view to define our file data source.
```yaml
Name: BigQuery
Default Dataset ID: mlops_course  # where our data will go inside our BigQuery project
Project ID: made-with-ml-XXXXXX  # REPLACE this with your Google BiqQuery Project ID
Credentials JSON: SERVICE-ACCOUNT-KEY.json  # REPLACE this with your service account JSON location
Dataset location: US  # select US or EU, all other options will not be compatible with dbt later
```
3. Click the `Set up destination` button and our data destination will be tested and saved.

<div class="ai-center-all">
    <img width="1000" src="https://madewithml.com/static/images/mlops/data_stack/destinations.png" alt="data destinations">
</div>

#### Connecting File source to BigQuery destination

Now we're ready to create the connection between our sources and destination:

1. On our [Airbyte UI](http://localhost:8000/), click on `Connections` on the left menu. Then click the `+ New connection` button on the top right corner.
2. Under `Select a existing source`, click on the `Source` dropdown and choose `Projects` and click `Use existing source`.
3. Under `Select a existing destination`, click on the `Destination` dropdown and choose `BigQuery` and click `Use existing destination`.
```yaml
Connection name: Projects <> BigQuery
Replication frequency: Manual
Destination Namespace: Mirror source structure
Normalized tabular data: True  # leave this selected
```
4. Click the `Set up connection` button and our connection will be tested and saved.
5. Repeat the same for our `Tags` source with the same `BigQuery` destination.

> Notice that our sync mode is `Full refresh | Overwrite` which means that every time we sync data from our source, it'll overwrite the existing data in our destination. As opposed to `Full refresh | Append` which will add entries from the source to bottom of the previous syncs.

<div class="ai-center-all">
    <img width="1000" src="https://madewithml.com/static/images/mlops/data_stack/connections.png" alt="data connections">
</div>

#### Data sync

Our replication frequency is `Manual` because we'll trigger the data syncs ourselves:

1. On our [Airbyte UI](http://localhost:8000/), click on `Connections` on the left menu. Then click the `Projects <> BigQuery` connection we set up earlier.
2. Press the `🔄 Sync now` button and once it's completed we'll see that the projects are now in our BigQuery data warehouse.
3. Repeat the same with our `Tags <> BigQuery` connection.

```bash
# Inside our data warehouse
made-with-ml-XXXXXX               - Project
└── mlops_course                  - Dataset
│   ├── _airbyte_raw_projects     - table
│   ├── _airbyte_raw_tags         - table
│   ├── projects                  - table
│   └── tags                      - table
```

>In our [orchestration lesson](https://madewithml.com/courses/mlops/orchestration), we'll use Airflow to programmatically execute the data sync.

We can easily explore and query this data using SQL directly inside our warehouse:

1. On our BigQuery project page, click on the `🔍 QUERY` button and select `In new tab`.
2. Run the following SQL statement and view the data:
```sql linenums="1"
SELECT *
FROM `made-with-ml-XXXXXX.mlops_course.projects`
LIMIT 1000
```

<div class="output_subarea output_html rendered_html output_result" dir="auto"><div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>created_on</th>
      <th>title</th>
      <th>description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>6</td>
      <td>2020-02-20 06:43:18</td>
      <td>Comparison between YOLO and RCNN on real world...</td>
      <td>Bringing theory to experiment is cool. We can ...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7</td>
      <td>2020-02-20 06:47:21</td>
      <td>Show, Infer &amp; Tell: Contextual Inference for C...</td>
      <td>The beauty of the work lies in the way it arch...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9</td>
      <td>2020-02-24 16:24:45</td>
      <td>Awesome Graph Classification</td>
      <td>A collection of important graph embedding, cla...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>15</td>
      <td>2020-02-28 23:55:26</td>
      <td>Awesome Monte Carlo Tree Search</td>
      <td>A curated list of Monte Carlo tree search papers...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>19</td>
      <td>2020-03-03 13:54:31</td>
      <td>Diffusion to Vector</td>
      <td>Reference implementation of Diffusion2Vec (Com...</td>
    </tr>
  </tbody>
</table>
</div></div>

### Transform via dbt-cloud

Once we've extracted and loaded our data, we need to transform the data so that it's ready for downstream applications. These transformations are different from the [preprocessing](https://madewithml.com/courses/mlops/preprocessing#transformations) we've seen before but are instead reflective of business logic that's agnostic to downstream applications. Common transformations include defining schemas, filtering, cleaning and joining data across tables, etc. While we could do all of these things with SQL in our data warehouse (save queries as tables or views), dbt delivers production functionality around version control, testing, documentation, packaging, etc. out of the box. This becomes crucial for maintaining observability and high quality data workflows.

<div class="ai-center-all mb-4">
    <img width="500" src="https://madewithml.com/static/images/mlops/data_stack/transform.png" alt="data transform">
</div>

> In addition to data transformations, we can also process the data using large-scale analytics engines like Spark, Flink, etc. We'll learn more about batch and stream processing in our [systems design lesson](https://madewithml.com/courses/mlops/systems-design#processing).

### dbt Cloud

Now we're ready to transform our data in our data warehouse using [dbt](https://www.getdbt.com/). We'll be using a developer account on dbt Cloud (free), which provides us with an IDE, unlimited runs, etc.

> We'll learn how to use the [dbt-core](https://github.com/dbt-labs/dbt-core) in our [orchestration lesson](https://madewithml.com/courses/mlops/orchestration/). Unlike dbt Cloud, dbt core is completely open-source and we can programmatically connect to our data warehouse and perform transformations.

1. Create a [free account](https://www.getdbt.com/signup/) and verify it.
2. Go to [https://cloud.getdbt.com/](https://cloud.getdbt.com/) to get set up.
3. Click `continue` and choose `BigQuery` as the database.
4. Click `Upload a Service Account JSON file` and upload our file to autopopulate everything.
5. Click the `Test` > `Continue`.
6. Click `Managed` repository and name it `dbt-transforms` (or anything else you want).
7. Click `Create` > `Continue` > `Skip and complete`.
8. This will open the project page and click `>_ Start Developing` button.
9. This will open the IDE where we can click `🗂 initialize your project`.

Now we're ready to start developing our models:

1. Click the `···` next to the `models` directory on the left menu.
2. Click `New folder` called `models/labeled_projects`.
3. Create a `New file` under `models/labeled_projects` called `labeled_projects.sql`.
4. Repeat for another file under `models/labeled_projects` called `schema.yml`.

```bash
dbt-cloud-XXXXX-dbt-transforms
├── ...
├── models
│   ├── example
│   └── labeled_projects
│   │   ├── labeled_projects.sql
│   │   └── schema.yml
├── ...
└── README.md
```

### Joins

Inside our `models/labeled_projects/labeled_projects.sql` file we'll create a view that joins our project data with the appropriate tags. This will create the labeled data necessary for downstream applications such as machine learning models. Here we're joining based on the matching id between the projects and tags:

```sql linenums="1"
-- models/labeled_projects/labeled_projects.sql
SELECT p.id, created_on, title, description, tag
FROM `made-with-ml-XXXXXX.mlops_course.projects` p  -- REPLACE
LEFT JOIN `made-with-ml-XXXXXX.mlops_course.tags` t  -- REPLACE
ON p.id = t.id
```

We can view the queried results by clicking the `Preview` button and view the data lineage as well.

### Schemas

Inside our `models/labeled_projects/schema.yml` file we'll define the schemas for each of the features in our transformed data. We also define several tests that each feature should pass. View the full list of [dbt tests](https://docs.getdbt.com/docs/building-a-dbt-project/tests) but note that we'll use [Great Expectations](https://madewithml.com/courses/mlops/testing/#expectations) for more comprehensive tests when we orchestrate all these data workflows in our [orchestration lesson](https://madewithml.com/courses/mlops/orchestration/).


```yaml linenums="1"
# models/labeled_projects/schema.yml

version: 2

models:
    - name: labeled_projects
      description: "Tags for all projects"
      columns:
          - name: id
            description: "Unique ID of the project."
            tests:
                - unique
                - not_null
          - name: title
            description: "Title of the project."
            tests:
                - not_null
          - name: description
            description: "Description of the project."
            tests:
                - not_null
          - name: tag
            description: "Labeled tag for the project."
            tests:
                - not_null

```

### Runs

At the bottom of the IDE, we can execute runs based on the transformations we've defined. We'll run each of the following commands and once they finish, we can see the transformed data inside our data warehouse.

```bash
dbt run
dbt test
```

Once these commands run successfully, we're ready to move our transformations to a production environment where we can insert this view in our data warehouse.

### Jobs

In order to apply these transformations to the data in our data warehouse, it's best practice to create an [Environment](https://docs.getdbt.com/guides/legacy/managing-environments) and then define [Jobs](https://docs.getdbt.com/guides/getting-started/building-your-first-project/schedule-a-job):

1. Click `Environments` on the left menu > `New Environment` button (top right corner) and fill out the details:
```yaml
Name: Production
Type: Deployment
...
Dataset: mlops_course
```
2. Click `New Job` with the following details and then click `Save` (top right corner).
```yaml
Name: Transform
Environment: Production
Commands: dbt run
          dbt test
Schedule: uncheck "RUN ON SCHEDULE"
```
3. Click `Run Now` and view the transformed data in our data warehouse under a view called `labeled_projects`.

```bash
# Inside our data warehouse
made-with-ml-XXXXXX               - Project
└── mlops_course                  - Dataset
│   ├── _airbyte_raw_projects     - table
│   ├── _airbyte_raw_tags         - table
│   ├── labeled_projects          - view
│   ├── projects                  - table
│   └── tags                      - table
```

<div class="ai-center-all">
    <img width="800" src="https://madewithml.com/static/images/mlops/data_stack/dbt_run.png" alt="dbt run">
</div>


> There is so much more to dbt so be sure to check out their [official documentation](https://docs.getdbt.com/docs/building-a-dbt-project/documentation) to really customize any workflows. And be sure to check out our [orchestration lesson](https://madewithml.com/courses/mlops/orchestration) where we'll programmatically create and execute our dbt transformations.


### Applications

Hopefully we created our data stack for the purpose of gaining some actionable insight about our business, users, etc. Because it's these use cases that dictate which sources of data we extract from, how often and how that data is stored and transformed. Downstream applications of our data typically fall into one of these categories:

- `data analytics`: use cases focused on reporting trends, aggregate views, etc. via charts, dashboards, etc.for the purpose of providing operational insight for business stakeholders.
- `machine learning`: use cases centered around using the transformed data to construct predictive models (forecasting, personalization, etc.).

```bash
!pip install google-cloud-bigquery==1.21.0 -q
```
```python
from google.cloud import bigquery
from google.oauth2 import service_account

# Replace these with your own values
project_id = "made-with-ml-XXXXXX"
SERVICE_ACCOUNT_KEY_JSON = "/Users/goku/Downloads/made-with-ml-XXXXXX-XXXXXXXXXXXX.json"

# Establish connection
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_KEY_JSON)
client = bigquery.Client(credentials= credentials, project=project_id)

# Query data
query_job = client.query("""
   SELECT *
   FROM mlops_course.labeled_projects""")
results = query_job.result()
results.to_dataframe().head()
```

<div class="output_subarea output_html rendered_html output_result" dir="auto"><div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>created_on</th>
      <th>title</th>
      <th>description</th>
      <th>tag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1994.0</td>
      <td>2020-07-29 04:51:30</td>
      <td>Understanding the Effectivity of Ensembles in ...</td>
      <td>The report explores the ideas presented in Dee...</td>
      <td>computer-vision</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1506.0</td>
      <td>2020-06-19 06:26:17</td>
      <td>Using GitHub Actions for MLOps &amp; Data Science</td>
      <td>A collection of resources on how to facilitate...</td>
      <td>mlops</td>
    </tr>
    <tr>
      <th>2</th>
      <td>807.0</td>
      <td>2020-05-11 02:25:51</td>
      <td>Introduction to Machine Learning Problem Framing</td>
      <td>This course helps you frame machine learning (...</td>
      <td>mlops</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1204.0</td>
      <td>2020-06-05 22:56:38</td>
      <td>Snaked: Classifying Snake Species using Images</td>
      <td>Proof of concept that it is possible to identi...</td>
      <td>computer-vision</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1706.0</td>
      <td>2020-07-04 11:05:28</td>
      <td>PokeZoo</td>
      <td>A deep learning based web-app developed using ...</td>
      <td>computer-vision</td>
    </tr>
  </tbody>
</table>
</div></div>

### Set up Airflow

Now it's time to programmatically execute the workflows we set up above. We'll be using [Airflow](https://airflow.apache.org/) to author, schedule, and monitor our workflows. If you're not familiar with orchestration, be sure to check out the [lesson](https://madewithml.com/courses/mlops/orchestration/) first.

To install and run Airflow, we can either do so [locally](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html) or with [Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html). If using `docker-compose` to run Airflow inside Docker containers, we'll want to allocate at least 4 GB in memory.

```bash
# Configurations
export AIRFLOW_HOME=${PWD}/airflow
AIRFLOW_VERSION=2.3.3
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# Install Airflow (may need to upgrade pip)
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Initialize DB (SQLite by default)
airflow db init
```

This will create an `airflow` directory with the following components:

```bash
airflow/
├── logs/
├── airflow.cfg
├── airflow.db
├── unittests.cfg
└── webserver_config.py
```

We're going to edit the [airflow.cfg](https://github.com/GokuMohandas/data-engineering/blob/main/airflow/airflow.cfg) file to best fit our needs:
```bash
# Inside airflow.cfg
enable_xcom_pickling = True  # needed for Great Expectations airflow provider
load_examples = False  # don't clutter webserver with examples
```

And we'll perform a reset to implement these configuration changes.

```bash
airflow db reset -y
```

Now we're ready to initialize our database with an admin user, which we'll use to login to access our workflows in the webserver.

```bash
# We'll be prompted to enter a password
airflow users create \
    --username admin \
    --firstname FIRSTNAME \
    --lastname LASTNAME \
    --role Admin \
    --email EMAIL
```

#### Webserver

Once we've created a user, we're ready to launch the webserver and log in using our credentials.

```bash
# Launch webserver
source venv/bin/activate
export AIRFLOW_HOME=${PWD}/airflow
airflow webserver --port 8080  # http://localhost:8080
```

The webserver allows us to run and inspect workflows, establish connections to external data storage, manager users, etc. through a UI. Similarly, we could also use Airflow's [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) or [Command-line interface (CLI)](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html) to perform the same operations. However, we'll be using the webserver because it's convenient to visually inspect our workflows.

<div class="ai-center-all">
    <img src="https://madewithml.com/static/images/mlops/orchestration/webserver.png" width="700" alt="airflow webserver">
</div>

We'll explore the different components of the webserver as we learn about Airflow and implement our workflows.

#### Scheduler

Next, we need to launch our scheduler, which will execute and monitor the tasks in our workflows. The schedule executes tasks by reading from the metadata database and ensures the task has what it needs to finish running. We'll go ahead and execute the following commands on the *separate terminal* window:

```bash
# Launch scheduler (in separate terminal)
source venv/bin/activate
export AIRFLOW_HOME=${PWD}/airflow
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
airflow scheduler
```

### Extract and load

We're going to use the Airbyte connections we set up [above](#extract-via-airbyte) but this time we're going to programmatically trigger the data syncs with Airflow. First, let's ensure that Airbyte is running on a separate terminal in it's repository:

```bash
git clone https://github.com/airbytehq/airbyte.git  # skip if already create in data-stack lesson
cd airbyte
docker-compose up
```

Next, let's install the required packages and establish the connection between Airbyte and Airflow:

```bash
pip install apache-airflow-providers-airbyte==3.1.0
```

1. Go to the [Airflow webserver](http://localhost:8080/) and click `Admin` > `Connections` > ➕
2. Add the connection with the following details:
```yaml
Connection ID: airbyte
Connection Type: HTTP
Host: localhost
Port: 8000
```

> We could also establish connections [programmatically](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#connection-cli){:target=“_blank”} but it’s good to use the UI to understand what’s happening under the hood.

In order to execute our extract and load data syncs, we can use the [`AirbyteTriggerSyncOperator`](https://airflow.apache.org/docs/apache-airflow-providers-airbyte/stable/operators/airbyte.html):

```python linenums="1"
# airflow/dags/workflows.py
@dag(...)
def dataops():
    """Production DataOps workflows."""
    # Extract + Load
    extract_and_load_projects = AirbyteTriggerSyncOperator(
        task_id="extract_and_load_projects",
        airbyte_conn_id="airbyte",
        connection_id="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",  # REPLACE
        asynchronous=False,
        timeout=3600,
        wait_seconds=3,
    )
    extract_and_load_tags = AirbyteTriggerSyncOperator(
        task_id="extract_and_load_tags",
        airbyte_conn_id="airbyte",
        connection_id="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",  # REPLACE
        asynchronous=False,
        timeout=3600,
        wait_seconds=3,
    )

    # Define DAG
    extract_and_load_projects
    extract_and_load_tags
```

We can find the `connection_id` for each Airbyte connection by:

1. Go to our [Airbyte webserver](http://localhost:8000/) and click `Connections` on the left menu.
2. Click on the specific connection we want to use and the URL should be like this:
```bash
https://demo.airbyte.io/workspaces/<WORKSPACE_ID>/connections/<CONNECTION_ID>/status
```
3. The string in the `CONNECTION_ID` position is the connection's id.

We can trigger our DAG right now and view the extracted data be loaded into our BigQuery data warehouse but we'll continue developing and execute our DAG once the entire DataOps workflow has been defined.


### Validate via GE

The specific process of where and how we extract our data can be bespoke but what's important is that we have validation at every step of the way. We'll once again use [Great Expectations](https://greatexpectations.io/), as we did in our [testing lesson](https://madewithml.com/courses/mlops/testing#data), to [validate](https://madewithml.com/courses/mlops/testing#expectations) our extracted and loaded data before transforming it.

With the Airflow concepts we've learned so far, there are many ways to use our data validation library to validate our data. Regardless of what data validation tool we use (ex. [Great Expectations](https://greatexpectations.io/), [TFX](https://www.tensorflow.org/tfx/data_validation/get_started), [AWS Deequ](https://github.com/awslabs/deequ), etc.) we could use the BashOperator, PythonOperator, etc. to run our tests. However, Great Expectations has a [Airflow Provider package](https://github.com/great-expectations/airflow-provider-great-expectations) to make it even easier to validate our data. This package contains a [`GreatExpectationsOperator`](https://registry.astronomer.io/providers/great-expectations/modules/greatexpectationsoperator) which we can use to execute specific checkpoints as tasks.

```bash
pip install airflow-provider-great-expectations==0.1.1 great-expectations==0.15.19
great_expectations init
```

This will create the following directory within our data-engineering repository:

```bash
tests/great_expectations/
├── checkpoints/
├── expectations/
├── plugins/
├── uncommitted/
├── .gitignore
└── great_expectations.yml
```

#### Data source

But first, before we can create our tests, we need to define a new `datasource` within Great Expectations for our Google BigQuery data warehouse. This will require several packages and exports:

```bash
pip install pybigquery==0.10.2 sqlalchemy_bigquery==1.4.4
export GOOGLE_APPLICATION_CREDENTIALS=/Users/goku/Downloads/made-with-ml-XXXXXX-XXXXXXXXXXXX.json  # REPLACE
```

```bash
great_expectations datasource new
```
```bash
What data would you like Great Expectations to connect to?
    1. Files on a filesystem (for processing with Pandas or Spark)
    2. Relational database (SQL) 👈
```
```bash
What are you processing your files with?
1. MySQL
2. Postgres
3. Redshift
4. Snowflake
5. BigQuery 👈
6. other - Do you have a working SQLAlchemy connection string?
```

This will open up an interactive notebook where we can fill in the following details:
```yaml
datasource_name = “dwh"
connection_string = “bigquery://made-with-ml-359923/mlops_course”
```

#### Suite

Next, we can create a [suite of expectations](https://madewithml.com/courses/mlops/testing#suites) for our data assets:

```bash
great_expectations suite new
```

```bash
How would you like to create your Expectation Suite?
    1. Manually, without interacting with a sample batch of data (default)
    2. Interactively, with a sample batch of data 👈
    3. Automatically, using a profiler
```
```bash
Select a datasource
    1. dwh 👈
```
```bash
Which data asset (accessible by data connector "default_inferred_data_connector_name") would you like to use?
    1. mlops_course.projects 👈
    2. mlops_course.tags
```
```bash
Name the new Expectation Suite [mlops.projects.warning]: projects
```

This will open up an interactive notebook where we can define our expectations. Repeat the same for creating a suite for our tags data asset as well.

Expectations for `mlops_course.projects`:

```python linenums="1"
# data leak
validator.expect_compound_columns_to_be_unique(column_list=["title", "description"])
```
```python linenums="1"
# id
validator.expect_column_values_to_be_unique(column="id")

# create_on
validator.expect_column_values_to_not_be_null(column="created_on")

# title
validator.expect_column_values_to_not_be_null(column="title")
validator.expect_column_values_to_be_of_type(column="title", type_="STRING")

# description
validator.expect_column_values_to_not_be_null(column="description")
validator.expect_column_values_to_be_of_type(column="description", type_="STRING")
```

Expectations for `mlops_course.tags`:

```python linenums="1"
# id
validator.expect_column_values_to_be_unique(column="id")

# tag
validator.expect_column_values_to_not_be_null(column="tag")
validator.expect_column_values_to_be_of_type(column="tag", type_="STRING")
```

#### Checkpoints

Once we have our suite of expectations, we're ready to check [checkpoints](https://madewithml.com/courses/mlops/testing#checkpoints) to execute these expectations:

```bash
great_expectations checkpoint new projects
```

This will, of course, open up an interactive notebook. Just ensure that the following information is correct (the default values may not be):
```yaml
datasource_name: dwh
data_asset_name: mlops_course.projects
expectation_suite_name: projects
```

And repeat the same for creating a checkpoint for our tags suite.

#### Tasks

With our checkpoints defined, we're ready to apply them to our data assets in our warehouse.

```python linenums="1"
GE_ROOT_DIR = Path(BASE_DIR, "great_expectations")

@dag(...)
def dataops():
    ...
    validate_projects = GreatExpectationsOperator(
        task_id="validate_projects",
        checkpoint_name="projects",
        data_context_root_dir=GE_ROOT_DIR,
        fail_task_on_validation_failure=True,
    )
    validate_tags = GreatExpectationsOperator(
        task_id="validate_tags",
        checkpoint_name="tags",
        data_context_root_dir=GE_ROOT_DIR,
        fail_task_on_validation_failure=True,
    )

    # Define DAG
    extract_and_load_projects >> validate_projects
    extract_and_load_tags >> validate_tags
```

### Transform via dbt-core

Once we've validated our extracted and loaded data, we're ready to [transform](https://madewithml.com/courses/mlops/data-stack#transform) it. Our DataOps workflows are not specific to any particular downstream application so the transformation must be globally relevant (ex. cleaning missing data, aggregation, etc.). Just like in our [data stack lesson](https://madewithml.com/courses/mlops/data-stack), we're going to use [dbt](https://www.getdbt.com/) to transform our data. However, this time, we're going to do everything programmatically using the open-source [dbt-core](https://github.com/dbt-labs/dbt-core) package.

In the root of our data-engineering repository, initialize our dbt directory with the following command:
```bash
dbt init dbf_transforms
```
```bash
Which database would you like to use?
[1] bigquery 👈
```
```bash
Desired authentication method option:
[1] oauth
[2] service_account 👈
```
```yaml
keyfile: /Users/goku/Downloads/made-with-ml-XXXXXX-XXXXXXXXXXXX.json  # REPLACE
project (GCP project id): made-with-ml-XXXXXX  # REPLACE
dataset: mlops_course
threads: 1
job_execution_timeout_seconds: 300
```
```bash
Desired location option:
[1] US  👈  # or what you picked when defining your dataset in Airbyte DWH destination setup
[2] EU
```

#### Models

We'll prepare our dbt models as we did using the [dbt Cloud IDE](https://madewithml.com/courses/mlops/data-stack#dbt-cloud) in the previous lesson.

```bash
cd dbt_transforms
rm -rf models/example
mkdir models/labeled_projects
touch models/labeled_projects/labeled_projects.sql
touch models/labeled_projects/schema.yml
```

and add the following code to our model files:

```sql linenums="1"
-- models/labeled_projects/labeled_projects.sql
SELECT p.id, created_on, title, description, tag
FROM `made-with-ml-XXXXXX.mlops_course.projects` p  -- REPLACE
LEFT JOIN `made-with-ml-XXXXXX.mlops_course.tags` t  -- REPLACE
ON p.id = t.id
```

```yaml linenums="1"
# models/labeled_projects/schema.yml

version: 2

models:
    - name: labeled_projects
      description: "Tags for all projects"
      columns:
          - name: id
            description: "Unique ID of the project."
            tests:
                - unique
                - not_null
          - name: title
            description: "Title of the project."
            tests:
                - not_null
          - name: description
            description: "Description of the project."
            tests:
                - not_null
          - name: tag
            description: "Labeled tag for the project."
            tests:
                - not_null

```

And we can use the BashOperator to execute our dbt commands like so:

```python linenums="1"
DBT_ROOT_DIR = Path(BASE_DIR, "dbt_transforms")

@dag(...)
def dataops():
    ...
    # Transform
    transform = BashOperator(task_id="transform", bash_command=f"cd {DBT_ROOT_DIR} && dbt run && dbt test")

    # Define DAG
    extract_and_load_projects >> validate_projects
    extract_and_load_tags >> validate_tags
    [validate_projects, validate_tags] >> transform
```

#### Validate

And of course, we'll want to validate our transformations beyond dbt's built-in methods, using great expectations. We'll create a suite and checkpoint as we did above for our projects and tags data assets.
```bash
great_expectations suite new  # for mlops_course.labeled_projects
```

Expectations for `mlops_course.labeled_projects`:

```python linenums="1"
# data leak
validator.expect_compound_columns_to_be_unique(column_list=["title", "description"])
```

```python linenums="1"
# id
validator.expect_column_values_to_be_unique(column="id")

# create_on
validator.expect_column_values_to_not_be_null(column="created_on")

# title
validator.expect_column_values_to_not_be_null(column="title")
validator.expect_column_values_to_be_of_type(column="title", type_="STRING")

# description
validator.expect_column_values_to_not_be_null(column="description")
validator.expect_column_values_to_be_of_type(column="description", type_="STRING")

# tag
validator.expect_column_values_to_not_be_null(column="tag")
validator.expect_column_values_to_be_of_type(column="tag", type_="STRING")
```

```bash
great_expectations checkpoint new labeled_projects
```

```yaml
datasource_name: dwh
data_asset_name: mlops_course.labeled_projects
expectation_suite_name: labeled_projects
```

and just like how we added the validation task for our extracted and loaded data, we can do the same for our transformed data in Airflow:

```python linenums="1"
@dag(...)
def dataops():
    ...
    # Transform
    transform = BashOperator(task_id="transform", bash_command=f"cd {DBT_ROOT_DIR} && dbt run && dbt test")
    validate_transforms = GreatExpectationsOperator(
        task_id="validate_transforms",
        checkpoint_name="labeled_projects",
        data_context_root_dir=GE_ROOT_DIR,
        fail_task_on_validation_failure=True,
    )

    # Define DAG
    extract_and_load_projects >> validate_projects
    extract_and_load_tags >> validate_tags
    [validate_projects, validate_tags] >> transform >> validate_transforms
```

<hr>

Now we have our entire DataOps DAG define and executing it will prepare our data from extraction to loading to transformation (and with validation at every step of the way) for [downstream applications](https://madewithml.com/courses/mlops/data-stack#applications).

<div class="ai-center-all">
    <img src="https://madewithml.com/static/images/mlops/orchestration/dataops.png" width="700" alt="dataops">
</div>


## Learn more

Learn a lot more about data engineering, including infrastructure that we haven't covered in code here and how it's poised for downstream analytics and machine learning applications in our [data stack](https://madewithml.com/courses/mlops/data-stack/), [orchestration](https://madewithml.com/courses/mlops/orchestration/) and [feature store](https://madewithml.com/courses/mlops/feature-store/) lessons.