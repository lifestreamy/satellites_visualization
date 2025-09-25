# Mermaid flowchart for the satellite program workflow
# This chart is already saved as workflow_chart.png

diagram_code = """
flowchart TD
    A[User Inputs] --> B[Parameter Validation]
    B --> C[Fetch Satellite Data]
    C --> D[N2YO API / CelesTrak TLE / Landsat DE]
    D --> E[Coordinate Conversion]
    E --> F[Filter Satellites by Distance]
    F --> G[Display List]
    G --> H[3D Visualization matplotlib]
"""

print("Mermaid diagram code for satellite program workflow:")
print(diagram_code)
print("\nNote: workflow_chart.png already exists in the project directory.")