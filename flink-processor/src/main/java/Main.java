import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.datastream.DataStreamSource;


public class Main {

        static final String BROKERS = "kafka:9092";
    
        public static void main(String[] args) throws Exception {
            StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
    
            KafkaSource<Event> source = KafkaSource.<Event>builder()
                .setBootstrapServers(BROKERS)
                .setProperty("partition.discovery.interval.ms", "1000")
                .setTopics("netflix-event")
                .setGroupId("groupdId-919292")
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new EventDeserializationSchema())
                .build();
    
            DataStreamSource<Event> kafka = env.fromSource(source, WatermarkStrategy.noWatermarks(), "kafka");
            
            DeviceGenreAggregator.aggregateViewsByDeviceAndGenre(kafka);
            GenderAgeGroupAggregator.aggregateViewsByGenderAndAgeGroup(kafka);
            LocationMRAggregator.aggregateViewsByLocationAndMR(kafka);
        
            env.execute("Netflix Event Processor");
        }
    }
    
