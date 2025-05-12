# MAAR: A Multimodal Benchmark for Animal Re-Identification with Environmental Metadata

## Abstract
Identifying individual animals within large wildlife populations is essential for effective wildlife monitoring and conservation efforts. Recent advancements in computer vision have shown promise in animal re-identification (Animal ReID) by leveraging data from camera traps. However, existing Animal ReID datasets rely exclusively on visual data, overlooking environmental metadata that ecologists have identified as highly correlated with animal behavior and identity, such as temperature and circadian rhythms. Moreover, the emergence of multimodal models capable of jointly processing visual and textual data presents new opportunities for Animal ReID, but existing benchmarks fail to leverage these models' text-processing capabilities, limiting their full potential. To address these limitations, we present the Metadata Augmented Animal Re-Identification (MAAR) dataset, a multimodal Animal ReID benchmark pairing images with environmental metadata extracted from embedded camera trap overlays and scene contexts. MAAR contains 20,890 images spanning six representative species, providing a robust resource for systematically evaluating multimodal approaches in Animal ReID. Additionally, to facilitate the use of metadata in existing ReID methods, we propose the Meta-Feature Adapter (MFA), a lightweight module that can be incorporated into existing vision-language model (VLM)-based Animal ReID methods, allowing ReID models to leverage both environmental metadata and visual information to improve ReID performance. Experiments on MAAR show that combining baseline ReID models with MFA to incorporate metadata consistently improves performance compared to using visual information alone, validating the effectiveness of incorporating metadata in re-identification. We hope that our benchmark can inspire further exploration of multimodal approaches for Animal ReID.


## Data Availability
Our dataset is accessible through:
* [Hugging face](https://huggingface.co/datasets/uqtwei2/PlantWild)

## Supplementary Material

## Architecture
<!-- ![MFA Architecture](fig/method.png) -->

## Installation
```
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
```
python train_mfareid.py --config_file configs/animal/vit_mfareid.yml
```
<!-- For inquiries about early access to the dataset for research purposes, please contact [contact information]. -->