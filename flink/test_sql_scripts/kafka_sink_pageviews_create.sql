CREATE TABLE pageviews_kafka (
    `url` STRING,
    `user_id` STRING,
    `browser` STRING,
    `ts` TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'pageviews',
    'properties.group.id' = 'demoGroup',
    'scan.startup.mode' = 'earliest-offset',
    'properties.bootstrap.servers' = 'broker:19092',
    'value.format' = 'json',
    'sink.partitioner' = 'fixed'
);