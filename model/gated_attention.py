import torch
import torch.nn as nn
import math
from torch.nn import functional as F

class TextualMetadataExpert(nn.Module):
    def __init__(self, input_dim=512, hidden_dim=256):
        super(TextualMetadataExpert, self).__init__()
        
        # MLP-based adapter with residual connections
        self.adapter = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, input_dim)
        )
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, text_features):
        # Residual connection
        adapted_features = self.adapter(text_features)
        return text_features + adapted_features


class VisualFeatureExpert(nn.Module):
    def __init__(self, input_dim=512, hidden_dim=256):
        super(VisualFeatureExpert, self).__init__()
        
        # MLP-based adapter with residual connections
        self.adapter = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, input_dim)
        )
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, visual_features):
        # Residual connection
        adapted_features = self.adapter(visual_features)
        return visual_features + adapted_features

class GatedCrossAttention(nn.Module):
    def __init__(self, d_in, d_out_kq, d_out_v, num_heads=8, dropout=0.1):
        super().__init__()
        self.d_out_kq = d_out_kq
        self.num_heads = num_heads
        self.head_dim = d_out_kq // num_heads
        
        # Projection matrices
        self.W_query = nn.Linear(d_in, d_out_kq)
        self.W_key = nn.Linear(d_in, d_out_kq)
        self.W_value = nn.Linear(d_in, d_out_v)
        
        # Gate MLP
        self.gate_net = nn.Sequential(
            nn.Linear(d_in * 2, d_in),
            nn.LayerNorm(d_in),
            nn.ReLU(),
            nn.Linear(d_in, d_out_v),
            nn.Sigmoid()
        )
        
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(d_out_v)
        
        # Initialize weights
        nn.init.xavier_uniform_(self.W_query.weight)
        nn.init.xavier_uniform_(self.W_key.weight)
        nn.init.xavier_uniform_(self.W_value.weight)

    def forward(self, x_img, x_meta):
        # Ensure input dimensions
        if len(x_img.shape) == 2:
            x_img = x_img.unsqueeze(1)
        if len(x_meta.shape) == 2:
            x_meta = x_meta.unsqueeze(1)
            
        batch_size = x_img.shape[0]
            
        # Project to query, key, value
        Q = self.W_query(x_img)
        K = self.W_key(x_meta)
        V = self.W_value(x_meta)
        
        # Calculate attention scores
        attention = torch.bmm(Q, K.transpose(1, 2)) / math.sqrt(self.d_out_kq)
        attention = F.softmax(attention, dim=-1)
        attention = self.dropout(attention)
        
        # Apply attention to values
        context = torch.bmm(attention, V)
        
        # Calculate gate weights using concatenated features
        gate_input = torch.cat([
            x_img.view(batch_size, -1), 
            x_meta.view(batch_size, -1)
        ], dim=-1)
        gate_weights = self.gate_net(gate_input)
        
        # print("-------------Gated Attention-----------")
        # print(gate_weights.shape)
        # print(gate_weights.min(), gate_weights.max())
        # print(gate_weights)
        
        # Apply gating and ensure output dimensions
        context = context.squeeze(1)  # Remove sequence dimension
        gated_output = gate_weights * context
        
        # Residual connection and layer norm
        x_img = x_img.squeeze(1)  # Remove sequence dimension
        output = self.layer_norm(x_img + gated_output)
        
        return output

def get_attention_mask(seq_length):
    mask = torch.ones(seq_length, seq_length)
    mask = torch.triu(mask, diagonal=1)
    mask = mask.masked_fill(mask == 1, float('-inf'))
    return mask

def compute_cross_attention_loss(image_features, text_features, targets, temperature=0.07):
    batch_size = image_features.shape[0]
    
    # Normalize features
    image_features = F.normalize(image_features, p=2, dim=1)
    text_features = F.normalize(text_features, p=2, dim=1)
    
    # Compute similarity scores
    logits = torch.mm(image_features, text_features.t()) / temperature
    
    # Create labels for positive pairs
    labels = torch.arange(batch_size, device=image_features.device)
    
    # Cross-entropy loss for alignment
    loss = F.cross_entropy(logits, labels)
    
    return loss