# Experiment Setting
## 🚀 Baselines
We evaluate our approach using several state-of-the-art ReID methods:

- **CLIP-ReID**: Adapts CLIP for human and vehicle ReID, achieving state-of-the-art performance.  
- **ReID-AW**: A recent universal Animal ReID model that uses dynamic visual prompts and semantic knowledge from large language models.  
- **CLIP Fine-Tuning (CLIP-FT)**: A variant that fine-tunes only the CLIP image encoder without additional modifications.  
- **CLIP-ZeroShot (CLIP-ZS)**: Directly applies CLIP in a zero-shot setting for ReID.

---

## 📈 Evaluation Metrics
Our evaluation employs two standard metrics in ReID tasks:

- **Mean Average Precision (mAP)**: Measures retrieval performance by calculating the average precision across all queries.  
- **Cumulative Matching Characteristic (CMC)**: Measures the rate at which the correct match appears within the top-$k$ nearest neighbors. We specifically report **CMC-1**.

Performance measures are averaged over **ten runs** with corresponding **95% confidence intervals**.

---

## 📝 Reproducibility Details
- **Framework**: PyTorch  
- **Backbone**: ViT-B/16  
- **Optimizer**: Adam with a momentum of 0.9 and weight decay of $1 \times 10^{-4}$.  
- **Learning Rate**: Initial rate of $1 \times 10^{-6}$, decaying by a factor of 0.1 every 10 epochs.  
- **Training Epochs**: 50  
- **Batch Size**: 16  
- **Image Resolution**: $256 \times 128$  
- **Hardware**: NVIDIA Tesla A100 GPUs