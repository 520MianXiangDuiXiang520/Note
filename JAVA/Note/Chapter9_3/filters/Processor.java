package Note.Chapter9_3.filters;

public interface Processor {
    String name();
    Object process(Object input);
}
