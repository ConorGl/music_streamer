# Eventsim

As detailed in the README this is the event generator. In order to set up please change to this working directory and run:

```commandline
bash eventsim_setup.sh
```

This will set up and run the eventsim locally to produce some message. Navigate to the kafka command centre in order to see the production at play, otherwise you can follow the direct logs from the docker machine at `docker logs --follow million_events`