# Experiment Setting
## Baselines
We evaluate our approach using several state-of-the-art ReID methods:

- **CLIP-ReID**: Adapts CLIP for human and vehicle ReID, achieving state-of-the-art performance.  
- **ReID-AW**: A recent universal Animal ReID model that uses dynamic visual prompts and semantic knowledge from large language models.  
- **CLIP Fine-Tuning (CLIP-FT)**: A variant that fine-tunes only the CLIP image encoder without additional modifications.  
- **CLIP-ZeroShot (CLIP-ZS)**: Directly applies CLIP in a zero-shot setting for ReID.


## Evaluation Metrics
Our evaluation employs two standard metrics in ReID tasks:

- **Mean Average Precision (mAP)**: Measures retrieval performance by calculating the average precision across all queries.  
- **Cumulative Matching Characteristic (CMC)**: Measures the rate at which the correct match appears within the top-k nearest neighbors. We specifically report **CMC-1**.

Performance measures are averaged over **ten runs** with corresponding **95% confidence intervals**.

## Reproducibility Details
- **Framework**: PyTorch  
- **Backbone**: ViT-B/16  
- **Optimizer**: Adam with a momentum of 0.9 and weight decay of 1 × 10⁻⁴.  
- **Learning Rate**: Initial rate of 1 × 10⁻⁶, decaying by a factor of 0.1 every 10 epochs.  
- **Training Epochs**: 50  
- **Batch Size**: 16  
- **Image Resolution**: 256 × 128  
- **Hardware**: NVIDIA Tesla A100 GPUs

## Installation
```python
conda create -n 'your-env-name' python=3.8
conda activate 'your-env-name'
conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=10.2 -c pytorch
pip install yacs
pip install timm
pip install scikit-image
pip install tqdm
pip install ftfy
pip install regex
```

To reproduce the animal re-identification experiments, use the following command:
```python
python train_mfareid.py --config_file configs/animal/vit_mfareid.yml
```
This command launches the training process for the MFA framework using the ViT backbone. The configuration file ``vit_mfareid.yml`` contains all necessary hyperparameters and training settings.

### Configuration Details
```yaml
IMS_PER_BATCH: 16        # Training batch size
OPTIMIZER_NAME: "Adam"
BASE_LR: 0.000001        # Learning rate
WARMUP_METHOD: 'linear'
WARMUP_ITERS: 10
WARMUP_FACTOR: 0.1
WEIGHT_DECAY:  0.0001
WEIGHT_DECAY_BIAS: 0.0001
MAX_EPOCHS: 50           # Maximum training epochs
CHECKPOINT_PERIOD: 50
LOG_PERIOD: 10
EVAL_PERIOD: 50          # Evaluation frequency
```

The configuration file allows for precise control of the training process parameters. The training batch size is set through ``IMS_PER_BATCH``, which we configured as 16 for our experiments. The learning rate is managed by ``BASE_LR``, and the total training duration is controlled by ``MAX_EPOCHS``, with our experiments running for 50 epochs. The ``EVAL_PERIOD`` parameter determines how frequently the model's performance is evaluated during training, which we set to 50 epochs to align with our experimental requirements. The configuration file also includes additional parameters for model architecture, input preprocessing, and optimisation settings, which remained constant throughout our experimental evaluation. The configuration file also specifies dataset paths and species selection for our experiments on the MAAR dataset. For example, we can use the following command to evaluate the model ReID performance using images of Hare.
```yaml
DATASETS:
  NAMES: ('hare')    # Target species for training/evaluation
  ROOT_DIR: ('/data')  # Dataset root directory
OUTPUT_DIR: '/data/Hare/MFA-ReID'  # Results output path
```
For intra-species experiments, we modify the ``NAMES`` parameter to specify which of the six species (Deer, Hare, Penguin, Pūkeko, Stoat, or Wallaby) to use for training and evaluation, along with its corresponding data directory. For inter-species experiments, we created combined datasets that also need to be specified in the ``NAMES`` parameter. For instance, to obtain the results of inter-species re-identification, we created a training set by merging all images from three source species (Deer, Hare, and Penguin), while validation was performed using the original query and gallery sets from the remaining three species (Stoat, Pūkeko, and Wallaby).