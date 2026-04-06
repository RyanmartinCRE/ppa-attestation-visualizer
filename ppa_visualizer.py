#!/usr/bin/env python3
"""
PPA Attestation Visualizer
Renders RustChain PPA fingerprint data as visual hardware identity cards

Bounty: https://github.com/Scottcjn/Rustchain/issues/2148
Reward: 75 RTC
"""

import json
import math
import sys
from typing import Dict, List, Any
import xml.etree.ElementTree as ET

class PPAVisualizer:
    """Generate visual hardware identity cards from PPA fingerprint data"""
    
    def __init__(self, fingerprint_data: Dict[str, Any]):
        self.data = fingerprint_data
        self.channels = fingerprint_data.get('channels', {})
        self.architecture = fingerprint_data.get('architecture', 'Unknown')
        self.hardware_id = fingerprint_data.get('hardware_id', 'unknown')
        self.overall_score = fingerprint_data.get('overall_score', 0)
        
    def generate_svg(self, width: int = 800, height: int = 600) -> str:
        """Generate SVG hardware identity card"""
        # Create SVG root
        svg = ET.Element('svg')
        svg.set('width', str(width))
        svg.set('height', str(height))
        svg.set('viewBox', f'0 0 {width} {height}')
        svg.set('xmlns', 'http://www.w3.org/2000/svg')
        
        # Background gradient
        defs = ET.SubElement(svg, 'defs')
        gradient = ET.SubElement(defs, 'linearGradient')
        gradient.set('id', 'bg-gradient')
        gradient.set('x1', '0%')
        gradient.set('y1', '0%')
        gradient.set('x2', '100%')
        gradient.set('y2', '100%')
        
        stop1 = ET.SubElement(gradient, 'stop')
        stop1.set('offset', '0%')
        stop1.set('style', 'stop-color:#1a1a2e;stop-opacity:1')
        
        stop2 = ET.SubElement(gradient, 'stop')
        stop2.set('offset', '100%')
        stop2.set('style', 'stop-color:#16213e;stop-opacity:1')
        
        # Background rect
        bg = ET.SubElement(svg, 'rect')
        bg.set('width', str(width))
        bg.set('height', str(height))
        bg.set('fill', 'url(#bg-gradient)')
        bg.set('rx', '20')
        
        # Title
        title = ET.SubElement(svg, 'text')
        title.set('x', str(width // 2))
        title.set('y', '40')
        title.set('text-anchor', 'middle')
        title.set('fill', '#00d9ff')
        title.set('font-family', 'monospace')
        title.set('font-size', '24')
        title.set('font-weight', 'bold')
        title.text = 'PPA HARDWARE IDENTITY'
        
        # Architecture
        arch = ET.SubElement(svg, 'text')
        arch.set('x', str(width // 2))
        arch.set('y', '70')
        arch.set('text-anchor', 'middle')
        arch.set('fill', '#ffffff')
        arch.set('font-family', 'monospace')
        arch.set('font-size', '18')
        arch.text = self.architecture
        
        # Hardware ID
        hwid = ET.SubElement(svg, 'text')
        hwid.set('x', str(width // 2))
        hwid.set('y', '95')
        hwid.set('text-anchor', 'middle')
        hwid.set('fill', '#888888')
        hwid.set('font-family', 'monospace')
        hwid.set('font-size', '12')
        hwid.text = self.hardware_id
        
        # Overall score badge
        score_color = '#00ff88' if self.overall_score >= 0.8 else '#ffaa00' if self.overall_score >= 0.6 else '#ff4444'
        score_circle = ET.SubElement(svg, 'circle')
        score_circle.set('cx', str(width - 80))
        score_circle.set('cy', '80')
        score_circle.set('r', '35')
        score_circle.set('fill', 'none')
        score_circle.set('stroke', score_color)
        score_circle.set('stroke-width', '4')
        
        score_text = ET.SubElement(svg, 'text')
        score_text.set('x', str(width - 80))
        score_text.set('y', '85')
        score_text.set('text-anchor', 'middle')
        score_text.set('fill', score_color)
        score_text.set('font-family', 'monospace')
        score_text.set('font-size', '20')
        score_text.set('font-weight', 'bold')
        score_text.text = f'{self.overall_score:.0%}'
        
        # Generate radar chart
        self._add_radar_chart(svg, 200, 280, 120)
        
        # Generate waveform
        self._add_waveform(svg, 450, 200, 300, 100)
        
        # Generate heatmap
        self._add_heatmap(svg, 450, 350, 300, 100)
        
        # Generate constellation
        self._add_constellation(svg, 200, 480, 120)
        
        return ET.tostring(svg, encoding='unicode')
    
    def _add_radar_chart(self, svg: ET.Element, cx: int, cy: int, radius: int):
        """Add radar/spider chart of 7 channel scores"""
        channel_names = list(self.channels.keys())
        n_channels = len(channel_names)
        
        if n_channels == 0:
            return
        
        # Draw grid circles
        for i in range(1, 5):
            r = radius * i / 4
            circle = ET.SubElement(svg, 'circle')
            circle.set('cx', str(cx))
            circle.set('cy', str(cy))
            circle.set('r', str(r))
            circle.set('fill', 'none')
            circle.set('stroke', '#333333')
            circle.set('stroke-width', '1')
        
        # Draw axis lines and labels
        for i, name in enumerate(channel_names):
            angle = 2 * math.pi * i / n_channels - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            
            # Axis line
            line = ET.SubElement(svg, 'line')
            line.set('x1', str(cx))
            line.set('y1', str(cy))
            line.set('x2', str(x))
            line.set('y2', str(y))
            line.set('stroke', '#333333')
            line.set('stroke-width', '1')
            
            # Label
            label_x = cx + (radius + 25) * math.cos(angle)
            label_y = cy + (radius + 25) * math.sin(angle)
            label = ET.SubElement(svg, 'text')
            label.set('x', str(label_x))
            label.set('y', str(label_y))
            label.set('text-anchor', 'middle')
            label.set('dominant-baseline', 'middle')
            label.set('fill', '#aaaaaa')
            label.set('font-family', 'monospace')
            label.set('font-size', '9')
            label.text = name.replace('_', '\n')[:8]
        
        # Draw data polygon
        points = []
        for i, name in enumerate(channel_names):
            score = self.channels[name].get('score', 0)
            angle = 2 * math.pi * i / n_channels - math.pi / 2
            x = cx + radius * score * math.cos(angle)
            y = cy + radius * score * math.sin(angle)
            points.append(f'{x},{y}')
        
        polygon = ET.SubElement(svg, 'polygon')
        polygon.set('points', ' '.join(points))
        polygon.set('fill', 'rgba(0, 217, 255, 0.3)')
        polygon.set('stroke', '#00d9ff')
        polygon.set('stroke-width', '2')
        
        # Title
        title = ET.SubElement(svg, 'text')
        title.set('x', str(cx))
        title.set('y', str(cy - radius - 40))
        title.set('text-anchor', 'middle')
        title.set('fill', '#ffffff')
        title.set('font-family', 'monospace')
        title.set('font-size', '12')
        title.text = 'Channel Scores'
    
    def _add_waveform(self, svg: ET.Element, x: int, y: int, width: int, height: int):
        """Add oscilloscope-style waveform for clock drift"""
        clock_data = self.channels.get('clock_drift', {})
        waveform = clock_data.get('waveform', [0.5] * 10)
        
        # Background
        bg = ET.SubElement(svg, 'rect')
        bg.set('x', str(x))
        bg.set('y', str(y))
        bg.set('width', str(width))
        bg.set('height', str(height))
        bg.set('fill', '#0a0a0f')
        bg.set('stroke', '#333333')
        bg.set('rx', '5')
        
        # Grid lines
        for i in range(5):
            line_y = y + height * i / 4
            line = ET.SubElement(svg, 'line')
            line.set('x1', str(x))
            line.set('y1', str(line_y))
            line.set('x2', str(x + width))
            line.set('y2', str(line_y))
            line.set('stroke', '#1a1a2e')
            line.set('stroke-width', '1')
        
        # Waveform path
        if waveform:
            points = []
            for i, val in enumerate(waveform):
                px = x + width * i / (len(waveform) - 1)
                py = y + height * (1 - val)
                points.append(f'{px},{py}')
            
            path = ET.SubElement(svg, 'polyline')
            path.set('points', ' '.join(points))
            path.set('fill', 'none')
            path.set('stroke', '#00ff88')
            path.set('stroke-width', '2')
        
        # Title
        title = ET.SubElement(svg, 'text')
        title.set('x', str(x + width // 2))
        title.set('y', str(y - 10))
        title.set('text-anchor', 'middle')
        title.set('fill', '#ffffff')
        title.set('font-family', 'monospace')
        title.set('font-size', '12')
        title.text = 'Clock Drift Waveform'
    
    def _add_heatmap(self, svg: ET.Element, x: int, y: int, width: int, height: int):
        """Add cache latency heatmap"""
        cache_data = self.channels.get('cache_timing', {})
        heatmap = cache_data.get('heatmap', [[50] * 4 for _ in range(4)])
        
        # Title
        title = ET.SubElement(svg, 'text')
        title.set('x', str(x + width // 2))
        title.set('y', str(y - 10))
        title.set('text-anchor', 'middle')
        title.set('fill', '#ffffff')
        title.set('font-family', 'monospace')
        title.set('font-size', '12')
        title.text = 'Cache Latency Heatmap'
        
        if not heatmap or not heatmap[0]:
            return
        
        rows = len(heatmap)
        cols = len(heatmap[0])
        cell_w = width / cols
        cell_h = height / rows
        
        # Find min/max for normalization
        all_vals = [v for row in heatmap for v in row]
        min_val, max_val = min(all_vals), max(all_vals)
        
        for row_idx, row in enumerate(heatmap):
            for col_idx, val in enumerate(row):
                # Normalize to 0-1
                norm = (val - min_val) / (max_val - min_val) if max_val > min_val else 0.5
                
                # Color: blue (cold) to red (hot)
                r = int(255 * norm)
                g = int(255 * (1 - norm))
                b = 100
                color = f'#{r:02x}{g:02x}{b:02x}'
                
                rect = ET.SubElement(svg, 'rect')
                rect.set('x', str(x + col_idx * cell_w))
                rect.set('y', str(y + row_idx * cell_h))
                rect.set('width', str(cell_w - 1))
                rect.set('height', str(cell_h - 1))
                rect.set('fill', color)
    
    def _add_constellation(self, svg: ET.Element, cx: int, cy: int, radius: int):
        """Add jitter constellation star map"""
        jitter_data = self.channels.get('instruction_jitter', {})
        constellation = jitter_data.get('constellation', [])
        
        # Title
        title = ET.SubElement(svg, 'text')
        title.set('x', str(cx))
        title.set('y', str(cy - radius - 15))
        title.set('text-anchor', 'middle')
        title.set('fill', '#ffffff')
        title.set('font-family', 'monospace')
        title.set('font-size', '12')
        title.text = 'Jitter Constellation'
        
        # Background circle
        bg = ET.SubElement(svg, 'circle')
        bg.set('cx', str(cx))
        bg.set('cy', str(cy))
        bg.set('r', str(radius))
        bg.set('fill', '#0a0a0f')
        bg.set('stroke', '#333333')
        
        # Draw stars
        for star in constellation:
            sx = cx + radius * (star.get('x', 0.5) - 0.5) * 2
            sy = cy + radius * (star.get('y', 0.5) - 0.5) * 2
            
            # Star glow
            glow = ET.SubElement(svg, 'circle')
            glow.set('cx', str(sx))
            glow.set('cy', str(sy))
            glow.set('r', '6')
            glow.set('fill', '#ffaa00')
            glow.set('opacity', '0.3')
            
            # Star core
            core = ET.SubElement(svg, 'circle')
            core.set('cx', str(sx))
            core.set('cy', str(sy))
            core.set('r', '3')
            core.set('fill', '#ffdd00')
        
        # Connect stars with lines
        if len(constellation) > 1:
            for i in range(len(constellation)):
                s1 = constellation[i]
                s2 = constellation[(i + 1) % len(constellation)]
                
                x1 = cx + radius * (s1.get('x', 0.5) - 0.5) * 2
                y1 = cy + radius * (s1.get('y', 0.5) - 0.5) * 2
                x2 = cx + radius * (s2.get('x', 0.5) - 0.5) * 2
                y2 = cy + radius * (s2.get('y', 0.5) - 0.5) * 2
                
                line = ET.SubElement(svg, 'line')
                line.set('x1', str(x1))
                line.set('y1', str(y1))
                line.set('x2', str(x2))
                line.set('y2', str(y2))
                line.set('stroke', '#ffaa00')
                line.set('stroke-width', '1')
                line.set('opacity', '0.5')


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: ppa_visualizer.py <fingerprint.json> [output.svg]")
        print("\nGenerates visual hardware identity cards from PPA fingerprint data")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'hardware_identity.svg'
    
    # Load fingerprint data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Generate visualization
    viz = PPAVisualizer(data)
    svg_output = viz.generate_svg()
    
    # Save output
    with open(output_file, 'w') as f:
        f.write(svg_output)
    
    print(f"✅ Hardware identity card generated: {output_file}")
    print(f"   Architecture: {viz.architecture}")
    print(f"   Overall Score: {viz.overall_score:.0%}")
    print(f"   Channels: {len(viz.channels)}")


if __name__ == '__main__':
    main()