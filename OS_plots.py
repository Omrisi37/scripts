import plotly.graph_objects as go
import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output
import io
import plotly.io as pio # הוספנו את הייבוא הזה

# ==============================================================================
#  פונקציה 1: היגיון הליבה (ה"מנוע")
# ==============================================================================

def create_plot_from_dfs(dataframes, x_col, y_cols):
    
    df = None
    
    if not isinstance(dataframes, list) or len(dataframes) not in [1, 2]:
        print("Error: 'dataframes' must be a list containing one or two DataFrames.")
        return None

    if len(dataframes) == 1:
        df = dataframes[0]
    elif len(dataframes) == 2:
        df1 = dataframes[0]
        df2 = dataframes[1]
        
        if x_col not in df1.columns or x_col not in df2.columns:
            print(f"Error: X-axis column '{x_col}' not found in one or both dataframes.")
            return None
        
        df = pd.merge(df1, df2, on=x_col, how='inner')

    if isinstance(y_cols, str):
        y_cols = [y_cols]

    traces = []
    valid_y_cols = [col for col in y_cols if col in df.columns]
    missing_cols = set(y_cols) - set(valid_y_cols)
    if missing_cols:
        print(f"Warning: Columns not found and will be skipped: {missing_cols}")

    for y_col in valid_y_cols:
        traces.append(go.Bar(
            x=df[x_col], 
            y=df[y_col], 
            name=y_col, 
            text=df[y_col].round(2), 
            textposition='outside'
        ))

    if not traces:
        print("Error: No valid Y-axis columns to plot.")
        return None

    fig = go.Figure(data=traces)
    fig.update_layout(
        title=f"Bar Chart: {', '.join(valid_y_cols)} vs {x_col}",
        xaxis_title=x_col,
        yaxis_title="Value",
        hovermode='x unified',
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    
    return fig


# ==============================================================================
#  פונקציה 2: מפעיל ה-GUI
# ==============================================================================

def launch_interactive_plotter():
    
    # --- התיקון עבור Google Colab ---
    pio.renderers.default = 'colab'
    # ---------------------------------
    
    app_data = {'dfs': []}

    file_uploader = widgets.FileUpload(
        accept='.csv',
        multiple=True,
        description='Upload CSV(s)',
        tooltip='Upload one or two CSV files'
    )
    x_axis_selector = widgets.Dropdown(options=[], description='Select X-Axis:', disabled=True)
    y_axis_selector = widgets.SelectMultiple(options=[], description='Select Y-Axis:', disabled=True)
    plot_button = widgets.Button(description='Create Plot', disabled=True)
    status_label = widgets.Label(value="Please upload 1 or 2 CSV files.")
    output_area = widgets.Output()

    def on_file_upload(change):
        x_axis_selector.options = []
        y_axis_selector.options = []
        x_axis_selector.disabled = True
        y_axis_selector.disabled = True
        plot_button.disabled = True
        app_data['dfs'] = []
        output_area.clear_output()
        
        uploaded_files = file_uploader.value
        
        if not (1 <= len(uploaded_files) <= 2):
            status_label.value = "Error: Please upload EXACTLY 1 or 2 CSV files."
            return

        try:
            dfs = []
            for file_info in uploaded_files.values():
                content = file_info['content']
                df = pd.read_csv(io.BytesIO(content), encoding='latin1')
                dfs.append(df)
            
            app_data['dfs'] = dfs
            
            if len(dfs) == 1:
                all_cols = sorted(list(dfs[0].columns))
                x_axis_selector.options = all_cols
                y_axis_selector.options = all_cols
            elif len(dfs) == 2:
                common_cols = sorted(list(set(dfs[0].columns) & set(dfs[1].columns)))
                if not common_cols:
                    status_label.value = "Error: The two files have no common columns."
                    return
                all_cols = sorted(list(set(dfs[0].columns) | set(dfs[1].columns)))
                x_axis_selector.options = common_cols
                y_axis_selector.options = all_cols

            x_axis_selector.disabled = False
            y_axis_selector.disabled = False
            plot_button.disabled = False
            status_label.value = f"{len(dfs)} file(s) loaded. Please select axes."
            
        except Exception as e:
            status_label.value = f"Error processing file: {e}"

    def on_plot_button_clicked(b):
        output_area.clear_output()
        status_label.value = "Generating plot..."
        
        x_col = x_axis_selector.value
        y_cols = list(y_axis_selector.value)
        
        if not x_col or not y_cols:
            status_label.value = "Error: Must select an X-axis and one Y-axis."
            return
            
        try:
            fig = create_plot_from_dfs(app_data['dfs'], x_col, y_cols)
            
            if fig:
                with output_area:
                    fig.show()
                status_label.value = "Plot created successfully."
            else:
                status_label.value = "Error creating plot. Check console."
                
        except Exception as e:
            status_label.value = f"An error occurred: {e}"
            with output_area:
                print(f"An unexpected error occurred: {e}")

    file_uploader.observe(on_file_upload, names='value')
    plot_button.on_click(on_plot_button_clicked)

    gui_layout = widgets.VBox([
        file_uploader,
        x_axis_selector,
        y_axis_selector,
        plot_button,
        status_label,
        output_area
    ])

    display(gui_layout)
