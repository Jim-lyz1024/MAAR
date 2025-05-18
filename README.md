# MAAR: A Multimodal Benchmark for Animal Re-Identification with Environmental Metadata

## Introduction
The Metadata Augmented Animal Re-Identification (MAAR) dataset is a multimodal benchmark designed to improve animal re-identification (Animal ReID) by integrating environmental metadata with visual data. Unlike existing datasets that rely solely on images, MAAR includes 20,890 images spanning six representative species, each image is paired with metadata such as temperature and circadian rhythms, providing valuable context for distinguishing individual animals. Additionally, to facilitate the use of metadata in existing ReID methods, we propose the Meta-Feature Adapter (MFA), a lightweight module that can be incorporated into existing vision-language model (VLM)-based Animal ReID methods, allowing ReID models to leverage both environmental metadata and visual information to improve ReID performance. Our experiments on MAAR show that incorporating metadata with MFA consistently improves ReID performance over using visual data alone. We hope that our benchmark can inspire further exploration of multimodal approaches for Animal ReID.

## Data Availability
Our dataset is accessible through:
* [Hugging face](https://huggingface.co/datasets/uqtwei2/PlantWild)

## Supplementary Material
[Link to another page](./supplementary-material.html).
### Experiment Setting
#### 🚀 Baselines
We evaluate our approach using several state-of-the-art ReID methods:

- **CLIP-ReID**: Adapts CLIP for human and vehicle ReID, achieving state-of-the-art performance.  
- **ReID-AW**: A recent universal Animal ReID model that uses dynamic visual prompts and semantic knowledge from large language models.  
- **CLIP Fine-Tuning (CLIP-FT)**: A variant that fine-tunes only the CLIP image encoder without additional modifications.  
- **CLIP-ZeroShot (CLIP-ZS)**: Directly applies CLIP in a zero-shot setting for ReID.
---
#### 📈 Evaluation Metrics
Our evaluation employs two standard metrics in ReID tasks:

- **Mean Average Precision (mAP)**: Measures retrieval performance by calculating the average precision across all queries.  
- **Cumulative Matching Characteristic (CMC)**: Measures the rate at which the correct match appears within the top-$k$ nearest neighbors. We specifically report **CMC-1**.

Performance measures are averaged over **ten runs** with corresponding **95% confidence intervals**.

---
#### 📝 Reproducibility Details
- **Framework**: PyTorch  
- **Backbone**: ViT-B/16  
- **Optimizer**: Adam with a momentum of 0.9 and weight decay of $1 \times 10^{-4}$.  
- **Learning Rate**: Initial rate of $1 \times 10^{-6}$, decaying by a factor of 0.1 every 10 epochs.  
- **Training Epochs**: 50  
- **Batch Size**: 16  
- **Image Resolution**: $256 \times 128$  
- **Hardware**: NVIDIA Tesla A100 GPUs  




## Method
![MFA Architecture](fig/MFA.png)

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

## Training
```python
python train_mfareid.py --config_file configs/animal/vit_mfareid.yml
```
<!-- For inquiries about early access to the dataset for research purposes, please contact [contact information]. -->