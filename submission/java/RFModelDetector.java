import org.apache.tika.detect.TrainedModelDetector;
import weka.classifiers.trees.RandomForest;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.Random;

/**
 * Created by minhpham on 3/1/16.
 */
public class RFModelDetector extends TrainedModelDetector {

    public RFModelDetector(File modelFile) throws FileNotFoundException {
        loadDefaultModels(new FileInputStream(modelFile));
    }

    @Override
    public void loadDefaultModels(InputStream inputStream) {
        try {
            RFTrainedModel rfTrainedModel = new RFTrainedModel(inputStream);
            super.registerModels(rfTrainedModel.getMediaType(), rfTrainedModel);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void loadDefaultModels(ClassLoader classLoader) {
        return;
    }

    public static void main(String[] args) throws FileNotFoundException {

    }
}
