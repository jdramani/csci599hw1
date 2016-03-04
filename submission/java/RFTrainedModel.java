import org.apache.tika.detect.TrainedModel;
import org.apache.tika.mime.MediaType;
import weka.classifiers.trees.RandomForest;
import weka.core.Attribute;
import weka.core.DenseInstance;
import weka.core.Instance;
import weka.core.Instances;

import java.io.FileInputStream;
import java.io.InputStream;
import java.util.ArrayList;

/**
 * Created by minhpham on 3/1/16.
 */
public class RFTrainedModel extends TrainedModel {

    private RandomForest randomForest;
    private MediaType mediaType;

    public RFTrainedModel(InputStream inputStream) throws Exception {
        Object[] objects = weka.core.SerializationHelper.readAll(inputStream);
        mediaType = (MediaType) objects[0];
        randomForest = (RandomForest) objects[1];
    }

    @Override
    public double predict(double[] doubles) {
        Instance instance = new DenseInstance(1, doubles);
        try {
            double prob = randomForest.classifyInstance(instance);
            return 1 - prob;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return 0;
    }

    public MediaType getMediaType() {
        return mediaType;
    }

    @Override
    public float predict(float[] floats) {

        ArrayList<Attribute> attributeList = new ArrayList<Attribute>();

        for (int i = 1; i <= 257; i++) {
            Attribute attribute = new Attribute(i + "");
            attributeList.add(attribute);
        }

        Instances testingData = new Instances("testing", attributeList, 1000);

        testingData.setClassIndex(256);

        double[] doubles = new double[floats.length];

        for(int i = 0; i < doubles.length; i++){
            doubles[i] = floats[i];
        }

        Instance instance = new DenseInstance(1, doubles);
        instance.setDataset(testingData);
        testingData.add(instance);
        try {
            double prob = randomForest.classifyInstance(instance);
            return (float) (1 - prob);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return 0;
    }
}
