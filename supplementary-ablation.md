# Supplementary Material: Ablation Study
## **Effect of Fusion Strategies**
To investigate the effect of different fusion strategies for integrating metadata with visual features in our ReID models, we conducted a comprehensive ablation study. We compared three fusion approaches:

- **Basic Fusion (BF)**: This approach directly concatenates metadata embeddings with visual features, followed by a linear projection layer. It provides a simple integration method without any interaction between the two modalities.

- **Cross-Attention (CA)**: This strategy allows feature interaction by computing attention weights between metadata and visual features. This approach enables the model to dynamically focus on relevant metadata information.

- **Gated Cross-Attention (GCA)**: Our proposed method further enhances cross-attention by introducing an adaptive gating mechanism. This gate dynamically adjusts the influence of metadata based on the relevance of visual content, allowing the model to balance between visual and metadata information.

The results of this comparison are presented in **Table 1**. Basic Fusion (BF) provides modest improvements across species, such as a **1.5% mAP gain on Deer** for the CLIP-FT model. Cross-Attention (CA) further enhances performance, particularly on datasets like Penguin, with **0.3% and 1.3% mAP improvements** for CLIP-FT and CLIP-ReID, respectively. Our Gated Cross-Attention (GCA) achieves the best results, consistently outperforming both BF and CA. For instance, GCA leads to a **2.5% mAP gain over BF** on Wallaby using the ReID-AW model. This improvement can be attributed to GCA's ability to adaptively control metadata influence based on visual content relevance. When visual features are highly distinctive, the gate reduces reliance on metadata, while for visually ambiguous cases, the gate increases metadata influence.

| Model      | Strategy | Deer (mAP) | Deer (CMC-1) | Hare (mAP) | Hare (CMC-1) | Penguin (mAP) | Penguin (CMC-1) | Pūkeko (mAP) | Pūkeko (CMC-1) | Stoat (mAP) | Stoat (CMC-1) | Wallaby (mAP) | Wallaby (CMC-1) |
|-------------|-----------|-------------|---------------|-------------|---------------|----------------|------------------|----------------|----------------|---------------|-----------------|------------------|------------------|
| CLIP-FT     | BF        | 64.2±.4      | 93.8±.3        | 56.1±.2      | 90.2±.4        | 44.5±.3         | 62.4±.3           | 57.2±.2         | 79.1±.3         | 67.2±.2        | 89.6±.4           | 55.3±.2           | 88.9±.2           |
|              | CA        | 66.5±.2      | 94.6±.2        | 57.4±.3      | 91.5±.2        | 44.8±.2         | 63.8±.3           | 57.3±.2         | 80.4±.2         | 68.5±.2        | 90.8±.3           | 55.9±.2           | 89.8±.2           |
|              | GCA       | **66.7±.2**  | **95.7±.3**    | **58.4±.3**  | **92.6±.2**    | **46.0±.2**     | **64.9±.3**       | **58.2±.2**     | **81.6±.3**     | **69.8±.2**    | **91.8±.2**       | **56.8±.4**       | **90.7±.3**       |
| CLIP-ReID   | BF        | 67.1±.3      | 96.2±.2        | 62.2±.4      | 93.4±.3        | 47.8±.3         | 66.5±.2           | 57.6±.2         | 81.5±.2         | 70.2±.1        | 90.1±.2           | 59.6±.1           | 90.2±.2           |
|              | CA        | 67.7±.2      | 95.4±.3        | 62.4±.1      | 94.5±.2        | 49.1±.2         | 67.6±.2           | 57.8±.3         | 82.6±.2         | 70.4±.2        | 91.2±.4           | 61.1±.2           | 91.3±.2           |
|              | GCA       | **69.4±.2**  | **98.1±.1**    | **63.2±.1**  | **95.4±.1**    | **50.3±.4**     | **68.6±.2**       | **59.8±.1**     | **83.7±.2**     | **71.5±.2**    | **92.0±.1**       | **61.8±.2**       | **92.1±.1**       |
| ReID-AW     | BF        | 70.2±.3      | 95.1±.2        | 64.2±.3      | 94.5±.2        | 52.5±.4         | 68.2±.3           | 59.8±.3         | 81.2±.3         | 72.2±.2        | 92.5±.3           | 61.2±.2           | 90.8±.4           |
|              | CA        | 71.5±.1      | 96.2±.2        | 65.4±.3      | 95.2±.2        | 54.2±.3         | 69.8±.2           | 60.8±.2         | 84.5±.2         | 73.2±.3        | 94.2±.2           | 62.5±.2           | 91.9±.4           |
|              | GCA       | **72.4±.2**  | **97.0±.2**    | **66.2±.1**  | **96.8±.2**    | **55.3±.4**     | **70.8±.4**       | **61.8±.2**     | **86.7±.3**     | **74.1±.4**    | **95.0±.2**       | **63.5±.1**       | **92.7±.2**       |

Table 1. Ablation Study: Impact of Fusion Strategies (Basic Fusion, Cross-Attention, and Gated Cross-Attention) on mAP and CMC-1 performance across six species. Bold values indicate the highest performance within each model.

**Key Observations**
- **Gated Cross-Attention (GCA)** consistently achieves the best performance, demonstrating its ability to adaptively balance metadata and visual information.
- The improvements are particularly notable for the ReID-AW model, with GCA achieving a **2.2% mAP gain on Deer** and **2.8% on Penguin** compared to BF.
- The flexibility of GCA allows it to enhance metadata contribution in visually ambiguous cases while minimizing its impact when visual features are distinctive.

* * *