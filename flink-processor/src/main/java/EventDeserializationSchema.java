/*
- When your Flink application receives a Kafka message, the message comes as a byte array.
- Flink uses EventDeserializationSchema to turn those bytes into an Event object.
- It does this by using the Jackson library's ObjectMapper to interpret the bytes as JSON and map them to the structure of the Event class.
- This deserialized Event object is then passed through your Flink application for further processing.
*/


import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.json.JsonMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import java.io.IOException;
import org.apache.flink.api.common.serialization.AbstractDeserializationSchema;

// EventDeserializationSchema which extends AbstractDeserializationSchema provided by Flink, parameterized with the type Event.
// This means your custom schema will be converting to Event objects.
public class EventDeserializationSchema extends AbstractDeserializationSchema<Event> {

  // unique identifier for the class's version used in serialization and deserialization
  private static final long serialVersionUUID = 1L;

  // declares an ObjectMapper, which is a Jackson class for JSON processing. The keyword transient indicates that this field should not be serialized.
  private transient ObjectMapper objectMapper;

  @Override
  public void open(InitializationContext context) {
    objectMapper = JsonMapper.builder().build().registerModule(new JavaTimeModule());
  }

  @Override
  // this method is overridden from AbstractDeserializationSchema and is where the actual deserialization happens.
  public Event deserialize(byte[] message) throws IOException {
    // uses the ObjectMapper to convert the byte array (message) into an Event object.
    return objectMapper.readValue(message, Event.class);
  }
}