#!/usr/bin/env python3
"""
Générateur d'icônes PWA haute définition (SVG & PNG purs sans dépendance externe).
Crée des icônes pour Android, iOS (Apple Touch Icon), Desktop et Favicon.
"""
import os
import zlib
import struct
import math

def generate_svg_icon(filepath="icon.svg", size=512):
    """Crée une icône vectorielle SVG moderne Bilatérale France-Turquie."""
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
    <defs>
        <!-- Dégradé de fond obsidian profond -->
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0f172a" />
            <stop offset="100%" stop-color="#090d16" />
        </linearGradient>
        
        <!-- Dégradé or pour l'anneau VIP -->
        <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#f59e0b" />
            <stop offset="50%" stop-color="#d97706" />
            <stop offset="100%" stop-color="#b45309" />
        </linearGradient>
        
        <!-- Dégradé bleu France -->
        <linearGradient id="frBlueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#2563eb" />
            <stop offset="100%" stop-color="#1d4ed8" />
        </linearGradient>

        <!-- Dégradé rouge Turquie -->
        <linearGradient id="trRedGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ef4444" />
            <stop offset="100%" stop-color="#dc2626" />
        </linearGradient>
        
        <!-- Ombre portée -->
        <filter id="dropGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="8" stdDeviation="16" flood-color="#2563eb" flood-opacity="0.25"/>
        </filter>
    </defs>

    <!-- Fond squircle moderne style iOS / Android Adaptive -->
    <rect x="16" y="16" width="{size-32}" height="{size-32}" rx="108" fill="url(#bgGrad)" stroke="url(#goldGrad)" stroke-width="6" />

    <!-- Disque central avec halo -->
    <g transform="translate({size/2}, {size/2})">
        <!-- Cercle de fond interne -->
        <circle cx="0" cy="0" r="160" fill="#141e33" stroke="rgba(255,255,255,0.08)" stroke-width="3" filter="url(#dropGlow)" />
        
        <!-- Côté gauche : Rouge Turquie -->
        <path d="M 0 -150 A 150 150 0 0 0 0 150 Z" fill="url(#trRedGrad)" opacity="0.9" />
        
        <!-- Côté droit : Bleu France -->
        <path d="M 0 -150 A 150 150 0 0 1 0 150 Z" fill="url(#frBlueGrad)" opacity="0.9" />
        
        <!-- Séparateur blanc central subtil -->
        <line x1="0" y1="-150" x2="0" y2="150" stroke="#ffffff" stroke-width="4" stroke-opacity="0.8" />
        
        <!-- Croissant de lune Turquie (Côté gauche) -->
        <g transform="translate(-65, -10) scale(0.95)">
            <circle cx="0" cy="0" r="42" fill="#ffffff" />
            <circle cx="12" cy="0" r="34" fill="#dc2626" />
            <!-- Étoile turque -->
            <polygon points="26,0 34,-6 31,3 38,8 29,8 26,16 23,8 14,8 21,3 18,-6" fill="#ffffff" transform="rotate(-15, 26, 0) scale(1.1)" />
        </g>
        
        <!-- Emblème France (Côté droit) : Tour Eiffel stylisée & Étoile talent -->
        <g transform="translate(65, -5) scale(0.95)">
            <!-- Silhouette Tour Eiffel / Flèche montante -->
            <path d="M -24,48 L -14,10 L -4,-40 L 4,-40 L 14,10 L 24,48 L 10,48 L 7,20 L -7,20 L -10,48 Z" fill="#ffffff" />
            <circle cx="0" cy="-44" r="5" fill="#f59e0b" />
            <line x1="-12" y1="20" x2="12" y2="20" stroke="#2563eb" stroke-width="3" />
        </g>

        <!-- Bandeau horizontal central avec symbole bilatéral ⇄ -->
        <rect x="-80" y="55" width="160" height="38" rx="19" fill="#0f172a" stroke="url(#goldGrad)" stroke-width="3" />
        <text x="0" y="80" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-size="20" font-weight="800" fill="#f8fafc" text-anchor="middle" letter-spacing="2">TR ⇄ FR</text>

        <!-- Couronne supérieure : Étoile dorée Passeport Talent -->
        <g transform="translate(0, -115) scale(0.85)">
            <polygon points="0,-18 5,-5 18,-5 8,4 12,17 0,9 -12,17 -8,4 -18,-5 -5,-5" fill="#f59e0b" />
        </g>
    </g>
    
    <!-- Typographie inférieure -->
    <text x="{size/2}" y="{size - 48}" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-size="28" font-weight="800" fill="#f8fafc" text-anchor="middle" letter-spacing="3">FRANSA İŞ</text>
</svg>
'''
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[✓] SVG Icon généré : {filepath}")

def generate_png_icon(filepath, size=192):
    """
    Générateur PNG pur en Python (sans PIL/Pillow).
    Génère une icône PNG 32-bit RGBA de qualité supérieure.
    """
    def png_chunk(chunk_type, data):
        return struct.pack('>I', len(data)) + chunk_type + data + struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)

    header = b'\x89PNG\r\n\x1a\n'
    # 8-bit RGBA (color type 6)
    ihdr = png_chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0))
    
    raw_rows = bytearray()
    cx, cy = size / 2.0, size / 2.0
    radius = size * 0.46
    inner_r = size * 0.38
    center_disk_r = size * 0.28
    
    # Corner radius pour squircle
    corner_r = size * 0.22
    
    for y in range(size):
        raw_rows.append(0) # Filter byte 0 (None)
        dy = y - cy
        
        for x in range(size):
            dx = x - cx
            dist = math.sqrt(dx*dx + dy*dy)
            
            # Squircle mask
            # distance to squircle border
            qx = abs(dx) - (size/2 - corner_r)
            qy = abs(dy) - (size/2 - corner_r)
            
            in_squircle = True
            if qx > 0 and qy > 0:
                if math.sqrt(qx*qx + qy*qy) > corner_r:
                    in_squircle = False
            elif abs(dx) > size/2 or abs(dy) > size/2:
                in_squircle = False
                
            if not in_squircle:
                # Transparent outside squircle
                raw_rows.extend([0, 0, 0, 0])
                continue
                
            # Default background gradient : #0f172a to #090d16
            t_grad = (x + y) / (size * 2)
            bg_r = int(15 * (1 - t_grad) + 9 * t_grad)
            bg_g = int(23 * (1 - t_grad) + 13 * t_grad)
            bg_b = int(42 * (1 - t_grad) + 22 * t_grad)
            alpha = 255
            
            # Bordure or autour du squircle
            dist_to_edge = min(size/2 - abs(dx), size/2 - abs(dy))
            if qx > 0 and qy > 0:
                dist_to_edge = corner_r - math.sqrt(qx*qx + qy*qy)
            if 0 <= dist_to_edge <= 4:
                # Gold border
                bg_r, bg_g, bg_b = 217, 119, 6
                
            # Disque central
            if dist < center_disk_r:
                if dist > center_disk_r - 3:
                    # Gold border of center circle
                    bg_r, bg_g, bg_b = 245, 158, 11
                elif abs(dx) < 2 and abs(dy) < center_disk_r - 4:
                    # White vertical separator
                    bg_r, bg_g, bg_b = 255, 255, 255
                elif dx < -2:
                    # Left side : Turkish Flag Red (#dc2626)
                    bg_r, bg_g, bg_b = 220, 38, 38
                    # Croissant blanc
                    cdx = dx + center_disk_r * 0.45
                    cdy = dy + 2
                    c_dist = math.sqrt(cdx*cdx + cdy*cdy)
                    c_inner_dist = math.sqrt((cdx - size*0.03)**2 + cdy**2)
                    if c_dist <= size * 0.08 and c_inner_dist >= size * 0.065:
                        bg_r, bg_g, bg_b = 255, 255, 255
                    # Etoile turque
                    s_dx = cdx - size * 0.05
                    s_dy = cdy
                    if math.sqrt(s_dx*s_dx + s_dy*s_dy) <= size * 0.022:
                        bg_r, bg_g, bg_b = 255, 255, 255
                else:
                    # Right side : French Flag Blue (#2563eb)
                    bg_r, bg_g, bg_b = 37, 99, 235
                    # Eiffel tower silhouette blanc
                    fx = abs(dx - center_disk_r * 0.45)
                    fy = dy
                    if fy > -center_disk_r * 0.6 and fy < center_disk_r * 0.6:
                        w_allowed = (fy + center_disk_r * 0.6) * 0.22 + 2
                        if fx <= w_allowed:
                            bg_r, bg_g, bg_b = 255, 255, 255
                            
            # Badge central inférieur "TR ⇄ FR"
            badge_y = center_disk_r * 0.6
            badge_h = size * 0.08
            badge_w = size * 0.36
            if abs(dx) < badge_w/2 and (badge_y <= dy <= badge_y + badge_h):
                if abs(dx) >= badge_w/2 - 2 or dy <= badge_y + 2 or dy >= badge_y + badge_h - 2:
                    bg_r, bg_g, bg_b = 217, 119, 6
                else:
                    bg_r, bg_g, bg_b = 15, 23, 42
                    
            raw_rows.extend([bg_r, bg_g, bg_b, alpha])
            
    compressed = zlib.compress(bytes(raw_rows), 9)
    idat = png_chunk(b'IDAT', compressed)
    iend = png_chunk(b'IEND', b'')
    
    with open(filepath, 'wb') as f:
        f.write(header + ihdr + idat + iend)
    print(f"[✓] PNG Icon généré : {filepath} ({size}x{size})")

if __name__ == "__main__":
    generate_svg_icon("icon.svg", 512)
    generate_svg_icon("favicon.svg", 64)
    generate_png_icon("icon-192.png", 192)
    generate_png_icon("icon-512.png", 512)
    generate_png_icon("apple-touch-icon.png", 180)
    print("[🎉] Toutes les icônes PWA ont été créées avec succès !")
