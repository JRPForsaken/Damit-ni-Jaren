"""
Report Generator Module
Generates detailed reports about the sorting process
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import json
import config


class ReportGenerator:
    """Generate reports about clothing sorting results"""
    
    def __init__(self, output_folder: str = None):
        """
        Initialize the report generator
        
        Args:
            output_folder: Path to output folder
        """
        self.output_folder = Path(output_folder) if output_folder else Path(config.OUTPUT_FOLDER_NAME)
        self.report_format = config.REPORT_FORMAT
    
    def generate_report(self, image_paths: List[Path],
                       classifications: List[Dict[str, str]],
                       groups: Dict[str, Dict[int, List[Path]]],
                       organized: Dict[str, List[tuple]],
                       processing_time: float = None):
        """
        Generate comprehensive report
        
        Args:
            image_paths: List of original image paths
            classifications: List of classification results
            groups: Grouped images by type and similarity
            organized: Organized file mappings
            processing_time: Total processing time in seconds
        """
        print("Generating reports...")
        
        # Generate CSV report
        if self.report_format in ['csv', 'both']:
            self._generate_csv_report(image_paths, classifications, organized)
        
        # Generate HTML report
        if self.report_format in ['html', 'both']:
            self._generate_html_report(image_paths, classifications, groups, 
                                      organized, processing_time)
        
        # Generate JSON summary
        self._generate_json_summary(image_paths, classifications, groups, 
                                   organized, processing_time)
        
        print(f"Reports saved to: {self.output_folder}")
    
    def _generate_csv_report(self, image_paths: List[Path],
                            classifications: List[Dict[str, str]],
                            organized: Dict[str, List[tuple]]):
        """Generate CSV report with file details"""
        
        # Create file mapping
        file_mapping = {}
        for clothing_type, file_pairs in organized.items():
            for old_path, new_path in file_pairs:
                file_mapping[str(old_path)] = str(new_path)
        
        # Prepare data
        data = []
        for img_path, classification in zip(image_paths, classifications):
            new_path = file_mapping.get(str(img_path), 'N/A')
            
            data.append({
                'Original_Filename': img_path.name,
                'Original_Path': str(img_path),
                'New_Filename': Path(new_path).name if new_path != 'N/A' else 'N/A',
                'New_Path': new_path,
                'Clothing_Type': classification['type'],
                'Color': classification['color'],
                'File_Size_KB': img_path.stat().st_size / 1024 if img_path.exists() else 0
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save to CSV
        csv_path = self.output_folder / 'sorting_report.csv'
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"CSV report saved: {csv_path}")
        
        # Also create summary by type
        summary_df = df.groupby('Clothing_Type').agg({
            'Original_Filename': 'count',
            'File_Size_KB': 'sum'
        }).rename(columns={
            'Original_Filename': 'Count',
            'File_Size_KB': 'Total_Size_KB'
        })
        
        summary_path = self.output_folder / 'summary_by_type.csv'
        summary_df.to_csv(summary_path, encoding='utf-8')
        print(f"Summary report saved: {summary_path}")
    
    def _generate_html_report(self, image_paths: List[Path],
                             classifications: List[Dict[str, str]],
                             groups: Dict[str, Dict[int, List[Path]]],
                             organized: Dict[str, List[tuple]],
                             processing_time: float = None):
        """Generate HTML report with visualizations"""
        
        # Count statistics
        total_images = len(image_paths)
        type_counts = {}
        color_counts = {}
        
        for classification in classifications:
            clothing_type = classification['type']
            color = classification['color']
            
            type_counts[clothing_type] = type_counts.get(clothing_type, 0) + 1
            color_counts[color] = color_counts.get(color, 0) + 1
        
        # Count groups
        total_groups = sum(len(type_groups) for type_groups in groups.values())
        
        # Generate HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clothing Sorting Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .stats-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 1.1em;
        }}
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
        }}
        .section {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .bar-chart {{
            margin-top: 20px;
        }}
        .bar {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}
        .bar-label {{
            width: 150px;
            font-weight: bold;
        }}
        .bar-fill {{
            height: 30px;
            background-color: #3498db;
            border-radius: 5px;
            display: flex;
            align-items: center;
            padding: 0 10px;
            color: white;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 AI Clothing Sorting Report</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="stats-container">
        <div class="stat-card">
            <h3>Total Images</h3>
            <div class="value">{total_images}</div>
        </div>
        <div class="stat-card">
            <h3>Clothing Types</h3>
            <div class="value">{len(type_counts)}</div>
        </div>
        <div class="stat-card">
            <h3>Similar Groups</h3>
            <div class="value">{total_groups}</div>
        </div>
        <div class="stat-card">
            <h3>Processing Time</h3>
            <div class="value">{processing_time:.1f}s</div>
        </div>
    </div>
    
    <div class="section">
        <h2>Distribution by Clothing Type</h2>
        <div class="bar-chart">
"""
        
        # Add bar chart for types
        max_count = max(type_counts.values()) if type_counts else 1
        for clothing_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            width = (count / max_count) * 100
            html_content += f"""
            <div class="bar">
                <div class="bar-label">{clothing_type.capitalize()}</div>
                <div class="bar-fill" style="width: {width}%;">{count}</div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    <div class="section">
        <h2>Distribution by Color</h2>
        <div class="bar-chart">
"""
        
        # Add bar chart for colors
        max_count = max(color_counts.values()) if color_counts else 1
        for color, count in sorted(color_counts.items(), key=lambda x: x[1], reverse=True):
            width = (count / max_count) * 100
            html_content += f"""
            <div class="bar">
                <div class="bar-label">{color.capitalize()}</div>
                <div class="bar-fill" style="width: {width}%;">{count}</div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    <div class="section">
        <h2>Detailed Breakdown</h2>
        <table>
            <thead>
                <tr>
                    <th>Clothing Type</th>
                    <th>Count</th>
                    <th>Groups</th>
                    <th>Avg per Group</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add detailed table
        for clothing_type in sorted(type_counts.keys()):
            count = type_counts[clothing_type]
            n_groups = len(groups.get(clothing_type, {}))
            avg_per_group = count / n_groups if n_groups > 0 else count
            
            html_content += f"""
                <tr>
                    <td>{clothing_type.capitalize()}</td>
                    <td>{count}</td>
                    <td>{n_groups}</td>
                    <td>{avg_per_group:.1f}</td>
                </tr>
"""
        
        html_content += """
            </tbody>
        </table>
    </div>
    
    <div class="footer">
        <p>Generated by AI Clothing Photo Sorter v1.0.0</p>
        <p>Powered by Deep Learning & Computer Vision</p>
    </div>
</body>
</html>
"""
        
        # Save HTML report
        html_path = self.output_folder / 'sorting_report.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML report saved: {html_path}")
    
    def _generate_json_summary(self, image_paths: List[Path],
                              classifications: List[Dict[str, str]],
                              groups: Dict[str, Dict[int, List[Path]]],
                              organized: Dict[str, List[tuple]],
                              processing_time: float = None):
        """Generate JSON summary"""
        
        # Count statistics
        type_counts = {}
        color_counts = {}
        
        for classification in classifications:
            clothing_type = classification['type']
            color = classification['color']
            
            type_counts[clothing_type] = type_counts.get(clothing_type, 0) + 1
            color_counts[color] = color_counts.get(color, 0) + 1
        
        summary = {
            'generated_at': datetime.now().isoformat(),
            'total_images': len(image_paths),
            'processing_time_seconds': processing_time,
            'statistics': {
                'by_type': type_counts,
                'by_color': color_counts,
                'total_groups': sum(len(type_groups) for type_groups in groups.values())
            },
            'output_folder': str(self.output_folder),
            'configuration': {
                'similarity_threshold': config.SIMILARITY_THRESHOLD,
                'clustering_method': config.CLUSTERING_METHOD,
                'copy_files': config.COPY_FILES
            }
        }
        
        # Save JSON
        json_path = self.output_folder / 'summary.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"JSON summary saved: {json_path}")
