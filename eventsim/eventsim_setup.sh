echo "Building Eventsim Image..."
docker build -t events:1.0 .

echo "Running Eventsim in detached mode..."
docker run -itd \
  --network kafka-network \
  --name million_events \
  --memory="5.5g" \
  --memory-swap="7g" \
  --oom-kill-disable \
  --rm \
  events:1.0 \
    -c "examples/example-config.json" \
    --start-time "2024-09-01T00:00:00" \
    --end-time "2024-09-02T00:00:00" \
    --nusers 1000000 \
    --growth-rate 10 \
    --userid 1 \
    --kafkaBrokerList broker:19092 \
    --randomseed 1 \
    --continuous

echo "Started streaming events for 1 Million users..."
echo "Eventsim is running in detached mode. "
echo "Run 'docker logs --follow million_events' to see the logs."