# pylint: disable=import-error
# pylint: disable=no-name-in-module

from collections import defaultdict

from train.utils import polarity, calculate_acc


class SentimentPseudoLabeler:
    """
    Generate pseudo labels for unlabeled data using unsupervised and semi-supervised models.

    Attributes:
        to_calc_acc (list): Store predicted and ground truth labels to calculate accuracy 
                            batch-wise.
        collection (dict): Dictionary containing both predictions and confidence score for
                            same text.

    Constants:
        ADAPTIVE_UNSUPERVISED_PREDICTION_WEIGHT: Dynamic weight for unsupervised model for 
                                                ensembled predictions.
        ADAPTIVE_SEMI_SUPERVISED_PREDICTION_WEIGHT: Dynamic weight for semi-supervised model for 
                                                ensembled predictions.
    """
    ADAPTIVE_UNSUPERVISED_PREDICTION_WEIGHT = 0.5
    ADAPTIVE_SEMI_SUPERVISED_PREDICTION_WEIGHT = 0.5

    def __init__(self):
        """
        Initialize class to generate pseudo labels.
        """
        self.to_calc_acc = []
        self.collector = defaultdict(dict)

    def get_confidence_score(self, data):
        """
        Calculate confidence score for final prediction from both learning methods.

        Args:
            data (dict): Contains predicted results of both models.
                            - {'us': [us_conf, us_pred, text], 'ss': [ss_conf, ss_pred, label]}

        Returns:
            float: Confidence score of final prediction.
        """

        # Calculate unsupervised model's weighted confidence.
        us_conf = data['us'][0] * polarity(data['us'][1]) * \
            SentimentPseudoLabeler.ADAPTIVE_UNSUPERVISED_PREDICTION_WEIGHT

        # Calculate semi-supervised model's weighted confidence.
        ss_conf = data['ss'][0] * polarity(data['ss'][1]) * \
            SentimentPseudoLabeler.ADAPTIVE_SEMI_SUPERVISED_PREDICTION_WEIGHT

        # Store final prediction to calculate sentistream's accuracy.
        self.to_calc_acc.append([
            [data['ss'][2]], [data['us'][1] if us_conf > ss_conf else data['ss'][1]]])

        return us_conf + ss_conf

    def get_model_acc(self):
        """
        Calculate model's final predictions' accuracy.

        Returns:
            float: Accuracy of final output.
        """
        if self.to_calc_acc:
            acc = calculate_acc(self.to_calc_acc)
            self.to_calc_acc = []
            return acc
        return None

    def generate_pseudo_label(self, us_output, ss_output):
        """
        Generate pseudo label for incoming output from both models.

        Args:
            us_output (tuple): contains data from unsupervised model's output.
                                - us_idx: index of outputs from unsupervised model.
                                - us_flag: indicates unsupervised model's output.
                                - us_conf: unsupervised model's confidence for predicted label.
                                - us_pred: unsupervised model's prediction.
                                - text: text data / review.
            ss_output (tuple): contains data from semi-supervised model's output.
                                - ss_idx: index of outputs from semi-supervised model.
                                - ss_flag: indicates semi-supervised model's output.
                                - ss_conf: semi-supervised model's confidence for predicted label.
                                - ss_pred: semi-supervised model's prediction.
                                - label: ground truth label.

        Returns:
            list: pseudo label for current data.
        """

        # Store outputs in dictionary to map them easily.
        if us_output:
            self.collector[us_output[0]][us_output[1]] = us_output[2:]
        if ss_output:
            self.collector[ss_output[0]][ss_output[1]] = ss_output[2:]

        output = []

        if ss_output and len(self.collector[ss_output[0]]) == 2:
            conf = self.get_confidence_score(self.collector[ss_output[0]])
            output.append(self.get_pseudo_label(conf, ss_output[0]))
        if us_output and len(self.collector[us_output[0]]) == 2:
            conf = self.get_confidence_score(self.collector[us_output[0]])
            output.append(self.get_pseudo_label(conf, us_output[0]))

        return output

    def get_pseudo_label(self, conf, key):
        """
        Generate pseudo label based on finalized confidence score.

        Args:
            conf (float): Model's finalized confidence score.
            key (int): Key for dictionary of predicted outputs.

        Returns:
            str or list: 'LOW_CONFIDENCE' if confidence score is too low to make it as pseudo label,
                        else, model's predicted senitment along with text.
        """

        text = self.collector[key]['us'][2]

        # Delete item from collector to avoid re-generating labels.
        del self.collector[key]

        return 'LOW_CONFIDENCE' if -0.5 < conf < 0.5 else [1 if conf >= 0.5 else 0, text]
