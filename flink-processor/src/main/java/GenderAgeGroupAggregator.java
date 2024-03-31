import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.KeyedStream;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import org.apache.flink.api.java.tuple.Tuple4;
import org.apache.flink.connector.jdbc.JdbcSink;
import org.apache.flink.connector.jdbc.JdbcExecutionOptions;
import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
import java.sql.Timestamp;


public class GenderAgeGroupAggregator {

    public static String getAgeGroup(int age) {
        int lowerBound = (age / 10) * 10;
        return lowerBound + "-" + (lowerBound + 9);
    }

    public static void aggregateViewsByGenderAndAgeGroup(DataStream<Event> eventsStream) {
        KeyedStream<Tuple3<String, String, Integer>, Tuple2<String, String>> keyedStream = eventsStream
            .map(event -> new Tuple3<>(event.UserGender, getAgeGroup(event.UserAge), 1))
            .returns(Types.TUPLE(Types.STRING, Types.STRING, Types.INT))
            .keyBy(new KeySelector<Tuple3<String, String, Integer>, Tuple2<String, String>>() {
                @Override
                public Tuple2<String, String> getKey(Tuple3<String, String, Integer> value) {
                    return new Tuple2<>(value.f0, value.f1);
                }
            });

        DataStream<Tuple4<String, String, Integer, String>> viewsByGenderAgeGroup = keyedStream
            .window(TumblingProcessingTimeWindows.of(Time.seconds(300)))
            .reduce((value1, value2) -> new Tuple3<>(value1.f0, value1.f1, value1.f2 + value2.f2),
                new ProcessWindowFunction<Tuple3<String, String, Integer>, Tuple4<String, String, Integer, String>, Tuple2<String, String>, TimeWindow>() {
                    @Override
                    public void process(Tuple2<String, String> key, Context context, Iterable<Tuple3<String, String, Integer>> elements, Collector<Tuple4<String, String, Integer, String>> out) {
                        Tuple3<String, String, Integer> result = elements.iterator().next();
                        String windowEndTime = String.valueOf(context.window().getEnd());
                        out.collect(new Tuple4<>(result.f0, result.f1, result.f2, windowEndTime));
                    }
                });

            viewsByGenderAgeGroup.addSink(JdbcSink.sink(
            "insert into viewsByGenderAgeGroupAggregation (gender, age_group, view_count, window_end_utctime) values (?, ?, ?, ?)",
            (statement, tuple) -> {
                statement.setString(1, tuple.f0);
                statement.setString(2, tuple.f1);
                statement.setInt(3, tuple.f2);

                long windowEndTimeMillis = Long.parseLong(tuple.f3);
                Timestamp windowEndTimestamp = new Timestamp(windowEndTimeMillis);
                statement.setTimestamp(4, windowEndTimestamp);
            },
            JdbcExecutionOptions.builder()
                .withBatchSize(1000)
                .withBatchIntervalMs(200)
                .withMaxRetries(5)
                .build(),
            new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
                .withUrl("jdbc:postgresql://host.docker.internal:5438/postgres")
                .withDriverName("org.postgresql.Driver")
                .withUsername("postgres")
                .withPassword("postgres")
                .build()
        ));
    }
}
