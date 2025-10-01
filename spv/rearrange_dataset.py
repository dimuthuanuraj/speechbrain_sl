import os
import shutil

def rearrange_dataset(source_path, destination_path):
    print(f"Starting dataset rearrangement...")
    print(f"Source path: {source_path}")
    print(f"Destination path: {destination_path}")
    
    total_files_processed = 0
    total_speakers_processed = 0
    
    # Traverse through the source directory (VoxCeleb1)
    speakers = os.listdir(source_path)
    print(f"Found {len(speakers)} potential speaker folders")
    
    for speaker_folder in speakers:
        speaker_folder_path = os.path.join(source_path, speaker_folder)
        
        # Skip if it's not a directory
        if not os.path.isdir(speaker_folder_path):
            print(f"Skipping {speaker_folder} as it's not a directory")
            continue
        
        print(f"\nProcessing speaker: {speaker_folder}")
        speaker_files_processed = 0
        
        # Iterate through each immediate subfolder inside the speaker folder
        subfolders = os.listdir(speaker_folder_path)
        for subfolder in subfolders:
            subfolder_path = os.path.join(speaker_folder_path, subfolder)
            
            # Skip if it's not a directory
            if not os.path.isdir(subfolder_path):
                continue
            
            # Iterate through the audio files in the subfolder
            for file_name in os.listdir(subfolder_path):
                if file_name.endswith(('.wav', '.WAV', '.wave', '.WAVE')):
                    # Construct new file name (always use .wav extension)
                    base_name = os.path.splitext(file_name)[0]
                    new_file_name = f"{base_name}_{subfolder}.wav"
                    
                    # Define the destination path
                    destination_file_path = os.path.join(destination_path, speaker_folder, new_file_name)
                    
                    # Ensure the destination folder exists
                    os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
                    
                    try:
                        # Copy the file to the new location
                        source_file_path = os.path.join(subfolder_path, file_name)
                        shutil.copy2(source_file_path, destination_file_path)
                        speaker_files_processed += 1
                        total_files_processed += 1
                    except Exception as e:
                        print(f"Error processing {file_name}: {str(e)}")
        
        if speaker_files_processed > 0:
            print(f"Processed {speaker_files_processed} files for speaker {speaker_folder}")
            total_speakers_processed += 1
        else:
            print(f"No audio files found for speaker {speaker_folder}")

    print(f"\nRearrangement complete!")
    print(f"Total speakers processed: {total_speakers_processed}")
    print(f"Total files processed: {total_files_processed}")
    print(f"Files have been rearranged in: {destination_path}")

if __name__ == "__main__":
    # Define your source and destination paths
    source_path = '/mnt/ricproject3/2025/data/voxceleb1'
    destination_path = '/mnt/ricproject3/2025/data/rearranged_voxceleb1'

    # Call the function
    rearrange_dataset(source_path, destination_path)
