import plotly.graph_objects as go
import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output
import io
import plotly.io as pio 

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

    # ***************************************************************
    # *** הנה התיקון הקריטי! שימוש ב-FigureWidget ***
    fig = go.FigureWidget(data=traces)
    # ***************************************************************

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
#  פונקציה 2: מפעיל ה-GUI (נשארת זהה)
# ==============================================================================

def launch_interactive_plotter():
    
    # הגדרה עבור Google Colab
    pio.renderers.default = 'colab'
    
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
                    # שיטת התצוגה נשארת זהה
                    display(fig) 
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




# פונקציה מס 2 גישה פשוטה יותר

# --- הוסף את זה לקובץ OS_plots.py שלך ---

import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

def plot_from_path(file_paths, x_col, y_cols):
    """
    יוצר גרף פלוטלי מנתיבי קבצים ושמות עמודות.
    פשוט וקל - בלי GUI.
    
    Args:
        file_paths (str or list): נתיב לקובץ בודד, או רשימה של שני נתיבים.
        x_col (str): שם עמודת ציר ה-X.
        y_cols (str or list): שם עמודת ציר ה-Y, או רשימה של שמות.

    Returns:
        plotly.graph_objects.Figure: אובייקט הגרף (fig) שניתן להציג.
    """
    
    # 1. הגדרת סביבת התצוגה של Colab (ליתר ביטחון)
    pio.renderers.default = 'colab'
    
    df = None
    
    # 2. ודא ש-file_paths הוא רשימה
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    if not (1 <= len(file_paths) <= 2):
        print("שגיאה: 'file_paths' חייב להיות נתיב אחד או רשימה של שני נתיבים.")
        return None

    # 3. טעינת הנתונים
    try:
        if len(file_paths) == 1:
            df = pd.read_csv(file_paths[0], encoding='latin1')
        elif len(file_paths) == 2:
            df1 = pd.read_csv(file_paths[0], encoding='latin1')
            df2 = pd.read_csv(file_paths[1], encoding='latin1')
            
            if x_col not in df1.columns or x_col not in df2.columns:
                print(f"שגיאה: עמודת X '{x_col}' לא קיימת בשני הקבצים.")
                return None
            
            df = pd.merge(df1, df2, on=x_col, how='inner')
            
    except FileNotFoundError as e:
        print(f"שגיאה: הקובץ לא נמצא. {e}")
        return None
    except Exception as e:
        print(f"שגיאה בטעינה או מיזוג הקבצים: {e}")
        return None

    # 4. הכנת הנתונים לגרף
    if isinstance(y_cols, str):
        y_cols = [y_cols]

    traces = []
    # ודא שהעמודות קיימות ב-DataFrame
    valid_y_cols = [col for col in y_cols if col in df.columns]
    
    if not valid_y_cols:
        print(f"שגיאה: אף אחת מעמודות ה-Y שצוינו ({y_cols}) לא נמצאה בנתונים.")
        return None

    for y_col in valid_y_cols:
        traces.append(go.Bar(
            x=df[x_col], 
            y=df[y_col], 
            name=y_col,
            text=df[y_col].round(2),
            textposition='outside'
        ))

    # 5. יצירת הגרף (עם go.Figure רגיל!)
    fig = go.Figure(data=traces)
    fig.update_layout(
        title=f"גרף עמודות: {', '.join(valid_y_cols)} מול {x_col}",
        xaxis_title=x_col,
        yaxis_title="Value",
        hovermode='x unified'
    )
    
    # 6. החזרת הגרף!
    return fig



# פונקציה נוספת - חישוב קורלציה וגרפים

def plot_correlation(file_path, col1_name, col2_name):
    """
    מחשב ומציג גרף קורלציה (פירסון) בין שתי עמודות.
    כולל גרף פיזור, קו רגרסיה, רווח סמך, ומדדי הקורלציה.

    Args:
        file_path (str): נתיב מלא לקובץ ה-CSV.
        col1_name (str): שם העמודה הראשונה (תופיע בציר X).
        col2_name (str): שם העמודה השנייה (תופיע בציר Y).

    Returns:
        matplotlib.figure.Figure: אובייקט הגרף (fig) שניתן להציג.
    """
    
    # 1. טעינת הנתונים
    try:
        df = pd.read_csv(file_path, encoding='latin1')
    except FileNotFoundError:
        print(f"שגיאה: הקובץ לא נמצא בנתיב {file_path}")
        return None
    except Exception as e:
        print(f"שגיאה בטעינת הקובץ: {e}")
        return None

    # 2. בדיקת קיום העמודות
    if col1_name not in df.columns or col2_name not in df.columns:
        print(f"שגיאה: אחת העמודות ('{col1_name}', '{col2_name}') לא קיימת בקובץ.")
        return None
        
    # 3. ניקוי נתונים חסרים (NaN) - חובה עבור קורלציה
    #    נשמיט שורות שבהן *אחת* מהעמודות הרלוונטיות חסרה
    clean_df = df[[col1_name, col2_name]].dropna()
    
    if clean_df.empty:
        print("שגיאה: לא נשארו נתונים תקפים לאחר ניקוי ערכים חסרים.")
        return None
        
    col1 = clean_df[col1_name]
    col2 = clean_df[col2_name]

    # 4. חישוב הקורלציה
    corr, p_value = pearsonr(col1, col2)
    
    # 5. יצירת הגרף
    #    ניצור אובייקט Figure ו-Axis של Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    
    #    זו פונקציית הקסם של Seaborn
    sns.regplot(
        x=col1,
        y=col2,
        ax=ax,  # מציין ל-Seaborn לצייר על ה-Axis שיצרנו
        line_kws={"color": "red", "lw": 2}, # צובע את קו הרגרסיה באדום
        scatter_kws={"alpha": 0.6} # הופך את הנקודות למעט שקופות
    )
    
    # 6. הוספת הטקסט האינפורמטיבי על הגרף
    #    נבנה את מחרוזת הטקסט
    text_str = f"Pearson's r: {corr:.3f}\np-value: {p_value:.3f}"
    
    #    נוסיף את הטקסט בפינה השמאלית העליונה של הגרף
    ax.text(
        0.05, 0.95,  # מיקום: 5% מהשמאל, 95% מהתחתית (כלומר, למעלה)
        text_str,
        transform=ax.transAxes,  # מגדיר שהמיקום יחסי לגודל הגרף
        fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7) # קופסה לבנה לרקע
    )
    
    # 7. עיצוב סופי
    ax.set_title(f"Correlation: {col1_name} vs {col2_name}", fontsize=16)
    ax.set_xlabel(col1_name, fontsize=12)
    ax.set_ylabel(col2_name, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6) # מוסיף רשת (גריד)
    
    print(f"Pearson's correlation (r): {corr:.3f}")
    print(f"p-value: {p_value:.3f}")

    # 8. החזרת אובייקט הגרף
    return fig
