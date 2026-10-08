#!/usr/bin/env python3
"""
Custom IPTV Playlist Generator for Pakistan, Iran, English News, and Sports.
Source: Official iptv-org/iptv project (https://github.com/iptv-org/iptv)
"""

import json
import os
import sys

def generate_playlist():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'final_inventory_validated.json')
    output_path = os.path.join(script_dir, 'pakistan-iptv.m3u')
    
    if not os.path.exists(json_path):
        json_path = os.path.join(script_dir, 'final_inventory.json')
        
    if not os.path.exists(json_path):
        print(f"Error: Inventory source file not found at {json_path}")
        sys.exit(1)
        
    with open(json_path, 'r', encoding='utf-8') as f:
        channels = json.load(f)
        
    if not channels or len(channels) < 50:
        print(f"Validation failed: Channel list is suspiciously small ({len(channels)} entries). Refusing to overwrite.")
        sys.exit(1)
        
    m3u_lines = []
    # Header with EPG reference
    m3u_lines.append('#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/pk.xml,https://iptv-org.github.io/epg/guides/ir.xml,https://iptv-org.github.io/epg/guides/uk.xml,https://iptv-org.github.io/epg/guides/us.xml"')
    m3u_lines.append('')
    
    current_group = None
    for ch in channels:
        group = ch.get('group', 'Other')
        # Normalize group if needed
        if group == 'English News':
            group = 'English | News'
            
        if group != current_group:
            current_group = group
            m3u_lines.append(f'# ==========================================')
            m3u_lines.append(f'# GROUP: {current_group}')
            m3u_lines.append(f'# ==========================================')
            
        tvg_id = ch.get('tvg_id', '')
        tvg_name = ch.get('tvg_name', ch.get('clean_name', ''))
        tvg_logo = ch.get('tvg_logo', '')
        name = ch.get('name', tvg_name)
        url = ch.get('url', '')
        headers = ch.get('headers', [])
        
        # Build EXTINF line
        extinf_parts = [f'#EXTINF:-1']
        if tvg_id:
            extinf_parts.append(f'tvg-id="{tvg_id}"')
        if tvg_name:
            extinf_parts.append(f'tvg-name="{tvg_name}"')
        if tvg_logo:
            extinf_parts.append(f'tvg-logo="{tvg_logo}"')
        extinf_parts.append(f'group-title="{group}"')
        
        # Add any inline http-user-agent or referrer attribute if needed
        for h in headers:
            if 'http-user-agent=' in h:
                ua = h.split('http-user-agent=')[1].strip()
                extinf_parts.append(f'http-user-agent="{ua}"')
            elif 'http-referrer=' in h:
                ref = h.split('http-referrer=')[1].strip()
                extinf_parts.append(f'http-referrer="{ref}"')
                
        extinf_line = ' '.join(extinf_parts) + f',{name}'
        m3u_lines.append(extinf_line)
        
        # Add #EXTGRP for maximum HotPlayer & IPTV client compatibility
        m3u_lines.append(f'#EXTGRP:{group}')
        
        # Add VLC opt headers if present
        for h in headers:
            if h.startswith('#EXTVLCOPT:'):
                m3u_lines.append(h)
                
        # Stream URL
        m3u_lines.append(url)
        m3u_lines.append('')
        
    content = '\n'.join(m3u_lines)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Successfully generated {output_path}")
    print(f"Total channels written: {len(channels)}")
    print(f"File size: {len(content.encode('utf-8'))} bytes")

if __name__ == '__main__':
    generate_playlist()
