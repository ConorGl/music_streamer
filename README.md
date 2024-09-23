# music_streamer

- Dealing with old JARs is not my forte so `eventsim/` folder completely copied over
- [Eventsim](https://github.com/Interana/eventsim) is used to generate event data that replicates page requests for a fake music website. The results mimic real user data but are entirely synthetic. This project uses a [subset](http://millionsongdataset.com/pages/getting-dataset/#subset) of 10,000 songs from the Million Songs Dataset to generate events.

    --start-time "`date +"%Y-%m-%dT%H:%M:%S"`" \
    --end-time "`date --date="tomorrow" +"%Y-%m-%dT%H:%M:%S"`" \

# Setting up the Kafka Cluster
The docker-compose file will handle most of the local setup. The thing that was annoying to deal with was M2 silicon so I had to independently pull all the images with `--platform linux/arm64`.

```commandline
docker compose up --build --detach
```

Currently the docker compose file is set up to manage everything locally.
Create a python virtual env, install the requirements and then run

```commandline
python kafka/components/test_setup.py
python kafka/components/test_producer.py
```

The producer will run and output success logs as it loads messages into the topic `test-topic` which can be verified using kafka cli command
```commandline
kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic
```

# Setting up Flink
Flink is also within the docker-compose file. You can access to the [Web UI](http://localhost:8081/#/overview).

In order to run a SQL client you can run the command

```commandline
docker compose run --rm sql-client
```

In order to run a test and check that things are working correct firstly ensure that the `pageviews` topic exists within kafka by running

```commandline
kafka-topics --bootstrap-server localhost:9092 --topic pageviews --create --partitions 1 --replication-factor 1
```
 *NOTE* the partitions and replication factor are 1 at the moment as there is only a single broker created but the docker-compose can be amended to deal with this.

Next please create both tables in `flink/test_sql_scripts` then once created run the SQL statements:

```sql
select * from pageviews; -- This statement should show up within the SQL client
insert into pageviews_kafka select * from pageviews; -- This statement will require looking at kafka in order to check it is running
```

You can check that the `pageviews` sink is running correctly in two places. Firstly by using 
```commandline
kafka-console-consumer --bootstrap-server localhost:9092 --topic pageviews
```
and checking the output is as expected. Secondly by visiting the flink [Web UI](http://localhost:8081/#/overview) and navigating to the correct space.