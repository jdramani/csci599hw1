import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.IntBuffer;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.filefilter.TrueFileFilter;
import org.apache.tika.Tika;
import org.apache.tika.io.TikaInputStream;
import org.apache.tika.mime.MediaType;


public class TypeDetection {

    //    static String from = "/Users/minhpham/data";
    static String from = "/Users/minhpham/projects/data1/";
    static String to = "/Users/minhpham/projects/data1/";
    private Tika tika = new Tika();
    private HashMap<String, Integer> typeCountMap = new HashMap<String, Integer>();
    RFModelDetector detector = new RFModelDetector(new File("rf.model"));


    public TypeDetection() throws IOException {

        final File folder = new File(from);

        Files.walkFileTree(folder.toPath(), new ClassifyFileVisitor());


        for (String type : typeCountMap.keySet()) {
            System.out.printf("%s: %d\n", type, typeCountMap.get(type));
        }
    }

    public static void main(String[] args) throws Exception {
        new TypeDetection();
    }

    private class ClassifyFileVisitor extends SimpleFileVisitor<Path> {

        @Override
        public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
            File fileEntry = file.toFile();

//            MediaType mediaType = detector.detect(TikaInputStream.get(fileEntry), null);
//
//            String type = mediaType.getType() + "/" + mediaType.getSubtype();

//            System.out.println(type);

            String type = tika.detect(fileEntry);

//            File mimeFolder = new File(to, type.replace("/", "-"));
//            if (!mimeFolder.exists()) {
//                mimeFolder.mkdirs();
//            }

//            File newFile = new File(mimeFolder, fileEntry.getName());
//
//            Files.move(fileEntry.toPath(), newFile.toPath());

            if (typeCountMap.containsKey(type)) {
                typeCountMap.put(type, typeCountMap.get(type) + 1);
            } else {
                typeCountMap.put(type, 1);
            }


            return FileVisitResult.CONTINUE;
        }

        @Override
        public FileVisitResult visitFileFailed(Path file, IOException exc) throws IOException {
            return FileVisitResult.CONTINUE;
        }

        @Override
        public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
            return FileVisitResult.CONTINUE;
        }
    }
}