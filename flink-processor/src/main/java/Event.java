import java.util.Objects;

// declare Event class
public class Event {
    public String EventId;
    public String UserId;
    public String UserName;
    public int UserAge;
    public String UserGender;
    public String UserLocation;
    public String DeviceType;
    public String ContentType;
    public String ContentID;
    public String ContentName;
    public String Genre;
    public int ReleaseYear;
    public int ContentLength;
    public String Language;
    public String MaturityRating;
    public String EventTimestamp;

    // instantiation of an Event object without setting any fields initially.
    public Event() {}
    
    // parameterized constructor that initializes an Event object with specific values for each field.
    // It’s useful for creating an Event object with all its details in one go.
    public Event(String EventId, String UserId, String UserName, int UserAge, String UserGender, String UserLocation, String DeviceType, String ContentType, String ContentID, String ContentName, String Genre, int ReleaseYear, int ContentLength, String Language, String MaturityRating, int EpisodeNumber, String EventTimestamp) {
        this.EventId = EventId;
        this.UserId = UserId;
        this.UserName = UserName;
        this.UserAge = UserAge;
        this.UserGender = UserGender;
        this.UserLocation = UserLocation;
        this.DeviceType = DeviceType;
        this.ContentType = ContentType;
        this.ContentID = ContentID;
        this.ContentName = ContentName;
        this.Genre = Genre;
        this.ReleaseYear = ReleaseYear;
        this.ContentLength = ContentLength;
        this.Language = Language;
        this.MaturityRating = MaturityRating;
        this.EventTimestamp = EventTimestamp;
    }

    @Override
    // returns a string representation of the Event object, which is useful for logging or debugging.
    public String toString() {
        final StringBuilder sb = new StringBuilder("Event{");
        sb.append("EventId='").append(EventId).append('\'');
        sb.append(", UserId='").append(UserId).append('\'');
        sb.append(", UserName='").append(UserName).append('\'');
        sb.append(", UserAge=").append(UserAge);
        sb.append(", UserGender='").append(UserGender).append('\'');
        sb.append(", UserLocation='").append(UserLocation).append('\'');
        sb.append(", DeviceType='").append(DeviceType).append('\'');
        sb.append(", ContentType='").append(ContentType).append('\'');
        sb.append(", ContentID='").append(ContentID).append('\'');
        sb.append(", ContentName='").append(ContentName).append('\'');
        sb.append(", Genre='").append(Genre).append('\'');
        sb.append(", ReleaseYear=").append(ReleaseYear);
        sb.append(", ContentLength=").append(ContentLength);
        sb.append(", Language='").append(Language).append('\'');
        sb.append(", MaturityRating='").append(MaturityRating).append('\'');
        sb.append(", EventTimestamp='").append(EventTimestamp).append('\'');
        sb.append('}');
        return sb.toString();
    }

    // calculates a hash code for the Event object based on its fields.
    // This is important for using Event objects in hash-based collections like HashMap or HashSet
    public int hashCode() {
        // The Objects.hash() method is a utility method in Java that generates a hash code based on the values of the fields you pass to it.
        return Objects.hash(super.hashCode(), EventId, UserId, UserName, UserAge, UserGender, UserLocation, DeviceType, ContentType, ContentID, ContentName, Genre, ReleaseYear, ContentLength, Language, MaturityRating, EventTimestamp);
    }
}


