import numpy as np
import tifffile
import matplotlib.pyplot as plt
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import os

def load_tif_stack(file_path):
    """Load a TIFF stack and return it as a numpy array."""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Try to read the file
        try:
            return tifffile.imread(file_path)
        except Exception as e:
            print(f"Error reading file with tifffile: {e}")
            print("Trying alternative reading method...")
            # If tifffile fails, try with imageio
            import imageio
            return imageio.mimread(file_path)
            
    except Exception as e:
        print(f"Error loading file: {e}")
        raise

def analyze_z_axis(tif_stack):
    """
    Analyze pixel values along the z-axis of a TIFF stack.
    Returns various statistics for each pixel position (x,y).
    """
    # Get dimensions
    z_dim, height, width = tif_stack.shape
    
    # Initialize arrays to store statistics
    mean_values = np.zeros((height, width))
    std_values = np.zeros((height, width))
    max_values = np.zeros((height, width))
    min_values = np.zeros((height, width))
    
    # Calculate statistics for each pixel position
    for y in range(height):
        for x in range(width):
            z_values = tif_stack[:, y, x]
            mean_values[y, x] = np.mean(z_values)
            std_values[y, x] = np.std(z_values)
            max_values[y, x] = np.max(z_values)
            min_values[y, x] = np.min(z_values)
    
    return {
        'mean': mean_values,
        'std': std_values,
        'max': max_values,
        'min': min_values
    }

def plot_z_analysis(stats, save_path=None):
    """Create and optionally save plots of the z-axis analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 15))
    fig.suptitle('Z-axis Analysis of TIFF Stack', fontsize=16)
    
    # Plot mean values
    im1 = axes[0, 0].imshow(stats['mean'], cmap='viridis')
    axes[0, 0].set_title('Mean Values')
    plt.colorbar(im1, ax=axes[0, 0])
    
    # Plot standard deviation
    im2 = axes[0, 1].imshow(stats['std'], cmap='viridis')
    axes[0, 1].set_title('Standard Deviation')
    plt.colorbar(im2, ax=axes[0, 1])
    
    # Plot max values
    im3 = axes[1, 0].imshow(stats['max'], cmap='viridis')
    axes[1, 0].set_title('Maximum Values')
    plt.colorbar(im3, ax=axes[1, 0])
    
    # Plot min values
    im4 = axes[1, 1].imshow(stats['min'], cmap='viridis')
    axes[1, 1].set_title('Minimum Values')
    plt.colorbar(im4, ax=axes[1, 1])
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    
    plt.show()

def create_raster_plot(tif_stack, save_path=None, max_pixels=1000, interval_sec=2):
    """
    Create a raster plot showing the traces from each pixel.
    If there are too many pixels, it will sample them evenly.
    
    Args:
        tif_stack: numpy array of shape (z_dim, height, width)
        save_path: optional path to save the plot
        max_pixels: maximum number of pixels to plot
        interval_sec: time interval between frames in seconds
    """
    z_dim, height, width = tif_stack.shape
    total_pixels = height * width
    
    # Create time array
    time_points = np.arange(z_dim) * interval_sec
    
    # Determine sampling if needed
    if total_pixels > max_pixels:
        # Calculate sampling step
        step = int(np.ceil(total_pixels / max_pixels))
        # Create evenly spaced indices
        indices = np.arange(0, total_pixels, step)
        y_indices = indices // width
        x_indices = indices % width
    else:
        y_indices, x_indices = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
        y_indices = y_indices.flatten()
        x_indices = x_indices.flatten()
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Plot each pixel trace
    for i, (y, x) in enumerate(zip(y_indices, x_indices)):
        trace = tif_stack[:, y, x]
        # Normalize the trace to [0, 1] for better visualization
        trace_norm = (trace - np.min(trace)) / (np.max(trace) - np.min(trace))
        plt.plot(time_points, trace_norm + i, 'k-', linewidth=0.5, alpha=0.5)
    
    plt.title('Pixel Traces Raster Plot')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Pixel Index')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Raster plot saved to {save_path}")
    
    plt.show()

def main():
    # Use direct file path with forward slashes
    file_path = r"C:/Users/rasmu/Desktop/TEMP LOCAL FILES/LED 2s/240916_pl100_pc001_LED_min10_ex02/DATA/SUPPORT_ChanA/suite2p files/combined_registered.tif"
    
    try:
        # Load and analyze the stack
        print("Loading TIFF stack...")
        print(f"Attempting to load file: {file_path}")
        # Convert to Path object to handle spaces and special characters
        file_path = str(Path(file_path))
        tif_stack = load_tif_stack(file_path)
        
        print(f"Successfully loaded stack with shape: {tif_stack.shape}")
        
        print("Analyzing z-axis values...")
        stats = analyze_z_axis(tif_stack)
        
        # Create output directory if it doesn't exist
        output_dir = Path(file_path).parent / "z_analysis_results"
        output_dir.mkdir(exist_ok=True)
        
        # Save the analysis results
        output_path = output_dir / f"{Path(file_path).stem}_z_analysis.png"
        plot_z_analysis(stats, save_path=str(output_path))
        
        # Create and save the raster plot with 2-second interval
        raster_path = output_dir / f"{Path(file_path).stem}_raster.png"
        create_raster_plot(tif_stack, save_path=str(raster_path), interval_sec=2)
        
        # Save numerical results
        np.save(output_dir / f"{Path(file_path).stem}_mean.npy", stats['mean'])
        np.save(output_dir / f"{Path(file_path).stem}_std.npy", stats['std'])
        np.save(output_dir / f"{Path(file_path).stem}_max.npy", stats['max'])
        np.save(output_dir / f"{Path(file_path).stem}_min.npy", stats['min'])
        
        print(f"Analysis complete. Results saved in {output_dir}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check if:")
        print("1. The file path is correct")
        print("2. The file exists")
        print("3. You have read permissions for the file")
        print("4. The file is a valid image stack")

if __name__ == "__main__":
    main() 