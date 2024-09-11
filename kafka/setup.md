# Setting up the Kafka Cluster
The docker-compose file will handle most of the local setup. The thing that was annoying to deal with was M2 silicon so I had to independently pull all the images with `--platform linux/arm64`.

```commandline
docker compose up --build --detach
```

Currently the docker compose file is set up to manage everything locally.

To test that kafka is working correctly please go to the command centre bundled with the docker-compose file by visiting `http://localhost:9021`. Create a python virtual env, install the requirements and then run

```commandline
python test_setup.py
python test_producer.py
```

The producer will run and output success logs as it loads messages into the topic `test-topic` which can be verified from within the command center.