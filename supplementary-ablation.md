# Supplementary Material: Ablation Study
## **Effect of Fusion Strategies**
To investigate the effect of different fusion strategies for integrating metadata with visual features in our ReID models, we conducted a comprehensive ablation study. We compared three fusion approaches:

- **Basic Fusion (BF)**: This approach directly concatenates metadata embeddings with visual features, followed by a linear projection layer, providing a simple integration method without any interaction between the two modalities.

- **Cross-Attention (CA)**: This strategy allows feature interaction by computing attention weights between metadata and visual features.

- **Gated Cross-Attention (GCA)**: Our proposed method further improves cross-attention by introducing an adaptive gating mechanism to control the influence of metadata based on visual content.


*Table 1. Ablation Study: Impact of Fusion Strategies (Basic Fusion, Cross-Attention, and Gated Cross-Attention) on mAP and CMC-1 performance across six species. Bold values indicate the highest performance within each model.*
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


The results of this comparison are presented in **Table 1**. Basic Fusion (BF) provides modest improvements across species, such as a 1.5% mAP gain on Deer for the CLIP-FT model. Cross-Attention (CA) strategy outperforms basic fusion by enabling selective feature integration, with particularly notable gains on datasets such as Penguin (0.3% and 1.3% mAP improvements for CLIP-FT and CLIP-ReID respectively). 

Our Gated Cross-Attention (GCA) achieves the best results, consistently outperforming both BF and CA, GCA achieves the best results with improvements of up to 2.5% mAP over basic fusion. This pattern is also observed in the ReID-AW model, where GCA achieves substantial improvements over BF across all species (*e.g.*, 2.2% mAP gain on Deer and 2.8% on Penguin).This performance can be attributed to its ability to adaptively adjust metadata influence based on visual content relevance. For instance, when visual features are highly distinctive, the gate can reduce reliance on metadata while increasing metadata influence for visually ambiguous cases.

* * *

### **Effect of Different Metadata Features**
To investigate the contribution of each metadata feature and to identify potential interactions between different metadata combinations, we progressively integrated three types of metadata into our models: **Temperature (T)**, **Circadian Rhythm (C)**, and **Face Orientation (F)**. These features were incorporated in three ReID models: **CLIP-FT+MFA**, **CLIP-ReID+MFA**, and **ReID-AW+MFA**.


*Table 2. Ablation study on different combinations of metadata features in CLIP-FT+MFA, CLIP-ReID+MFA and ReID-AW+MFA models. Temperature (T), Circadian Rhythm (C), and Face Orientation (F) features are progressively combined to analyze their individual and combined effects on model ReID performance.*

**CLIP-FT+MFA - mAP (%)**
| T | C | F | Deer | Hare | Penguin | Pūkeko | Stoat | Wallaby |
|---|---|---|------|------|---------|--------|-------|----------|
| ✅ | - | - | 64.8 | 57.4 | 45.4    | 57.1   | 68.5  | 55.7     |
| - | ✅ | - | 64.5 | 57.1 | 44.3    | 56.8   | 68.2  | 55.7     |
| - | - | ✅ | 64.2 | 56.8 | 44.9    | 56.5   | 67.9  | 55.4     |
| ✅ | ✅ | - | 66.1 | 58.0 | 45.7    | 57.7   | 69.2  | 56.5     |
| ✅ | - | ✅ | 65.7 | 57.8 | 45.1    | 58.0   | 68.9  | 56.3     |
| - | ✅ | ✅ | 65.3 | 57.6 | 44.6    | 57.4   | 69.5  | 56.0     |
| ✅ | ✅ | ✅ | **66.7** | **58.4** | **46.0** | **58.2** | **69.8** | **56.8** |

**CLIP-ReID+MFA - mAP (%)**
| T | C | F | Deer | Hare | Penguin | Pūkeko | Stoat | Wallaby |
|---|---|---|------|------|---------|--------|-------|----------|
| ✅ | - | - | 67.4 | 61.8 | 47.4    | 58.5   | 70.1  | 59.2     |
| - | ✅ | - | 67.1 | 61.5 | 46.8    | 58.2   | 69.2  | 58.4     |
| - | - | ✅ | 66.8 | 61.2 | 47.1    | 57.9   | 69.8  | 58.9     |
| ✅ | ✅ | - | 68.8 | 62.7 | 48.5    | 59.5   | 70.9  | 60.8     |
| ✅ | - | ✅ | 68.5 | 62.4 | 49.4    | 59.2   | 71.1  | 60.5     |
| - | ✅ | ✅ | 68.2 | 62.1 | 49.1    | 58.9   | 70.6  | 60.1     |
| ✅ | ✅ | ✅ | **69.4** | **63.2** | **50.3** | **59.8** | **71.5** | **61.8** |

**ReID-AW+MFA - mAP (%)**
| T | C | F | Deer | Hare | Penguin | Pūkeko | Stoat | Wallaby |
|---|---|---|------|------|---------|--------|-------|----------|
| ✅ | - | - | 70.2 | 64.5 | 53.1    | 59.8   | 72.2  | 61.4     |
| - | ✅ | - | 69.8 | 64.1 | 52.8    | 59.5   | 71.8  | 61.0     |
| - | - | ✅ | 69.5 | 63.8 | 52.5    | 59.2   | 71.5  | 60.8     |
| ✅ | ✅ | - | 71.5 | 65.1 | 54.5    | 60.2   | 73.2  | 62.5     |
| ✅ | - | ✅ | 71.2 | 65.4 | 54.2    | 60.3   | 73.5  | 62.2     |
| - | ✅ | ✅ | 70.8 | 64.8 | 53.5    | 59.3   | 73.0  | 61.8     |
| ✅ | ✅ | ✅ | **72.4** | **66.2** | **55.3** | **61.8** | **74.1** | **63.5** |

The results of this ablation study are summarized in **Table 2**, which reveals the impact of each metadata type on model performance, as measured by mean Average Precision (mAP). The results show that temperature contributes most to ReID performance across all models, achieving the highest mAP. This aligns with zoological research showing that temperature significantly influences animal behavior and appearance[^1]. As the temperature fluctuates, animals may exhibit variations in posture, movement patterns, and even fur characteristics, providing additional discriminative features for ReID. Moreover, different individuals often show distinct temperature preferences and behavioral adaptations[^2], making temperature-related features valuable for ReID tasks. When combining all three metadata types (T+C+F), we observe the best performance across all datasets, suggesting that each metadata type contributes complementary information. 


[^1]: Shermeister, B., Mor, D., & Levy, O. (2024). Leveraging camera traps and artificial intelligence to explore thermoregulation behaviour. Journal of Animal Ecology, 93(9), 1246-1261.
[^2]: Lagerspetz, K. Y., & Vainio, L. A. (2006). Thermal behaviour of crustaceans. Biological Reviews, 81(2), 237-258.