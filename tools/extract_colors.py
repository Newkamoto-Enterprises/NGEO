import sys
from PIL import Image
from collections import Counter

def get_palette(image_path, n=80):
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        # Resize to speed up processing
        img = img.resize((100, 100))
        pixels = list(img.getdata())
        # Simple frequent color extraction
        # For better "tone colors", we might want something smarter, 
        # but Counter is a good start for "collecting".
        # To ensure variety, maybe we simply sample or cluster, 
        # but 80 most common might be too dominated by one shade.
        # Let's use simple quantization to reduce noise first.
        img_q = img.quantize(colors=n)
        img_q = img_q.convert('RGB')
        palette = img_q.getpalette() # This returns [r,g,b, r,g,b...] flattened
        
        # The getpalette() for quantize might return 768 items (256 colors),
        # but we only asked for n=80. 
        # Let's just grab the colors used.
        colors = img_q.getcolors(maxcolors=n+1)
        # colors is list of (count, (r,g,b))
        
        # Sort by count desc
        colors.sort(key=lambda x: x[0], reverse=True)
        
        hex_colors = []
        for c in colors[:n]:
            rgb = c[1]
            hex_colors.append('#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2]))
            
        return hex_colors
    except Exception as e:
        print(f"Error: {e}")
        return []

palette = get_palette('/Users/sofianedelloue/Desktop/Workspaces/NGEO/assets/images/ngeo.png', 80)
print(palette)
