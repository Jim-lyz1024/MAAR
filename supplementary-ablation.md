# Supplementary Material: Ablation Study
## Effect of Fusion Strategies
To investigate the effect of different fusion strategies for integrating metadata with visual features in our ReID models, we conducted a comprehensive ablation study. We compared three fusion approaches:

- **Basic Fusion (BF)**: This approach directly concatenates metadata embeddings with visual features, followed by a linear projection layer, providing a simple integration method without any interaction between the two modalities.

- **Cross-Attention (CA)**: This strategy allows feature interaction by computing attention weights between metadata and visual features.

- **Gated Cross-Attention (GCA)**: Our proposed method further improves cross-attention by introducing an adaptive gating mechanism to control the influence of metadata based on visual content.

<div style="text-align: center;">
  <p style="font-size: 14px; max-width: 100%; margin: 0 auto;">
    Table 1. Ablation Study: Impact of Fusion Strategies on mAP and CMC-1 performance across six species.
  </p>
  <img src="fig/ablation_fusion.png" alt="Ablation Study - Fusion" style="width: 100%; max-width: 700px; margin-top: 10px;">
</div>

The results of this comparison are presented in **Table 1**. Basic Fusion (BF) provides modest improvements across species, such as a 1.5% mAP gain on Deer for the CLIP-FT model. Cross-Attention (CA) strategy outperforms basic fusion by enabling selective feature integration, with particularly notable gains on datasets such as Penguin (0.3% and 1.3% mAP improvements for CLIP-FT and CLIP-ReID respectively). 

Our Gated Cross-Attention (GCA) achieves the best results, consistently outperforming both BF and CA, GCA achieves the best results with improvements of up to 2.8% mAP over basic fusion. This pattern is also observed in the ReID-AW model, where GCA achieves substantial improvements over BF across all species (*e.g.*, 2.2% mAP gain on Deer and 2.8% on Penguin).This performance can be attributed to its ability to adaptively adjust metadata influence based on visual content relevance. For instance, when visual features are highly distinctive, the gate can reduce reliance on metadata while increasing metadata influence for visually ambiguous cases.

---

## Effect of Different Metadata Features
To investigate the contribution of each metadata feature and to identify potential interactions between different metadata combinations, we progressively integrated three types of metadata into our models: **Temperature (T)**, **Circadian Rhythm (C)**, and **Face Orientation (F)**. These features were incorporated in three ReID models: **CLIP-FT+MFA**, **CLIP-ReID+MFA**, and **ReID-AW+MFA**.

<div style="text-align: center;">
  <p style="font-size: 14px; max-width: 100%; margin: 0 auto;">
    Table 2. Ablation study on different combinations of metadata features in CLIP-FT+MFA, CLIP-ReID+MFA and ReID-AW+MFA models. Temperature (T), Circadian Rhythm (C), and Face Orientation (F) features are progressively combined to analyze their individual and combined effects on model ReID performance.
  </p>
  <img src="fig/ablation_combination.png" alt="Ablation Study - Metafeature" style="width: 70%; max-width: 700px; margin-top: 10px;">
</div>

The results of this ablation study are summarized in **Table 2**, which reveals the impact of each metadata type on model performance, as measured by mean Average Precision (mAP). The results show that temperature contributes most to ReID performance across all models, achieving the highest mAP. This aligns with zoological research showing that temperature significantly influences animal behavior and appearance[^1]. As the temperature fluctuates, animals may exhibit variations in posture, movement patterns, and even fur characteristics, providing additional discriminative features for ReID. Moreover, different individuals often show distinct temperature preferences and behavioral adaptations[^2], making temperature-related features valuable for ReID tasks. When combining all three metadata types (T+C+F), we observe the best performance across all datasets, suggesting that each metadata type contributes complementary information. 

---
## Effectiveness of Feature Experts in Metadata Fusion
To evaluate the design choice of incorporating feature experts within MFA, we conduct an ablation study comparing model performance with and without the expert modules across three representative baselines: CLIP-FT, CLIP-ReID, and ReID-AW. The results are reported in **Table 3**. The **“w/o Experts”** variants directly fuse visual and textual metadata embeddings through cross attention without applying the Textual Metadata Expert (TME) or Visual Feature Expert (VFE), while the **“with Experts”** variants apply the full MFA design with learned feature transformation.

<div style="text-align: center;">
  <p style="font-size: 14px; max-width: 100%; margin: 0 auto;">
    Table 3. Ablation Study: Impact of Feature Experts on mAP and CMC-1 performance across six species.
  </p>
  <img src="fig/ablation_experts.png" alt="Ablation Study - Feature Experts" style="width: 100%; max-width: 700px; margin-top: 10px;">
</div>

The results show that integrating feature experts consistently improves performance across all models and species. In the CLIP-FT+MFA configuration, for instance, the mAP score on the Hare dataset increases from 57.2% (w/o Experts) to 58.4% (with Experts), while on Penguin it rises from 44.7% to 46.0%. Similarly, CLIP-ReID+MFA also benefits from expert modules, improving from 68.3% to 69.4% mAP on Deer and from 48.5% to 50.3% on Penguin. These improvements are also reflected in the CMC-1 scores, where Deer increases from 97.3% to 98.1%, and Wallaby from 91.0% to 92.1%.

The ReID-AW backbone, also benefits from feature expert integration. For example, mAP on Deer improves from 70.8% to 72.4%, and on Penguin from 52.6% to 55.3%. The gains extend to CMC-1 as well, such as Stoat improving from 94.2% to 95.0%. Although the performance gap is narrower for some species—such as Pūkeko under ReID-AW+MFA—overall, the experts consistently contribute to better accuracy and generalization.

These findings show the effectiveness of learning task-adaptive transformations through the Textual Metadata Expert (TME) and Visual Feature Expert (VFE). By refining raw embeddings before fusion, these modules improve the alignment of visual and metadata information, enabling more discriminative and robust ReID features.


---

## Effect of Noisy Metadata
To evaluate the robustness of metadata and determine whether its benefits persist under noisy conditions, we introduced artificial noise into three metadata types: **Temperature (T)**, **Circadian Rhythm (C)**, and **Face Orientation (F)**. The noise levels were set at **30%**, **60%**, and **100%**, representing progressively higher levels of noise, the results are presented in **Table 4**.

<div style="text-align: center;">
  <p style="font-size: 14px; max-width: 100%; margin: 0 auto;">
    Table 4. ReID-AW+MFA performance with Temperature Conditions (T), Circadian Rhythms (C), and Face Orientation (F) at different noise levels.
  </p>
  <img src="fig/ablation_noise.png" alt="Ablation Study - Metafeature" style="width: 60%; max-width: 700px; margin-top: 10px;">
</div>

For **Temperature**, at a moderate noise level of 30%, the performance drop from clean to noisy metadata is generally small. For instance, Deer drops slightly from 70.2±.3 to 69.5±.3, and Stoat from 72.2±.5 to 70.6±.3. This robustness can be attributed to the discretisation process applied to temperature metadata, where numerical values are mapped into categorical bins (e.g., cold,'' warm''). Minor perturbations due to noise may not result in a change of category, reducing the impact of noise. However, at 60% and 100% noise, the performance consistently declines across all species. For example, Pūkeko drops from 59.8±.2 to 55.6±.2 (100% noise), returning to or below the ReID-AW baseline.

For **Circadian Rhythm**, which categorises images as ``day`` or ``night``, performance gradually declines as noise increases. For example, Hare decreases from 64.1±.3 to 60.3±.1, and Penguin from 52.8±.6 to 47.1±.2 as noise reaches 100%. Although performance at 30% noise remains relatively stable (*e.g.*, Stoat at 71.8±.3 to 71.1±.3), the benefit diminishes rapidly beyond that. This shows that while the binary nature of circadian labels offers some robustness, incorrect labels quickly introduce confusion and diminish the advantage.

For most species (*e.g.*, Deer, Stoat, Wallaby), performance under 30% **face orientation** noise remains above the ReID-AW baseline. However, as noise increases, the benefit narrows. At 100% noise, results converge close to the baseline for Deer (67.3±.3) and drop below for Wallaby (54.9±.3). Notably, for Pūkeko and Penguin, orientation metadata becomes harmful even at moderate noise levels. For example, Penguin drops from 52.5±.3 (clean) to 48.0±.2 at 100% noise, which is lower than the baseline (48.8±.5). A possible explanation is that Pūkeko’s head is proportionally small compared to its body, making it difficult to determine precise orientation. Additionally, Penguins, when facing forward, exhibit minimal visual distinction between slight left-right head tilts, which could lead to unreliable orientation labels.

These results highlight that metadata can substantially improve ReID performance when reliable. Metadata types such as temperature and circadian rhythm, which are discretised and broadly applicable, show higher resilience to moderate noise. Face orientation is beneficial for species where pose strongly correlates with identity, but can degrade performance when annotation is noisy or the visual signal is weak. Overall, the findings emphasize that not all metadata types are equally informative across species, and that careful selection and robust annotation of metadata are essential for maximizing its utility in ReID tasks.

<!-- The overall results show that metadata can improve re-identification performance when reliable. Face Orientation benefits certain species (Deer, Stoat, Wallaby) but is ineffective for Pūkeko and Penguin, suggesting that not all metadata features are equally applicable across species. For practical applications, these findings emphasise the importance of careful metadata selection. When metadata is well-structured and correlates with identity-distinguishing traits, it provides a meaningful boost to re-identification performance. However, metadata that is difficult to annotate consistently or lacks sufficient intra-class variation may fail to contribute or even degrade performance under noise. These insights highlight the necessity of robust annotation protocols and species-specific considerations when integrating environmental metadata into ReID models. -->

---

## Algorithm
We outline the training process of Meta-Feature Adapter (MFA) in Algorithm 1.
<div style="text-align: center;">
  <img src="fig/algorithm.png" alt="algorithm" style="width: 100%; max-width: 700px; margin-top: 10px;">
</div>

[^1]: Shermeister, B., Mor, D., & Levy, O. (2024). Leveraging camera traps and artificial intelligence to explore thermoregulation behaviour. Journal of Animal Ecology, 93(9), 1246-1261.
[^2]: Lagerspetz, K. Y., & Vainio, L. A. (2006). Thermal behaviour of crustaceans. Biological Reviews, 81(2), 237-258.