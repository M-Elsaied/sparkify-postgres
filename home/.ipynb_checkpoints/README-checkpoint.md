![Logo of the project](https://860793.smushcdn.com/1993727/wp-content/uploads/2020/05/2EfCIIF.png?size=580x290&lossy=1&strip=1&webp=1)

# Data Modeling with Postgres
> Sparkify Analytics Warehouse

In this project, we apply what we've learned on data modeling with Postgres and build an ETL pipeline using Python. We define fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.

## Installing / Getting started

A quick introduction of the minimal setup you need to get Sparkify Warehouse up &
running.

```shell
git clone https://github.com/M-Elsaied/potgres-project.git
cd postgres-project/
```

## Run the code

You will need to have postgres setup on your local machine, there 
are 2 main functions `create_tables.py` that creates the tables 
and `etl.py` that runs the ETL pipeline and inserts the data into your tables

```shell
python3 create_tables.py
python3 etl.py
```

## Features

What's all the bells and whistles this project can perform?
* Transforms the raw log and songs data into analytics ready warehouse
* All the data are represented in a star schema
* Makes understanding what songs users listen to an easy task for data anaylsts to answer


#### Data
Type: `String`  
Default: `'default value'`

The data are in a folder `data` that has `songs` and `logs` each of them
have `JSON` files that the program use. The path to the data is hard coded in
`etl.py` 


## Licensing

One really important part: Give your project a proper license. Here you should
state what the license is and how to find the text version of the license.
Something like:

"The code in this project is licensed under MIT license."
