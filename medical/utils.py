from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings

def generate_medical_certificate(client, template):
    # Load template image
    template_path = template.template_image.path
    img = Image.open(template_path).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Font settings
    # Try multiple bold fonts to ensure it looks bold
    font_paths = [
        "C:\\Windows\\Fonts\\arialbd.ttf",   # Arial Bold (Preferred for visibility)
        "C:\\Windows\\Fonts\\calibrib.ttf",  # Calibri Bold
        "C:\\Windows\\Fonts\\verdanab.ttf",  # Verdana Bold
        "C:\\Windows\\Fonts\\tahomabd.ttf",  # Tahoma Bold
    ]
    
    font = None
    font_size = template.font_size or 11
    
    for path in font_paths:
        try:
            font = ImageFont.truetype(path, font_size)
            # print(f"DEBUG: Loaded font {path}") # Uncomment for debugging
            break
        except Exception as e:
            continue
            
    if not font:
        font = ImageFont.load_default()

    # Draw Text
    text_color = (0, 0, 0) # Black
    
    if template.name_x and template.name_y:
        draw.text((template.name_x, template.name_y), client.client_name.title(), font=font, fill=text_color)
    
    if template.passport_x and template.passport_y:
        draw.text((template.passport_x, template.passport_y), client.passport_no.upper(), font=font, fill=text_color)
        
    if template.age_x and template.age_y:
        draw.text((template.age_x, template.age_y), f"{client.age} Years", font=font, fill=text_color)
        
    if template.date_x and template.date_y:
        draw.text((template.date_x, template.date_y), client.date.strftime('%d/%m/%Y'), font=font, fill=text_color)

    # Draw Photo using 2-point bounding box (Top-Left and Bottom-Right)
    # Check if we have both points (at least x2/y2 should be non-zero if x1/y1 are 0)
    has_photo_coords = (template.photo_x1 != 0 or template.photo_y1 != 0) or (template.photo_x2 != 0 or template.photo_y2 != 0)
    
    if client.photo and has_photo_coords:
        # Get actual coordinates in case they were clicked in any order
        x1, x2 = sorted([template.photo_x1, template.photo_x2])
        y1, y2 = sorted([template.photo_y1, template.photo_y2])
        
        width = x2 - x1
        height = y2 - y1
        
        print(f"DEBUG: Injecting photo for {client.client_name}")
        print(f"DEBUG: Coordinates: ({x1}, {y1}) to ({x2}, {y2}), Size: {width}x{height}")
        
        if width > 0 and height > 0:
            try:
                photo_path = client.photo.path
                print(f"DEBUG: Photo path: {photo_path}")
                photo = Image.open(photo_path)
                photo = photo.resize((width, height), Image.Resampling.LANCZOS)
                img.paste(photo, (x1, y1))
                print(f"DEBUG: Photo pasted successfully")
            except Exception as e:
                print(f"DEBUG: Error drawing photo: {e}")
    else:
        print(f"DEBUG: Photo injection skipped. client.photo: {bool(client.photo)}, x1: {template.photo_x1}, y1: {template.photo_y1}, x2: {template.photo_x2}, y2: {template.photo_y2}")

    # Save final image
    output_name = f"certificate_{client.id}.jpg"
    output_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_name)
    
    img.save(output_path, "JPEG", quality=95)
    return os.path.join(settings.MEDIA_URL, 'certificates', output_name)
