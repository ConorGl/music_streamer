CREATE TABLE `pageviews` (
    `url` STRING,
    `user_id` STRING,
    `browser` STRING,
    `ts` TIMESTAMP(3)
)
WITH (
    'connector' = 'faker',
    'rows-per-second' = '10',
    'fields.url.expression' = '/#{GreekPhilosopher.name}.html',
    'fields.user_id.expression' = '#{numerify ''user_##''}',
    'fields.browser.expression' = '#{Options.option ''chrome'', ''firefox'', ''safari'')}',
    'fields.ts.expression' =  '#{date.past ''5'',''1'',''SECONDS''}'
);
