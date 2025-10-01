import os
import numpy as np
import torch
import torchaudio
import torchaudio.transforms as T

# Path to the dataset folder
dataset_path = "/mnt/ricproject3/2025/data/rearranged_voxceleb1"

# Initialize the MFCC transform
mfcc_transform = T.MFCC(
    sample_rate=16000,
    n_mfcc=40,
    melkwargs={
        'n_fft': 400,
        'n_mels': 40,
        'hop_length': 160,
        'mel_scale': 'htk',
    }
)

# Function to load and process audio file
def load_audio(file_path):
    """Load an audio file and return waveform"""
    waveform, sample_rate = torchaudio.load(file_path)
    return waveform, sample_rate

# Create output directory
output_dir = "extracted_features"
os.makedirs(output_dir, exist_ok=True)

# Initialize empty lists for features and labels
features = []
labels = []

# Process each speaker
print("Starting feature extraction...")
speakers = os.listdir(dataset_path)

for speaker_idx, speaker in enumerate(speakers):
    speaker_path = os.path.join(dataset_path, speaker)
    print(f"Processing speaker {speaker_idx + 1}/{len(speakers)}: {speaker}")
    
    # Skip if not a directory
    if not os.path.isdir(speaker_path):
        continue
    
    # Process each audio file for this speaker
    for audio_file in os.listdir(speaker_path):
        if not audio_file.endswith(('.wav', '.flac', '.mp3')):
            continue
            
        audio_path = os.path.join(speaker_path, audio_file)
        
        try:
            # Load and process audio
            waveform, sample_rate = load_audio(audio_path)
            
            # Extract MFCC features
            mfcc = mfcc_transform(waveform)
            
            # Average over time dimension to get fixed-size features
            mfcc_mean = torch.mean(mfcc, dim=2)
            
            # Add to our lists
            features.append(mfcc_mean.numpy().flatten())
            labels.append(speaker)
            
        except Exception as e:
            print(f"Error processing {audio_path}: {str(e)}")
            continue

# Convert lists to arrays
features_array = np.array(features)
labels_array = np.array(labels)

# Save the features and labels
np.save(os.path.join(output_dir, "features.npy"), features_array)
np.save(os.path.join(output_dir, "labels.npy"), labels_array)

print("\nFeature extraction complete!")
print(f"Features shape: {features_array.shape}")
print(f"Number of speakers: {len(np.unique(labels_array))}")
print(f"Files saved in: {os.path.abspath(output_dir)}")
