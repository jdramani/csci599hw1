import org.apache.tika.mime.MediaType;
import weka.classifiers.trees.RandomForest;
import weka.core.Attribute;
import weka.core.DenseInstance;
import weka.core.Instance;
import weka.core.Instances;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Created by minhpham on 3/1/16.
 */
public class ModelTrainer {

    private RandomForest randomForest;
    private String type;

    public ModelTrainer(String type) throws FileNotFoundException {
        this.type = type;
    }

    public double[] getBFA(File file, int label) throws IOException {
        FileInputStream in = new FileInputStream(file);

        int c;

        double[] bfa = new double[256];

        while ((c = in.read()) != -1) {
            bfa[c]++;
        }

        double max = 0;

        for (double d : bfa) {
            if (max < d) max = d;
        }

        double[] result = new double[257];


        for (int i = 0; i < 256; i++) {
            result[i] = bfa[i] * 1.0 / max;
        }

        result[256] = label;

        in.close();
        return result;
    }

    public void trainAndSave(String type, String folderPath) throws Exception {

        File folder = new File(folderPath);

        ArrayList<Attribute> attributeList = new ArrayList<Attribute>();

        for (int i = 1; i <= 257; i++) {
            Attribute attribute = new Attribute(i + "");
            attributeList.add(attribute);
        }

        Instances trainingData = new Instances("training", attributeList, 1000);
        int count = 0;
        for (File subFolder : folder.listFiles()) {
            Instance instance;

            if (subFolder.isFile()) continue;

            if (subFolder.getName().equals(type)) {
                for (File file : subFolder.listFiles()) {
                    instance = new DenseInstance(1, getBFA(file, 1));
                    instance.setDataset(trainingData);
                    trainingData.add(instance);
                }
            } else {
                File[] files = subFolder.listFiles();
                if (count < 10) {
                    count++;
                    if (files.length / 10 >= 100) {
                        for (int i = 0; i < 100; i++) {
                            instance = new DenseInstance(1, getBFA(files[i], 0));
                            instance.setDataset(trainingData);
                            trainingData.add(instance);
                        }
                    }
                }
            }

        }

        trainingData.setClassIndex(256);

        randomForest = new RandomForest();
        randomForest.setOptions(new String[]{"-I", "500",});
        randomForest.buildClassifier(trainingData);

        MediaType mediaType = MediaType.parse(type);

        weka.core.SerializationHelper.writeAll("rf.model", new Object[]{mediaType, randomForest});
    }

    public static void main(String[] args) throws Exception {
        ModelTrainer modelTrainer = new ModelTrainer("video-mp4");
        modelTrainer.trainAndSave("video/mp4", "/Users/minhpham/projects/data1");
    }
}
