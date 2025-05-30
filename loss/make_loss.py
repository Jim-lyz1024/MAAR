import torch
import torch.nn.functional as F
from .softmax_loss import CrossEntropyLabelSmooth, LabelSmoothingCrossEntropy
from .triplet_loss import TripletLoss
from .center_loss import CenterLoss
from ..model.gated_attention import compute_cross_attention_loss


def make_loss(cfg, num_classes):
    sampler = cfg.DATALOADER.SAMPLER
    feat_dim = 2048
    center_criterion = CenterLoss(num_classes=num_classes, feat_dim=feat_dim, use_gpu=True)  # center loss
    if 'triplet' in cfg.MODEL.METRIC_LOSS_TYPE:
        if cfg.MODEL.NO_MARGIN:
            triplet = TripletLoss()
            print("using soft triplet loss for training")
        else:
            triplet = TripletLoss(cfg.SOLVER.MARGIN)  # triplet loss
            print("using triplet loss with margin:{}".format(cfg.SOLVER.MARGIN))
    else:
        print('expected METRIC_LOSS_TYPE should be triplet'
              'but got {}'.format(cfg.MODEL.METRIC_LOSS_TYPE))

    if cfg.MODEL.IF_LABELSMOOTH == 'on':
        xent = CrossEntropyLabelSmooth(num_classes=num_classes)
        print("label smooth on, numclasses:", num_classes)

    if sampler == 'softmax':
        def loss_func(score, feat, target):
            return F.cross_entropy(score, target)

    elif cfg.DATALOADER.SAMPLER == 'softmax_triplet':
        def loss_func(score, feat, target, target_cam, i2tscore=None, meta_features=None, text_features=None):
            total_loss = 0.0
            
            if cfg.MODEL.METRIC_LOSS_TYPE == 'triplet':
                if cfg.MODEL.IF_LABELSMOOTH == 'on':
                    # Identity classification loss L_id
                    if isinstance(score, list):
                        ID_LOSS = [xent(scor, target) for scor in score]
                        ID_LOSS = sum(ID_LOSS)
                    else:
                        ID_LOSS = xent(score, target)

                    # Triplet loss L_tri
                    if isinstance(feat, list):
                        TRI_LOSS = [triplet(feats, target)[0] for feats in feat]
                        TRI_LOSS = sum(TRI_LOSS) 
                    else:   
                        TRI_LOSS = triplet(feat, target)[0]
                    
                    total_loss = cfg.MODEL.ID_LOSS_WEIGHT * ID_LOSS + cfg.MODEL.TRIPLET_LOSS_WEIGHT * TRI_LOSS

                    if i2tscore is not None:
                        I2T_LOSS = xent(i2tscore, target)
                        total_loss += cfg.MODEL.I2T_LOSS_WEIGHT * I2T_LOSS
                    
                    if meta_features is not None and text_features is not None:
                        CROSS_ATTN_LOSS = compute_cross_attention_loss(
                            meta_features, text_features, target, temperature=0.07
                        )
                        total_loss += CROSS_ATTN_LOSS
                        
                else:
                    # Without label smoothing
                    if isinstance(score, list):
                        ID_LOSS = [F.cross_entropy(scor, target) for scor in score]
                        ID_LOSS = sum(ID_LOSS)
                    else:
                        ID_LOSS = F.cross_entropy(score, target)

                    if isinstance(feat, list):
                        TRI_LOSS = [triplet(feats, target)[0] for feats in feat]
                        TRI_LOSS = sum(TRI_LOSS)
                    else:
                        TRI_LOSS = triplet(feat, target)[0]

                    total_loss = cfg.MODEL.ID_LOSS_WEIGHT * ID_LOSS + cfg.MODEL.TRIPLET_LOSS_WEIGHT * TRI_LOSS
                    
                    if i2tscore is not None:
                        I2T_LOSS = F.cross_entropy(i2tscore, target)
                        total_loss += cfg.MODEL.I2T_LOSS_WEIGHT * I2T_LOSS
                    
                    if meta_features is not None and text_features is not None:
                        CROSS_ATTN_LOSS = compute_cross_attention_loss(
                            meta_features, text_features, target, temperature=0.07
                        )
                        total_loss += CROSS_ATTN_LOSS

                return total_loss
            else:
                print('expected METRIC_LOSS_TYPE should be triplet'
                      'but got {}'.format(cfg.MODEL.METRIC_LOSS_TYPE))

    else:
        print('expected sampler should be softmax, triplet, softmax_triplet'
              'but got {}'.format(cfg.DATALOADER.SAMPLER))
    return loss_func, center_criterion


def compute_cross_attention_loss(image_features, text_features, targets, temperature=0.07):
    batch_size = image_features.shape[0]
    
    # Normalize features
    image_features = F.normalize(image_features, p=2, dim=1)
    text_features = F.normalize(text_features, p=2, dim=1)
    
    # Compute similarity matrix
    similarity_matrix = torch.mm(text_features, image_features.t()) / temperature
    
    # Create labels for positive pairs (diagonal elements)
    labels = torch.arange(batch_size, device=image_features.device)
    
    # Cross-entropy loss
    loss = F.cross_entropy(similarity_matrix, labels)
    
    return loss